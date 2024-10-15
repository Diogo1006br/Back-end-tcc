from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework.decorators import permission_classes, api_view
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from .serializers import LoginSerializer

class IsAuthenticatedView(APIView):
    """
    Verifica se o usuário está autenticado.
    """
    def get(self, request):
        if request.user.is_authenticated:
            return Response({'message': 'Usuário está autenticado'}, status=status.HTTP_200_OK)
        return Response({'message': 'Usuário não está autenticado'}, status=status.HTTP_401_UNAUTHORIZED)

class CurrentUserView(APIView):
    """
    Retorna informações do usuário logado.
    """
    def get(self, request):
        user = request.user
        return Response({
            "username": user.username,
            "email": user.email,
            "company": user.companyId
        })

@permission_classes([AllowAny])
class ObtainTokenView(APIView):
    """
    Gera e retorna os tokens de autenticação JWT.
    """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)

        response = Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_200_OK)

        # Cookies HttpOnly (modifique para produção)
        max_age = 3600 * 24 * 14  # duas semanas
        response.set_cookie('refresh_token', str(refresh), httponly=True, secure=True, max_age=max_age)
        response.set_cookie('access_token', str(refresh.access_token), httponly=True, secure=True, max_age=max_age)
        
        user.lastConnection = timezone.now()
        user.save(update_fields=['lastConnection'])
        return response

@permission_classes([AllowAny])
@method_decorator(csrf_exempt, name='dispatch')
class ObtainTokenViewMOBILE(APIView):
    """
    Gera tokens para mobile sem cookies.
    """
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_200_OK)

@permission_classes([AllowAny])
@method_decorator(csrf_exempt, name='dispatch')
class RefreshTokenViewMOBILE(APIView):
    """
    Atualiza o token de acesso para mobile.
    """
    def post(self, request):
        serializer = TokenRefreshSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'access': serializer.validated_data['access']}, status=status.HTTP_200_OK)

class LogoutView(APIView):
    """
    Realiza logout limpando os cookies de autenticação.
    """
    def get(self, request):
        response = Response({'message': 'Logout realizado com sucesso'})
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')
        return response
