import scrapy
import shutil
from gruposwhatsapp import directory as dir
from ..items import GruposwhatsappItem
from scrapy.http.request import Request

class grupos_whatsapp(scrapy.Spider):
    name = 'gruposwhatsapp'
    page_number = 2
    start_urls = ['https://gruposwhats.app/']
    filename = "gruposwhats_07-10-2020.csv"
    name_url = 'https://gruposwhats.app/'

    def parse(self, response):
        first_page = response.css('.group')
        #print(first_page)

        for site in first_page:
            title = site.css('.card-title::text').extract()
            about = site.css('.card-text::text').extract()
            link  = site.css('a::attr(href)').extract()
            group = site.css('.card-category::text').extract()

            concat_string = grupos_whatsapp.name_url + 'join-'
            for my_link in link:
                whats_link = concat_string + my_link[1:12]

            new_url = response.urljoin(whats_link)
            request = Request(new_url, callback = self.parse_link, cb_kwargs = {'title': title, 'about': about, 'group': group})
            yield request

        next_page = 'https://gruposwhats.app/?page='+ str(grupos_whatsapp.page_number)

        if grupos_whatsapp.page_number <= 1696:
            grupos_whatsapp.page_number += 1
            yield response.follow(next_page, callback = self.parse)

        if grupos_whatsapp.page_number >= 1697:
            shutil.move(grupos_whatsapp.filename, dir.my_directory)

    def parse_link(self, response, title, about, group):
        items = GruposwhatsappItem()
        whats_page = response.css('._whatsapp_www__block_action')
        new_link = whats_page.css('a::attr(href)').extract()

        items['title'] = title
        items['about'] = about
        items['group']  = group
        items['new_link'] = new_link

        yield items
