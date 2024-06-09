from bs4 import BeautifulSoup
import markdownify

from api.models import Product


def handle_images(soup):
    """
    Convert <img> tags into Markdown image format.
    """
    for img in soup.find_all("img"):
        alt_text = img.get("alt", "")
        src = img.get("src", "")
        markdown_image = f"![{alt_text}]({src})"
        img.replace_with(markdown_image)


def html_to_markdown(html_content):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Handle images
    handle_images(soup)

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
