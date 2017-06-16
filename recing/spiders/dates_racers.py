import scrapy
from recing.items import RecingItem
import datetime


class MySpider(scrapy.Spider):
    name = 'racers2'
    allowed_domains = ['racing.hkjc.com']
    start_urls = []


    def __init__(self, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        date_from = datetime.datetime.strptime('20160901', '%Y%m%d').date()
        date_to = datetime.datetime.strptime('20170614', '%Y%m%d').date()
        dates = [(date_from + datetime.timedelta(days=i)).strftime('%Y%m%d') for i in
                 range((date_to - date_from).days + 1)]

        for racedate in dates:
            self.start_urls.append('http://racing.hkjc.com/racing/Info/meeting/Results/english/Local/%s' % (racedate))

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        item = RecingItem()
        racecourse = response.xpath('//td[@class="racingTitle"]/text()').extract()
        # noraces = response.xpath('count(//div[@class="raceNum clearfix"]/table/tr/td[@width="24px"])').extract()
        noraces = response.xpath('count(//div[@class="raceNum clearfix"]/table//tr[1]//td/a)').extract()
        racedate1 = response.url
        racedate1 = racedate1.split('/')
        racedate1 = racedate1[-1]

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
            item['racedate_str'] = racedate1
            item['racedate'] = datetime.datetime.strptime(racedate1, '%Y%m%d')
            item['racecourse'] = racecourse or None
            item['noraces'] = noraces
            yield item

        else:
            url = 'http://racing.hkjc.com/racing/Info/meeting/Results/english/Local/%s' % racedate1
            yield scrapy.Request(url, callback=self.parse, method="GET", dont_filter=True)
