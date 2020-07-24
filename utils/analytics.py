from crawler.models import Link, Category


def category_count():

    temp = list()

    categories = Category.objects.all()

    for category in categories:

        links = len(Link.objects.filter(category__name=category.name))

        temp.append(links)


    return temp


def category_percent():

    temp = category_count()
    total = sum(temp)
    percent = list()
    context = dict()

    for item in temp:
        percent.append(( item/total ) * 100)

    categories = Category.objects.all()

    for category, p in zip(categories, percent):
        context[category.name] = round(p, 2)

    return context
