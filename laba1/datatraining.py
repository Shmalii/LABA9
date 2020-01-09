


import requests
from bs4 import BeautifulSoup

import numpy as np
import pandas as pd

import re

provinces = {1: "Вінницька", 13: "Миколаївська", 2: "Волинська", 14: "Одеська", 3: "Дніпропетровська", 15: "Полтавська",
             4: "Донецька", 16: "Рівенська", 5: "Житомирська", 17: 'Сумська', 6: "Закарпатська", 18: "Тернопільська",
             7: "Запорізька", 19: "Харківська",
             8: "Івано-Франківська", 20: "Херсонська", 9: "Київська", 21: "Хмельницька", 10: "Кіровоградська",
             22: "Черкаська", 11: "Луганська", 23: "Чернівецька",
             12: "Львівська", 24: "Чернігівська", 25: "Республіка Крим"}







def get_url(url):
    response = requests.get(url)
    content = response.content.decode("utf8")
    return content


def get_provinces_data(oblast, when):
    parse_from,parse_to = when
    url = "https://www.star.nesdis.noaa.gov/smcd/emb/vci/VH/get_provinceData.php?country=UKR&provinceID={}&year1={}&year2={}&type=Mean".format(
            oblast, parse_from, parse_to)

    resp = get_url(url)

    filename = oblast + "_" + 'Mean' + "_" + parse_from + "-" + parse_to + '.txt'
    open(filename, 'wb').write(str.encode(resp))
    print(filename, " created.")
    return filename


def choose_province():
    for every in dict.keys(provinces):
        print(every, " <=> ", provinces[every])
    while True:
        oblast = input("Яку область оберете?: ")
        if int(oblast)<=25 and int(oblast)>=1:
            break
    while True:
        from_to = input('Виберіть роки пошуку?: ').split()
        a,c= from_to
        if a<=c and int(a)>=1981 and int(c) <=2020:
            break
    print("Зачекайте, триває завантаження")
    return get_provinces_data(oblast, from_to)

def get_file_to_normal_stage(file):
    data = open(file, 'r').read()
    data = data[data.find('<pre>') + 5:data.find("</pre></tt>")]
    write_to = open(file, 'w').write(data)


def mean_file(file):
    raw = open(file, 'r+')
    headers = raw.readline().rstrip()
    headers = headers.split(',')[:2] + headers.split(',')[4:]
    data = raw.readlines()

    result = []

    # deleting stuff to get it in df
    for every in data:
        result.append(str(re.sub(r',\s\s|\s\s|\s|,\s', ',', every)[:-1]).split(','))

    df = pd.DataFrame(result, columns=headers)
    return df




filename = choose_province()
get_file_to_normal_stage(filename)

df = mean_file(filename)

print(df.head(40))
print("Minimum VHI: ",df.VHI.min())
print("Maximum VHI: ",df.VHI.max())



res = 0
res1= 0
res2 = 0
res3 =0 
res4 =0 
for every in df.VHI:
    if float(every) < 35 and float(every) >=15:
        res += 1
    elif float(every) < 40 and float(every) >= 35:
	    res1+=1
    elif float(every) >= 60:
	    res3+=1
    elif float(every) < 15:
	    res2+=1
    elif float(every) < 60 and float(every) >=40:
	    res4+=1
	  
print("Результати аналізу даних")
print ("Всього тижнів: ", res1+res2+res3+res4+res)
print("Cтресові умови: ", res1)
print("Сприятливі умови: ", res3)
print("Посуха, інтенсивність якої від середньої до надзвичайної: ", res2)
print("посуха, інтенсивність якої від помірної до надзвичайної: ", res)
print("Майже сприятливі умови: ", res4)
