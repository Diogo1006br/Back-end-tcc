# Código no arquivo urls.py

from django.contrib import admin
from django.urls import path, include
from Accounts.views import (
    IsAutenticatedView, CurrentUserView, ObtainTokenView, CookieTokenRefreshView,
    ObtainTokenViewMOBILE, RefreshTokenViewMOBILE, LogoutView
)
from rest_framework import routers
from Projects.API.viewsets import ProjectViewSet
from Accounts.API.viewsets import CompanyViewSet, UserViewSet, ReturnLogedUser, PasswordViewSet
from Forms.API.viewsets import FormsViewSet, Form_ResponseViewSet, DropBoxAnswerListViewSet
from Registrations.API.viewsets import (
    SubItemDBTableViewSet, AssetSubElementViewSet, imagesViewSet,
    ActionViewSet, AssetDBTableViewSet, SubItemperAssetViewSet, CommentViewSet
)
from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from django.conf.urls.static import static
from Forms.views import FormNumberView, ChangeFormStatus, ResponsesByProject
from Registrations.views import AssetNumbersView, AssetChangeStatus
from Projects.views import ProjectNumberView, RecentProjectsView, ChangeProjectStatus

# Configuração do roteador para os viewsets
router = routers.DefaultRouter()
router.register('assets', AssetDBTableViewSet, basename='asset')
router.register('projects', ProjectViewSet)
router.register('companies', CompanyViewSet)
router.register('users', UserViewSet)
router.register('elements', SubItemDBTableViewSet)
router.register('sub-elements', AssetSubElementViewSet)
router.register('images', imagesViewSet)
router.register('forms', FormsViewSet)
router.register('form-responses', Form_ResponseViewSet)
router.register('actions', ActionViewSet)
router.register('dropboxanswers', DropBoxAnswerListViewSet)
router.register('logeduser', ReturnLogedUser, basename='logeduser')
router.register('elementperasset', SubItemperAssetViewSet)
router.register('password', PasswordViewSet, basename='password')
router.register('comments', CommentViewSet)

# Definindo as URLs
urlpatterns = [
    # URLs de autenticação do DRF
    path('/api/api-auth/', include('rest_framework.urls')),

    # URLs de autenticação de tokens (Obter token e refresh)
    path('/api/api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('/api/api/token/mobile/', ObtainTokenViewMOBILE.as_view(), name='token_obtain_mobile'),
    path('/api/api/token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('/api/api/token/refresh/mobile', RefreshTokenViewMOBILE.as_view(), name='token_obtain_pair'),

    # URLs para verificar se o usuário está autenticado e fazer logout
    path('/api/is-authenticated/', IsAutenticatedView.as_view(), name='is_authenticated'),
    path('/api/logout/', LogoutView.as_view(), name='logout'),

    # URLs para interagir com Assets
    path('/api/asset_numbers/<int:project>/', AssetNumbersView.as_view(), name='asset_numbers'),
    path('api/change_asset_status/<int:id>/', AssetChangeStatus.as_view(), name='change_asset_status'),

    # URLs do Admin do Django
    path('/api/admin/', admin.site.urls),

    # URLs geradas pelo roteador (viewsets)
    path('/api/', include(router.urls)),

    # Outras URLs de projetos, formulários e respostas
    path('/api/userinfo/', CurrentUserView.as_view(), name='userInfo'),
    path('/api/form_numbers/', FormNumberView.as_view(), name='form_numbers'),
    path('/api/project_numbers/', ProjectNumberView.as_view(), name='project_numbers'),
    path('/api/recent_projects/', RecentProjectsView.as_view(), name='recent_projects'),
    path('/api/change_form_status/<int:id>/', ChangeFormStatus.as_view(), name='change_form_status'),
    path('/api/change_project_status/<int:id>/', ChangeProjectStatus.as_view(), name='change_project_status'),
    path('/api/responses_by_project/<int:project>/<int:form>/', ResponsesByProject.as_view(), name='responses_by_project'),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Para servir arquivos de mídia
