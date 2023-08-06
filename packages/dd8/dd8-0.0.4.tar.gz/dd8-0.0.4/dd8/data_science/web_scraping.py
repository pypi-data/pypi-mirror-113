# -*- coding: utf-8 -*-
"""
Created on Wed Apr 10 17:06:50 2019

@author: yuanq
"""

# Protocol for robots.txt can be found at http://www.robotstxt.org
# Sitemap standard is defined at http://www.sitemaps.org/protocol.html

# Road Map
# 1. check robots.txt
# 2. check sitemap
# 3. estimating size of website
#    - search for 'site:example.webscraping.com'; number of results will 
#      provide rought indication on size of website
#    - can try to use google api to automate this process
#      (https://developers.google.com/api-client-library/python/start/get_started)
# 4. get web technologies to determine scraping methods
# 5. get web owner to determine if domain is known to block crawlers
# 6. download web pages
# 7. crawl web pages

#import requests
#import urllib.request
#import time
#from bs4 import BeautifulSoup
#import re
#
#url = 'http://web.mta.info/developers/turnstile.html'
#response = requests.get(url)
#
#soup = BeautifulSoup(response.text, 'html.parser')
#results = soup.findAll('a')
#lst_results = list(results)
#
#for i in range(len(lst_results)):
#    
#    if re.findall('turnstile_[0-9]+.txt',str(lst_results[i])):
#        counter = i
#        break
#
#print(counter)

import builtwith as bw
import whois
import urllib
import urllib3
from bs4 import BeautifulSoup
import re

import dd8
import dd8.utility.utils as utils

logger = utils.get_basic_logger(__name__, dd8.LOG_PRINT_LEVEL, dd8.LOG_WRITE_LEVEL)

