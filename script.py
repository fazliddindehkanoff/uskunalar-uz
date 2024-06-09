from bs4 import BeautifulSoup
import markdownify

from api.models import Product


def html_to_markdown(html_content):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Convert the parsed HTML content to Markdown format
    markdown_content = markdownify.markdownify(str(soup), heading_style="ATX")

    return markdown_content


def convert_html_to_markdown():
    products = Product.objects.all()
    for product in products:
        product.description_uz = html_to_markdown(product.description_uz)
        product.description_ru = html_to_markdown(product.description_ru)
        product.description_en = html_to_markdown(product.description_en)
        product.save()
