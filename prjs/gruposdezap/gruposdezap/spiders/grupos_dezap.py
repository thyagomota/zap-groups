import scrapy
import shutil
from gruposdezap import directory as dir
from ..items import GruposdezapItem

class grupos_dezap(scrapy.Spider):
    name = 'grupos_dezap'
    page_number = 2
    start_urls = ['https://gruposdezap.com//']
    filename = "gruposdezap_06-26-2020.csv"
    first_container = 0

    def parse(self, response):
        items = GruposdezapItem()
        first_page = response.css('div.desc')
        print(first_page)

        for each_box in first_page:
            about = each_box.css('.text-desc::text').extract()
            link  = each_box.css('a::attr(href)')[1].extract()

            items['about'] = about
            items['link'] = link

            yield items

        next_page = 'https://gruposdezap.com/page/'+ str(grupos_dezap.page_number) +'/'

        if grupos_dezap.page_number <= 1824:
            grupos_dezap.page_number += 1
            yield response.follow(next_page, callback = self.parse)

        if grupos_dezap.page_number >= 1825:
            shutil.move(grupos_dezap.filename, dir.my_directory)
