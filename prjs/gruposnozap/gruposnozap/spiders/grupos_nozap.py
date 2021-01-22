import scrapy
import shutil
from gruposnozap import directory as dir
from ..items import GruposnozapItem

class grupos_nozap(scrapy.Spider):
    name = 'grupos_nozap'
    page_number = 2
    start_urls = ['https://gruposnozap.com/']
    filename = "Test_groups28.csv"

    def parse(self, response):
        items = GruposnozapItem()
        first_page = response.css('.home-main')
        #print(first_page)

        for site in first_page:
            title = site.css('.single-title-conteudo::text').extract()
            about = site.css('.text-desc::text').extract()
            link  = site.css('a::attr(href)').extract()

            items['title'] = title
            items['about'] = about
            items['link'] = link

            yield items

        next_page = 'https://gruposnozap.com/page/'+ str(grupos_nozap.page_number) + '/'

        if grupos_nozap.page_number <= 3:
            grupos_nozap.page_number += 1
            yield response.follow(next_page, callback = self.parse)

        if grupos_nozap.page_number >= 6:
            shutil.move(grupos_nozap.filename, dir.my_directory)
