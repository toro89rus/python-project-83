from bs4 import BeautifulSoup


def get_seo_content(html):
    soup = BeautifulSoup(html, "html.parser")
    title = soup.title.contents[0] if soup.title else ""
    h1 = soup.h1.contents[0] if soup.h1 else ""
    content = soup.find("meta", attrs={"name": "description"}).get(
        "content", ""
    )
    return {
        "h1": h1,
        "title": title,
        "content": content
        }
