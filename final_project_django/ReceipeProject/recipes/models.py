from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, email, name, mobile, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
            name=name,
            mobile=mobile,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, mobile, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_superuser', True)  # Set is_superuser
        user = self.create_user(email, name, mobile, password)
        user.role = 'admin'
        user.is_staff = extra_fields.get('is_staff')
        user.is_active = extra_fields.get('is_active')
        user.is_admin = extra_fields.get('is_admin')
        user.is_superuser = extra_fields.get('is_superuser')
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=255)
    mobile = models.CharField(max_length=15)
    role = models.CharField(max_length=10, default='user')
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)  # Ensure is_superuser is present

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'mobile']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        """Grant all permissions to superusers or admin users."""
        return self.is_superuser or self.is_admin

    def has_module_perms(self, app_label):
        """Grant module permissions to superusers or admin users."""
        return self.is_superuser or self.is_admin

class Recipe(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    ingredients = models.TextField()
    instructions = models.TextField()
    youtube_link = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=50)
    occasion = models.CharField(max_length=50, blank=True, null=True)
    
    image_filename = models.CharField(max_length=100, blank=True, null=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes')
    wishlist = models.ManyToManyField(User, related_name='wishlist', blank=True)
    is_vegetarian = models.BooleanField(default=False)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return self.title

class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    feedback = models.TextField()

    def __str__(self):
        return self.name