DIC_GOOGLE_COUNTRY_CODES_MAPPING = {"AFGHANISTAN":"af","ALBANIA":"al","ALGERIA":"dz","AMERICAN SAMOA":"as","ANDORRA":"ad","ANGOLA":"ao","ANGUILLA":"ai","ANTARCTICA":"aq","ANTIGUA AND BARBUDA":"ag","ARGENTINA":"ar","ARMENIA":"am","ARUBA":"aw","AUSTRALIA":"au","AUSTRIA":"at","AZERBAIJAN":"az","BAHAMAS":"bs","BAHRAIN":"bh","BANGLADESH":"bd","BARBADOS":"bb","BELARUS":"by","BELGIUM":"be","BELIZE":"bz","BENIN":"bj","BERMUDA":"bm","BHUTAN":"bt","BOLIVIA":"bo","BOSNIA AND HERZEGOVINA":"ba","BOTSWANA":"bw","BOUVET ISLAND":"bv","BRAZIL":"br","BRITISH INDIAN OCEAN TERRITORY":"io","BRUNEI DARUSSALAM":"bn","BULGARIA":"bg","BURKINA FASO":"bf","BURUNDI":"bi","CAMBODIA":"kh","CAMEROON":"cm","CANADA":"ca","CAPE VERDE":"cv","CAYMAN ISLANDS":"ky","CENTRAL AFRICAN REPUBLIC":"cf","CHAD":"td","CHILE":"cl","CHINA":"cn","CHRISTMAS ISLAND":"cx","COCOS (KEELING) ISLANDS":"cc","COLOMBIA":"co","COMOROS":"km","CONGO":"cg","CONGO, THE DEMOCRATIC REPUBLIC OF THE":"cd","COOK ISLANDS":"ck","COSTA RICA":"cr","COTE D'IVOIRE":"ci","CROATIA":"hr","CUBA":"cu","CYPRUS":"cy","CZECH REPUBLIC":"cz","DENMARK":"dk","DJIBOUTI":"dj","DOMINICA":"dm","DOMINICAN REPUBLIC":"do","ECUADOR":"ec","EGYPT":"eg","EL SALVADOR":"sv","EQUATORIAL GUINEA":"gq","ERITREA":"er","ESTONIA":"ee","ETHIOPIA":"et","FALKLAND ISLANDS (MALVINAS)":"fk","FAROE ISLANDS":"fo","FIJI":"fj","FINLAND":"fi","FRANCE":"fr","FRENCH GUIANA":"gf","FRENCH POLYNESIA":"pf","FRENCH SOUTHERN TERRITORIES":"tf","GABON":"ga","GAMBIA":"gm","GEORGIA":"ge","GERMANY":"de","GHANA":"gh","GIBRALTAR":"gi","GREECE":"gr","GREENLAND":"gl","GRENADA":"gd","GUADELOUPE":"gp","GUAM":"gu","GUATEMALA":"gt","GUINEA":"gn","GUINEA-BISSAU":"gw","GUYANA":"gy","HAITI":"ht","HEARD ISLAND AND MCDONALD ISLANDS":"hm","HOLY SEE (VATICAN CITY STATE)":"va","HONDURAS":"hn","HONG KONG":"hk","HUNGARY":"hu","ICELAND":"is","INDIA":"in","INDONESIA":"id","IRAN, ISLAMIC REPUBLIC OF":"ir","IRAQ":"iq","IRELAND":"ie","ISRAEL":"il","ITALY":"it","JAMAICA":"jm","JAPAN":"jp","JORDAN":"jo","KAZAKHSTAN":"kz","KENYA":"ke","KIRIBATI":"ki","KOREA, DEMOCRATIC PEOPLE'S REPUBLIC OF":"kp","KOREA, REPUBLIC OF":"kr","KUWAIT":"kw","KYRGYZSTAN":"kg","LAO PEOPLE'S DEMOCRATIC REPUBLIC":"la","LATVIA":"lv","LEBANON":"lb","LESOTHO":"ls","LIBERIA":"lr","LIBYAN ARAB JAMAHIRIYA":"ly","LIECHTENSTEIN":"li","LITHUANIA":"lt","LUXEMBOURG":"lu","MACAO":"mo","MACEDONIA, THE FORMER YUGOSALV REPUBLIC OF":"mk","MADAGASCAR":"mg","MALAWI":"mw","MALAYSIA":"my","MALDIVES":"mv","MALI":"ml","MALTA":"mt","MARSHALL ISLANDS":"mh","MARTINIQUE":"mq","MAURITANIA":"mr","MAURITIUS":"mu","MAYOTTE":"yt","MEXICO":"mx","MICRONESIA, FEDERATED STATES OF":"fm","MOLDOVA, REPUBLIC OF":"md","MONACO":"mc","MONGOLIA":"mn","MONTSERRAT":"ms","MOROCCO":"ma","MOZAMBIQUE":"mz","MYANMAR":"mm","NAMIBIA":"na","NAURU":"nr","NEPAL":"np","NETHERLANDS":"nl","NETHERLANDS ANTILLES":"an","NEW CALEDONIA":"nc","NEW ZEALAND":"nz","NICARAGUA":"ni","NIGER":"ne","NIGERIA":"ng","NIUE":"nu","NORFOLK ISLAND":"nf","NORTHERN MARIANA ISLANDS":"mp","NORWAY":"no","OMAN":"om","PAKISTAN":"pk","PALAU":"pw","PALESTINIAN TERRITORY, OCCUPIED":"ps","PANAMA":"pa","PAPUA NEW GUINEA":"pg","PARAGUAY":"py","PERU":"pe","PHILIPPINES":"ph","PITCAIRN":"pn","POLAND":"pl","PORTUGAL":"pt","PUERTO RICO":"pr","QATAR":"qa","REUNION":"re","ROMANIA":"ro","RUSSIAN FEDERATION":"ru","RWANDA":"rw","SAINT HELENA":"sh","SAINT KITTS AND NEVIS":"kn","SAINT LUCIA":"lc","SAINT PIERRE AND MIQUELON":"pm","SAINT VINCENT AND THE GRENADINES":"vc","SAMOA":"ws","SAN MARINO":"sm","SAO TOME AND PRINCIPE":"st","SAUDI ARABIA":"sa","SENEGAL":"sn","SERBIA AND MONTENEGRO":"cs","SEYCHELLES":"sc","SIERRA LEONE":"sl","SINGAPORE":"sg","SLOVAKIA":"sk","SLOVENIA":"si","SOLOMON ISLANDS":"sb","SOMALIA":"so","SOUTH AFRICA":"za","SOUTH GEORGIA AND THE SOUTH SANDWICH ISLANDS":"gs","SPAIN":"es","SRI LANKA":"lk","SUDAN":"sd","SURINAME":"sr","SVALBARD AND JAN MAYEN":"sj","SWAZILAND":"sz","SWEDEN":"se","SWITZERLAND":"ch","SYRIAN ARAB REPUBLIC":"sy","TAIWAN, PROVINCE OF CHINA":"tw","TAJIKISTAN":"tj","TANZANIA, UNITED REPUBLIC OF":"tz","THAILAND":"th","TIMOR-LESTE":"tl","TOGO":"tg","TOKELAU":"tk","TONGA":"to","TRINIDAD AND TOBAGO":"tt","TUNISIA":"tn","TURKEY":"tr","TURKMENISTAN":"tm","TURKS AND CAICOS ISLANDS":"tc","TUVALU":"tv","UGANDA":"ug","UKRAINE":"ua","UNITED ARAB EMIRATES":"ae","UNITED KINGDOM":"uk","UNITED STATES":"us","UNITED STATES MINOR OUTLYING ISLANDS":"um","URUGUAY":"uy","UZBEKISTAN":"uz","VANUATU":"vu","VENEZUELA":"ve","VIET NAM":"vn","VIRGIN ISLANDS, BRITISH":"vg","VIRGIN ISLANDS, U.S.":"vi","WALLIS AND FUTUNA":"wf","WESTERN SAHARA":"eh","YEMEN":"ye","ZAMBIA":"zm","ZIMBABWE":"zw"}
DIC_GOOGLE_LANGUAGE_CODES_MAPPING = {"AFRIKAANS":"af","ALBANIAN":"sq","AMHARIC":"sm","ARABIC":"ar","AZERBAIJANI":"az","BASQUE":"eu","BELARUSIAN":"be","BENGALI":"bn","BIHARI":"bh","BOSNIAN":"bs","BULGARIAN":"bg","CATALAN":"ca","CHINESE (SIMPLIFIED)":"zh-CN","CHINESE (TRADITIONAL)":"zh-TW","CROATIAN":"hr","CZECH":"cs","DANISH":"da","DUTCH":"nl","ENGLISH":"en","ESPERANTO":"eo","ESTONIAN":"et","FAROESE":"fo","FINNISH":"fi","FRENCH":"fr","FRISIAN":"fy","GALICIAN":"gl","GEORGIAN":"ka","GERMAN":"de","GREEK":"el","GUJARATI":"gu","HEBREW":"iw","HINDI":"hi","HUNGARIAN":"hu","ICELANDIC":"is","INDONESIAN":"id","INTERLINGUA":"ia","IRISH":"ga","ITALIAN":"it","JAPANESE":"ja","JAVANESE":"jw","KANNADA":"kn","KOREAN":"ko","LATIN":"la","LATVIAN":"lv","LITHUANIAN":"lt","MACEDONIAN":"mk","MALAY":"ms","MALAYAM":"ml","MALTESE":"mt","MARATHI":"mr","NEPALI":"ne","NORWEGIAN":"no","NORWEGIAN (NYNORSK)":"nn","OCCITAN":"oc","PERSIAN":"fa","POLISH":"pl","PORTUGUESE (BRAZIL)":"pt-BR","PORTUGUESE (PORTUGAL)":"pt-PT","PUNJABI":"pa","ROMANIAN":"ro","RUSSIAN":"ru","SCOTS GAELIC":"gd","SERBIAN":"sr","SINHALESE":"si","SLOVAK":"sk","SLOVENIAN":"sl","SPANISH":"es","SUDANESE":"su","SWAHILI":"sw","SWEDISH":"sv","TAGALOG":"tl","TAMIL":"ta","TELUGU":"te","THAI":"th","TIGRINYA":"ti","TURKISH":"tr","UKRAINIAN":"uk","URDU":"ur","UZBEK":"uz","VIETNAMESE":"vi","WELSH":"cy","XHOSA":"xh","ZULU":"zu"}

