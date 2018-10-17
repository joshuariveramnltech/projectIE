from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import RegexValidator

# Create your models here.

GENDER_CHOICES = (('male', 'Male'), ('female', 'Female'))
ACCOUNT_TYPE_CHOICES = (
    ('---Select---', '---Select---'),
    ('Student', 'Student'), ('Faculty', 'Faculty'),
    ('Staff', 'Staff'), ('Administrator', 'Administrator')
)
SCHOLASTIC_STATUS_CHOICES = (('Regular', 'Regular'), ('Irregular', 'Irregular'))
YEAR_CHOICES = (
    ('1', '1'), ('2', '2'), ('3', '3'),
    ('4', '4'), ('5', '5')
)
SECTION_CHOICES = YEAR_CHOICES
CIVIL_STATUS_CHOICES = (('single', 'Single'), ('married', 'Married'))
JOB_STATUS = (('Full Time', 'Full Time'), ('Part Time', 'Part Time'))

COURSE_DESCRIPTION = (
    ('Bachelor of Science in Civil Engineering', 'Bachelor of Science in Civil Engineering'),
    ('Bachelor of Science in Computer Engineering', 'Bachelor of Science in Computer Engineering'),
    (
        'Bachelor of Science in Electronics and Communications Engineering',
        'Bachelor of Science in Electronics and Communications Engineering'
    ),
    ('Bachelor of Science in Electrical Engineering', 'Bachelor of Science in Electrical Engineering'),
    ('Bachelor of Science in Industrial Engineering', 'Bachelor of Science in Industrial Engineering'),
    ('Bachelor of Science in Mechanical Engineering', 'Bachelor of Science in Mechanical Engineering'),
)

COURSE_CODE_CHOICES = (
    ('BSCE', 'BSCE'), ('BSCOE', 'BSCOE'),
    ('BSECE', 'BSECE'), ('BSEE', 'BSEE'),
    ('BSIE', 'BSIE'), ('BSME', 'BSME')
)
SEMESTER_CHOICES = (
    ('First Semester', 'First Semester'),
    ('Second Semester', 'Second Semester'),
    ('Summer Semester', 'Summer Semester')
)

phone_regex = RegexValidator(regex="^\+63-\d{3}\-\d{4}\-\d{3}$", message="Format: +63-999-9999-999")


class UserManager(BaseUserManager):
    def create_user(
            self, username=None, email=None,
            first_name=None, last_name=None,
            middle_name='', password=None,
            is_active=True, is_staff=False,
            is_superuser=False
    ):
        if email is None:
            raise ValueError("Users must have an email address!")
        if username is None:
            raise ValueError("Users must have username!")
        if password is None:
            raise ValueError("Users must have a password!")
        if first_name is None:
            raise ValueError("Users must have a first name!")
        if last_name is None:
            raise ValueError("Users must have a last name!")
        if not is_staff and not is_superuser:
            raise ValueError("Users must have account type!")
        user = self.model(
            username=username,
            email=self.normalize_email(email),
            first_name=first_name.title(),
            last_name=last_name.title(),
            middle_name=middle_name.title(),
        )
        user.set_password(password)
        user.is_active = is_active
        user.is_staff = is_staff
        user.is_superuser = is_superuser
        user.save(using=self._db)
        return user

    def create_staffuser(self, username, email, first_name, last_name, password):
        user = self.create_user(
            username,
            email,
            first_name=first_name.title(),
            last_name=last_name.title(),
            password=password,
            is_staff=True
        )
        return user

    def create_superuser(self, username, email, first_name, last_name, password):
        user = self.create_user(
            username,
            email,
            first_name=first_name.title(),
            last_name=last_name.title(),
            password=password,
            is_staff=True,
            is_superuser=True
        )
        return user


