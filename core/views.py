from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.core.mail import send_mail
from django.conf import settings
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserProfileSerializer
from .permissions import IsAdminOrModerator


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    
    if not username or not email or not password:
        return Response({'error': 'Please provide username, email, and password'}, status=status.HTTP_400_BAD_REQUEST)
    
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = User.objects.create_user(username=username, email=email, password=password)
    user.is_active = False
    user.save()
    
    # Generate verification token
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    verification_link = f"{settings.SITE_URL}/verify-email/{uid}/{token}/"
    
    # Send verification email
    subject = 'Verify your EcoSphere account'
    message = f'Please click the following link to verify your account: {verification_link}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)
    
    return Response({'message': 'User registered successfully. Please check your email to verify your account.'}, status=status.HTTP_201_CREATED)

@api_view(['GET'])
@permission_classes([AllowAny])
def verify_email(request, uidb64, token):
    try:
        uid = str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        return Response({'message': 'Email verified successfully. You can now log in.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid verification link'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    
    user = authenticate(username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    
@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_request(request):
    email = request.data.get('email')
    if not email:
        return Response({'error': 'Please provide an email address'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'message': 'If a user with this email exists, a password reset link has been sent.'}, status=status.HTTP_200_OK)
    
    # Generate password reset token
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    reset_link = f"{settings.SITE_URL}/reset-password/{uid}/{token}/"
    
    # Send password reset email
    subject = 'Reset your EcoSphere password'
    message = f'Please click the following link to reset your password: {reset_link}'
    from_email = settings.DEFAULT_FROM_EMAIL
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)
    
    return Response({'message': 'If a user with this email exists, a password reset link has been sent.'}, status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([AllowAny])
def password_reset_confirm(request, uidb64, token):
    try:
        uid = str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    
    if user is not None and default_token_generator.check_token(user, token):
        new_password = request.data.get('new_password')
        if not new_password:
            return Response({'error': 'Please provide a new password'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password reset successful. You can now log in with your new password.'}, status=status.HTTP_200_OK)
    else:
        return Response({'error': 'Invalid password reset link'}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT'])
@permission_classes([IsAuthenticated])
def user_profile(request):
    if request.method == 'GET':
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = UserProfileSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsAdminOrModerator])
def admin_dashboard(request):
    # This view is only accessible to users in the Admin or Moderator groups
    return Response({'message': 'Welcome to the admin dashboard'})