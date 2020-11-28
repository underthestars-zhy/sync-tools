#  Copyright (c) 2020.
#  You can freely change the code part, but you must follow the MIT protocol
#  You cannot delete any information about UTS
#  You cannot use this program to disrupt social order.

import sys
import argparse
import json
import shelve
import os
import random
import shutil



# 多语言设置
file_lists = os.listdir(os.path.expanduser('~'))
if 'mop.json' in file_lists:
    file = open(os.path.expanduser('~/mop.json'), 'r')
    mop_db_path = json.load(file)
    file.close()
    mop_db = shelve.open(mop_db_path + 'mop')
    if mop_db['language'] == 'en':
        sync_help = 'SYNC file'
        dir_help = 'Set the folder to sync'
        dir_text = 'n: new, del: Delete'
        successful = 'Success'
        sync_text = 'Start syncing...'
        sync_sync = 'Syncing now...'
        language = 'en'
    else:
        sync_help = '同步文件'
        dir_help = '设置同步的文件夹'
        dir_text = 'n: 新建, del: 删除'
        successful = '成功'
        sync_text = '开始同步...'
        sync_sync = '正在同步...'
        language = 'cn'
    mop_db.close()
else:
    print('Error|出错')
    sys.exit()

# 命令参数设置
parser = argparse.ArgumentParser(description='SyncTool-MacOS-11')

parser.add_argument('-s', type=str, help=sync_help, nargs='?')
parser.add_argument('-dir', type=str, help=dir_help, nargs='?')

args = parser.parse_args()
sync_ = False
dir = False

try:
    if sys.argv[1] == '-s':
        sync_ = True
except:
    pass


try:
    if sys.argv[1] == '-dir':
        dir = True
except:
    pass


if dir:
    print(dir_text)
    mop_db = shelve.open(mop_db_path + 'mop')
    from_to_dict = dict(mop_db['sync_dir_set'])
    i = 1
    for id_, dir_list in from_to_dict.items():
        print('%d) %s ----> %s' %(id_, dir_list[0], dir_list[1]))
        i += 1
    command = input()
    if command == 'n':
        from_dir = input('From: ')
        to_dir = input('To: ')
        dir_dict = dict(mop_db['sync_dir_set'])
        dir_dict[i] = [from_dir, to_dir]
        mop_db['sync_dir_set'] = dir_dict
        print(successful)
    elif command == 'del':
        del_id = input('ID: ')
        dir_dict = dict(mop_db['sync_dir_set'])
        del dir_dict[int(del_id)]
        mop_db['sync_dir_set'] = dir_dict
        print(successful)
    mop_db.close()

if sync_:
    print(sync_text)
    mop_db = shelve.open(mop_db_path + 'mop')
    from_to_dict = dict(mop_db['sync_dir_set'])
    from_dir = []
    to_dir = []
    i = 0
    for dir_list in from_to_dict.values():
        from_dir.append(str(dir_list[0]).split('&&'))
        to_dir.append(dir_list[1])
    print(sync_sync)
    for to_dir_name in to_dir:
        to_dir_name += str(random.randint(0, 999)) + str(random.randint(0, 999)) + str(random.randint(0, 999))
        for from_dir_name in from_dir[i]:
            to_dir_name_base = str(from_dir_name).split(os.path.sep)[-1]
            shutil.copytree(os.path.expanduser(from_dir_name), os.path.expanduser(to_dir_name + '/' + to_dir_name_base))
        i += 1
    print(successful)
    mop_db.close()
