# -*- coding:utf-8 -*-
from __future__ import unicode_literals

__author__ = 'yang_da'
__date__ = '2018/6/6 下午3:34'

import requests
import pandas as pd


def parse():
    total_data = pd.read_csv('地址.csv', header=0)
    return total_data

def pickAddress():
    all_data = parse()
    df = pd.DataFrame(columns=['序号', '出现频率最高的地址', '重复次数'])
    index_num = -1
    for row_data in all_data.itertuples(index=False, name='Pandas'):
        # 计算每一行
        print('计算第%d行', index_num)
        index_num += 1
        current_dict = {}
        for index in range(len(row_data)):
            # 算出现次数
            now_str = row_data[index]
            if isinstance(now_str, (float, int, bool)) or len(now_str) == 0:
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
        df.loc[index_num] = [index_num, big_key_str, big_key_num]
        print('第%d个, 地址:%d, 次数:%d',index_num, big_key_str, big_key_num)
    df.to_csv('查重地址.csv', index=True)
    print('输出csv成功')


if __name__ == '__main__':
    pickAddress()
