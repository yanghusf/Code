# -*- coding:utf-8 -*-

import pandas as pd

data = []
char_replace_dict = {':': '  ', '（': '(', '）': ')', '，': ','}

with open('xmq_survey.txt', 'r', encoding='utf-8') as file:
    for line in file.readlines():
        for key, value in char_replace_dict.items():
            line = line.replace(key, value)  # 原来这个是深度引用
            # 这条代码比自己写的简介的多，也更python
        data.append(line)

with open('survey.txt', 'w', encoding='utf-8') as file:
    for line in data:
        file.write(line)

raw_data = pd.read_table('survey.txt', delimiter='    ', header=None)  # 查看read_table函数的用法
raw_data.columns = ['Name', 'Raw Info']
raw_data.count()
print('successful')
