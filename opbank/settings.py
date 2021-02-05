BOT_NAME = 'opbank'

SPIDER_MODULES = ['opbank.spiders']
NEWSPIDER_MODULE = 'opbank.spiders'
FEED_EXPORT_ENCODING = 'utf-8'
LOG_LEVEL = 'ERROR'
DOWNLOAD_DELAY = 0

ROBOTSTXT_OBEY = True

ITEM_PIPELINES = {
	'opbank.pipelines.OpbankPipeline': 100,

}