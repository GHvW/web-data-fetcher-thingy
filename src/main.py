import aiohttp
import asyncio
from itertools import chain
from bs4 import BeautifulSoup
from jinja2 import Environment, FileSystemLoader

print("hello world")

def replace_anchor_text(paragraph: BeautifulSoup) -> None:
    for anchor in filter(lambda it: it is not None, paragraph.find_all("a")):
        anchor.replace_with(anchor.get_text())


def get_marvel_character_text(html: str) -> list[str]:
    soup = BeautifulSoup(html, "html.parser")

    results = list(
        chain.from_iterable(
            map(
                lambda it: it.find_all("p"), 
                soup.find_all(class_="text"))))

    for item in results:
        replace_anchor_text(item)

    return results


async def main():
    pages = [
        ("Venom", "https://www.marvel.com/characters/venom-eddie-brock/in-comics"),
        ("Wolverine", "https://www.marvel.com/characters/wolverine-logan/in-comics")
    ]

    env = Environment(loader=FileSystemLoader('./templates'))

    template = env.get_template('marvel.html')

    async with aiohttp.ClientSession() as session:
        for character, url in pages:
            async with session.get(url) as response:

                page_html = await response.text()

                results = get_marvel_character_text(page_html)

                final_html = template.render({ 
                    "header": character, 
                    "paragraphs": results 
                })

                with open(f"dist/{character}.html", "w") as writer:
                    writer.write(final_html)


asyncio.run(main())