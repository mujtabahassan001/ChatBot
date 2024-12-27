from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db import models
from django.conf import settings
from twilio.rest import Client

class ChatMessage(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}: {self.message[:50]}"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):

        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser):

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = [] 

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser

    @property
    def is_authenticated(self):

        return True



#################   TWILIO PHONE NUMBER VERIFICATION ###################


class Score(models.Model):
    score = models.PositiveIntegerField()

    def __str__(self):
        return str(self.score)

    def save(self, *args, **kwargs):
        if self.score < 60:
            account_sid = 'ACc5ca92d65de09866083afb033173ae4d'
            auth_token = '22f7469c7a025b71caae8100332aeec3'
            client = Client(account_sid, auth_token)
            twilio_phone_number = '+12314224251'
            message = client.messages.create(
                from_= twilio_phone_number,
                body='Hi Whatsup. This is Twilio',
                to='+923499691406'
            )
            print(message.sid)
            
        super().save(*args, **kwargs)
        if self.score < 40:
            account_sid = 'ACc5ca92d65de09866083afb033173ae4d'
            auth_token = '22f7469c7a025b71caae8100332aeec3'
            client = Client(account_sid, auth_token)

            to_phone_number = '+923499691406'  

            try:
                verification = client.verify \
                    .v2 \
                    .services('VA5cc2e2bfe68041154494af4dccf70205') \
                    .verifications \
                    .create(to=to_phone_number, channel='sms')

                print(f"OTP sent: {verification.status}")

            except Exception as e:
                print(f"Error sending OTP: {e}")

        super().save(*args, **kwargs)