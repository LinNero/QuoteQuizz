from django.core.management.base import BaseCommand, CommandError
from bs4 import BeautifulSoup
import urllib.request
from quiz.models import Category, Source, Quote


class Command(BaseCommand):
    help = 'Start the parser'

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
        if Source.objects.exists():
            print('Источники уже существуют')
            return

        for category in Category.objects.all():
            url = 'https://citaty.info' + category.url
            response = urllib.request.urlopen(url)
            html_doc = response.read()
            soup = BeautifulSoup(html_doc, 'html.parser')

            div_list = soup.find_all("div", class_=["field-item field-name-field-books-ref odd",
                                                    "field-item field-name-field-books-ref even"])
            for div in div_list:
                link = div.find('a')
                source_name = link.get_text()
                source_href = link.get('href')
                source = Source(name=source_name, url=source_href, category_id=category)
                source.save()
                print(source)
            break



    def parse_quotelist(self):
        if Quote.objects.exists():
            print('Цитаты уже существуют')
            return

        for source in Source.objects.all():
            response = urllib.request.urlopen(source.url)
            html_doc = response.read()

            soup = BeautifulSoup(html_doc, 'html.parser')

            mydivs = soup.find_all("div", {"class": "field-item even last"})
            for quote_div in mydivs:
                paragraph = quote_div.find('p')
                if paragraph:
                    text = paragraph.get_text()
                    quote = Quote(text=text, source=source)
                    quote.save()
                    print(text)
            break
