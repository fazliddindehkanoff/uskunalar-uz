from api.models import Product


def product_detail(request, lang_code: str, product_id: int) -> dict:
    product_data = {}
    product = Product.objects.filter(pk=product_id).first()

    if product:
        # Incrementing the views count
        product.view_count += 1
        product.save()

        # price
        if product.price and product.price != 0:
            product_data["price"] = f"{product.price}"
        else:
            product_data["price"] = f"{product.min_price}-{product.max_price}"

        product_data["images"] = [
            request.build_absolute_uri(image.image.url)
            for image in product.images.all()
        ]

        product_data["specifications"] = [
            {
                "title": feature.get_translated_field("title", lang_code),
                "value": feature.get_translated_field("value", lang_code),
            }
            for feature in product.specifications.all()
        ]
        # Translated fields
        product_data["name"] = product.get_translated_field("name", lang_code)
        product_data["description"] = product.get_translated_field(
            "description", lang_code
        )

        # Standard fields
        product_data["category"] = (
            product.category.get_translated_field("title", lang_code)
            if product.category
            else None
        )
        product_data["subcategory"] = (
            product.subcategory.get_translated_field("title", lang_code)
            if product.subcategory
            else None
        )

        product_data["availability_status"] = product.get_availability_status_display()
        product_data["discount"] = product.discount
        product_data["cip_type"] = product.get_cip_type_display()
        product_data["views"] = product.view_count

    return product_data


def product_list(lang_code: str) -> list:
    pass
