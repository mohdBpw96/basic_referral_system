from django.db import models 
from django.contrib.auth import get_user_model


# Create your models here.

class ReferralCodes(models.Model):
    id = models.AutoField(null=False, primary_key=True)

    # Setting a foreign key field, using OneToOneField because a user can have only a single referral code
    user_id = models.OneToOneField(get_user_model(), unique=True ,on_delete=models.CASCADE)
    referral_code = models.CharField(null=False, max_length=8, unique=True)

    total_referrals = models.PositiveIntegerField(null=False, default=0)


    # This will show the username in the django admin app
    def __str__(self) -> str:
        return str(self.user_id)


