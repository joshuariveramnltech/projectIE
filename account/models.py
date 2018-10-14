from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


# Create your models here.


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
    GENDER_CHOICES = (('male', 'Male'), ('female', 'Female'))
    username = models.CharField(max_length=25, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, null=True)
    last_name = models.CharField(max_length=255, null=True)
    middle_name = models.CharField(max_length=255, null=True, blank=True)
    birthday = models.DateField(
        max_length=255, blank=True, null=True,
    )
    gender = models.CharField(
        max_length=25, blank=True, null=True, choices=GENDER_CHOICES, default='male')
    address = models.CharField(max_length=255, blank=True, default='')
    is_active = models.BooleanField(default=True, verbose_name=u"Active")
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
        else:
            return self.get_short_name

    @property
    def get_short_name(self):
        return "{} {}".format(self.first_name.title(), self.last_name.title())

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def __str__(self):
        return self.get_full_name
