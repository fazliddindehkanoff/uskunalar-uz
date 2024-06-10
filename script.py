import html2text
from api.models import Product


def html_to_markdown(html_content):

    # Convert the remaining HTML content to Markdown format
    markdown_content = html2text.html2text(html_content)

    return markdown_content


def convert_html_to_markdown():
    products = Product.objects.all()
    for product in products:
        product.description_uz = html_to_markdown(product.description_uz)
        product.description_ru = html_to_markdown(product.description_ru)
        product.description_en = html_to_markdown(product.description_en)
        product.save()
