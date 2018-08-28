#!/usr/bin/env python3
# coding=utf-8
# a old dirver RSS list https://pastebin.com/raw/zmKcfPqg
# from https://www.92ez.com/?action=show&id=23460

import requests
import sys
import os
import re


def get_source(nickname, page_index, source_type):
    aim_url = "https://%s.tumblr.com/page/%d" % (nickname, page_index)
    print('[o] Get source from blog %s ...' % aim_url)
    try:
        response_string = requests.get(url=aim_url, timeout=50).content.decode('utf8')
        if "posts-no-posts content" not in response_string:
            if source_type == "images":
                source_elements = re.findall(r'<img(.+?)>', response_string)
            else:
                source_elements = re.findall(r'<iframe(.+?)>', response_string)

            if len(source_elements) > 0:
                dir_path = sys.path[0] + '/' + aim_url.split('//')[1].split('.')[0] + '/'
                if not os.path.exists(dir_path):
                    os.makedirs(dir_path)

                for this_source in source_elements:
                    if source_type == "images":
                        image_url = re.findall(r'src="(.+?)"', this_source)[0]
                        image_name = image_url.split('/')[-1]
                        if "tumblr_" in image_name:
                            write_file(image_url, dir_path, image_name)
                    else:
                        if "/video/" in this_source:
                            video_url = re.findall(r"src='(.+?)'", this_source)[0]
                            video_response = requests.get(url=video_url, timeout=50).content.decode('utf8')
                            video_source = re.findall(r'<source src="(.+?)"', video_response)[0]
                            video_name = video_source.split('tumblr_')[1].split('/')[0] + '.mp4'
                            write_file(video_source, dir_path, video_name)

            else:
                print('[x] Can not get any source.')
            page_index += 1
            get_source(nickname, page_index, source_type)
        else:
            print('[!] Get source complete!')
    except Exception as e:
        print(e)
        get_source(nickname, page_index, source_type)


def write_file(source_url, dir_path, file_name):
    if not os.path.exists(dir_path + file_name):
        print('[*] Source %s is downloading...' % file_name)
        file_download = requests.get(url=source_url, timeout=50)
        if file_download.status_code == 200:
            open(dir_path + file_name, 'wb').write(file_download.content)
    else:
        print('[*] Source %s has been downloaded.' % file_name)


if __name__ == '__main__':
    source_type = sys.argv[1]
    user_nickname = sys.argv[2]
    get_source(user_nickname, 1, source_type)