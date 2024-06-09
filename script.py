import html2text
from api.models import Product


def handle_images(html_content):
    """
    Convert <img> tags into Markdown image format.
    """
    h = html2text.HTML2Text()
    h.ignore_images = False
    h.ignore_links = False
    h.images_as_html = False
    return h.handle(html_content)


def parse_table(html_content):
    """
    Convert an HTML table to Markdown format while preserving the structure.
    """
    h = html2text.HTML2Text()
    h.ignore_tables = False
    return h.handle(html_content)


def html_to_markdown(html_content):
    # Convert images
    html_content = handle_images(html_content)

    # Convert tables
    html_content = parse_table(html_content)

    # Convert the remaining HTML content to Markdown format
    h = html2text.HTML2Text()
    h.ignore_images = True
    h.ignore_tables = True
    h.ignore_links = False
    h.body_width = 0
    markdown_content = h.handle(html_content)

    return markdown_content


def convert_html_to_markdown():
    products = Product.objects.all()
    for product in products:
        product.description_uz = html_to_markdown(product.description_uz)
        product.description_ru = html_to_markdown(product.description_ru)
        product.description_en = html_to_markdown(product.description_en)
        product.save()
