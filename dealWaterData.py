# -*- coding:utf-8 -*-
from __future__ import unicode_literals

__author__ = 'yang_da'
__date__ = '2018/5/6 下午1:36'

import pandas as pd
import time
import sys

RANK = ['Ⅰ', 'ⅠⅠ', 'ⅠⅠⅠ', 'ⅠⅤ', 'Ⅴ', '劣Ⅴ1', '劣Ⅴ2', '劣Ⅴ3', '劣Ⅴ4']


def dealLevel(level):
    if isinstance(level, str) is False:
        level = 'Ⅴ'
    level = level.replace('V', 'Ⅴ')
    level = level.replace('I', 'Ⅰ')
    level = level.replace('Ⅳ', 'ⅠⅤ')
    return level


def searchLevelTable(name, levelTable):
    is_have = False
    index = 0
    list_all = levelTable['基本项目']
    for i in range(len(list_all)):
        row_name = list_all[i] if isinstance(list_all[i], str) else ''
        if row_name.count(name) > 0 or name.count(row_name) > 0:
            is_have = True
            index = i
            return is_have, index
    return is_have, index


def getAim(name, needLevel, levelTable):
    needLevel = dealLevel(needLevel)
    is_have, row = searchLevelTable(name, levelTable)
    row_data = levelTable.loc[row]
    if is_have is True and needLevel in RANK:
        return row_data[RANK.index(needLevel)+1]
    print('判断目标浓度出错')
    return -10


def judgeIs(judge, standard):
    if isinstance(judge, str) == False or isinstance(standard, str) == False:
        print('输入类型有问题')
        return False, False
    judge = judge.replace('V','Ⅴ')
    judge = judge.replace('I', 'Ⅰ')
    judge = judge.replace('Ⅳ', 'ⅠⅤ')
    standard = standard.replace('V', 'Ⅴ')
    standard = standard.replace('I', 'Ⅰ')
    standard = standard.replace('Ⅳ', 'ⅠⅤ')
    if judge not in RANK or standard not in RANK:
        print('判断是否合格出错')
        return False, False
    else:
        return RANK.index(judge) <= RANK.index(standard), True


def parseLevel():
    total_data = pd.read_csv('劣五类标准.csv')
    return total_data


def parse():
    total_data = pd.read_csv('water.csv', header=0)
    list = []
    for data in total_data.itertuples(index=True, name='Pandas'):
        if data[3] != '0' and (data[1] != '均值' and isinstance(data[1], str)):
            list.append(data)
    return list


if __name__ == '__main__':
    df1 = pd.DataFrame(columns=['序号', '河道名称', '权属', '断面名称', '考核街乡', '水质目标', '断面现状水质类别', '河道现状水质类别', '是否合格', '生成是否成功'])
    data_all = parse()
    df1_index = 0
    for row_data in data_all:
        is_check_out, is_over = judgeIs(row_data[9], row_data[7])
        df1.loc[df1_index] = [
            row_data[1],
            row_data[3],
            row_data[4],
            row_data[5],
            row_data[6],
            row_data[7],
            row_data[9],
            '参考均值',
            '是' if is_check_out else '否',
            '成功' if is_over else '失败',
        ]
        df1_index = df1_index+1
        print('正在生成df1:%d', df1_index)

    df2 = pd.DataFrame(columns=['河流名称', '断面名称', '超标指标', '现状浓度（mg/L)', '目标浓度（mg/L)', '生成是否成功'])
    df2_index = 0
    check_num_indexs = {
        8: 'pH值',
        10: '溶解氧（mg/L)',
        12: '高锰酸盐指数（mg/L)',
        14: '化学需氧量（mg/L)',
        16: '五日生化需氧量（mg/L)',
        18: '氨氮（mg/L)',
        20: '总磷（mg/L)',
        22: '铜（mg/L)',
        24: '锌（mg/L)',
        26: '氟化物（mg/L)',
        28: '硒（mg/L)',
        30: '砷（mg/L)',
        32: '汞（mg/L)',
        34: '镉（mg/L)',
        36: '六价铬（mg/L)',
        38: '氰化物（mg/L)',
        40: '挥发酚（mg/L)',
        42: '石油类（mg/L)',
        44: '阴离子表面活性剂（mg/L)',
        46: '硫化物（mg/L)',
    }
    for data in data_all:
        for index in range(len(data)):
            if index not in check_num_indexs.keys():
                continue
            is_check_out, is_over = judgeIs(data[9], data[7])
            check_out_num = getAim(name=check_num_indexs[index], needLevel=data[7], levelTable=parseLevel())
            if is_check_out is False and check_out_num != -10:
                df2.loc[df2_index] = [
                    data[1],
                    data[5],
                    check_num_indexs[index],
                    data[index],
                    check_out_num,
                    '成功' if is_over else '失败',
                ]
                df2_index = df2_index + 1
                print('正在生成df2:%d', df2_index)

    df1.to_csv('water1.csv', index=True)
    print('输出water1成功')
    df2.to_csv('water2.csv', index=True)
    print('输出water2成功')
