from django.db import models
from django.contrib.auth.models import User





# jessie code about bookmark & Review

# Bookmark Function
class Bookmark(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place_id = models.CharField(max_length=300)
    place_name = models.CharField(max_length=300)


# Reviews Function
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    place_id = models.CharField(max_length=300)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
