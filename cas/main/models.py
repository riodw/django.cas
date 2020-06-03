import uuid
import random
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.utils import timezone

def keyGen(num):
    d = str(uuid.uuid4())
    return d.replace('-','')[0:num]

def gen_token():
    chars = 'abcdefghkmnopqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789'
    temp_pass = ''
    for i in range(3):
        temp_pass = temp_pass.join(random.sample(chars,4))
    print(temp_pass)
    return temp_pass

class UserModelManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given username, email and password.
        """
        now = timezone.now()
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            last_login=now, date_joined=now, **extra_fields)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        u = self.create_user(email, password, **extra_fields)
        # u.is_staff = True
        u.is_active = True
        u.is_superuser = True
        u.is_admin = True
        u.save(using=self._db)
        return u


class User(AbstractBaseUser):
    # Standard fields
    id = models.CharField(primary_key=True, max_length=32, editable=False, unique=True, default=keyGen(7))

    first_name = models.CharField(blank=True, default='', max_length=254)
    middle_name = models.CharField(blank=True, default='', max_length=254)
    last_name = models.CharField(blank=True, default='', max_length=254)
    email = models.CharField(max_length=254, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    # is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # Extra fields
    phone_number = models.CharField(blank=True, default='', max_length=20)
    institution = models.CharField(blank=True, default='', max_length=254)

    objects = UserModelManager()

    USERNAME_FIELD = 'email'

    def __str__(self):
        return self.email

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

    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = '%s %s' % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class NoPasswordWaitingForEmailConfirm(models.Model):
    key = models.CharField(max_length=255, editable=False, unique=True, default=gen_token)
    email = models.EmailField()
    cookie = models.CharField(max_length=25, editable=False, unique=True, default=keyGen(20))
    browser = models.CharField(max_length=255, blank=True, default='')
    url = models.TextField(max_length=255, unique=False, editable=True, blank=True, default='')
    date_time = models.DateTimeField(auto_now_add=True)
    email_sent = models.BooleanField(default=False)
    user = models.OneToOneField(User, db_column='user', null=True, on_delete=models.CASCADE, default=None, related_name='email_confirm')


class UserCookie(models.Model):
    user = models.OneToOneField(User, primary_key=True, db_column='user', on_delete=models.CASCADE, related_name='user_cookie')
    cookie = models.CharField(max_length=25, editable=False)