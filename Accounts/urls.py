from django.urls import path
from .views import UserProfileCreateAPIView, LoginAPIView, OtpVerificationAPIView, KYCPanAPIView, KYCImageAPIView, PhoneNumbrAPIView, PasswordAPIView, AddressAPIView, FetchBankDetailsAPIView, WithdrawAPIView, DepositAPIView, TotalAPIView, EditProfileAPIView


urlpatterns = [ 
    path('sign-up/', UserProfileCreateAPIView.as_view(), name="sign-up"),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('otp-verification/', OtpVerificationAPIView.as_view(), name='otp-verification'),
    path('kyc-pan/', KYCPanAPIView.as_view(), name='kyc-pan'),
    path('kyc-img/', KYCImageAPIView.as_view(), name='kyc-img'),
    path('forgot-password/', PhoneNumbrAPIView.as_view(), name='forgot-password'),
    path('update-password/', PasswordAPIView.as_view(), name='update-password'),
    path('edit-profile/', EditProfileAPIView.as_view(), name='edit-profile'),
    path('address/', AddressAPIView.as_view(), name='address'),
    path('fetch-bank-details/', FetchBankDetailsAPIView.as_view(), name='fetch-bank-details'),
    path('withdraw/',WithdrawAPIView.as_view(), name='withdraw' ),
    path('deposit/', DepositAPIView.as_view(), name="deposit"),
    path('total/', TotalAPIView.as_view(), name="total")
]

# 37778eabdd57b5861b152156fe12df75f09ce1f8