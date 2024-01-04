from django.db import models
from django.utils import timezone


class Advertiser(models.Model):
    id = models.IntegerField(primary_key=True)
    clicks = models.IntegerField()
    views = models.IntegerField()
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Ad(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=20)
    imgUrl = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    approve = models.BooleanField(default=False)
    advertiser = models.ForeignKey(
        Advertiser, related_name='ads', on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    @property
    def avg_time_diff(self):
        all_views = View.objects.filter(ad=self)
        all_clicks = Click.objects.filter(ad=self)
        all_ip_addresses = View.objects.values('viewer_ip').distinct()
        total_diff = 0
        count = 0
        for ip in all_ip_addresses:
            ip = ip['viewer_ip']
            view_time = all_views.filter(viewer_ip=ip).order_by('time')
            click_time = all_clicks.filter(
                clicker_ip=ip).order_by('time_clicked')
            if view_time and click_time:
                total_diff += (view_time.last().time -
                               click_time.last().time_clicked).total_seconds()
                count += 1
        if count == 0:
            return 0
        return round(total_diff / count, 2)

    @property
    def click_rate(self):
        rate = 0 if self.view_count() == 0 else self.click_count()/self.view_count()
        return round(rate, 2)

    @property
    def click_count(self):
        click_count = View.objects.filter(ad_id=self.id).count
        return click_count

    @property
    def view_count(self):
        view_count = View.objects.filter(ad_id=self.id).count
        return view_count


class View(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    time = models.DateTimeField(default=timezone.now)
    viewer_ip = models.GenericIPAddressField()

    def __str__(self):
        return f'view of {self.ad.title}'


class Click(models.Model):
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE)
    time_clicked = models.DateTimeField(default=timezone.now)
    clicker_ip = models.GenericIPAddressField()

    def __str__(self):
        return f'clicked on {self.ad.title}'
