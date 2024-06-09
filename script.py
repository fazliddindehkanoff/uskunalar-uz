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


def table_to_markdown(table):
    """
    Convert an HTML table to Markdown format.
    """
    md_table = []
    rows = table.find_all("tr")

    for row in rows:
        md_row = []
        cols = row.find_all(["td", "th"])
        for col in cols:
            col_content = col.get_text(separator=" ").strip()
            md_row.append(col_content)
        md_table.append(" | ".join(md_row))

    if md_table:
        md_table.insert(1, " | ".join(["---"] * len(md_table[0].split(" | "))))

    return "\n".join(md_table)


def html_to_markdown(html_content):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Handle images
    handle_images(soup)

    # Handle tables manually
    for table in soup.find_all("table"):
        markdown_table = table_to_markdown(table)
        table.replace_with(markdown_table)

    # Convert the remaining HTML content to Markdown format
    markdown_content = markdownify.markdownify(str(soup), heading_style="ATX")

    return markdown_content


def convert_html_to_markdown():
    products = Product.objects.all()
    for product in products:
        product.description_uz = html_to_markdown(product.description_uz)
        product.description_ru = html_to_markdown(product.description_ru)
        product.description_en = html_to_markdown(product.description_en)
        product.save()
