from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
# Create your models here.

# class User(models.Model):
# 	user_id = models.CharField(primary_key=True,max_length=100)
# 	username = models.CharField(max_length=100)
# 	profile_picture = models.URLField()
# 	email = models.EmailField()
#
# 	def __str__(self):
# 		return self.username

class Level(models.Model):
    #options = (
    #    ('A', 'Audio'),
    #    ('I', 'Image'),
    #    ('G', 'Gif'),
    #)
	level = models.IntegerField(default =1)
	answer = models.TextField()
	source_hint = models.TextField(blank=True,null=True)
	#level_file =  models.FileField(upload_to = 'level_images/',null=True)
	#filetype = models.CharField(max_length = 10,choices=options,default='Audio')
	def __str__(self):
		return str(self.level)

class KryptosUser(models.Model):
    # TODO: Bring user ID from auth
    user_id = models.OneToOneField(User,primary_key=True, on_delete=models.CASCADE)
    level = models.IntegerField(default=1)
    rank = models.IntegerField(default=10000)
    created_at = models.DateTimeField(auto_now_add=True, editable=True)
    updated_at = models.DateTimeField(auto_now=True, editable=True)

    class Meta:
        ordering = ['-level', 'updated_at']

    def __str__(self):
        return str(self.user_id.email)

    @receiver(post_save, sender=User)
    def build_kryptos_user_model(sender, instance, created, **kwargs):
        if created:
	        kryptos = KryptosUser(user_id=instance)
	        kryptos.save()
