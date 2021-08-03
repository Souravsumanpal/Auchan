import scrapy


class ProductSpider(scrapy.Spider):
    name = 'product'
    # allowed_domains = ['a']
    page_number = 2
    start_urls = ['https://www.auchan.fr/marques/harry-potter/c-55565']


    def parse(self, response):
        links = response.css('.sub a')
        for link in links:
            link_each = link.css('a::attr(href)').get()
            flink = response.urljoin(link_each)
            # print(flink)
            yield scrapy.Request(url=flink, callback=self.parse_item_toy)


    def parse_item_toy(self, response):
        links = response.css('.product-item--wrapper a')
        for link in links:
            link_each = link.css('a::attr(href)').get()
            flink = response.urljoin(link_each)
            # print(flink)
            yield scrapy.Request(url=flink, callback=self.parse_item)

        next_page = 'https://www.auchan.fr/marques/harry-potter/c-55565?sort=position-asc&engine=fh&show=FORTY_EIGHT&page='+ str(ProductSpider.page_number)  
        if ProductSpider.page_number <= 8:
            ProductSpider.page_number += 1
            yield response.follow(next_page, callback=self.parse)  

    def parse_item(self,response):
        title = response.css('.product-detail--title::text').get()
        price = response.css('.product-price--formattedValue::text').get()
        image = response.css('.js-native-scroller--item img::attr(src)').getall()

        yield {
            'title': title,
            'price': price,
            'image': image,
        }


