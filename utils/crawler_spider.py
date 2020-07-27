import requests
import re, random
from bs4 import BeautifulSoup
from googleapiclient.discovery import build

api_key = "AIzaSyA-xf1iJjNQCELDVGDtYJ7aM0t1ZulB0kQ"
cse_id = "016133495723645302024:cfibqauizrm"


def google_query(query, **kwargs):
    query_service = build("customsearch", "v1", developerKey=api_key)
    query_results = query_service.cse().list(q=query, cx=cse_id, **kwargs).execute()

    try:
        return query_results['items']
    except:
        return dict()


keywords = ["Crime",
            "Child Abuse",
            "Women Abuse",
            "Cyber Bullying"]


def crawling(query, keywords):
    general = list()
    crime = list()
    child_abuse = list()
    women_abuse = list()
    pornography = list()
    rape = list()
    cyber_bullying = list()
    general_scrape = list()
    crime_scrape = list()
    child_abuse_scrape = list()
    women_abuse_scrape = list()
    pornography_scrape = list()
    rape_scrape = list()
    cyber_bullying_scrape = list()
    lists = [general, crime, child_abuse, women_abuse, pornography, rape, cyber_bullying]
    scrape_lists = [general_scrape, crime_scrape, child_abuse_scrape, women_abuse_scrape, pornography_scrape, rape_scrape, cyber_bullying_scrape]

    for keyword, list_update, scrape_list_update in zip(keywords, lists, scrape_lists):
        try:
            num = random.randint(7, 10)
            pages = google_query(f'{query} {keyword}', num=num)
            for result in pages:
                list_update.append(result['link'])
                # print(result)
                scrape_list_update.append(result['snippet'])

        except:
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
    # print(scrape_lists)

    # scrape_context = {
    #     'general_scrape': general_scrape,
    #     'crime_scrape': crime_scrape,
    #     'child_scrape': child_abuse_scrape,
    #     'woman_scrape': women_abuse_scrape,
    #     'cyber_scrape': cyber_bullying_scrape
    # }

    return context, reduced, lists, scrape_lists


# def crawling(query, keywords):
#     general = list()
#     crime = list()
#     child_abuse = list()
#     women_abuse = list()
#     cyber_bullying = list()
#     lists = [general, crime, child_abuse, women_abuse, cyber_bullying]
#
#     for keyword, list_update in zip(keywords, lists):
#         page = requests.get("https://www.google.co.in/search?q=" + query + keyword)
#         soup = BeautifulSoup(page.content, 'html.parser')
#         links = soup.findAll("a")
#         result_div = soup.find_all("a", href=re.compile("(?<=/url\?q=)(htt.*://.*)"))
#         for link in result_div:
#             link = re.split(":(?=http)", link["href"].replace("/url?q=", ""))
#             x = str(link).split('&')
#
#             list_update.append(x[0].replace("['", ""))
#
#     context = {
#         'general': general,
#         'crime': crime,
#         'child abuse': child_abuse,
#         'woman abuse': women_abuse,
#         'cyber bullying': cyber_bullying
#     }
#
#     reduced = [
#         general[:4],
#         crime[:4],
#         child_abuse[:4],
#         women_abuse[:4],
#         cyber_bullying[:4]
#     ]
#
#     return (context, reduced, lists)


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
