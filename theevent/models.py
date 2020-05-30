from django.db import models
from usercp.models import User
from startup.models import StartUp
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# Create your models here.


class CreateEventManager(models.Manager):
    """A custom model manager for CreateEvent for filter and create based on model class instance

    Arguments:
        models {MODULE} -- a django built-in module to create custom ORM
    """
    def create_by_model(self, instance):
        """create a record based on model instances

        Arguments:
            instance {OBJECT} -- an object that will be used as content_object

        Returns:
            QUERYSET -- returns queryset of created object
        """        
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.pk
        queryset = super().create(content_type=content_type, object_id=obj_id)
        return queryset

    def filter_by_model(self, instance):
        """filter the records or objects based on model class instance

        Arguments:
            instance {OBJECT} -- an object that will be used as content_object

        Returns:
            QUERYSET -- returns queryset of filtered objects
        """        
        content_type = ContentType.objects.get_for_model(instance.__class__)
        obj_id = instance.id
        return super().filter(content_type=content_type, object_id=obj_id)




class CreateEvent(models.Model):
    """this model is actully define the user that we wants offer/assign some values such as startups or busy or free status

    Arguments:
        models {MODULE} -- a django built-in class to define tables
    """    
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField(default=0)
    content_object = GenericForeignKey('content_type', 'object_id')
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    objects = CreateEventManager()

    def __str__(self):
        try:
            return f'{self.content_object.user.first_name} {self.content_object.user.last_name}'
        except:
            return str(self.id)

class EventAbstract(models.Model):
    """an abstract class to create only one table with nearly same fields for models like:
       - StartupsEvent
       - CoachEvent
       - LeaderModel

    Arguments:
        models {MODULE} -- a django built-in class to define tables
    """    
    event = models.ForeignKey(
        CreateEvent, related_name="%(app_label)s_%(class)s", on_delete=models.CASCADE)
    startup = models.ForeignKey(
        StartUp, related_name="%(app_label)s_%(class)s", blank=True, null=True, on_delete=models.SET_NULL)
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True

class TheEvent(models.Model):
    """the table that will be use in every event that store the id of the event and the type of the event

    Arguments:
        models {MODULE} -- a django built-in class to define tables
    """    
    id = models.IntegerField(blank=True, null=True)
    the_id = models.AutoField(primary_key=True, unique=True)
    owner = models.ForeignKey(
        User, related_name='theevent', on_delete=models.CASCADE)
    c_event = models.ManyToManyField(
        CreateEvent, related_name='theevent', blank=True)
    THE_TYPE = (
        ('investor', "سرمایه گذار"),
        ('coach', "مربی"),
        ('leader', "راهبر"),
    )
    th_type = models.CharField(
        max_length=20, default='investor', choices=THE_TYPE)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.th_type} -- {self.c_event.all()}"

class StartupsEvent(EventAbstract):
    """an inharitansed model to assign startups to investors (create_event)

    Arguments:
        EventAbstract {ABSTRACT MODEL} -- this class is inharitanced from EventAbstract for less table craetion
    """    
    schedule = models.OneToOneField('StartupTime', related_name='startupsevent', blank=True, null=True, on_delete=models.CASCADE)
    class Meta:
        ordering = ('-created_date',)


class CoachEvent(EventAbstract):
    THE_TYPE = (
        (1, 'ازاد'),
        (2, 'پر'),
    )
    th_time = models.SmallIntegerField(choices=THE_TYPE)
    schedule = models.OneToOneField('StartupTime', related_name='coachevent', blank=True, null=True, on_delete=models.CASCADE)


class WantsMeet(models.Model):
    the_event = models.OneToOneField(
        TheEvent, related_name='wantsmeet', on_delete=models.CASCADE)
    startup = models.ForeignKey(
        StartUp, related_name='wantsmeet', blank=True, null=True, on_delete=models.SET_NULL)
    c_event = models.ForeignKey(
        CreateEvent, related_name='wantsmeet', blank=True, null=True, on_delete=models.SET_NULL)
    event_counter = models.SmallIntegerField(default=1)

    created_date = models.DateTimeField(auto_now_add=True)


class StartupTime(models.Model):
    the_event = models.ForeignKey(
        TheEvent, related_name='startuptime', blank=True, null=True, on_delete=models.SET_NULL)
    the_date = models.DateTimeField(blank=True, null=True)
    to_date = models.DateTimeField(blank=True, null=True)
    from_time = models.TimeField(blank=True, null=True)
    to_time = models.TimeField(blank=True, null=True)
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)


class LeaderModel(EventAbstract):
    THE_STATUS = (
        (1, 'iwant'),
        (0, 'idontwant'),
    )
    status = models.IntegerField(choices=THE_STATUS, default=0)

    def __str__(self):
        return f"{self.startup} {self.status}"
