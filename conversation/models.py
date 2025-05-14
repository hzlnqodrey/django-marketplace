from django.contrib.auth.models import User
from django.db import models

from item.models import Item, User


# Create your models here.
class Conversation(models.Model):
    # If owner delete the item, so the conversation inside the item is deleted too
    item = models.ForeignKey(Item, related_name='conversations', on_delete=models.CASCADE)

    # Multiple Users can chat [at this point, owner and buyer]
    members = models.ManyToManyField(User, related_name='conversations', )

    # Everytime we save this object, it's automatically updated
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-modified_at', )

class ConversationMessage(models.Model):
    conversation = models.ForeignKey(Conversation, related_name='messages', on_delete=models.CASCADE)

    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='created_messages', on_delete=models.CASCADE)