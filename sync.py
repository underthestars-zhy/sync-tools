#  Copyright (c) 2020.
#  You can freely change the code part, but you must follow the MIT protocol
#  You cannot delete any information about UTS
#  You cannot use this program to disrupt social order.

import sys
import argparse
import json
import shelve
import os
import threading
import random
import shutil

def say():
    lock = threading.RLock
    while True:
        lock.acquire()
        ok = is_ok
        lock.release()
        if ok:
            return
        else:
            if language == 'cn':
                print("\b\b\b\b\b\b\b" + sync_sync, end='')
            else:
                print("\b\b\b\b\b\b\b\b\b\b\b\b\b\b" + sync_sync, end='')

def sync():
    i = 0
    for to_dir_name in to_dir:
        to_dir_name += str(random.randint(0, 9))+str(random.randint(0, 9))+str(random.randint(0, 9))
        try:
            os.makedirs(to_dir_name)
        except:
            pass
        for from_dir_name in from_dir:
            shutil.copy(os.path.expanduser(from_dir_name), os.path.expanduser(to_dir_name))
    lock = threading.RLock
    lock.acquire()
    is_ok = True
    lock.release()
    return



if __name__ == '__main__':
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
            dir_text = 'n: new, d: Delete'
            successful = 'Success'
            sync_text = 'Start syncing...'
            sync_sync = 'Syncing now...'
            language = 'en'
        else:
            sync_help = '同步文件'
            dir_help = '设置同步的文件夹'
            dir_text = 'n: 新建, d: 删除'
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

    parser.add_argument('-s', type=str, help=sync_help)
    parser.add_argument('-dir', type=str, help=dir_help)

    args = parser.parse_args()

    try:
        if args.s == None:
            sync = True
    except:
        sync = False

    try:
        if args.dir == None:
            dir = True
    except:
        dir = False

    if dir:
        print(dir_text)
        mop_db = shelve.open(mop_db_path + 'mop')
        from_to_dict = dict(mop_db['dir_set'])
        i = 1
        for id_, dir_list in from_to_dict.items():
            print('%d) %s ----> %s' % id_, dir_list[0], dir_list[1])
            i += 1
        command = input()
        if command == 'n':
            from_dir = input('From: ')
            to_dir = input('To: ')
            dir_dict = mop_db['dir_set']
            dir_dict[i] = [from_dir, to_dir]
            mop_db['dir_set'] = dir_dict
            print(successful)
        elif command == 'del':
            del_id = input('ID: ')
            dir_dict = mop_db['dir_set']
            del dir_dict[int(del_id)]
            mop_db['dir_set'] = dir_dict
            print(successful)
        mop_db.close()

    if sync:
        print(sync_text)
        mop_db = shelve.open(mop_db_path + 'mop')
        from_to_dict = dict(mop_db['dir_set'])
        from_dir = []
        to_dir = []
        for dir_list in from_to_dict.values():
            from_dir.append(str(dir_list[0]).split('&&'))
            to_dir.append(dir_list[1])
        global is_ok
        is_ok = False
        say_thread = threading.Thread(target=say)
        sync_thread = threading.Thread(target=sync)
        sync_thread.start()
        sync_thread.start()
        sync_thread.join()
        say_thread.join()
        print(successful)
