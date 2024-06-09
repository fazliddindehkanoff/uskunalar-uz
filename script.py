import html2text
from api.models import Product


def html_to_markdown(html_content):

    # Convert the remaining HTML content to Markdown format
    h = html2text.HTML2Text()
    h.ignore_images = False
    h.ignore_tables = False
    h.ignore_links = False
    markdown_content = h.handle(html_content)

    return markdown_content


def convert_html_to_markdown():
    products = Product.objects.all()
    for product in products:
        product.description_uz = html_to_markdown(product.description_uz)
        product.description_ru = html_to_markdown(product.description_ru)
        product.description_en = html_to_markdown(product.description_en)
        product.save()
