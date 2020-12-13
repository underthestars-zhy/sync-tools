#!/usr/bin/env python3
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
import datetime

today = datetime.datetime

# 多语言设置
file_lists = os.listdir(os.path.expanduser('~'))
if 'mop.json' in file_lists:
    file = open(os.path.expanduser('~/mop.json'), 'r')
    mop_db_path = json.load(file)
    file.close()
    mop_db = shelve.open(mop_db_path + 'mop')
    LANGUAGE = mop_db['language']
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
        dir_text = 'n: 新建, d: 删除, e: 修改'
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

parser.add_argument('-s', type=str, help=sync_help, nargs='*')
parser.add_argument('-dir', type=str, help=dir_help, nargs='*')
parser.add_argument('-t', type=str, help=dir_help, nargs='*')

args = parser.parse_args()

if args.t:
    if LANGUAGE == 'cn':
        print('正在打包')
    else:
        print('Packing up')


if args.s:
    print(sync_text)
    mop_db = shelve.open(mop_db_path + 'mop')
    # TODO: 多线程

    if args.s[0] == 'all':
        for [from_dir_list, to_dir] in dict(mop_db['sync_dir_set']).values():
            to_dir_path = to_dir + str(today.now())
            for from_dir_path in from_dir_list:
                from_dir_base = os.path.basename(from_dir_path)
                shutil.copytree(from_dir_path, to_dir_path + '/' + from_dir_base)
    else:
        for sync_name in list(args.s):
            for name, [from_dir_list, to_dir] in dict(mop_db['sync_dir_set']).items():
                if name != sync_name:
                    continue

                to_dir_path = to_dir + str(today.now())

                for from_dir_path in from_dir_list:
                    from_dir_base = os.path.basename(from_dir_path)
                    shutil.copytree(from_dir_path, to_dir_path + '/' + from_dir_base)

    mop_db.close()
    print(successful)

if args.dir:
    mop_db = shelve.open(mop_db_path + 'mop')

    sync_set_dict = dict(mop_db['sync_dir_set'])
    for sync_name, sync_list in sync_set_dict.items():
        print(sync_name + ') ' + str(sync_list[0]) + ' => ' + sync_list[1])

    if args.dir[0] == 'n':
        sync_name = input('Name: ')
        if sync_name.lower() == 'all':
            sys.exit()
        from_dir = input('FromDir: ')
        to_dir = input('ToDir: ')
        from_dir_list = from_dir.split('&&')

        t_dict = mop_db['sync_dir_set']
        t_dict[sync_name] = [from_dir_list, to_dir]
        mop_db['sync_dir_set'] = t_dict
    elif args.dir[0] == 'l':
        pass
    elif args.dir[0] == 'd':
        del_sync_name = input('DelName: ')

        t_dict = mop_db['sync_dir_set']
        del t_dict[del_sync_name]
        mop_db['sync_dir_set'] = t_dict
    elif args.dir[0] == 'e':
        edit_sync_name = input('EditName: ')

        if LANGUAGE == 'cn':
            print('$代表原本即不做改动')
        else:
            print('$means that nothing has been changed')

        t_dict = mop_db['sync_dir_set']
        edit_list = t_dict[edit_sync_name]
        t_list = []

        edit_from_dir = input('EditFromDir: ')
        if edit_from_dir == '$':
            t_list.append(edit_list[0])
        else:
            t_list.append(edit_from_dir.split('&&'))

        edit_to_dir = input('EditToDir: ')
        if edit_to_dir == '$':
            t_list.append(edit_list[1])
        else:
            t_list.append(edit_to_dir)

        t_dict[edit_sync_name] = t_list

        mop_db['sync_dir_set'] = t_dict

    mop_db.close()
