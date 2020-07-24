from crawler.models import Link, Category, UserProfile, CrawledLinks


def category_count(user):

    temp = list()

    categories = Category.objects.all()
    userprofile = UserProfile.objects.get(user=user)

    for category in categories:

        links = len(CrawledLinks.objects.filter(userprofile=userprofile, link__category__name=category.name))


        temp.append(links)


    return temp


def category_percent(user):

    temp = category_count(user)
    total = sum(temp)
    percent = list()
    context = dict()

    for item in temp:
        if total != 0:
            percent.append(( item/total ) * 100)

    categories = Category.objects.all()

    for category, p in zip(categories, percent):
        context[category.name] = round(p, 2)

    return context
