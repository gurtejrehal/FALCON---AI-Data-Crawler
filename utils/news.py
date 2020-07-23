from GoogleNews import GoogleNews



def news(query):

    googlenews = GoogleNews(lang='en')
    googlenews.search(query)
    return googlenews.result()
