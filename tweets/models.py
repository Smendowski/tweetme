from django.db import models
import random 

class Tweet(models.Model):
  # Automatically generated by django is id:
  # id = models.AutoFiels(primary_key=True)
  content = models.TextField()
  image = models.FileField(upload_to='images/', blank=True, null=True)

  # Reordering tweets to see the oldest at the bottom
  class Meta:
    ordering = ['-id']

  def serialize(self):
    return{
      "id": self.id,
      "content": self.content,
      "likes": random.randint(0,200)
    }
  