from builtins import print

from bs4 import BeautifulSoup
import re
from urllib.request import Request, urlopen



def scrape_poets_links(url):
    global poet_link
    poet_link = []
    global poet_name
    poet_name = []
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    plain = urlopen(req).read()
    soup = BeautifulSoup(plain, "html.parser")
    mydivs = soup.find_all("div",{"class":"poet"})
    for s in mydivs:
        if(s.find('a')['href'] not in poet_link):
            poet_link.append(s.find('a')['href'])
    for s1 in poet_link:
        match = re.search(r'https://ganjoor.net/(\w+)', s1)
        if match:
            poet_name.append(match.group(1))

    return poet_name



def scrape_subsection_links(url,poet_name_value):
    s1= []
    final_sub_links = []
    final_sub_section_name = []
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    plain = urlopen(req).read()
    soup = BeautifulSoup(plain, "html.parser")
    mydivs = soup.find_all("p")
    r = re.compile('(?<=href=").*?(?=")')
    create_link = 'https://ganjoor.net/{}/'.format(poet_name_value)
    for s in mydivs:
        temp = r.findall(str(s.find('a')))
        if(temp != []):
            s1.append(temp)
    for sublinks in range(len(s1)):
        if(s1[sublinks][0] not in final_sub_links):
            z = re.match(create_link+'(.*)',str(s1[sublinks][0]))
            if(z):
                final_sub_links.append(s1[sublinks][0])
    for value in final_sub_links:
        match = re.search(r''+create_link+'(.*)', value)
        if match:
            final_sub_section_name.append(match.group(1))
    return final_sub_links, final_sub_section_name


def scrape_poem_count(url):
    req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    plain = urlopen(req).read()
    soup = BeautifulSoup(plain, "html.parser")
    mydivs = soup.find_all("a")
    count = 0
    for s in mydivs:
        match = re.search(r'.*sh\d+', str(s))
        if(match):
            count = count+1
    return count


def final_call():
    scrape_poets_links('https://ganjoor.net/');  # Perfect
    for s in range(len(poet_link)):
        f = open("/home/castiel/PycharmProjects/Poems/data/input/{}.txt".format(poet_name[s]), "a")
        f.write('poem_link,arabic_poet,subsection,poems')
        f.write("\n")
        final_sub_links, final_sub_section_name = scrape_subsection_links(poet_link[s], poet_name[s])
        print("{} {} {}".format(poet_name[s], poet_link[s], len(final_sub_section_name)))
        print()
        for sub in range(len(final_sub_links)):
            count = scrape_poem_count(final_sub_links[sub])
            f.write("{},{},{},{}".format(final_sub_links[sub], poet_name[s], final_sub_section_name[sub], count))
            f.write("\n")
        f.close()

def create_name_list():
    poet_name = scrape_poets_links('https://ganjoor.net/')
    f = open("/home/castiel/PycharmProjects/Poems/data/input/names.txt", "a")
    for s in poet_name:
        f.write('Name')
        f.write(s)
        f.write("\n")




final_call()
create_name_list()




