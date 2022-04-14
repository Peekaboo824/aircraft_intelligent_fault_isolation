from django.db import models

# Create your models here.
class Image(models.Model):
    name_cms = models.CharField(max_length=100,null=True)
    image_cms = models.ImageField(upload_to='static/image/CMS',null=True)
    res_cms = models.TextField(null=True)
    name_fr = models.CharField(max_length=100,null=True)
    image_fr = models.ImageField(upload_to='static/image/FR',null=True)
    res_fr = models.TextField(null=True)
    def __str__(self):
        return self.name_cms
