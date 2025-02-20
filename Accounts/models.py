import uuid
from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    referral_code = models.CharField(max_length=10, unique=True, blank=True, null=True)
    referred_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True, related_name='referred_users')
    referred_count = models.IntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def save(self, *args, **kwargs):
        if not self.referral_code:
            self.referral_code = str(uuid.uuid4().hex[:10]) 
        super().save(*args, **kwargs)

    def increment_referred_count(self):
        self.referred_count += 1
        self.save()

    def __str__(self):
        return self.user.username
    

class KYC(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="kyc_details")
    pan_number = models.CharField(max_length=10, unique=True)
    user_image = models.ImageField(upload_to='user_images/', null=True, blank=True)
    
    def __str__(self):
        return f"KYC details for {self.user.username}"

    def get_document_name(self):
        return f"kyc_{self.user.username}.jpg"


STATE_CHOICES = [
    ('andhra pradesh', 'Andhra Pradesh'),
    ('arunachal pradesh', 'Arunachal Pradesh'),
    ('assam', 'Assam'),
    ('bihar', 'Bihar'),
    ('chhattisgarh', 'Chhattisgarh'),
    ('goa', 'Goa'),
    ('gujarat', 'Gujarat'),
    ('haryana', 'Haryana'),
    ('himachal pradesh', 'Himachal Pradesh'),
    ('jharkhand', 'Jharkhand'),
    ('karnataka', 'Karnataka'),
    ('kerala', 'Kerala'),
    ('madhya pradesh', 'Madhya Pradesh'),
    ('maharashtra', 'Maharashtra'),
    ('manipur', 'Manipur'),
    ('meghalaya', 'Meghalaya'),
    ('mizoram', 'Mizoram'),
    ('nagaland', 'Nagaland'),
    ('odisha', 'Odisha'),
    ('punjab', 'Punjab'),
    ('rajasthan', 'Rajasthan'),
    ('sikkim', 'Sikkim'),
    ('tamil nadu', 'Tamil Nadu'),
    ('telangana', 'Telangana'),
    ('tripura', 'Tripura'),
    ('uttar pradesh', 'Uttar Pradesh'),
    ('uttarakhand', 'Uttarakhand'),
    ('west bengal', 'West Bengal'),
    ('andaman and nicobar islands', 'Andaman and Nicobar Islands'),
    ('chandigarh', 'Chandigarh'),
    ('dadra and nagar haveli and daman and diu', 'Dadra and Nagar Haveli and Daman and Diu'),
    ('lakshadweep', 'Lakshadweep'),
    ('delhi', 'Delhi'),
    ('puducherry', 'Puducherry'),
    ('jammu & kashmir', 'Jammu & Kashmir'),
    ('ladakh', 'Ladakh')
]


class Address(models.Model):
    userprofile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='addresses')
    house_flat_apartment = models.CharField(max_length=255)
    road_street = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100)
    pincode = models.CharField(max_length=10)
    state = models.CharField(max_length=100, choices=STATE_CHOICES)
    address_type = models.CharField(
        max_length=10,
        choices=[('home', 'Home'), ('work', 'Work'), ('other', 'Other')],
        default='home',
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.house_flat_apartment}-{self.address_type}"


class BankDetails(models.Model):
    user_profile = models.OneToOneField(User, on_delete=models.CASCADE, related_name='bank_details')
    name = models.CharField(max_length=255) 
    vpa = models.CharField(max_length=255, unique=True)  
    merchant_ifsc = models.CharField(max_length=20) 
    tpap = models.JSONField() 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} - {self.vpa}"
    

class withdraw(models.Model):
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='withdraw')
    wallet_address = models.CharField(max_length=255, unique=False)
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    verification_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Withdrawal {self.id} - {self.wallet_address} - {self.amount}"


class Deposit(models.Model):
    user_profile = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Deposit')
    amount = models.DecimalField(max_digits=20, decimal_places=8)
    network = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.amount} via {self.network}"

    