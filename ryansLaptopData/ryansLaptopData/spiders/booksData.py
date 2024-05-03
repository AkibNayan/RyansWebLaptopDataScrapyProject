import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BooksdataSpider(CrawlSpider):
    name = "booksData"
    start_urls = [
        "https://www.ryans.com/category/laptop-all-laptop?limit=100&sort=LT&osp=1&st=0&page=1"]

    rules = (Rule(LinkExtractor(
        restrict_xpaths='//div[@class="image-box"]/a'), callback="parse_item", follow=True),
        Rule(LinkExtractor(restrict_xpaths='//a[@aria-label="Next »"]'), callback="parse_item", follow=False))

    def parse_item(self, response):
        title = response.xpath('//div/h1[@itemprop="name"]/text()').get()
        rating_cnts = response.xpath(
            '//div[@class="product_content h-100"]/div[@class="rating"]//span[@class="fas fa-star stars"]').getall()
        rating = 0
        for rating_cnt in rating_cnts:
            rating += 1
        review = response.xpath(
            '//span[@class="review-text"]//a[@class="review-link"]//text()').get()
        if response.xpath('//span[@class="sp-block"]//text()'):
            regularPrice = response.xpath('//span[@class="sp-block"]//text()').get()
            regularPrice = regularPrice.split(" ")
            regularPrice = regularPrice[-1]
        else:
            regularPrice = response.xpath('(//span[@class="sp-block"]/span)[1]//text()').get()
            regularPrice = regularPrice.split(" ")
            regularPrice = regularPrice[-1]
        short_description = response.xpath('//div[@class="short-desc-attr"]/ul/li/text()').getall()
        desc = []
        for short_desc in short_description:
            desc.append(short_desc)
        specifications = response.xpath(
            '//div[@class="col-lg-4 col-12 ps-4 ps-lg-0"]/span/text()').getall()
        for index, category in enumerate(specifications, start=1):
            if category == "Brand":
                brand = response.xpath(
                    f'(//div[@class="col-lg-8 col-12 ps-5 ps-lg-0"]/span/text())[{index}]').get()
            elif category == "Model":
                model = response.xpath(
                    f'(//div[@class="col-lg-8 col-12 ps-5 ps-lg-0"]/span/text())[{index}]').get()

        yield {
            "title": title,
            "rating": rating,
            "review": review,
            "regularPrice": regularPrice,
            "short_desc": desc,
            "brand": brand,
            "model": model
        }
