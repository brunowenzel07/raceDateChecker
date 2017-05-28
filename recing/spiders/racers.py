import scrapy
from recing.items import RecingItem


class MySpider(scrapy.Spider):
    name = 'racers'
    allowed_domains = ['racing.hkjc.com']
    start_urls = []

    def __init__(self, racedate, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://racing.hkjc.com/racing/Info/meeting/Results/english/Local/%s' % (racedate)]
        self.racedate = racedate

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        item = RecingItem()
        racecourse = response.xpath('//td[@class="racingTitle"]/text()').extract()
        noraces = response.xpath('count(//div[@class="raceNum clearfix"]/table/tr/td[@width="24px"])').extract()

        if racecourse and noraces:
            racecourse = racecourse[0]
            noraces = int(float(noraces[0]))
            racecourse = ''.join(c for c in racecourse if c.isupper())
        else:
            racecourse = None
            noraces = None

        text_error = response.xpath('//div[@class="right620"]/div[@class="rowDivLeft font13"]/text()').extract()
        string_error = str(text_error)

        if string_error.find('NotReady') == -1:
            item['racedate'] = self.racedate
            item['racecourse'] = racecourse or None
            item['noraces'] = noraces
            yield item

        else:
            url = 'http://racing.hkjc.com/racing/Info/meeting/Results/english/Local/%s' % self.racedate
            yield scrapy.Request(url, callback=self.parse, method="GET", dont_filter=True)