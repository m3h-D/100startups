from django.db import models
from django.contrib.auth import get_user_model
from usercp.models import User
from usertracker.models import UserTracker
from category.models import Categories
from django.urls import reverse
from django.core.validators import RegexValidator
from django.contrib.contenttypes.fields import GenericRelation



class UserProfile(models.Model):
    """an additional table to store additional data for users with type of startup(the owner of startup)

    Arguments:
        models {MODULE} -- this module inharitanced from built-in Django Model

    Returns:
        STRING -- returns users phone
    """    
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    user = models.OneToOneField(
        User, related_name='userprofile', blank=True, on_delete=models.CASCADE)
    duration_per_month = models.PositiveIntegerField(blank=True, null=True)
    saham = models.PositiveSmallIntegerField(default=0)

    team_member = models.ManyToManyField(
        'TeamMember', related_name='userprofile', blank=True)
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)

    def __str__(self):
        try:
            return f'{self.user.phone}---{self.user.first_name}'
        except:
            return f'{self.user.phone}'


class ShetabDahande(models.Model):
    """a table to store data of Accelerators
       that the name namayande is a leader which been assigned to it 
       the user field is unusable for now...

    Arguments:
        models {MODULE} -- this module inharitanced from built-in Django Model
    """    
    # id = models.AutoField(primary_key=True, editable=False, unique=True)
    user = models.OneToOneField(
        User, related_name='shetabdahande', blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(blank=True, null=True, upload_to='accelerator/img/%Y-%m-%d')
    name_shtabdahande = models.CharField(
        max_length=120, blank=True, null=True)
    name_namayande = models.ForeignKey(
        User, related_name='namayande', blank=True, null=True, on_delete=models.SET_NULL)
    category = models.ManyToManyField(
        Categories, blank=True, related_name='shetabdahande')
    created_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ('-created_date',)



class StartUp(models.Model):
    """the startup that create by an user(specified with a ForeignKey)
       important fields:
       shetab_dahande if user choose an accelerator field of rahbar_asli will pupilate with name_namayandes accelerator (leader)
       rahbar recommended leader wich be selected or created by user at registeration process
       rahbar_asli wich will be selected by operational at inforamtion or accelerator
       status that is a choice field and will be change in every step of informaion process

    Arguments:
        models {MODULE} -- this module inharitanced from built-in Django Model

    Returns:
        STRING -- returns title, id, rahbar, is_not_presence_referee, is_leader, is_presence_referee, status, require_money
    """    
    id = models.AutoField(primary_key=True, unique=True)
    owner = models.OneToOneField(
        User, related_name='startup', blank=True, on_delete=models.CASCADE)
    shetab_dahande = models.ForeignKey(
        ShetabDahande, related_name='startup', blank=True, null=True, on_delete=models.SET_NULL)
    shetab_shude = models.BooleanField(default=False)
    rahbar = models.ForeignKey(
        User, related_name='startupleader', blank=True, null=True, on_delete=models.SET_NULL)
    rahbar_asli = models.ForeignKey(
        User, related_name='startupleaderasli', blank=True, null=True, on_delete=models.SET_NULL)
    image = models.ImageField(blank=True, null=True, upload_to='startup/img/%Y-%m-%d')
    title = models.CharField(max_length=120)
    site = models.URLField(blank=True, null=True)
    province_startup = models.CharField(max_length=120, blank=True, null=True)
    city_startup = models.CharField(max_length=120, blank=True, null=True)
    start_date = models.DateTimeField(blank=True, null=True)
    SAMPLE_CREATED = (
        ('yes', 'بله'),
        ('no', 'خیر'),
    )
    investment = models.CharField(max_length=3, choices=SAMPLE_CREATED)
    prototype = models.CharField(max_length=3, choices=SAMPLE_CREATED)
    STARTUP_REGISTER_STATUS = (
        ('not_complete', 'عدم تکمیل اطلاعات'),
        ('suspended', 'معلق'),
        ('pending', 'تکمیل اطلاعات'),
        ('editing', 'اصلاح شده'),
        ('accepted_document', 'تایید مدارک'),
        ('failed_document', 'عدم تایید مدارک'),
        ('accepted', 'تایید طرح'),
        ('failed', 'در انتظار ویرایش'),
        ('select_leader', 'انتخاب راهبر'),
        ('select_not_presence_referees', 'انتخاب داوری غیرحضوری'),
        ('accepted_not_presence', 'پذیرش داوری غیرحضوری'),
        ('failed_not_presence', 'عدم داوری غیرحضوری'),
        ('select_presence_referee', 'انتخاب داوران حضوری'),
        ('accepted_presence', 'تایید داوری حضوری'),
        ('failed_presence', 'رد داوری حضوری'),
        ('add_investor', 'پنل سرمایه گذار'),
    )
    status = models.CharField(
        max_length=30, choices=STARTUP_REGISTER_STATUS, default='not_complete')
    old_status = models.CharField(
        max_length=30, choices=STARTUP_REGISTER_STATUS, default='not_complete')
    is_leader = models.BooleanField(default=False)
    is_presence_referee = models.BooleanField(default=False)
    is_not_presence_referee = models.BooleanField(default=False)
    selected = models.BooleanField(default=False)
    credit = models.PositiveIntegerField(blank=True, null=True)
    category = models.ManyToManyField(
        Categories, related_name='startup', blank=True)

    video = models.FileField(blank=True)

    require_money = models.PositiveIntegerField(blank=True, null=True)
    attachfile_e = models.FileField(blank=True, null=True)
    attachfile_p = models.FileField(blank=True, null=True)

    explain_startup = models.CharField(max_length=70, blank=True, null=True)
    about_start = models.TextField(max_length=255, blank=True, null=True)
    problem = models.TextField(max_length=255, blank=True, null=True)
    mysolution = models.TextField(max_length=255, blank=True, null=True)
    solution = models.TextField(max_length=255, blank=True, null=True)
    market_size = models.TextField(max_length=255, blank=True, null=True)
    defect = models.TextField(max_length=255, blank=True, null=True)

    how_mem_meet = models.TextField(blank=True, null=True)
    what_m_better = models.TextField(blank=True, null=True)
    what_u_need = models.TextField(blank=True, null=True)
    who_sent_you = models.TextField(blank=True, null=True)

    usertracker = GenericRelation(UserTracker, related_name='startup')

    created_date = models.DateTimeField(
       auto_now_add=True)

    def __str__(self):
        return f"{self.title} {self.id} {self.rahbar} {self.is_not_presence_referee} {self.is_leader} {self.is_presence_referee} {self.status} {self.require_money}"

    def get_absolute_url(self):
        return reverse('startup:information', args=(self.pk,))


class TeamMember(models.Model):
    """team member of a startup with some informaions of them
       that will be added to the UserProfile of the creator of startup
       the user field is unusable for now...

    Arguments:
        models {MODULE} -- this module inharitanced from built-in Django Model

    Returns:
        STRING -- returns first_name last_name and linkedin of them to admin panel
    """
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(
        User, related_name='teammember', blank=True, null=True, on_delete=models.SET_NULL)
    startup = models.ForeignKey(
        StartUp, null=True, related_name='teammember', blank=True, on_delete=models.SET_NULL)
    t_first_name = models.CharField(max_length=120)
    phone_reg = RegexValidator(regex=r'[0][9][0-9]{9,9}$')
    t_phone = models.CharField(
        validators=[phone_reg],
        max_length=11,
        blank=True,
        null=True,
    )
    t_last_name = models.CharField(max_length=120, null=True)
    t_email = models.EmailField(blank=True, null=True)
    t_linkdin = models.CharField(max_length=120, blank=True, null=True)
    t_birth_date = models.DateField(blank=True, null=True)
    t_skill = models.CharField(max_length=200)
    STUDIED = (
        ('diploma', 'دیپلم'),
        ('associate', 'کاردانی'),
        ('bachelor', 'کارشناسی'),
        ('master', 'کارشناسی ارشد'),
        ('phd', 'دکتری'),

    )
    tgrade = models.CharField(
        max_length=70, blank=True, null=True, choices=STUDIED)
    t_avatar = models.ImageField(blank=True, null=True)
    t_role_in_startup = models.CharField(max_length=120, blank=True, null=True)
    t_the_role = models.CharField(max_length=120, blank=True, null=True)
    t_duration_per_month = models.PositiveIntegerField(blank=True, null=True)
    t_saham = models.PositiveSmallIntegerField(blank=True, null=True)
    t_cv = models.FileField(blank=True, null=True)
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f'{self.t_first_name} {self.t_last_name} {self.t_linkdin}'


class Referee(models.Model):
    """this table will be created when operational select a referee for a startup at inforamtion stage
       after that the scores given by referees will be stored in a BinaryField

    Arguments:
        models {MODULE} -- this module inharitanced from built-in Django Model

    Returns:
        STRING -- returns first_name, the_type, total_score, startup to admin panel
    """    
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(
        User, related_name='referee', on_delete=models.CASCADE)
    startup = models.ForeignKey(
        StartUp, related_name='referee', blank=True, null=True, on_delete=models.CASCADE)
    score_comment = models.TextField(blank=True, null=True)
    nomre = models.BinaryField(blank=True, null=True)
    is_accepted = models.BooleanField(default=False)
    THE_TYPE = (
        ('pres', 'حضوری'),
        ('not_pres', 'غیر حضوری'),
    )
    the_type = models.CharField(
        max_length=9, choices=THE_TYPE, blank=True, null=True)
    lead = models.BooleanField(default=False)
    invest = models.BooleanField(default=False)
    scored = models.BooleanField(default=False)
    total_score = models.DecimalField(
        max_digits=6, decimal_places=1, blank=True, null=True)
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.first_name} {self.the_type} -- {self.total_score} {self.startup}"


