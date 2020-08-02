from celery import shared_task
from datetime import datetime, timedelta
from scheduler.models import ScrapedLink, RescrapedLink
from utils.score import Score

@shared_task
def rescrape_save(old_link, new_data):
    check = Score()
    old_data = ScrapedLink.objects.get(link=old_link)
    score = check.total_score(old_data.scrape_data, new_data)
    done = False

    if score > 0:
        rescrape = RescrapedLink(link=old_data, scrape_data=new_data, score=score, done=True)
        rescrape.save()
        done = True

    return done




# scheduled_day = datetime.utcnow() + timedelta(days=1)
# rescrape_save.apply_async(eta=scheduled_day)



