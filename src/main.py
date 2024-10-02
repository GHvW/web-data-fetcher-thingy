import aiohttp
import asyncio
from itertools import chain
from bs4 import BeautifulSoup

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
    async with aiohttp.ClientSession() as session:
        # async with session.get("https://www.marvel.com/characters/venom-eddie-brock/in-comics") as response:
        async with session.get("https://www.marvel.com/characters/wolverine-logan/in-comics") as response:

            print("Status:", response.status)
            print("Content-type:", response.headers['content-type'])

            html = await response.text()

            results = get_marvel_character_text(html)

            print("#results", len(results))

            with open("venom.html", "w") as writer:
                writer.write("<html><head><link rel='stylesheet' type='text/css' href='./pages.css'></head><body>")

                writer.write("<div class='container'><div id='heading'>")
                writer.write("Venom")
                writer.write("</div></div>")

                writer.write("<div class='container'><div id='content'>")

                for item in results:
                    writer.write(str(item))

                writer.write("</div></div></body></html>")


asyncio.run(main())