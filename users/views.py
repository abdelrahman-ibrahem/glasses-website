import traceback
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework.authtoken.models import Token 
from rest_framework.decorators import api_view, permission_classes


@api_view(['POST'])
def sign_up(request):
    try:
        username = request.data.get('username')
        email = request.data.get('email')
        password = request.data.get('password')

        user = User(username=username, email=email)
        user.set_password(password)
        user.save()
        token = Token.objects.create(user=user)
        return Response({
            'pk': user.id,
            'username': user.username,
            'email': user.email,
            'token': str(token.key)
        }, status=status.HTTP_201_CREATED)
    except:
        print(traceback.formart_exc())
        return Response(status=status.HTTP_409_CONFLICT)


@api_view(['POST'])
def login_token(request):
    try:
        username = request.data.get('username')
        password = request.data.get('password')

        user = User.objects.get(username=username)
        if user.check_password(password):
            token = Token.objects.get(user=user)
            return Response({
                'pk': user.id,
                'username': user.username,
                'email': user.email,
                'token': str(token.key)
            }, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        print(traceback.format_exc())
        return Response({
            'message': 'Invalid credentials'
        }, status=status.HTTP_400_BAD_REQUEST)