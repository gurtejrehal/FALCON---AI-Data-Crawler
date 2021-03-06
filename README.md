# SMART INDIA HACKATHON 2020 (Winner)

## SK216: Data Crawlers to crawl keywords in area of crime, child abuse, woman abuse etc.

## FALCON - AI Data Crawler

See installation [here](#how-to-install)

## What is this?
Falcon Search has been created to aid the National Crime Records Bureau keeping in mind the need for an efficient data crawler that collects classified data from the web based on given keywords. It is a SaaS web data integration (WDI) platform which converts unstructured web data into structured format by extracting, preparing and integrating web data in areas of crime for consumption in criminal investigation agencies. 


Falcon provides a visual environment for automating the workflow of extracting and transforming web data. After specifying the target website url, the web data extraction module provides a visual environment for designing automated workflows for harvesting data, going beyond HTML/XML parsing of static content to automate end user interactions yielding data that would otherwise not be immediately visible. Once extracted, the software provides full data preparation capabilities that are used for harmonizing and cleansing the web data. 

For consuming the results, Falcon provides several options. It has its own visualization and dashboarding module to help criminal investigators gain the insights that they need. It also provides APIs that offer full access to everything that can be done on our platform, allowing web data to be integrated directly.  


FALCON is capable of crawling ten million links and scrape one million links per month using Celery Worker. It moreover has the potential of outperforming this number if tested under standard cloud platforms. 

![falcon](https://user-images.githubusercontent.com/28597524/100134752-b1f8ec80-2eae-11eb-9852-51a6c2e5a5ba.png "FALCON")



## Deployed on Pythonanywhere
The first version of FALCON (only a demo version) is deployed, it is limited to threaded crawling/scraping. AI tasks and CELERY workers are disabled due to free hosting service provider. To experience FALCON to its full capability please [install](#how-to-install) it and use.

Deployed [here](http://sih2020sk216slytherin.pythonanywhere.com "here").

[![Deploy](https://www.pythonanywhere.com/static/anywhere/images/PA-logo.svg)](http://sih2020sk216slytherin.pythonanywhere.com)

### Test User
username - sih2020sk216
password - Sih#2020


## Features
- Structured data
- News 
- Email PDF report
- Graphical Data
- Scraped Data in text, images,pdf, docx and video format.
- Trends and Analytica
- Recent Tweets (Social Media Crawling/Scraping)
- Multiple keywords search
- Multiple filters option
- Schedule the scraping time
- User registration and advance admin panel
- AI to search smart
- Search with rotating proxy to avoid ban.
- Falcon own custom REST API
- Multilingual support
- Media data AI Processing
- Scalable to Crawl 10 Millions Link and Scrape 1 Million Links


![collage (1)](https://user-images.githubusercontent.com/28597524/100134680-9392f100-2eae-11eb-9e32-071c90947766.jpg "FALCON")



### Efficient
FALCON uses the celery worker feature to take up multiple tasks from the user and perform it in a queue.
We can have upto 10 celery workers at a time. This feature allows us to crawl around ten million links and scrap around one million links.


## How to Install
- Create virtual enviorement, then activate it.
- Install all the requirements file, ``` pip install -r requirements.txt```
- Setup RabbitMQ server for broker service, ``` docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3-management```
- start your rabbitmq broker service.
- In falcon setting change ```CELERY_BROKER_URL = 'your_rabbitmq_address'```, if your not using the default port for RabbitMQ.
- Run celery worker, ```celery -A falcon worker -l info```
- For first time usage, ```python manage.py migrate``` and create admin ```python manage.py createsuperuser```
- Run FALCON, ```python manage.py runserver```





