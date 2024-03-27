from rest_framework.exceptions import NotFound

from api.models import Product
from .supplier import get_supplier_data


def _calc_product_cost(product: Product) -> str:
    if product.price and product.price != 0:
        return f"{product.price}"
    else:
        return f"{product.min_price}-{product.max_price}"


def product_detail(request, lang_code: str, product_id: int) -> dict:
    product_data = {}
    product = Product.objects.filter(pk=product_id).first()

    if product:
        # Incrementing the views count
        product.view_count += 1
        product.save()

        product_data["id"] = product.pk
        product_data["price"] = _calc_product_cost(product=product)
        product_data["images"] = [
            request.build_absolute_uri(image.image.url)
            for image in product.images.all()
        ]
        product_data["background_image"] = (
            request.build_absolute_uri(product.background_image.image.url)
            if product.background_image
            else ""
        )

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
        product_data["short_description"] = product.get_translated_field(
            "short_description", lang_code
        )

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

        product_data["availability_status"] = product.get_availability_status_display(
            lang_code=lang_code
        )
        product_data["discount"] = product.discount
        product_data["cip_type"] = product.get_cip_type_display()
        product_data["view_count"] = product.view_count
        product_data["related_products"] = get_products_list(
            product.related_products.all(),
            lang_code=lang_code,
            request=request,
        )
        product_data["similar_products"] = get_products_list(
            Product.objects.filter(
                category=product.category, subcategory=product.subcategory
            ).exclude(pk=product_id),
            lang_code=lang_code,
            request=request,
        )
        product_data["supplier"] = get_supplier_data(product.supplier)

    else:
        raise NotFound("There is no product with given id")
    return product_data


def list_products(
    request,
    lang_code: str,
    category_id: int = 0,
    sub_category_id: int = 0,
    search_query: str = "",
    order_by: str = "views",
    page: int = 1,
    page_size: int = 10,
) -> dict:
    queryset = Product.objects.all()
    # Searching
    if search_query:
        queryset = queryset.filter(name__icontains=search_query)

    if category_id != 0:
        queryset = queryset.filter(category_id=category_id)

    if sub_category_id != 0:
        queryset = queryset.filter(subcategory_id=sub_category_id)

    # Ordering
    if order_by:
        queryset = queryset.order_by(order_by)

    # Pagination
    start = (page - 1) * page_size
    end = start + page_size
    total_count = queryset.count()
    queryset = queryset[start:end]

    # Formatting the result
    products_data = get_products_list(
        queryset=queryset, lang_code=lang_code, request=request
    )

    return {
        "products": products_data,
        "total_count": total_count,
        "page": page,
        "page_size": page_size,
    }


def get_products_list(queryset, lang_code, request):
    products_data = []
    for product in queryset:
        product_data = {
            "id": product.pk,
            "name": product.get_translated_field("name", lang_code),
            "price": _calc_product_cost(product=product),
            "images": [
                request.build_absolute_uri(image.image.url)
                for image in product.images.all()
            ],
            "background_image": (
                request.build_absolute_uri(product.background_image.image.url)
                if product.background_image
                else ""
            ),
            "cip_type": product.get_cip_type_display(),
            "availability_status": product.get_availability_status_display(
                lang_code=lang_code
            ),
            "view_count": product.view_count,
        }
        product_data["specifications"] = [
            {
                "title": feature.get_translated_field("title", lang_code),
                "value": feature.get_translated_field("value", lang_code),
            }
            for feature in product.specifications.all()
        ]
        products_data.append(product_data)

    return products_data
