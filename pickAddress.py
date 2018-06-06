# -*- coding:utf-8 -*-
from __future__ import unicode_literals

__author__ = 'yang_da'
__date__ = '2018/6/6 下午3:34'

import requests
import pandas as pd
import re


def parse():
    total_data = pd.read_csv('地址.csv', header=0)
    return total_data

def pickAddress():
    all_data = parse()
    df = pd.DataFrame(columns=['序号', '出现频率最高的地址', '最高重复次数', '各数据出现次数'])
    index_num = -1
    for row_data in all_data.itertuples(index=False, name='Pandas'):
        # 计算每一行
        print('计算第%d行', index_num)
        index_num += 1
        current_dict = {}
        for index in range(len(row_data)):
            # 算出现次数
            now_str = row_data[index]
            if not isinstance(now_str, str):
                print('有问题的地址:', now_str)
                continue
            now_str = row_data[index].strip()
            if len(now_str) == 0 or now_str == 'TRUE' or now_str == 'FALSE' or now_str.isspace():
                print('有问题的字符串地址:', now_str)
                continue
            if now_str not in current_dict.keys():
                current_dict[now_str] = 1
            else:
                current_dict[now_str] += 1

        big_key_str = ''
        big_key_num = 0
        for key in current_dict.keys():
            # 取最大的key
            if current_dict[key] > big_key_num:
                big_key_str = key
                big_key_num = current_dict[key]
        df.loc[index_num] = [index_num+1, big_key_str, big_key_num, current_dict]
        print('第几个, 地址, 次数,次数详情,',index_num, big_key_str, big_key_num, current_dict)
    df.to_csv('查重地址.csv', index=True)
    print('输出csv成功')


if __name__ == '__main__':
    pickAddress()
