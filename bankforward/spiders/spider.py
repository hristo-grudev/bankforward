import scrapy

from scrapy.loader import ItemLoader

from ..items import BankforwardItem
from itemloaders.processors import TakeFirst


class BankforwardSpider(scrapy.Spider):
	name = 'bankforward'
	start_urls = ['https://www.bankforward.com/news']

	def parse(self, response):
		post_links = response.xpath('//*[contains(concat( " ", @class, " " ), concat( " ", "gray", " " ))]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//div[@class="main-content"]/h2/text()').get()
		description = response.xpath('//div[@class="main-content"]/p//text()[normalize-space() and not(ancestor::p[@class="small gray"])]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//p[@class="small gray"]/text()').get()

		item = ItemLoader(item=BankforwardItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
