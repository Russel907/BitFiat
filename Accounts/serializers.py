import re
from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from .models import UserProfile, KYC, Address, BankDetails, withdraw, Deposit



class UserSerializer(serializers.ModelSerializer):
    phone_number = serializers.CharField(source='username')  
    name = serializers.CharField(source='first_name')  

    class Meta:
        model = User
        fields = ['phone_number', 'name', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}  

    def validate_phone_number(self, value):
        phone_regex = r'^\+?\d{10,15}$'  
        if not re.match(phone_regex, value):
            raise serializers.ValidationError("Invalid phone number format. It should be 10-15 digits.")

        if User.objects.filter(username=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("This phone number is already registered.")
        
        return value
    

    def validate_email(self, value):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value):
            raise serializers.ValidationError("Invalid email format.")
        
        if User.objects.filter(email=value).exclude(pk=self.instance.pk if self.instance else None).exists():
            raise serializers.ValidationError("This email is already in use.")
        return value
    
     
class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer(required=True)
    referral_code = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'referral_code']


    def create(self, validated_data):
        print("validated_data:", validated_data)
        referral_code = validated_data.pop('referral_code', None)
        user_data = validated_data.pop('user', None)
        
        if not user_data:
            raise serializers.ValidationError({"user": "User data is required."})

        print("referral_code:", referral_code)

        referred_by_profile = None
        if referral_code:
            try:
                referred_by_profile = UserProfile.objects.get(referral_code=referral_code)
                referred_by_profile.increment_referred_count()
            except UserProfile.DoesNotExist:
                raise serializers.ValidationError({"referral_code": "Invalid referral code."})

        # Create the user instance properly
        user = User.objects.create_user(
            username=user_data['username'],  # Use phone_number instead of username
            email=user_data['email'],
            first_name=user_data['first_name'],
            password=user_data['password']
        )
    
        user_instance = User.objects.get(username=user_data['username'])  # Ensure it's a User instance
        print("user_error:",user_instance)
        user_profile = UserProfile.objects.create(user=user_instance, referred_by=referred_by_profile)
        
        return user_profile


class OtpVerificationSerializer(serializers.ModelSerializer):
    is_verified = serializers.BooleanField()

    class Meta:
        model = UserProfile
        fields = ['is_verified']

    def create(self, validated_data):
        is_verified = validated_data.get('is_verified')
        request = self.context.get('request')
        user = request.user
        try:
            userprofile = UserProfile.objects.get(user = user)
        except UserProfile.DoesNotExist:
            raise serializers.ValidationError("UserProfile profile not found for this user.")
        
        userprofile.is_verified = is_verified
        userprofile.save()

        return userprofile


class KYCPanSerializer(serializers.ModelSerializer):
    pan_number = serializers.CharField(max_length=10, min_length=10)

    class Meta:
        model = KYC
        fields = ['pan_number']

    def validate_pan_number(self, value):
        # PAN number validation (simple pattern: 5 letters, 4 digits, 1 letter)
        pan_pattern = r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$"
        if not re.match(pan_pattern, value):
            raise serializers.ValidationError("Invalid PAN number format. It should be in the format: ABCDE1234F")
        if KYC.objects.filter(pan_number=value).exists():
            raise serializers.ValidationError("This PAN Number is already in use.")
        return value
    
    def create(self, validated_data):
        pan_number = validated_data.get('pan_number')
        request = self.context.get('request')
        user = request.user

        kyc_pan = KYC.objects.create(
            user = user,
            pan_number = pan_number
        )

        return kyc_pan
    

class KYCImageSerializer(serializers.ModelSerializer):
    user_image = serializers.ImageField(required = True)

    class Meta:
        model = KYC
        fields = ['user_image']

    def create(self, validated_data):
        user_image = validated_data.get('user_image')
        request = self.context.get('request')
        user = request.user
        try:
            kyc = KYC.objects.get(user=user)
        except KYC.DoesNotExist:
            raise serializers.ValidationError("KYC profile not found for this user.")
        
        kyc.user_image = user_image
        kyc.save()

        return kyc


class PhoneNumberSerializer(serializers.Serializer):
    phone_number = serializers.CharField(max_length=15)

    def validate_phone_number(self, value):
        phone_regex = r'^\+?\d{10,15}$'  
        if not re.match(phone_regex, value):
            raise ValidationError("Invalid phone number format. It should be 10-15 digits.")

        if not  User.objects.filter(username=value).exists():
            raise ValidationError("This phone number is not registered.")
        
        return value


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError("The  passwords do not match.")
        return data
    

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ['house_flat_apartment','road_street','landmark','city','pincode', 'state', 'address_type']

    def validate_pincode(self, value):
        if not re.match(r'^\d{6}$', value): 
            raise serializers.ValidationError("Pincode must be exactly 6 digits.")
        return value
    
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        address = Address.objects.create(userprofile=user, **validated_data)
        return address
    

class BankDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankDetails
        fields = '__all__'


class WithdrawSerializer(serializers.ModelSerializer):
    class Meta:
        model = withdraw
        fields = ['wallet_address','amount','verification_code']

    def validate_wallet_address(self, value):
        if len(value) < 10 or len(value) > 255:
            raise serializers.ValidationError("Invalid wallet address length.")
        if not value.isalnum():
            raise serializers.ValidationError("Wallet address must be alphanumeric.")
        return value
        
    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        Withdraw = withdraw.objects.create(user_profile=user, **validated_data)
        return Withdraw


class DepositSerializer(serializers.ModelSerializer):
    class Meta:
        model = Deposit
        fields = ['network','amount']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        deposit = Deposit.objects.create(user_profile=user, **validated_data)
        return deposit
