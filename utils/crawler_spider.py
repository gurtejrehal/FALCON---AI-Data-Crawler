import requests
import re
from bs4 import BeautifulSoup



keywords = ["Crime",
            "Child Abuse",
            "Women Abuse",
            "Cyber Bullying"]




def crawling(query, keywords):

    general = list()
    crime = list()
    child_abuse = list()
    women_abuse = list()
    cyber_bullying = list()
    lists = [general, crime, child_abuse, women_abuse, cyber_bullying]

    for keyword, list_update in zip(keywords, lists):
        page = requests.get("https://www.google.co.in/search?q=" + query + keyword)
        soup = BeautifulSoup(page.content, 'html.parser')
        links = soup.findAll("a")
        result_div = soup.find_all("a", href=re.compile("(?<=/url\?q=)(htt.*://.*)"))
        for link in result_div:
            link = re.split(":(?=http)", link["href"].replace("/url?q=", ""))
            x = str(link).split('&')

            list_update.append(x[0].replace("['", ""))

    context = {
        'general': general,
        'crime': crime,
        'child abuse': child_abuse,
        'woman abuse': women_abuse,
        'cyber bullying': cyber_bullying
    }

    reduced = [
        general[:4],
        crime[:4],
        child_abuse[:4],
        women_abuse[:4],
        cyber_bullying[:4]
    ]





    return (context, reduced, lists)


def count_items(context):

    list_count_dict = dict()
    temp = list()

    for key, value in context.items():

        for key2, value2 in value.items():
            temp.append(len(value2))

        list_count_dict[key] = temp
        temp = []

    return list_count_dict


def wiki_data(lists):
    context = dict()

    temp = list()

    for i in lists:
        temp.append(i.split('%')[0])


    for link in temp:
        page = requests.get(str(link))
        infobox = dict()
        if page.status_code is 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            try:
                table = soup.select(".infobox")[0]
            except:
                print(f"no table in {link}")
                continue
            rows = table.find_all('tr')
            flag = 1
            i = 0
            length = len(rows)
            for i in range(length):
                try:
                    if (i == 0):
                        infobox['name'] = str(rows[i].th.text)
                        flag = 0
                    else:
                        infobox[str(rows[i].th.text)] = (str(rows[i].td.text))
                except:
                    pass
        else:
            print("Cant reach to servers")
        context[str(link)] = infobox
        # print(infobox)
    return context



