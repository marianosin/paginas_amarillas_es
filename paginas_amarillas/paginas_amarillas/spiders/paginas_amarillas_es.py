import scrapy


class PaginasAmarillasEsSpider(scrapy.Spider):
    name = "paginas_amarillas_es"
    allowed_domains = ["www.paginasamarillas.es"]
    start_urls = ["https://www.paginasamarillas.es"]

    #Function to get initial links to scrape
    def parse(self, response):

        #Get all links from the main page
        for link in response.xpath('//div[@class="directorio"]/div[@class="container"]/div[@class="row"]//a//@href').extract():
            yield scrapy.Request(link, callback=self.parse_page)


    #Function to get the information from the links

    def parse_page(self, response):

        # Get all items from page that are div with prop itemprop="itemListElement"
        for item in response.xpath('//div[@itemprop="itemListElement"]'):
            yield {
                'name': item.xpath('.//h2/span[@itemprop="name"]/text()').extract_first(),
                'address': item.xpath('.//div[@class="address"]/text()').extract_first(),
                'postal_code': item.xpath('.//span[@itemprop="postalCode"]/text()').extract_first(),
                'city': item.xpath('.//span[@itemprop="addressLocality"]/text()').extract_first(),
                'phone': item.xpath('.//span[@itemprop="telephone"]/text()').extract_first(),
                'email': item.xpath('.//a[@itemprop="email"]/text()').extract_first(),
                'website': item.xpath('.//a[@itemprop="url"]/@href').extract_first(),
                'category': response.xpath('//h1/text()').extract_first()
            }

        # Get next page list of links with div class pag2
        next_link_list = response.xpath('//div[@class="pag2"]//ul//li//a/@href').extract()
        if next_link_list:
            # Get the last link in the list for comparison
            last_link = next_link_list[-1]
            for link in next_link_list:
                if 'javascript' in link:
                    continue
                # Compare the current link with the last link instead of comparing page numbers
                if link == last_link:
                    break
                yield scrapy.Request(response.urljoin(link), callback=self.parse_page)