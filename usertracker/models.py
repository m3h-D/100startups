from django.db import models
from usercp.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
# Create your models here.

THE_STATUSES = (
    ('sending-message',  'ارسال پیام',),
    ('seeing-message',  'مشاهده پیام'),
    ('forget-password',  'فراموشی رمز'),
    ('creating-user',  'ایجاد کاربر'),
    ('accept-first',  'تایید اطلاعات'),
    ('fail-first',  'رد اطلاعات'),
    ('editing-user',  'ویرایش کاربر'),
    ('editing-startup',  'ویرایش استارت آپ'),
    ('submit-scores',  'ثبت نمرات'),
    ('accept-referee-scores',  'تایید داور غیر حضوری'),
    ('fail-referee-scores',  'رد داور غیر حضوری'),
    ('accept-first_referee',  'تایید داوری اولیه'),
    ('fail-first_referee',  'رد داوری اولیه'),
    ('accept-presence',  'تایید داوری حضوری'),
    ('fail-presence',  'رد داوری حضوری'),
    ('select-leader',  'انتخاب راهبر'),
    ('select-not-presence-referees',  'انتخاب داور غیر حضوری'),
    ('select-presence-referees',  'انتخاب داور حضوری'),
    ('delete-user',  'حذف کاربر'),
    ('delete-startup',  'حذف استارت آپ'),
    ('send-email',  'ارسال ایمیل'),
    ('send-sms',  'ارسال پیامک'),
    ('import-information',  'بازدید صفحه اطلاعات استارتاپ'),
    ('import-change_pass',  'تغییر پسورد'),
    ('import-verify-step',  'صفحه ی اعتبار سنجی'),
    ('verifying-step',  'دریافت کد ثبت نام'),
    ('import-startup-step',  'مرحله اطلاعات استارتاپ'),
    ('registering-startup-step',  'تکمیل اطلاعات استارتاپ'),
    ('import-team-step',  'مرحله اطلاعات تیم'),
    ('submit-team-step',  'تکمیل اطلاعات تیم'),
    ('import-upload-step',  'مرحله آپلود'),
    ('submit-upload-step',  'تکمیل اطلاعات آپلود'),
    ('import-presentation-step',  'مرحله پیچ دک'),
    ('submit-presentation-step',  'تکمیل مرحله پیچ دک'),
    ('import-finish-step',  'تکمیل ثبت نام'),
    ('search-list-user',  'جستجوی کاربران'),
    ('search-list-startup',  'جستجوی استارتاپ'),
    ('import-list-user',  'لیست کاربران'),
    ('import-list-startup',  'لیست استارتاپ ها'),
    ('import-list-coach',  'لیست مربیان'),
    ('import-list-referee',  'لیست داوران'),
    ('import-list-investor',  'لیست سرمایه گذاران'),
    ('import-list-cat',  'صفحه دسته بندی ها'),
    ('deleted-cat',  'حذف دسته'),
    ('import-profile',  'پروفایل'),
    ('edit-profile',  'اصلاح پروفایل'),
    ('import-dashboard-referee',  'پنل داور'),
    ('import-dashboard-operational',  'پنل مدیر عملیاتی'),
    ('import-dashboard-coach',  'پنل مربی'),
    ('import-dashboard-leader',  'پنل راهبر'),
    ('import-dashboard-investor',  'پنل سرمایه گذار'),
    ('import-dashboard-financial',  'پنل مالی'),
    ('import-dashboard-subscriber',  'پنل استارتاپ'),
    ('import-dashboard-administrator',  'پنل مدیریت'),
    ('import-edit-user',  'صفحه ویرایش کاربر'),
    ('import-edit-startup',  'صفحه ویرایش استارتاپ'),
    ('import-edit-cat',  'صفحه ویرایش دسته بندی'),
    ('import-create-cat',  'صفحه ساخت دسته بندی'),
    ('import-create-user',  'صفحه ساخت کاربر'),
    ('import-login-page',  'صفحه ورود به پنل'),
    ('fail-login-dashboard',  'عدم ورود به پنل'),
    ('import-list-coach',  'لیست مربیان/راهبران'),
    ('import-message-box',  'صندوق پیام'),
    ('import-send-message',  'صفحه ی ارسال پیام'),
    ('import-message-show',  'صفحه ی نمایش پیام'),
    ('seeing-message',  'مشاهده ی پیام'),
    ('import-request-money',  'صفحه ی درخواست'),
    ('sending-request-money',  'ارسال درخواست'),
    ('import-manage-request',  'صفحه ی مدیریت درخواست'),
    ('accept-manage-request',  'تایید درخواست'),
    ('fail-manage-request',  'رد درخواست'),
    ('accept-leader-request',  'تایید درخواست توسط راهبر'),
    ('fail-leader-request',  'رد درخواست توسط راهبر'),
    ('referer',  'لینک ارجاع استارت آپ'),
    ('phone-login-dashboard', 'ورود با شماره موبایل'),
    ('fail-document', 'رد مدارک'),
    ('accept-document', 'تایید مدارک'),
    ('submit-status-presence', 'تایید داوری حضوری'),
    ('submit-status-document', 'صحت سنجی مدارک'),
    ('chenge-username', 'تغییر نام کاربری'),
    ('import-list-accelerator', 'لیست شتاب دهنده'),
    ('create-accelerator', 'ساخت شتاب دهنده'),
    ('edit-accelerator', 'ویرایش شتاب دهنده'),
    ('delete-accelerator', 'ویرایش شتاب دهنده'),
    ('sort-mentors', 'مرتب سازی مربیان'),
    ('excel-mentors', 'اکسل مربیان'),
    ('reconsider', 'تجدید نظر'),
    ('selected-startup', 'استارتاپ منتخب'),
    ('not-selected-startup', 'عدم منتخب بودن استارتاپ'),
    ('suspended-startup', 'استارتاپ معلق'),
    ('accept-session-investor', 'شرکت درجلسه با استارتاپ(سرمایه گذار)'),
    ('fail-session-investor', 'عدم شرکت درجلسه با استارتاپ(سرمایه گذار)'),
    ('available-for-invest', 'استارتاپ قابل سرمایه گذاری است'),
    ('not-available-for-invest', 'استارتاپ قابل سرمایه گذاری نیست'),
    ('accept-referee-scores-pres', 'تایید داور حضوری'),
    ('fail-referee-scores-pres', 'رد داور حضوری'),
    ('selected-as-accelerator', 'انتخاب بعنوان شتاب دهنده'),
    ('sorted-mentor', 'تغییر لیست منتورها'),
    ('assigne-startup-to-leader', 'پیشنهاد استارتاپ به راهبر'),
    ('import-offerto-leader-list', 'لیست راهبران پیشنها شده به استارت ها'),
    ('import-meetingto-coach-list', 'لیست مربیان پیشنها شده به استارت ها'),
    ('create-meetingto-coach', 'ایجاد جلسه با مربی'),
    ('edit-meetingto-coach', 'تغییر میتینگ مربیان'),
    ('edit-offerto-leader', 'تغییر پیشنهاد استارتاپ با راهبر'),
    ('create-event-investor', 'پیشنهاد استارتاپ به سرمایه گذار'),
    ('wants-to-meet-startup', 'تمایل ملاقات راهبر  با استارتاپ'),
    ('not-wants-to-meet-startup', 'عدم تمایل ملاقات راهبر  با استارتاپ'),
    ('import-list-events', 'مشاهده لیست ایونت ها'),
    ('import-notification-panel', 'لیست نوتیفیکیشن ها'),
    ('investor-can-see-startup', 'اجازه دسترسی به استارتاپ'),
    ('investors-can-see-startup', 'شروع بررسی'),
    ('investors-cant-see-startup', 'پایان بررسی'),
    ('add-user-mentors', 'اضافه کردن به منتور ها'),
    ('delete-user-mentors', 'حذف از منتور ها'),
    ('requested-money-op', 'مبلغ درخواستی توسط مدیر عملیاتی'),
    ('delete-pres-referee', 'حذف داور حضوری'),
    ('delete-not-pres-referee', 'حذف داور غیر حضوری'),
    ('referee-wants-to-lead', 'علاقه داور به راهبری'),
    ('referee-wants-to-invest', 'علاقه داور به سرمایه گذاری'),
)

