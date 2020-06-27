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
    global formater
    os_platform = platform.system()
    if os_platform == 'Windows':
        formater = '\\'
    if os_platform in ['Linux','Darwin']:
        formater = '/'
    return formater

def fetch_videos(course_url, cookies):
    response = requests.get(course_url, cookies=cookies)
    soup = BeautifulSoup(response.text, 'lxml')
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
                video_title = str(content['course']['stepMap'][item]['data']['title']).strip()

                for sources in content['course']['stepMap'][item]['data']['player']['sources']:
                    if sources['quality'] == resolution and sources['type'] == 'video\u002Fmp4':
                        video_url = sources['src']
                        destination_path = output_dir +folder_sep + course_title + folder_sep + module + folder_sep +  prefix+video_title + folder_sep
                        video_file_name = destination_path + video_title + ".mp4"
                        subs_file_name = destination_path + video_title + ".vtt"
                        os.makedirs(destination_path, exist_ok=True)
                        request_file(video_url, video_file_name)
                        if (len(content['course']['stepMap'][item]['data']['player']['subtitles']) == 1):
                            subs_url = content['course']['stepMap'][item]['data']['player']['subtitles'][0]['url']
                            request_file(subs_url, subs_file_name)
    except KeyError as error:
        print(error)



def request_file(url, dest_filaneme):
    resp = requests.get(url, stream=True)
    content_size = int(resp.headers.get('content-length'))
    status_file = os.path.exists(dest_filaneme)
    try:
        status_file_size = os.stat(dest_filaneme).st_size
    except FileNotFoundError:
        status_file_size = 0

    if status_file and content_size == status_file_size:
        print('↪ File {file:<60} already exist, skipping this..'.format(file='"'+dest_filaneme+'"'))
    elif status_file and content_size != status_file_size:
        print('❌ File {file:<60} already exist but is corrupted, trying to download it again '.format(file='"' + dest_filaneme + '"'))
        download_file(resp, content_size, dest_filaneme)
    else:
        download_file(resp, content_size, dest_filaneme)



def download_file(response, content_size, destination_file_name):
    splitter = get_os_platform()
    total_downloaded = 0
    title = destination_file_name.rsplit(splitter, 1)[1]
    screen_file_name = (str(title[:27]).strip() + '....' + str(title[-27:]).strip()) if len(title) > 58 else title
    description = '⏬ Downloading {file:<60}:'.format(file='"' + screen_file_name + '"')

    while True:
        with tqdm.tqdm(total=content_size, dynamic_ncols=True, unit_scale=True, desc=description,
                       bar_format="{desc} %s{percentage:3.0f}%s %s|%s{bar:50}{r_bar}"
                                  % (Fore.LIGHTYELLOW_EX, '%', Fore.LIGHTYELLOW_EX, Fore.LIGHTYELLOW_EX)) as progress:

            with open(destination_file_name, 'wb') as f:
                try:
                    for chunk in response.iter_content(chunk_size=4096):
                        chunk_size = len(chunk)
                        total_downloaded += chunk_size
                        progress.update(chunk_size)
                        f.write(chunk)
                except requests.exceptions.StreamConsumedError:
                    print("❌ Error while downloading file, trying to download it again..")

            if (total_downloaded == content_size):
                progress.set_description('✅ File ready {file:<60}'.format(file='"' + screen_file_name + '"'))
                progress.bar_format = "{desc} %s{percentage:3.0f}%s %s|%s{bar:50}{r_bar}" \
                                      % (Fore.LIGHTGREEN_EX, '%', Fore.LIGHTGREEN_EX, Fore.LIGHTGREEN_EX)
                progress.close()
                break

def parse_cookie_file(course_url, video_res, output_dir, cookiefile):
    'find "config" request on XHR'
    f_in = open(cookiefile)
    requests_header = '\n'.join([line for line in (l.strip() for l in f_in) if line])
    f_in.close()
    auth = re.findall(r'authorization:\sBearer\s(.*)', requests_header)
    cookies = re.findall(r'cookie:\s(.*)', requests_header)
    if auth != None and cookies != None:
        auth_cookies = {'authorization': auth[0], 'cookie': cookies[0]}
        get_course_contents(course_url, auth_cookies, output_dir, video_res)
        print('Done!')
    else:
        print("Bad cookie file, check again")
        exit(1)


def main():
    args = docopt(__doc__)

    video_res = args['--res']
    if video_res not in ['360', '720', '1080']:
        exit('Invalid value for --res. Supported values are 360, 720 or 1080')
    output_dir = args['--out']
    cookiefile = args['--cookie']
    course_url = args['<url>']

    parse_cookie_file(course_url, video_res, output_dir, cookiefile)
if __name__ == '__main__':
    main()