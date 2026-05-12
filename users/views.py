from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from .models import CustomUser
from .serializers import UserSerializer
import random


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    # ========================
    # SIGNUP / CREATE USER
    # ========================
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user.verification_code = ''.join(random.choices("0123456789", k=6))
            user.email_verified = False
            user.save()
            print(f"OTP for {user.email}: {user.verification_code}")
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # ========================
    # LOGIN — returns token
    # ========================
    @action(detail=False, methods=['post'], url_path='login')
    def login_user(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        if not email or not password:
            return Response({'error': 'Email and password required'}, status=400)
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        if not user.email_verified:
            return Response({'error': 'Email not verified. Please verify your email first.'}, status=400)
        if not user.check_password(password):
            return Response({'error': 'Incorrect password'}, status=400)
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'status': 'success',
            'token': token.key,
            'user': UserSerializer(user).data
        }, status=200)

    # ========================
    # VERIFY OTP
    # ========================
    @action(detail=False, methods=['post'], url_path='verify')
    def verify_user(self, request):
        email = request.data.get('email')
        code = request.data.get('code')
        if not email or not code:
            return Response({'error': 'Email and code required'}, status=400)
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        if user.verification_code == code:
            user.email_verified = True
            user.verification_code = None
            user.save()
            return Response({'status': 'verified'}, status=200)
        return Response({'error': 'Invalid OTP'}, status=400)

    # ========================
    # RESEND OTP
    # ========================
    @action(detail=False, methods=['post'], url_path='resend-otp')
    def resend_otp(self, request):
        email = request.data.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=400)
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User not found'}, status=404)
        user.verification_code = ''.join(random.choices("0123456789", k=6))
        user.email_verified = False
        user.save()
        print(f"Resent OTP for {user.email}: {user.verification_code}")
        return Response({'status': 'otp_sent'}, status=200)

    # ========================
    # GET MY PROFILE
    # ========================
    @action(detail=False, methods=['get'], url_path='me',
            authentication_classes=[TokenAuthentication],
            permission_classes=[IsAuthenticated])
    def me(self, request):
        return Response(UserSerializer(request.user).data)

    # ========================
    # UPDATE PROFILE (name, phone)
    # ========================
    @action(detail=False, methods=['patch'], url_path='update-profile',
            authentication_classes=[TokenAuthentication],
            permission_classes=[IsAuthenticated])
    def update_profile(self, request):
        user = request.user
        allowed = ['full_name', 'phone', 'username']
        for field in allowed:
            if field in request.data:
                setattr(user, field, request.data[field])
        user.save()
        return Response(UserSerializer(user).data)

    # ========================
    # UPLOAD PROFILE IMAGE
    # ========================
    @action(detail=False, methods=['post'], url_path='upload-photo',
            authentication_classes=[TokenAuthentication],
            permission_classes=[IsAuthenticated])
    def upload_photo(self, request):
        user = request.user
        if 'profile_image' not in request.FILES:
            return Response({'error': 'No image provided.'}, status=400)
        user.profile_image = request.FILES['profile_image']
        user.save()
        return Response({
            'status': 'uploaded',
            'profile_image': request.build_absolute_uri(user.profile_image.url)
        })