class Requests(models.Model):
    """requests of money will be stored in this table. assign to requested user and startup that is defined

    Arguments:
        models {MODULE} -- this module inharitanced from built-in Django Model
    """    
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='requests')
    startup = models.ForeignKey(
        StartUp, on_delete=models.CASCADE, related_name='requests')
    request_title = models.CharField(max_length=120, blank=True, null=True)
    request_money = models.PositiveIntegerField(default=0, blank=True, null=True)
    THE_STATUS = (
        ('waiting', 'در انتظار'),
        ('accepted_leader', 'تایید شده راهبر'),
        ('failed_leader', 'تایید نشده راهبر'),
        ('accepted_investor', 'تایید شده مالی'),
        ('failed_investor', 'تایید نشده مالی'),
        ('accept_document', 'تایید شده اسناد'),
        ('failed_document', 'تایید نشده اسناد'),
    )
    status = models.CharField(
        max_length=50, choices=THE_STATUS, blank=True, null=True)
    THE_PEOPLE = (
        ('support', 'پشتیبانی'),
        ('human', 'نیروی انسانی'),
        ('bazzar', 'بازاریابی'),
        ('prototype_money', 'هزینه نمونه های اولیه'),
    )
    request_cat = models.CharField(max_length=20, choices=THE_PEOPLE, blank=True, null=True)
    request_expression = models.TextField(blank=True, null=True)
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)
    leader_comment = models.TextField(blank=True, null=True)
    leader_agree = models.BooleanField(default=False)
    investor_agree = models.BooleanField(default=False)
    investor_comment = models.TextField(blank=True, null=True)

    class Meta:
        ordering = ('-created_date',)


