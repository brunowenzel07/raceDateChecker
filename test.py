#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json

# try:
#     file = open('items.json')
# except IOError as e:
#     print(u'не удалось открыть файл')
# else:
#     with file:
#         print(u'нашли файл')

# with open("items.json", 'a') as infile:
#     # data = json.load(open('items.json', 'w'))
#     # data.append([{123: 456}])
#     data = [{123: 456}]
#     json.dump(data, infile)
#     print(data)

# with open("items.json", mode='w', encoding='utf-8') as f:
#     json.dump([], f)
#
# with open("items.json", mode='w', encoding='utf-8') as feedsjson:
#     entry = {'name': 123, 'url': 222}
#     feeds = json.load(feedsjson)
#     feeds.append(entry)
#     json.dump(feeds, feedsjson)

import os
t = os.path.isfile('items.json')

if t:
    print('file is exist')

else:
    print('file not exist')
    with open("items.json", 'a') as file:
        data = []
        json.dump(data, file)
        print('file not exist')




# import json
#
# a_dict = {'ddd': 'new_value'}
#
# with open('items.json') as f:
#     data = json.load(f)
#
# data.update(a_dict)
#
# print(data)
#
# with open('items.json', 'w') as f:
#     json.dump(data, f)

# data = json.load(open('items.json', 'r'))
# data.append([{123: 456}])
# json.dump(open('items.json', 'w'), data)