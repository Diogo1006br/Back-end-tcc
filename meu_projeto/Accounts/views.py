from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate

from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.throttling import AnonRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .API.serializers import LoginSerializer

from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.utils import timezone




class IsAutenticatedView(APIView):
 

    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return Response({'message': 'Usuário está autenticado'}, status=status.HTTP_200_OK)
        else:
            return Response({'message': 'Usuário não está autenticado'}, status=status.HTTP_401_UNAUTHORIZED)

class CurrentUserView(APIView):
  
    def get(self, request):
     
        user = request.user
        
        return Response({
            "username": user.username,
            "email": user.email,
            "company":user.companyId

        })
    


from rest_framework.decorators import api_view

@permission_classes([AllowAny])
class ObtainTokenView(APIView):
    def post(self, request, *args, **kwargs):
        request.skip_middleware = True
        
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            user = data['user']
            refresh = RefreshToken.for_user(user)

            res = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            response = Response('sucess', status=status.HTTP_200_OK)

            # Definir o token de acesso e o token de atualização como cookies HttpOnly
            max_age = 3600 * 24 * 14  # duas semanas

            #trocar o valor de scure para True quando for para produção
            #trocar o valor de samesite para 'None' quando for para produção
            response.set_cookie(key='refresh_token', value=str(refresh), httponly=True, samesite='None', secure=True, max_age=max_age)
            response.set_cookie(key='access_token', value=str(refresh.access_token), httponly=True, samesite='None', secure=True, max_age=max_age)
            user.lastConnection = timezone.now()
            user.save(update_fields=['lastConnection'])
            return response
        except ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Erro desconhecido: {e}")
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@permission_classes([AllowAny])
@method_decorator(csrf_exempt, name='dispatch')
class ObtainTokenViewMOBILE(APIView):
    def post(self, request, *args, **kwargs):
        
        try:
            serializer = LoginSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            data = serializer.validated_data
            user = data['user']
            refresh = RefreshToken.for_user(user)

            res = {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }

            return Response(res, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Erro desconhecido: {e}")
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
@permission_classes([AllowAny])
@method_decorator(csrf_exempt, name='dispatch')     
class RefreshTokenViewMOBILE(APIView):
    """
    View to refresh the access token using a refresh token.
    """
    def post(self, request, *args, **kwargs):
        serializer = TokenRefreshSerializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            access = serializer.validated_data['access']
            return Response({'access': access}, status=status.HTTP_200_OK)
        except TokenError as e:
            return Response({"detail": e.args[0]}, status=status.HTTP_401_UNAUTHORIZED)
        except ValidationError as e:
            return Response({"detail": e.detail}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Erro desconhecido: {e}")
            return Response({"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class CookieTokenRefreshSerializer(TokenRefreshSerializer):
    refresh = None

    def validate(self, attrs):
        attrs['refresh'] = self.context['request'].COOKIES.get('refresh_token')
        if attrs['refresh']:
            return super().validate(attrs)
        else:
            raise TokenError('No valid refresh token found in cookie')
class LogoutView(APIView):
    def get(self, request):
        response = Response()
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')
        return response

class CookieTokenRefreshView(TokenRefreshView):
    serializer_class = CookieTokenRefreshSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            response.set_cookie('access_token', response.data['access'])
        return response
            