class Investors(models.Model):
    """when a user with role of investor accpet of a meeting with a startup that has the status of add_investor
       this table will be created 

    Arguments:
        models {MODULE} -- this module inharitanced from built-in Django Model

    Returns:
        STRING -- returns user and startup title and status of if he/she wants to meet or not
    """    
    from theevent.models import CreateEvent
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    user = models.ForeignKey(
        User, related_name='investor', on_delete=models.CASCADE)
    startup = models.ForeignKey(
        StartUp, related_name='investor', blank=True, null=True, on_delete=models.CASCADE)
    THE_STATUS = (
        (1, 'iwant'),
        (0, 'idontwant'),
    )
    status = models.IntegerField(choices=THE_STATUS, default=0)
    create_event = GenericRelation(CreateEvent, related_query_name='investors')
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user} {self.startup.title} {self.get_status_display()}"


class StartupComments(models.Model):
    """all the comments of operational user and if he/she accepted or decliened satrtup in 
       any step on inforamion page will be stored here

    Arguments:
        models {MODULE} -- this module inharitanced from built-in Django Model

    Returns:
        STRING -- returns startup title
    """    
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    startup = models.OneToOneField(
        StartUp, related_name='startupcomment', on_delete=models.CASCADE)
    THE_STATUS = (
        ('accepted', 'تایید'),
        ('failed', 'رد'),
    )
    doc_stat = models.TextField(max_length=255, blank=True, null=True)
    doc_stat_status = models.CharField(
        max_length=8, choices=THE_STATUS, blank=True)
    startup_stat = models.TextField(max_length=255, blank=True, null=True)
    startup_stat_status = models.CharField(
        max_length=8, choices=THE_STATUS, blank=True)
    no_referee_stat = models.TextField(max_length=255, blank=True, null=True)
    no_referee_stat_status = models.CharField(
        max_length=8, choices=THE_STATUS, blank=True)
    referee_stat = models.TextField(max_length=255, blank=True, null=True)
    referee_stat_status = models.CharField(
        max_length=8, choices=THE_STATUS, blank=True)
    created_date = models.DateTimeField(
        auto_now_add=True, blank=True, null=True)

    def __str__(self):
        return f"{self.startup.title}"



class CreditAssigned(models.Model):
    user = models.ManyToManyField(User, related_name='creditassigned', blank=True)
    startup = models.ForeignKey(StartUp, related_name='creditassigned', on_delete=models.CASCADE)
    date = models.DateTimeField(blank=True, null=True)
    credit = models.IntegerField(blank=True, null=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} -- {self.credit} -- {self.startup}"