class User(AbstractBaseUser):
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    birth_date = models.DateField(
        max_length=255, blank=True, null=True, verbose_name='Birth Day'
    )
    gender = models.CharField(
        max_length=25, blank=True, null=True, choices=GENDER_CHOICES, default='male')
    address = models.CharField(max_length=255, blank=True, default='')
    photo = models.ImageField(upload_to='user/profile/photo/%Y/%m/%d/', blank=True, null=True)
    phone_number = models.CharField(
        validators=[phone_regex, ],
        max_length=20,
        blank=True, default='',
        help_text="Please use the format: +63-XXX-XXXX-XXX"
    )
    is_active = models.BooleanField(default=True, verbose_name=u"Active")
    is_student = models.BooleanField(default=False, editable=False, verbose_name=u'Student')
    is_faculty = models.BooleanField(default=False, editable=False, verbose_name=u'Faculty')
    is_staff = models.BooleanField(default=False, verbose_name=u"Staff")
    is_superuser = models.BooleanField(default=False, verbose_name=u"Superuser")
    date_joined = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']

    objects = UserManager()

    class Meta:
        ordering = ['-date_joined', ]

    @property
    def get_full_name(self):
        if self.middle_name is not None:
            return "{} {} {}".format(
                self.first_name.title(),
                self.middle_name.title(),
                self.last_name.title()
            )
        return self.get_short_name

    @property
    def get_short_name(self):
        return "{} {}".format(self.first_name.title(), self.last_name.title())

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        self.__account_type = "Floating Account"
        if self.is_superuser:
            self.__account_type = 'Administrator'
        elif self.is_student:
            self.__account_type = 'Student'
        elif self.is_faculty:
            self.__account_type = 'Faculty'
        elif self.is_staff:
            self.__account_type = 'Staff'
        return self.get_full_name + " (" + self.__account_type + ")"


class Year(models.Model):
    course = course = models.CharField(max_length=25, choices=COURSE_CODE_CHOICES, default=4)
    year = models.CharField(max_length=10, choices=YEAR_CHOICES, default='1')

    class Meta:
        verbose_name_plural = 'Year Levels'
        unique_together = ('course', 'year')

    def __str__(self):
        return self.course + " " + self.year


class YearAndSection(models.Model):
    year = models.ForeignKey(Year, on_delete=models.DO_NOTHING, related_name='sections')
    section = models.CharField(max_length=10, choices=YEAR_CHOICES, default='1')

    class Meta:
        verbose_name_plural = 'Year and Section'
        unique_together = ('section', 'year')

    def __str__(self):
        return str(self.year) + "-" + self.section


class StudentProfile(models.Model):
    user = models.OneToOneField(User, related_name='student_profile', on_delete=models.CASCADE)
    course = models.CharField(max_length=25, choices=COURSE_CODE_CHOICES, null=True, blank=True, default='BSIE')
    course_description = models.CharField(
        max_length=100, choices=COURSE_DESCRIPTION, null=True, blank=True,
        default='Bachelor of Science in Industrial Engineering'
    )
    year_and_section = models.ForeignKey(YearAndSection, on_delete=models.SET_NULL, related_name='students', null=True)
    status = models.CharField(max_length=25, choices=SCHOLASTIC_STATUS_CHOICES, default='Regular')

    class Meta:
        verbose_name_plural = 'Student Profiles'

    def __str__(self):
        return self.user.get_full_name + " " + str(self.year_and_section)

    # def save(self, *args, **kwargs):
    #     super(StudentProfile, self).save(*args, **kwargs)


class FacultyProfile(models.Model):
    user = models.OneToOneField(User, related_name='faculty_profile', on_delete=models.CASCADE)
    civil_status = models.CharField(
        max_length=25, choices=CIVIL_STATUS_CHOICES, default='single')
    spouse = models.CharField(max_length=50, null=True,
                              blank=True, help_text="If Applicable", default='N/A')
    school_graduated = models.CharField(max_length=255, null=True, blank=True)
    major = models.CharField(max_length=255, null=True, blank=True)
    status = models.CharField(max_length=25, choices=JOB_STATUS, default='Full Time', null=True, blank=True)
    is_chairperson = models.BooleanField(default=False, verbose_name=u'Chairperson?')
    additional_information = models.TextField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Faculty Profiles'

    def __str__(self):
        return self.user.get_full_name


class StaffProfile(models.Model):
    user = models.OneToOneField(User, related_name='staff_profile', on_delete=models.CASCADE)
    civil_status = models.CharField(
        max_length=25, choices=CIVIL_STATUS_CHOICES, default='single')
    spouse = models.CharField(max_length=50, null=True,
                              blank=True, help_text="If Applicable", default='N/A')
    additional_information = models.TextField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Staff Profiles'

    def __str__(self):
        return self.user.get_full_name


@receiver(post_save, sender=User)
def create_dynamic_profile(sender, **kwargs):
    if kwargs['created']:
        if kwargs['instance'].is_student:
            StudentProfile.objects.create(user=kwargs['instance'])
        elif kwargs['instance'].is_faculty:
            FacultyProfile.objects.create(user=kwargs['instance'])
        elif kwargs['instance'].is_staff:
            StaffProfile.objects.create(user=kwargs['instance'])