class TheStatus(models.Model):
    """the status of user that been used in usertracker and notification model
    
    Arguments:
        models {class Module} -- this table inharitanced from built-in Django Model
    
    Returns:
        STRING -- returns the status in persian
    """
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=100, choices=THE_STATUSES, blank=True)

    def __str__(self):
        return self.get_name_display()


class UserTrackerManager(models.Manager):
    """custom ORM
    
    Arguments:
        models {class Module} -- it's a model manager that inharitanced from django Manager
    
    Returns:
        QS -- returns/create a queryset of UserTracker record
    """

    def filter_by_model(self, instance, the_status=None):
        """a custome ORM that filter the UserTracker by Model or content_type
        
        Arguments:
            instance {OBJECT} -- instance is an object of a model that been selected as content_type in GenericForeignKey
        
        Returns:
            QS -- returns a queryset of usertracker records
        """
        content_type = ContentType.objects.get_for_model(instance.__class__)
        object_id = instance.id
        if the_status:
            queryset = super(UserTrackerManager, self).filter(
                content_type=content_type, object_id=object_id, the_status__in=the_status)
        else:
            queryset = super(UserTrackerManager, self).filter(
                content_type=content_type, object_id=object_id)
        return queryset

    def create_by_model(self, url, user_ip, user_agent, user=None, instance=None):
        """create a record in UserTracker table
        
        Arguments:
            instance {OBJECT} -- assign a model instance to detailing the info
            url {URL} -- a path that user has been visited
            user_ip {REMOTE_IP} -- the ip of requeted user
            user_agent {MODULE} -- a module tha specife the user agent(browser, device)
        
        Keyword Arguments:
            user {OBJECT} -- assign the requested user if is authenticated (default: {None})
        
        Returns:
            QS -- return queryset of created record
        """
        content_type = None
        object_id = 0
        if instance is not None:
            content_type = ContentType.objects.get_for_model(
                instance.__class__)
            object_id = instance.id

        queryset = super(UserTrackerManager, self).create(user=user,
                                                          content_type=content_type, object_id=object_id, url=url, user_ip=user_ip, user_agent=user_agent)
        return queryset


