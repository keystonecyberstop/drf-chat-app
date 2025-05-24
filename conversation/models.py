from django.db import models
from django.conf import settings

class Chat(models.Model):
    participants = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='chats',
        blank=True
    )
    name = models.CharField(max_length=100, blank=True, null=True)
    is_group_chat = models.BooleanField(default=False)
    admin = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='admin_chats'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.is_group_chat and self.name:
            return self.name
        return f"Chat {self.id}"


class Message(models.Model):
    chat = models.ForeignKey(
        'Chat',
        on_delete=models.CASCADE,
        related_name='messages'
    )
    sender = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sent_messages'
    )
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    attachment = models.FileField(upload_to='attachments/', blank=True, null=True)

    def __str__(self):
        return f"Message from {self.sender.username} in Chat {self.chat.id} at {self.timestamp}"

    class Meta:
        ordering = ['timestamp']


class Participant(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    joined_at = models.DateTimeField(auto_now_add=True)
    last_read_timestamp = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('user', 'chat')

    def __str__(self):
        return f"{self.user.username} in Chat {self.chat.id}"