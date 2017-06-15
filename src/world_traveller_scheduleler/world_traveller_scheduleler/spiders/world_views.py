# -*- coding: utf-8 -*-

# TODO scrapy支援logging 要把爬蟲的紀錄補上
import re
import uuid
import scrapy
from world_traveller_scheduleler.items import WorldTravellerSchedulelerItem
from urlparse import urlparse, parse_qs
import logging

class WorldViewsSpider(scrapy.Spider):
    """
    世界景點從tripadvisor抓取
    世界景點從景點家抓取
    """
    name = 'world_views'
    allowed_domains = ['mook.com.tw']    
    start_urls = ['http://www.mook.com.tw/scenerysearch.php?continent_id=0&country_id=0&area_id=0&city_id=0&district_id=0&keyword=&display=20']

    def __init__(self, *args, **kwargs):
        logger = logging.getLogger('scrapy.spidermiddlewares.httperror')
        logger.setLevel(logging.WARNING)

    def parse(self, response):
        """ 從此開始抓取景點 """
        for view in response.css('div.row > div.post'):
            href = view.css('figure.figure > a::attr(href)')[0]
            view_url = response.urljoin(href.extract())
            yield scrapy.Request(view_url, callback=self.parse_detail)
        
        current_page = response.css('ul.pagination>li.active')
        next_page_url = response.css('ul.pagination>li.active ~ li > a::attr(href)').extract_first(None)
        next_page_parsed = urlparse(next_page_url)
        next_page_querystring = parse_qs(next_page_parsed.query)

        if next_page_querystring:
            next_page = next_page_querystring['page'][0]

        if next_page.isdigit():
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)

    def parse_detail(self, response):
        """ 抓景點的詳細資料 """
        print 'detail view page: %s' % response.url
        item = WorldTravellerSchedulelerItem()
        item['viewid'] = uuid.uuid4()
        item['name'] = response.css('div.col-md-12 >h2.goviewcolor').xpath('//h2/text()').extract_first(None)
        item['location'] = response.css('div.col-md-12 > div.meta > small').xpath('//small/text()').extract_first(None)
        item['cover'] = response.css('div#owl-demo img::attr(src)').extract_first(None)
        item['description'] = response.css('div.container-fluid.maincontent > p').extract_first(None)
        item['address'] =  response.css('div.container-fluid.maincontent > div> ul.list-other > li > i.fa.fa-location-arrow ~ strong').xpath('//strong/text()').extract_first(None)
        item['contact'] =  response.css('div.container-fluid.maincontent > div> ul.list-other > li > i.fa.fa-phone ~ strong').xpath('//strong/text()').extract_first(None)
        item['homepage'] =  response.css('div.container-fluid.maincontent > div> ul.list-other > li > i.fa.fa-link ~ a::attr(href)').extract_first(None)
        item['business_hours'] =  response.css('div.container-fluid.maincontent > div> ul.list-other > li > i.fa.fa-clock-o ~ strong').xpath('//strong/text()').extract_first(None)

        parsed = urlparse(response.url)
        querystring = parse_qs(parsed.query)

        if querystring:
            item['outer_key'] = querystring['sceneryid'][0]

        re_lng = r'myLongitude_arr\[0\] = \d+\.\d+;'
        re_lat = r'myLatitude_arr\[0\] = \d+\.\d+;'

        if response.xpath('//script').re(re_lng):
            lng_str = response.xpath('//script').re(re_lng)[0]   
            item['lng'] = lng_str.replace('myLongitude_arr[0] = ', '').replace(';', '')

        if response.xpath('//script').re(re_lat):
            lat_str = response.xpath('//script').re(re_lat)[0]
            item['lat'] = lat_str.replace('myLatitude_arr[0] = ', '').replace(';', '')

        yield item
