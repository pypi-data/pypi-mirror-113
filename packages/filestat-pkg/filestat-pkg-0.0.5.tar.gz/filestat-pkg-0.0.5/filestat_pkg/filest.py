#!/usr/bin/python3
import os
import re
import sys
from prettytable import PrettyTable
from os.path import join, getsize

total_files = {}  # 总文件
size = 0  # 总大小


def file_get(file_dir):
    """
    :param file_dir:
    :return: 文件后缀,文件大小
    """
    global size
    for root, dirs, files in os.walk(file_dir):
        size += sum([getsize(join(root, name)) for name in files])
        for file in files:
            total_files[file] = getsize(join(root, file))


def file_analysis():
    """
    :return: 目录下文件详细信息
    """
    suffix_type = ['py', 'txt', 'zip', 'mp3', 'mp4', 'docx', 'pdf', 'rar',
                   '7z', 'java', 'dex', 'xml', 'yaml', 'yml', 'go', 'png', 'jpg',
                   'bat', 'html', 'js', 'css', 'tar', 'gz']
    format_list = []  # 所有文件后缀
    format_sizes = []  # 所有文件大小
    for i in total_files:
        for j in suffix_type:
            if re.search(f'{j}$', i) is not None:
                format_list.append(j)
                format_sizes.append({'format': j, 'size': total_files.get(i)})

    size_dic = {}
    for d in format_sizes:
        if d['format'] not in size_dic:
            size_dic[d['format']] = d['size']
        else:
            size_dic[d['format']] += d['size']
    format_size = {}  # 分类后格式大小关系
    for n, v in size_dic.items():
        format_size[n] = v

    dict_num = {}  # 分类后缀总数量
    for key in format_list:
        dict_num[key] = dict_num.get(key, 0) + 1
    table = PrettyTable(['编号', '文件类型', '文件数量', '数量占比', '文件大小', '大小占比'])  # 生成表格
    s_num = 0  # 统计编号
    bigness = 0  # 统计分类的格式占用数量
    class_szie = 0  # 统计分类的格式占用大小
    for i in dict_num:
        num_than = round(format_size.get(i) / size * 100, 2)  # 大小占比
        if num_than == 0:
            num_than = '微不足道'
        else:
            num_than = f'{num_than}%'
        s_num += 1
        bigness += dict_num.get(i)
        class_szie += format_size.get(i)
        table.add_row([s_num, i, dict_num.get(i), f'{round(float(dict_num.get(i) / len(total_files)) * 100, 2)}%',
                       format_size.get(i), num_than])
    other_bigness = len(total_files) - bigness  # 统计其他数量
    other_size = size - class_szie  # 统计其他大小
    table.add_row(
        [s_num + 1, '其他', other_bigness, f'{round(other_bigness / len(total_files) * 100, 2)}%', other_size,
         f'{round(other_size / size * 100, 2)}%'])

    return table


def main():
    try:
        dir = sys.argv[1]
        file_get(dir)
        print(file_analysis())
    except Exception:
        print(f"\033[0;31m请输入正确的路径!\033[0m")
