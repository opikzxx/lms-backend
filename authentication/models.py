from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid, datetime

# Create your models here.
class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email)
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.role = User.Role.SUPERUSER
        user.save(using=self._db)
        return user

class User(AbstractUser):
    class Gender(models.TextChoices):
        LAKILAKI = 'L', _('Laki-laki')
        PEREMPUAN = 'P', _('Perempuan')

    class AccountType(models.TextChoices):
        PRIBADI = 'PR', _('Pribadi')
        PERUSAHAAN = 'PE', _('Perusahaan')

    class AccountProvider(models.TextChoices):
        NORMAL = 'NO', _('Normal')
        GOOGLE = 'GO', _('Google')
        BOTH = 'BO', _('Both')

    class Role(models.TextChoices):
        ADMIN = 'AD', _('Admin')
        USER = 'US', _('User')
        SUPERUSER = 'SU', _('Superuser')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    email = models.CharField(max_length=128, unique=True, null=False)
    username = models.CharField(max_length=128, null=False)
    city = models.CharField(max_length=50, null=True)
    province = models.CharField(max_length=30, null=True)
    birth_date = models.DateField(default=datetime.date.today, null=False)
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        default=Gender.LAKILAKI,
        null=False
    )
    account_type = models.CharField(
        max_length=2,
        choices=AccountType.choices,
        default=AccountType.PRIBADI,
        null=False
    )
    profile_picture = models.CharField(max_length=255, null=True)
    phone_number = models.CharField(max_length=15, unique=True, null=False)
    google_id = models.CharField(max_length=50, null=True)
    is_verified = models.BooleanField(default=False, null=True)
    account_provider = models.CharField(
        max_length=2,
        choices=AccountProvider.choices,
        default=AccountProvider.NORMAL,
        null=True
    )
    role = models.CharField(
        max_length=2,
        choices=Role.choices,
        default=Role.USER,
        null=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = MyUserManager()
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'user'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
class CompanyAccount(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, null=False)
    name = models.CharField(max_length=64, null=False)
    address = models.CharField(max_length=255, null=True)

    class Meta:
        db_table = 'company_account'
        verbose_name = 'Company Account'
        verbose_name_plural = 'Company Accounts'

class PersonalAccount(models.Model):
    id = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True, null=False)
    occupancy = models.CharField(max_length=32, null=True)
    interest = models.CharField(max_length=32, null=True)
    motivation = models.TextField(null=True)

    class Meta:
        db_table = 'personal_account'
        verbose_name = 'Personal Account'
        verbose_name_plural = 'Personal Accounts'

class ResetPassword(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    status = models.BooleanField(default=False, null=True)
    # expiration_date = models.DateTimeField(datetime.datetime.now() + datetime.timedelta(minutes=30), null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'reset_password'
        verbose_name = 'Reset Password'
        verbose_name_plural = 'Reset Passwords'

class BlacklistedToken(models.Model):
    token = models.TextField()
    blacklisted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.token