def get_header():
    return {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:49.0) Gecko/20100101 Firefox/49.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate',
            'DNT': '1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
            }

# def google(q):
#     s = requests.Session()
#     q = '+'.join(q.split())
#     url = 'https://news.google.com/search?q=' + q + '&ie=utf-8&oe=utf-8&ceid=US:en'
#     r = s.get(url, headers=headers_Get)
#     print(url)
#     soup = BeautifulSoup(r.text, "html.parser")
#     output = []
#     for searchWrapper in soup.find_all('h3', {'class':'ipQwMb ekueJc RD0gLb'}): #this line may change in future based on google's web page structure
#         url = searchWrapper.find('a')["href"] 
#         text = searchWrapper.find('a').text.strip()
#         result = {'text': text, 'url': url}
#         output.append(result)

#     return output


# for link in google('covid vaccine'):
#     print(link['text'])

class Google(object):
    #https://developers.google.com/custom-search/docs/xml_results_appendices#countryCodes
    #https://developers.google.com/custom-search/v1/reference/rest/v1/cse/list
    #https://www.geeksforgeeks.org/performing-google-search-using-python-code/
    def __init__(self, str_domain, 
                 str_language,
                 str_geolocation,
                 str_encoding = 'utf-8'):
        pass
    
    
def get_url(str_url):
    """
    Wrapper for `urllib.request.urlopen` with error handling. Returns 
    `http.client.HTTPResponse` object which can work as a context manager.
    
    Parameters
    ----------
    str_url : str
        URL to open.
        
    Return
    ------
    http.client.HTTPResponse
        Context manager for given URL, `None` if error encountered.
    """
    response = None
    try:
        response = urllib.request.urlopen(str_url)        
    except urllib.error.HTTPError as e:
        logger.error(e)
    except urllib.error.URLError as e:
        logger.error('Server not found!')
    finally:
        return response

class HTML(object):
    pass

