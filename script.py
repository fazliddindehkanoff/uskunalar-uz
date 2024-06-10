from bs4 import BeautifulSoup
import markdownify as md

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


def parse_table(table):
    """
    Convert an HTML table to Markdown format while preserving the structure.
    """
    md_table = []
    rows = table.find_all("tr")

    # Process rows
    for row in rows:
        cols = row.find_all(["td", "th"])
        md_row = " | ".join(cell.get_text(" ", strip=True) for cell in cols)
        md_table.append(md_row)

    # If the table has data, add Markdown header style
    if md_table:
        # Add header separator if first row is a header
        header_cols_count = len(md_table[0].split(" | "))
        md_table.insert(1, " | ".join(["---"] * header_cols_count))

    return "\n".join(md_table)


def html_to_markdown(html_content):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Handle images
    handle_images(soup)

    # Handle tables manually
    for table in soup.find_all("table"):
        markdown_table = parse_table(table)
        table.replace_with(markdown_table)

    # Convert the remaining HTML content to Markdown format
    markdown_content = md.markdownify(str(soup), heading_style="ATX")

    return markdown_content


def convert_html_to_markdown():
    products = Product.objects.all()
    for product in products:
        product.description_uz = html_to_markdown(product.description_uz)
        product.description_ru = html_to_markdown(product.description_ru)
        product.description_en = html_to_markdown(product.description_en)
        product.save()
