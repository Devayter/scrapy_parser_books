import time

import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from books.items import BooksItem


class HitBookSpider(scrapy.Spider):
    name = "hitbook"
    allowed_domains = ["litres.ru"]
    start_urls = ["https://www.litres.ru/collections/hit"]

    def parse(self, response):
        options = webdriver.ChromeOptions()
        options.add_argument("--disable-application-cache")
        driver = webdriver.Chrome(
            service=Service(executable_path=ChromeDriverManager().install()),
            options=options
        )
        driver.get(response.url)
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR,
                'div.Grid-module__gridWrapper_3urZv'
            ))
        )
        scrols = 0
        while scrols < 50:
            scrols += 1
            driver.execute_script(
                "window.scrollTo(0, document.body.scrollHeight);"
            )
            time.sleep(2)
            if scrols % 3 == 0:
                button = driver.find_elements(
                    By.CSS_SELECTOR,
                    'a.Button-module__button_2hpyT'
                )
                if button:
                    driver.execute_script('arguments[0].click();', button[0])
        dynamic_html = driver.page_source
        dynamic_response = HtmlResponse(
            url=driver.current_url,
            body=dynamic_html,
            encoding='utf-8'
        )
        driver.quit()

        links = dynamic_response.css(
            'div.ArtInfo-modules__wrapper_2lOpZ > a::attr(href)'
        ).getall()
        for link in links:
            time.sleep(1)
            yield dynamic_response.follow(link, callback=self.parse_hitbook)

    def parse_hitbook(self, response):
        yield BooksItem(
            author=response.css(
                'div.BookAuthor-module__author__info_Kgg0a span::text'
                ).get(),
            title=response.css(
                'h1.BookCard-module__book__mainInfo__title_2zz4M::text'
                ).get().strip(),
            rating=response.css(
                'meta[itemprop="ratingValue"]::attr(content)'
            ).get(),
            ratings=response.css(
                'meta[itemprop="ratingCount"]::attr(content)'
            ).get(),
            genres=', '.join(response.css(
                'a.BookGenresAndTags-module__genresList__item_1J4yq::text'
                ).getall()).strip(),
            link=response.url
        )
