from bs4 import BeautifulSoup
import re
from urllib.request import Request, urlopen
from pandas import DataFrame, Series
import pandas as pd
import os


def read_csv(input_user):
    links = [];
    sublimits = [];
    poems_count = [];
    input_data = pd.read_csv("/home/castiel/PycharmProjects/Poems/data/input/{}.txt".format(input_user))
    poet = input_data.iloc[0].iloc[1]
    print('Poet {}'.format(poet.strip()))
    os.mkdir('/home/castiel/PycharmProjects/Poems/data/{}/'.format(poet.strip()))
    for s in input_data['poem_link']:
        links.append(s)
    for s in input_data['subsection']:
        sublimits.append(s[:-1])
    for s in input_data['poems']:
        poems_count.append(s)

    for a in range(len(links)):
        os.mkdir('/home/castiel/PycharmProjects/Poems/data/{}/{}'.format(poet.strip(),sublimits[a]))
        if(poems_count[a]>0):
            for s in range(1, poems_count[a]+1, 1):
                s1 = 'sh{}'.format(s)
                scrape_poems('{}/{}/'.format(links[a],str(s1)))
                clear_poems(poet.strip(),sublimits[a],s1)
        else:
            scrape_poems('{}/{}/'.format(links[a], str(sublimits[a])))
            clear_poems(poet.strip(), sublimits[a], sublimits[a])


def scrape_poems(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    plain = urlopen(req).read()
    soup = BeautifulSoup(plain, "html.parser")
    global mydivs
    mydivs=[]
    mydivs = soup.find_all("div",{"class":"m1"})
    global mydivs2
    mydivs2 = []
    mydivs2 = soup.find_all("div",{"class":"m2"})


def clear_poems(data1, data2, data3):
    first_stance = []
    second_stance = []
    for s in mydivs:
        p = re.compile(r'<.*?>')
        first_stance.append(p.sub(" ",str(s)))
    for s in mydivs2:
        p = re.compile(r'<.*?>')
        second_stance.append(p.sub(" ",str(s)))
    length = len(first_stance) if len(first_stance)>len(second_stance) else len(second_stance)
    first_stance_length = len(first_stance)
    second_stance_length = len(second_stance)
    c = 0;
    f = open("/home/castiel/PycharmProjects/Poems/data/{}/{}/{}.txt".format(data1,data2,data3), "a")
    for i in range(length*2):
        if i%2 == 0:
            f.write(first_stance[c])
            f.write("\n")
        else:
            if(second_stance_length>c):
                f.write(second_stance[c])
            f.write("\n")
            c=c+1;
    f.close()


def final_call():
    input_data = pd.read_csv("/home/castiel/PycharmProjects/Poems/data/names.txt")
    for s in input_data['Names']:
        read_csv(s)



final_call()


