import re

import scrapy

from scrapy.loader import ItemLoader
from ..items import OpbankItem
from itemloaders.processors import TakeFirst


class OpbankSpider(scrapy.Spider):
	name = 'opbank'
	start_urls = ['https://www.opbank.lv/blog/']

	def parse(self, response):
		year_links = response.xpath('//select[@name="place"]/option/@value').getall()
		for link in year_links[1:]:
			yield response.follow(link, self.parse_year)

	def parse_year(self, response):
		article_links = response.xpath('//div[@class="panel-body seesam_content"]/ul/li/a/@href')
		yield from response.follow_all(article_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@class="col-md-8 seesam_content"]/p//text()').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="col-md-8 seesam_content"]/span[contains(text(),"[")]/text()').get()

		item = ItemLoader(item=OpbankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', re.findall(r"(\d{2}.\d{2}.\d{4})", date)[0])

		return item.load_item()
