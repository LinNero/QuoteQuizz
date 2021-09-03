from django.core.management.base import BaseCommand
from bs4 import BeautifulSoup
import urllib.request
from quiz.models import Category, Source, Quote
import time


class Command(BaseCommand):
    help = 'Start the parser'
    BOOK_PARSER_PAGES = ['/book']
    MEDIA_PARSER_PAGES = ['/movie', '/series', '/anime', '/cartoon', '/game', '/tv']

    def handle(self, *args, **options):
        self.parse_categorylist()
        self.parse_sourcelist()
        self.parse_quotelist()

    def parse_categorylist(self):
        if Category.objects.exists():
            print('категории уже существуют')
            return

        response = urllib.request.urlopen('https://citaty.info')
        html_doc = response.read()
        soup = BeautifulSoup(html_doc, 'html.parser')
        subnav__list = soup.find("ul", {"class": "subnav__list"})
        links = subnav__list.find_all("a", {"class": "subnav__link"})
        for link in links:
            category_name = link.get_text()
            category_href = link.get('href')
            c = Category(name=category_name, url=category_href)
            c.save()
            print(c)

    def parse_sourcelist(self):
        # if Source.objects.exists():
        #     print('Источники уже существуют')
        #     return

        for category in Category.objects.all():
            if category.sources.exists():
                continue

            url = 'https://citaty.info' + category.url
            response = urllib.request.urlopen(url)
            html_doc = response.read()
            soup = BeautifulSoup(html_doc, 'html.parser')

            if category.url in self.BOOK_PARSER_PAGES:
                self.book_parser(category, soup)
            elif category.url in self.MEDIA_PARSER_PAGES:
                self.media_parser(category, soup)
            else:
                continue

    def book_parser(self, category, soup):
        print(f"BOOK_PARSER_PAGES: {category.url}")

        author_divs = soup.find_all("div", {"class": "taxonomy-term vocabulary-vocabulary-3"})
        for author_div in author_divs:
            author_name_div = author_div.find("div", {"class": "term-name field-type-entityreference"})
            author_name = author_name_div.find('a').get_text()

            div_list = author_div.find_all("div", class_=["field-item field-name-field-books-ref odd",
                                                    "field-item field-name-field-books-ref even"])
            for div in div_list:
                link = div.find('a')
                source_name = f"{link.get_text()} ({author_name})"
                source_href = link.get('href')
                source = Source(name=source_name, url=source_href, category_id=category)
                source.save()
                print(source)


    def media_parser(self, category, soup):
        print(f"MEDIA_PARSER_PAGES: {category.url}")

        div_list = soup.find_all("div", class_=["term-name field-type-entityreference"])
        for div in div_list:
            link = div.find('a')
            source_name = link.get_text()
            source_href = link.get('href')
            source = Source(name=source_name, url=source_href, category_id=category)
            source.save()
            print(source)


    def parse_quotelist(self):
        # if Quote.objects.exists():
        #     print('Цитаты уже существуют')
        #     return

        for source in Source.objects.all():
            # if source.category_id.url == '/book':
            #     continue
            if source.quotes.exists():
                continue

            print(f"PARSING {source.url}")
            response = urllib.request.urlopen(source.url)
            html_doc = response.read()

            soup = BeautifulSoup(html_doc, 'html.parser')

            articles = soup.find_all("article")
            for article in articles:

                quote_div = article.find("div", {"class": "field-item even last"})
                paragraph = quote_div.find('p')
                text = paragraph.get_text()
                print(text)

                rating_div = article.find("div", {"class": "rating__value__digits"})
                rating = int(rating_div.get_text())
                print(rating)

                quote = Quote(text=text, source=source, rating=rating)
                quote.save()

            print("Sleeping for 1 second...")
            time.sleep(1)

            q_count = Quote.objects.count()
            print(f"Quotes count: {q_count}")
            if Quote.objects.count() >= 10000:
                break
            # break


