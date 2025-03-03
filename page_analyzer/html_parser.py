from bs4 import BeautifulSoup


def get_seo_content(html):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.contents[0] if soup.title else ""
    h1 = soup.h1.text if soup.h1 else ""
    description = soup.find("meta", attrs={"name": "description"})
    content = description.get("content", "") if description else ""
    return {
        "h1": h1,
        "title": title,
        "content": content
        }
