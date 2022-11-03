import scrapy

reviews_url = 'https://www.amazon.com/product-reviews/{}'
asin_list = ['B00DBL0NLQ']


class ReviewsSpider(scrapy.Spider):
    name = 'reviews'
    

    def start_requests(self):
        for asin in asin_list:
            url = reviews_url.format(asin)
            yield scrapy.Request(url)


    def parse(self, response):
        for review in response.xpath('//div[@data-hook="review"]'):
            item = {
                'name': review.css(' [class="a-profile-name"]::text').get().strip(),
                'review_count': review.css(' a [class="a-icon-alt"]::text').get().strip(),
                'country_date': review.css(' [data-hook="review-date"]::text').get().strip(),
                'review_body': review.css(' [data-hook="review-body"] span::text').get().strip(),

            }

            yield item

        next_page = response.xpath('//a[text()="Next page"]/@href').get()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page))

