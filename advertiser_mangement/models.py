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
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

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



