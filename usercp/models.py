from django.db import models
from django.core.validators import RegexValidator
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from category.models import Categories

# Create your models here.


class Role(models.Model):
    """the roles that will assign to karmand users
    
    Arguments:
        models {MODEL} -- built-in django model
    
    Returns:
        STRING -- returns the persian side of each role
    """
    THE_ROLES = (
        ('financial', 'مالی'),
        ('coach', 'مربی'),
        ('leader', 'راهبر'),
        ('surpreme', 'راهبر ارشد'),
        ('investor', 'سرمایه گذار'),
        ('referee', 'داور'),
        ('operational', 'مدیر عملیات'),
    )
    name = models.CharField(max_length=11, choices=THE_ROLES)

    def __str__(self):
        return self.get_name_display()


class UserManager(BaseUserManager):
    """to create some custom manager (ORM)
    
    Arguments:
        BaseUserManager {CLASS} -- a django built-in class
    
    Raises:
        ValueError: ensure that the user must have a phone number
        ValueError: ensure that the user must have an email
    
    Returns:
        OBJECT -- created record of user
    """

    def create_startup_user(self, phone, password=None, username=None):
        """custom ORM to create an account for owner of startup
        
        Arguments:
            phone {STRING} -- startups owner phone number
        
        Keyword Arguments:
            password {STRING} -- a random password (default: {None})
            username {STRING} -- a random username (default: {None})
        
        Raises:
            ValueError: raise an error if user do not enter any phone number
        
        Returns:
            OBJECT -- returns created user
        """
        user = self.model(phone=phone)
        if not phone:
            raise ValueError('User must have phone')

        user.step = 'startup'
        user.username = username
        user.set_password(password)
        user.user_type = 'startup'
        user.save(using=self._db)

        return user


    def create_user(self, email, phone, password=None, **kwargs):
        """create and save a new user
        
        Arguments:
            email {STRING} -- an email value
            phone {STRING} -- a phone value
        
        Keyword Arguments:
            password {STRING} -- a password (default: {None})
        
        Raises:
            ValueError: raise an error if user don't enter an email
        
        Returns:
            OBJECT -- reutrns created user
        """
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email), phone=phone, **kwargs)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, phone, password=None):
        """Creates and saves a superuser with the given email, phone and password.
        
        Arguments:
            email {STRING} -- an email value
            phone {STRING} -- a phone value
        
        Keyword Arguments:
            password {STRING} -- a password (default: {None})
        
        Returns:
            OBJECT -- returns created user
        """
        user = self.create_user(
            email=email,
            phone=phone,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    """a custome user model that use phone number to login
    
    Arguments:
        AbstractBaseUser {CLASS} -- a django built-in class
    
    Returns:
        STRING -- returns user first_name last_name or phone number
    """

    id = models.AutoField(primary_key=True, editable=False, unique=True)

    username = models.CharField(
        max_length=150, unique=True, blank=True, null=True)
    first_name = models.CharField(max_length=120, blank=True)
    last_name = models.CharField(max_length=120, blank=True)
    email = models.EmailField(
        max_length=255, unique=False)
    phone_reg = RegexValidator(regex=r'[0][9][0-9]{9,9}$')
    phone = models.CharField(
        validators=[phone_reg],
        max_length=120,
        unique=True
    )
    avatar = models.ImageField(blank=True, null=True, upload_to='user/avatar/%Y-%m-%d')
    USER_TYPES = (
        ('startup', 'استارت اپ'),
        ('shetab', 'شتاب دهنده'),
        ('manager', 'مدیر'),
        ('karmand', 'کارمند'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPES, blank=True)
    user_type2 = models.CharField(
        max_length=10, choices=USER_TYPES, blank=True)
    STARTUP_STEPS = (
        ('register', 'آغاز ثبت نام'),
        ('verify', 'اعتبار سنجی'),
        ('startup', 'معرفی استارت اپ'),
        ('team', 'اطلاعات تیم'),
        ('upload', 'معرفی ویدئو'),
        ('presentation', 'پیج دک'),
        ('finish', 'تایید نهایی'),
    )
    step = models.CharField(
        max_length=15, choices=STARTUP_STEPS, default='register')

    role = models.ManyToManyField(
        Role, related_name='user', blank=True)
    category = models.ManyToManyField(
        Categories, related_name='user', blank=True)
    linkdin = models.CharField(max_length=120, blank=True, null=True)
    twitter = models.CharField(max_length=120, blank=True, null=True)
    instagram = models.CharField(max_length=120, blank=True, null=True)
    city = models.CharField(max_length=120, blank=True, null=True)
    site = models.URLField(max_length=120, blank=True, null=True)
    bio = models.TextField(max_length=255, blank=True, null=True)
    birth_date = models.DateField(max_length=100, blank=True, null=True)
    skill = models.CharField(max_length=200, blank=True, null=True)
    STUDIED = (
        ('diploma', 'دیپلم'),
        ('associate', 'کاردانی'),
        ('bachelor', 'کارشناسی'),
        ('master', 'کارشناسی ارشد'),
        ('phd', 'دکتری'),

    )
    grade = models.CharField(max_length=70, blank=True,
                             null=True, choices=STUDIED)
    multi = models.PositiveIntegerField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    # is_passed = models.BooleanField(default=True)
    add_to_mentors = models.BooleanField(default=False)
    mentor_user = models.BooleanField(default=False)
    sort = models.IntegerField(blank=True, null=True)
    is_compeleted = models.BooleanField(default=False)
    can_see = models.BooleanField(default=False)
    can_see_startups = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['email']

    def __str__(self):

        return f'{self.first_name} { self.last_name }' if self.first_name != '' or self.last_name != '' else f'{self.phone}'

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
