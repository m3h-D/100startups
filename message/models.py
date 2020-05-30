from django.db import models
from usercp.models import User
from usertracker.models import TheStatus
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.

class NotificationManager(models.Manager):
    """a custom manager model for conten_type objects

    Arguments:
        models {MODULE} -- a django built-in class to define tables
    """    
    def create_by_model(self, user, status, instance):
        """to create notification object

        Arguments:
            user {OBJECT} -- get User model object
            status {STRING} -- the status of the notification
            instance {OBJECT} -- is the object the norification is about

        Returns:
            ORM -- return inharitanced ORM(create)
        """        
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.pk
        return super().create(content_type=content_type, object_id=obj_id, status=status, user=user)

class Notification(models.Model):
    """this table contains user field to define requested user
       content_object is to define which object this notification is about

    Arguments:
        models {MODULE} -- a django built-in class to define tables

    Returns:
        STRING -- returns user and the status of the notification
    """    
    user = models.ForeignKey(User, related_name='notification', on_delete=models.CASCADE)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    status = models.ForeignKey(TheStatus, related_name='notification', on_delete=models.CASCADE)
    is_readed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    objects = NotificationManager()

    def __str__(self):
        return f"{self.user} -- {self.status}"



class SendMessage(models.Model):
    """this table contains sender receiver and receivers if there is bulk messages and content
       and is_readed field to check if message is readed or not

    Arguments:
        models {MODULE} -- a django built-in class to define tables

    Returns:
        STRING -- returns first name and last name of sender
    """    
    sender = models.ForeignKey(
        User, related_name='messagesender', on_delete=models.CASCADE)
    receiver = models.ForeignKey(
        User, related_name='messagereceiver', blank=True, null=True, on_delete=models.SET_NULL)
    receivers = models.ManyToManyField(
        User, related_name='messagereceivers', blank=True)
    message_content = models.TextField()
    url = models.URLField(blank=True, null=True)
    is_readed = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        return f"{self.sender.first_name} {self.sender.last_name}"


class AllMessages(models.Model):
    """this model acts like a chat room that includes some messages
       with the title of message and the type of message

    Arguments:
        models {MODULE} -- a django built-in class to define tables
    """    
    message_title = models.CharField(max_length=120)
    send_message = models.ManyToManyField(
        SendMessage, 'allmessages', blank=True)
    THE_TYPE = (
        ('chat', 'گفتگو'),
        ('error', 'گزارش خطا'),
    )
    message_type = models.CharField(max_length=5, choices=THE_TYPE, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)


class SupportModel(models.Model):
    """this model designed for startup ownres to send errors to support staff

    Arguments:
        models {MODULE} -- a django built-in class to define tables
    """    
    user = models.ForeignKey(
        blank=True, null=True, on_delete=models.SET_NULL, related_name='support', to=User)
    phone = models.CharField(max_length=15)
    name = models.CharField(max_length=120)
    image = models.ImageField(blank=True)
    content = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)
