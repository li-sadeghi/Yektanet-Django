from __future__ import absolute_import, unicode_literals
from celery import shared_task, Celery
from celery.schedules import crontab
from django.utils import timezone
from .models import Click, View, Ad

app = Celery()
data_hourly = {}


@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(
        crontab(hour=0, minute=0), daily_reset.s(), name='daily reset')
    sender.add_periodic_task(
        crontab(minute=0), hourly_report.s(), name='hourly report')
    sender.add_periodic_task(
        crontab(minute=0, hour=0), daily_report.s(), name='daily report')


@app.task
def daily_reset():
    data_hourly.clear()


@app.task
def hourly_report():
    end_time = timezone.now()
    start_time = end_time - timezone.timedelta(hours=1)
    status = ""

    ads = Ad.objects.all()
    for ad in ads:
        clicks = Click.objects.filter(
            ad=ad, time_clicked__range=(start_time, end_time)).count()
        views = View.objects.filter(
            ad=ad, time__range=(start_time, end_time)).count()

        existing_clicks, existing_views = data_hourly.get(ad.id, (0, 0))
        data_hourly[ad.id] = (clicks + existing_clicks, views + existing_views)

        status += f"The ad {ad.title} had {clicks} clicks and {views} views in the last hour.\n"

    return status


@app.task
def daily_report():
    status = ""

    ads = Ad.objects.all()
    for ad_id, (clicks, views) in data_hourly.items():
        ad = Ad.objects.get(id=ad_id)

        status += f"The ad {ad.title} had {clicks} clicks and {views} views in the last day.\n"

    return status
