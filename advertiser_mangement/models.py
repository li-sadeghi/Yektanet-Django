from django.db import models

class Advertiser(models.Model):
    id = models.IntegerField(primary_key=True)
    clicks = models.IntegerField()
    views = models.IntegerField()
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Ad(models.Model):
    id = models.AutoField(primary_key=True)
    click = models.IntegerField()
    views = models.IntegerField()
    title = models.CharField(max_length=20)
    imgUrl = models.CharField(max_length=255)
    link = models.CharField(max_length=255)
    advertiser = models.ForeignKey(Advertiser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
