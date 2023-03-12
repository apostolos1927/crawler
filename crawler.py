from requests_html import AsyncHTMLSession
import asyncio
import time
import DB

db = DB.connectDB()
cursor = db.get_cursor()
STMT = "INSERT INTO BOOK (URL) VALUES (%s)"

successful_urls = []
visited_urls = []


def save_to_db(data):
    cursor.executemany(STMT, data)


async def check_word(request, url):
    if request.html.find("p", containing="history"):
        successful_urls.append(url)


async def crawl(url, asession):
    request = await asession.get(url)
    await check_word(request, url)
    for link in request.html.absolute_links:
        if link not in visited_urls and "books.toscrape.com" in link:
            visited_urls.append(link)
            if len(visited_urls) >= 100:
                break
            await crawl(link, asession)


async def main(urls):
    start_time = time.perf_counter()
    asession = AsyncHTMLSession()
    tasks = [crawl(url, asession) for url in urls]
    await asyncio.gather(*tasks)
    end_time = time.perf_counter()
    print("Successful urls ", successful_urls)
    data = [(link,) for link in successful_urls]
    save_to_db(data)
    db.close_connection()
    print(f"The crawler finished in {end_time-start_time}")


if __name__ == "__main__":
    urls = [
        "http://books.toscrape.com/catalogue/page-1.html",
        "http://books.toscrape.com/catalogue/page-20.html",
        "http://books.toscrape.com/catalogue/page-40.html",
    ]
    asyncio.run(main(urls))
