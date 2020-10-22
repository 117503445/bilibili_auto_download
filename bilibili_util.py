import requests
from tqdm import tqdm
import json
import file_util
from lxml import etree


def get_one_page_list_video(page_num):
    params = (
        ('mid', '54992199'),
        ('cid', '82529'),
        ('pn', str(page_num)),
        ('ps', '100'),
    )

    response = requests.get(
        'https://api.bilibili.com/x/space/channel/video', params=params)

    js = json.loads(response.text)
    av = js['data']['list']['archives']

    list_video = []

    for a in av:
        bvid = a['bvid']
        title = a['title']
        list_video.append(
            [f'https://www.bilibili.com/video/{bvid}', f'{title}.mp4'])

    return list_video


def resolve_video_path(bv_url: str):

    session = requests.session()
    response = session.get('https://bilibili.syyhc.com')
    html = etree.HTML(response.text)
    csrf_token = html.xpath('//*[@id="csrf_token"]/@value')[0]

    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'https://bilibili.syyhc.com',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36 Edg/86.0.622.43',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'navigate',
        'Sec-Fetch-User': '?1',
        'Sec-Fetch-Dest': 'document',
        'Referer': 'https://bilibili.syyhc.com/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }

    data = {
        'url': 'https://www.bilibili.com/video/BV1954y167cs',
        'go': '',
        'csrf_token': csrf_token
    }

    response = session.post(
        'https://bilibili.syyhc.com/parser', headers=headers,  data=data)

    html = etree.HTML(response.text)
    return html.xpath('//*[@id="video"]/source/@src')[0]


def download(url: str, file_path: str):

    url = resolve_video_path(url)

    headers = {
        'authority': 'upos-sz-mirrorks3.bilivideo.com',
        'pragma': 'no-cache',
        'cache-control': 'no-cache',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.80 Safari/537.36 Edg/86.0.622.43',
        'accept': '*/*',
        'sec-fetch-site': 'cross-site',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-dest': 'video',
        'referer': 'https://bilibili.syyhc.com/',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'range': 'bytes=0-',
    }

    with requests.get(url, headers=headers, stream=True) as r:
        content_size = int(r.headers['content-length'])
        with open(file_path, 'wb') as f:
            with tqdm(total=content_size) as pbar:
                for i in r.iter_content(chunk_size=4096):
                    pbar.update(4096)
                    f.write(i)


def main():
    # get_one_page_list_video(1)
    # print(resolve_video_path('https://www.bilibili.com/video/BV1954y167cs'))
    download('http://upos-sz-mirrorks3.bilivideo.com/upgcxcode/09/37/247693709/247693709-1-208.mp4?e=ig8euxZM2rNcNbRBhWdVhwdlhWU1hwdVhoNvNC8BqJIzNbfq9rVEuxTEnE8L5F6VnEsSTx0vkX8fqJeYTj_lta53NCM=&uipk=5&nbs=1&deadline=1603288531&gen=playurl&os=ks3bv&oi=2015088686&trid=15206a4d849e47978622bbb0dc35120aT&platform=html5&upsig=c747a5cf93f25fe1034e80c89c50a49a&uparams=e,uipk,nbs,deadline,gen,os,oi,trid,platform&mid=0&orderid=0,1&logo=80000000', 'download/1.mp4')


if __name__ == '__main__':
    main()