class UserTracker(models.Model):
    """a model to track requested user by visited path, ip, id
    
    Arguments:
        models {class Module} -- a Model module that inharitanced from django Model to create Table
    
    Returns:
        STRING -- returns requested user specifications
    """
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(
        User, related_name='usertracker', blank=True, null=True, on_delete=models.SET_NULL)
    content_type = models.ForeignKey(
        ContentType, blank=True, null=True, on_delete=models.SET_NULL)
    object_id = models.PositiveIntegerField(default=0)
    content_object = GenericForeignKey('content_type', 'object_id')
    url = models.URLField()
    user_ip = models.GenericIPAddressField(blank=True, null=True)
    the_status = models.ForeignKey(
        TheStatus, related_name='usertrackers', null=True, blank=True, on_delete=models.SET_NULL)
    status = models.TextField(blank=True, null=True)
    user_agent = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)
    objects = UserTrackerManager()

    class Meta:
        ordering = ('-created_date',)

    def __str__(self):
        try:
            return f"{self.user.first_name} {self.user.last_name}/{self.user.phone} {self.status}"
        except:
            return self.content_object.title, self.status
        finally:
            return f"{self.user_ip} {self.status}"




class UserContent(models.Model):
    """a Model that contains additional information about user from UserTracker
    
    Arguments:
        models {OBJECT} -- a Model module that inharitanced from django Model to create Table 
    
    Returns:
        STRING -- returns user specifiaction if available
    """
    user_tracker = models.ForeignKey(UserTracker, related_name='usercontent', on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        try:
            return f'{self.user_tracker.user} -- {self.user_tracker.content}'
        except:
            return str(self.content)