class Webpage(object):
    """
    Represents a particular `Webpage` on a `Website`. Lazy loading is used and
    website is only accessed when `read` method of a `Webpage` object is called.
    
    Attributes
    ----------
    url : str
        URL of the webpage.
    web_tech : dict
        dictionary of lists the form {'webpage_component' : list_of_technologies}.
        For example, {'programming-language' : ['Lua']}.
    whois : whois.parser.WhoisCom
        dictionary of server details of webpage. For example, {'domain_name' :
        list_of_domain_names}.    
    html
    
    Methods
    -------
    read(parser='html.parser')
        Reads and return HTML of the given URL.   
    """    
    def __init__(self, str_url):
        self.url = str_url        
        
    @property
    def url(self):
        return self.__str_url
    
    @url.setter
    def url(self, str_url):
        self.__str_url = str_url
    
    @property
    def web_tech(self):
        return bw.parse(self.url)
    
    @property
    def whois(self):
        return whois.whois(self.url)

    @property
    def html(self):
        pass

    @property
    def read(self, parser='html.parser'):
        """
        Reads and return HTML of the given url.
        
        Parameters
        ----------
        parser : str, optional
            parser to be used by BeautifulSoup to parse the webpage (default is
            html.parser)
                html.parser - included with Python 3
                lxml - requires installation but more flexible and faster
                html5lib - requires installation and slower than both html.parser
                    and lxml but more flexible
        """
#        if self.__bln_verbose:
#            print('Downloading: ' + self.__str_url)
        
        headers = {'User-agent': 'wswp'}
        http = urllib3.PoolManager()
        response = http.request('GET', self.__str_url, headers = headers)            
#        print(response.status)
        if response.status == 200:
            html = response.data.decode('utf-8') 
        else:
            if response.status >= 500 and response.status < 600:
                response = http.request('GET', self.__str_url, retries=5)            
                if response.status != 200:
#                    if self.__bln_verbose:
#                        print('Download Error: ' + str(response.status))
                    html = None
                else:
                    html = response.data.decode('utf-8')
            else:
#                if self.__bln_verbose:
#                        print('Download Error: ' + str(response.status))
                html = None
        return html




class Website(object):
    def __init__(self, str_domain_url):
        self.url = str_domain_url
        self.domain = self.url
        
    @property
    def url(self):
        return self.__str_original_url
    
    @url.setter
    def url(self, str_url):
        self.__str_original_url = str_url
    
    @property
    def domain(self):
        return self.__str_domain_url
    
    @domain.setter
    def domain(self, str_domain_url):
        __ = str_domain_url.split('//')
        self.__str_domain_url = '//'.join(__[:-1]) + '//' +__[-1].split('/')[0]
        
    @property
    def robots(self):
        return Webpage(self.domain+'/robots.txt').html


class WebScrape():
    def __init__(self, str_url, 
                 bln_scrape_sitemap = False, 
                 bln_verbose = False):
        self.__str_url = str_url
        self.__bln_verbose = bln_verbose
    
    def __del__(self):
        pass
    
    def __len__(self):
        pass
    
    def __repr__(self):
        pass
    
    def get_web_tech(self):        
        return bw.parse(self.__str_url)

    def get_web_owner(self):
        return whois.whois(self.__str_url)    
    
    def get_sitemap_urls(self, str_sitemap_url):
        sitemap = self.get_web_page(str_sitemap_url)
        print(sitemap)
        links = re.findall('<loc>(.*?)</loc>', sitemap)
        return links
    
    def get_web_page(self, 
                     str_user_agent = 'wswp',
                     int_retries = 5):
        
    # https://stackoverflow.com/questions/630453/put-vs-post-in-rest
    
        if self.__bln_verbose:
            print('Downloading: ' + self.__str_url)
        
        headers = {'User-agent': str_user_agent}
        http = urllib3.PoolManager()
        response = http.request('GET', self.__str_url, headers = headers)            
        print(response.status)
        if response.status == 200:
            html = response.data.decode('utf-8') 
        else:
            if response.status >= 500 and response.status < 600:
                response = http.request('GET', self.__str_url, retries=int_retries)            
                if response.status != 200:
                    if self.__bln_verbose:
                        print('Download Error: ' + str(response.status))
                    html = None
                else:
                    html = response.data.decode('utf-8')
            else:
                if self.__bln_verbose:
                        print('Download Error: ' + str(response.status))
                html = None
        return html
        

if __name__ == '__main__':

#    scrape = WebScrape('https://www.careers.gov.sg')
#    print(scrape.get_web_tech())
    #scrape = WebScrape('http://www.bloomberg.com/')
    #print(scrape.get_web_tech())
    #print(scrape.get_web_page())
    
    #links = scrape.get_sitemap_urls('https://www.bloomberg.com/feeds/bbiz/sitemap_index.xml')
    #print(links)
    
#    ws = Website('https://www.bloomberg.com/asia')
    wp = Webpage('https://www.bloomberg.com/asia')
    