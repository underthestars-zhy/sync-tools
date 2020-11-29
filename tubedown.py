#!/usr/bin/env python
#  Copyright (c) 2020.
#  You can freely change the code part, but you must follow the MIT protocol
#  You cannot delete any information about UTS
#  You cannot use this program to disrupt social order.

import argparse
import json
import shelve
import os
import sys
from pytube import YouTube

# 多语言设置
file_lists = os.listdir(os.path.expanduser('~'))
if 'mop.json' in file_lists:
    file = open(os.path.expanduser('~/mop.json'), 'r')
    mop_db_path = json.load(file)
    file.close()
    mop_db = shelve.open(mop_db_path + 'mop')
    if mop_db['language'] == 'en':
        down_help = 'Download the file'
        dir_help = 'Set the default download folder'
        down_text = 'Downloading now -->'
        down_text = 'Downloading now -->'
        successful = 'Success'
        down_yet = 'Repeat Download (skip)=>'
    else:
        down_help = '下载文件'
        dir_help = '设置默认下载文件夹'
        down_text = '开始下载 -->'
        successful = '成功'
        down_yet = '重复下载(跳过)=>'
    mop_db.close()
else:
    print('Error|出错')
    sys.exit()

# 命令参数设置
parser = argparse.ArgumentParser(description='YouTubeDown-MacOS-11')

parser.add_argument('-d', type=str, help=down_help, nargs='+')
parser.add_argument('-dir', type=str, help=dir_help, nargs='?')

args = parser.parse_args()



if args.d:
    mop_db = shelve.open(mop_db_path + 'mop')
    down_list = list(mop_db['tubedown_down'])
    for url in list(args.d):
        if url in down_list:
            print(down_yet+url)
            continue
        print(down_text+' '+url)
        down_list.append(url)
        if len(args.d) == 2:
            YouTube(url).streams.first().download(args.d[1])
        else:
            path = mop_db['tubedown_save_path']
            YouTube(url).streams.first().download(os.path.expanduser(path))
    mop_db['tubedown_down'] = down_list
    print(successful)
    mop_db.close()

flag = False
if sys.argv[1] == '-dir':
    flag = True

if flag:
    mop_db = shelve.open(mop_db_path + 'mop')
    url = input('URL: ')
    mop_db['tubedown_save_path'] = url
    mop_db.close()
    print(successful)
