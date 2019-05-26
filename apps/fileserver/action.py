# -*- coding:utf8  -*-
import os, time

ALLOWED_EXTENSIONS = set(['txt', 'png', 'jpg', 'xls', 'JPG', 'PNG', 'xlsx', 'gif', 'GIF', 'exe', 'iso'])


def allowed_file(filename):
    return os.path.splitext(filename)[1].replace('.', '') in ALLOWED_EXTENSIONS


def getAllFile(dir):
    file_list = []
    for filename in os.listdir(dir):
        # print(filename)
        filepath = os.path.join(dir, filename)
        file_stat = os.stat(filepath)
        file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(file_stat.st_mtime))
        if os.path.isdir(filepath):
            file_size = '-'
            file_list.append({
                'name': filename + '/',
                'modify_time': file_modify_time,
                'size': file_size,
                'type': 'folder'
            })
        else:
            file_size = getFileSize(filepath)
            file_list.append({
                'name': filename,
                'modify_time': file_modify_time,
                'size': file_size,
                'type': 'file'
            })

    return file_list


def getFileSize(filepath):
    size = os.path.getsize(filepath)
    if size > 1024:
        if size > 1024*1024:
            if size > 1024*1024*1024:
                return '%.2fG' % (size/1024/1024/1024)
            else:
                return '%.0fM' % (size/1024/1024)
        else:
            return '%.0fK' % (size/1024)
    else:
        return '%.0f' % size


if __name__ == '__main__':
    file_list, dir_list = getAllFile(r'D:\myProject')
    print(file_list)
    print(dir_list)
