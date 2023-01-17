import asyncio
import json
from requests_html import AsyncHTMLSession

import os
SCRAPED_URLS_PATH = os.path.join(os.path.dirname(__file__),'data/urls.txt')
SCRAPED_DATA_PATH = os.path.join(os.path.dirname(__file__),'data/scraped.json')

async def fetch(s,url):
    r = await s.get(url)
    return {
        'url':url,
        'title':r.html.find('h1',first=True).text,
        'text':r.html.find('main',first=True).text
    }

async def main():
    s = AsyncHTMLSession()
    with open(SCRAPED_URLS_PATH,'r') as f:
        urls = [*map(str.strip,f.readlines())]
    return await asyncio.gather(*(fetch(s,url) for url in urls))


if __name__=='__main__':
    r = asyncio.run(main())
    with open(SCRAPED_DATA_PATH,'w') as f:
        json.dump(r,f)