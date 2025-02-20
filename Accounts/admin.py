from django.contrib import admin
from .models import UserProfile, KYC, Address, BankDetails, withdraw, Deposit



admin.site.register(UserProfile)
admin.site.register(KYC)
admin.site.register(Address)
admin.site.register(BankDetails)
admin.site.register(withdraw)
admin.site.register(Deposit)


