import json
import scrapy
import pipelines


class Spider(scrapy.Spider):
    name = 'ebohub'
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:7.0.1) Gecko/20100101 Firefox/7.0.1',
        'ITEM_PIPELINES': {
            'pipelines.MongoPipeline': 300
        }
    }

    def start_requests(self):
        yield scrapy.Request('https://www.pornhub.com/recommended')
        yield scrapy.Request('https://www.pornhub.com/video?o=ht')
        yield scrapy.Request('https://www.pornhub.com/video?o=mv')
        yield scrapy.Request('https://www.pornhub.com/video?o=tr')

    def parse(self, response):
        for x in response.xpath('//li[@_vkey]/@_vkey').extract():
            yield scrapy.Request('https://www.pornhub.com/view_video.php?viewkey=%s' % x, callback=self.details)

    def details(self, response):
        data = json.loads(response.xpath('//script').re_first(r'flashvars_\d+ = (.+);'))
        yield {
            '_id': response.url.split('=')[-1],
            'title': data.get('video_title'),
            'image': data.get('image_url'),
            'video': next(x['videoUrl'] for x in data['mediaDefinitions'] if x['quality'] == '480'),
            'duration': int(data.get('video_duration'))
        }