#!/usr/bin/env python3
'''
Downloads the video lectures for the given CloudAcademy course.

Usage:
    cloud-academy-dl --help
    cloud-academy-dl <url> [--cookie=<txt_file>] [--out=<output_dir>] [--res=<resolution>]

Options:
    --help              Shows this screen.

    --res=<resolution>  The required video resolution. Allowed values are 360,
                        720, and 1080 [default: 1080].
    --out=<output_dir>  The directory where the videos are saved
                        [default: courses].
    --cookie=<txt_file> Text file with all Request header from CloudAcademy
    url                 On windows platform the url must be in double quotes
'''

import json
import os
import re
import requests
from bs4 import BeautifulSoup
from colorama import Fore
from docopt import docopt
import platform
import tqdm

def get_os_platform():
    os_platform = platform.system()
    if os_platform == 'Windows':
        formater = '\\'
    if os_platform in ['Linux','Darwin']:
        formater = '/'
    return formater

def fetch_videos(course_url, cookies):
    resp = requests.get(course_url, cookies=cookies)
    soup = BeautifulSoup(resp.text, 'lxml')
    script = soup.find('script', text=re.compile('window\.__INITIAL_STATE__ '))
    json_text = re.search(r'^\s*window\.__INITIAL_STATE__\s*=\s*({.*?})\s*;\s*$', script.string,
                          flags=re.DOTALL | re.MULTILINE).group(1)
    data = json.loads(json_text)
    return data

def get_course_contents(course_url, cookies, output_dir, video_res):
    folder_sep = get_os_platform()
    data = fetch_videos(course_url, cookies)
    try:
        course_title = data['course']['includedIn'][0]['title']
        module = data['course']['entity']['title']
        print("Course : " + course_title)
        print("Module : " + module)
        resolution = video_res+'p'
        url_spliter = str(course_url).rsplit('/', 2)

        for index, modules in enumerate(data['course']['entity']['steps']):
            url = url_spliter[0] + '/' + data['course']['entity']['steps'][index]['slug'] + '/' + url_spliter[2]
            content = fetch_videos(url, cookies)

            for item in content['course']['stepMap']:
                if index < 9:
                    prefix = '0'+str(index+1)+'_'
                else:
                    prefix = str(index+1)+'_'
                title_video =  re.findall(r'([a-zA-Z0-9 -]*)', content['course']['stepMap'][item]['data']['title'])[0]
                subs_url = content['course']['stepMap'][item]['data']['player']['subtitles'][0]['url']

                for sources in content['course']['stepMap'][item]['data']['player']['sources']:
                    if sources['quality'] == resolution and sources['type'] == 'video\u002Fmp4':
                        video_url = sources['src']
                        path = output_dir +folder_sep + course_title + folder_sep + module + folder_sep +  prefix+title_video + folder_sep
                        video_file = path + title_video + ".mp4"
                        subs_name_file = path + title_video + ".vtt"
                        os.makedirs(path, exist_ok=True)
                        download_file(video_url, video_file)
                        download_file(subs_url, subs_name_file)
    except KeyError as error:
        print(error)



def download_file(url, dest_filaneme):
    splitter = get_os_platform()
    resp = requests.get(url, stream=True)

    total_size = int(resp.headers.get('content-length'))

    text = 'Downloading {file:<60}'.format(file=dest_filaneme.rsplit(splitter,1)[1])
    with tqdm.tqdm(total=total_size, dynamic_ncols=True, unit_scale=True, desc=text, bar_format="{desc:<11} {percentage:3.0f}%s %s|%s{bar:50}{r_bar}" % ('%',Fore.LIGHTGREEN_EX, Fore.LIGHTGREEN_EX)) as progress:
        with open(dest_filaneme, 'wb') as f:
            for chunk in resp.iter_content(chunk_size=4096):
                progress.update(len(chunk))
                f.write(chunk)
        progress.close()

def download_course(course_url,video_res, output_dir, cookiefile):
    'find ?serializer=full on XHR'
    f_in = open(cookiefile)
    requests_header = '\n'.join([line for line in (l.strip() for l in f_in) if line])
    f_in.close()
    auth = re.findall(r'authorization:\sBearer\s(.*)', requests_header)
    cookies = re.findall(r'cookie:\s(.*)', requests_header)
    auth_cookies = {'authorization': auth[0], 'cookie': cookies[0]}
    get_course_contents(course_url, auth_cookies, output_dir, video_res)
    print('Done!')


def main():
    args = docopt(__doc__)

    video_res = args['--res']
    if video_res not in ['360', '720', '1080']:
        exit('Invalid value for --res. Supported values are 360, 720 or 1080')
    output_dir = args['--out']
    cookiefile = args['--cookie']
    course_url = args['<url>']

    download_course(course_url, video_res, output_dir, cookiefile)
if __name__ == '__main__':
    main()