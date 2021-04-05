from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from phonenumber_field.modelfields import PhoneNumberField

# Custom account manager for custom user model.
class AccountManager(BaseUserManager):
    def create_user(self, name,phone_number, gender, city, profile_pic="", password = None):
        # import pdb; pdb.set_trace()
        if not name:
            raise ValueError('Name is required')
        if not phone_number:
            raise ValueError('Phone number is required')
        if not gender:
            raise ValueError('Gender is required')
        if not city:
            raise ValueError('City is required')
        # if not email:
        #     raise ValueError('Email is required')

        user = self.model(
			# email=self.normalize_email(email),
            name = name,
            phone_number=phone_number,
            gender= gender,
            city=city,
            profile_pic=profile_pic,
            # verified=verified,
		)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, phone_number, gender, city, password):
        user = self.create_user(
            # email=self.normalize_email(email),
            name=name,
            phone_number=phone_number,
            gender=gender,
            city=city,
            # profile_pic=profile_pic,
            password=password
        )
        user.verified = True
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# Creating custom user model
class Account(AbstractBaseUser):
    name                    = models.CharField(max_length=128)
    phone_number            = PhoneNumberField(verbose_name='phone number', unique=True)
    gender                  = models.CharField(verbose_name= 'gender', max_length=32)
    city                    = models.CharField(verbose_name= 'city', max_length=128)
    profile_pic             = models.ImageField(null = True, blank = True, upload_to='images/')
    # email                   = models.EmailField(verbose_name= 'email', max_length=60, unique= True)
    verified                = models.BooleanField(default=False)

    date_joined				= models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login				= models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin				= models.BooleanField(default=False)
    is_active				= models.BooleanField(default=True)
    is_staff				= models.BooleanField(default=False)
    is_superuser			= models.BooleanField(default=False)

    # Setting phone number as login field.
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = ['name', 'gender', 'city']
    
    objects = AccountManager()

    def __str__(self):
        return str(self.name) + ' | ' + str(self.phone_number)
       
    def has_perm(self, perm, obj = None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True