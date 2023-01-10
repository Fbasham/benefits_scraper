import asyncio
import json
from requests_html import AsyncHTMLSession


async def fetch(s,url):
    r = await s.get(url)
    return {'url':url,'text':r.html.find('main',first=True).text}

async def main():
    s = AsyncHTMLSession()
    with open('data.txt','r') as f:
        urls = [*map(str.strip,f.readlines())]
    return await asyncio.gather(*(fetch(s,url) for url in urls))


if __name__=='__main__':
    r = asyncio.run(main())
    with open('scraped.json','w') as f:
        json.dump(r,f)