from bs4 import BeautifulSoup
import markdownify


def html_to_markdown(html_content):
    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, "html.parser")

    # Convert the parsed HTML content to Markdown format
    markdown_content = markdownify.markdownify(str(soup), heading_style="ATX")

    return markdown_content
