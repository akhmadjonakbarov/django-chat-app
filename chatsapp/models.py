from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


# Create your models here.

class Contact(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='firends')
    friends = models.ManyToManyField('self', blank=True)

    def __str__(self) -> str:
        return self.user.get_username()


class Message(models.Model):
    contact = models.ForeignKey(
        Contact, on_delete=models.CASCADE, related_name="messages")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.contact.user.get_username()


class Chat(models.Model):
    owner = models.ForeignKey(User, related_name='set_chats', on_delete=models.SET_NULL, blank=True, null=True)
    name = models.CharField(max_length=250)
    participants = models.ManyToManyField(Contact, related_name='chats', blank=True)
    messages: Message = models.ManyToManyField(Message, blank=True)

    def last_30_messages(self):
        return self.messages.objects.order_by('-timestamp').all()[:30]

    def __str__(self) -> str:
        return f"{self.pk}"
