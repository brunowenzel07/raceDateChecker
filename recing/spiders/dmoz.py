import scrapy
from recing.items import RecingItem


class MySpider(scrapy.Spider):
    name = 'racing'
    allowed_domains = ['racing.hkjc.com']
    start_urls = []

    def __init__(self, racedate, racecourse, racenumber, *args, **kwargs):
        super(MySpider, self).__init__(*args, **kwargs)
        self.start_urls = ['http://racing.hkjc.com/racing/Info/meeting/Results/english/Local/%s/%s/%s' % (racedate,
                                                                                                          racecourse,
                                                                                                          racenumber)]
        self.racedate = racedate
        self.racecourse = racecourse
        self.racenumber = racenumber

    def parse(self, response):
        self.logger.info('A response from %s just arrived!', response.url)
        item = RecingItem()
        all_id = response.xpath(
            '//table[@class="tableBorder trBgBlue tdAlignC number12 draggable"]/tbody/tr/td[1]/text()').extract()
        all_race = response.xpath(
            '//table[@class="tableBorder trBgBlue tdAlignC number12 draggable"]/tbody/tr/td[3]/text()').extract()
        item['racedate'] = self.racedate
        item['racecourse'] = self.racecourse
        item['racenumber'] = self.racenumber
        item['runners'] = []
        for id, race in zip(all_id, all_race):
            item['runners'].append({'place': id, 'horsecode': race.strip('()')})
        return item

