
from django.contrib import admin
from django.urls import path
from django.contrib import admin
from django.urls import path, include
from Accounts.views import IsAutenticatedView,CurrentUserView,ObtainTokenView, CookieTokenRefreshView, ObtainTokenViewMOBILE, RefreshTokenViewMOBILE, LogoutView
from rest_framework import routers
from Projects.API.viewsets import ProjectViewSet
from Accounts.API.viewsets import CompanyViewSet,UserViewSet,ReturnLogedUser,passwordViewSet

from Forms.API.viewsets import FormsViewSet,Form_ResponseViewSet,DropBoxAnswerListViewSet
from Registrations.API.viewsets import SubItemDBTableViewSet,AssetSubElementViewSet,imagesViewSet,ActionViewSet, AssetDBTableViewSet,SubItemperAssetViewSet, CommentViewSet


from rest_framework_simplejwt.views import TokenObtainPairView
from django.conf import settings
from django.conf.urls.static import static
from Forms.views import FormNumberView, ChangeFormStatus, ResponsesByProject
from Registrations.views import AssetNumbersView, AssetChangeStatus
from Projects.views import ProjectNumberView, RecentProjectsView, ChangeProjectStatus


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
router.register('password', passwordViewSet, basename='password')
router.register('comments', CommentViewSet)


urlpatterns = [
    path('api-auth/', include('rest_framework.urls')),
    path('api/token/', ObtainTokenView.as_view(), name='token_obtain_pair'),
    path('api/token/mobile/', ObtainTokenViewMOBILE.as_view(), name='token_obtain_mobile'),
    path('api/token/refresh/', CookieTokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/refresh/mobile', RefreshTokenViewMOBILE.as_view(), name='token_obtain_pair'),
    path('is-authenticated/', IsAutenticatedView.as_view(), name='is_authenticated'),
    path('logout/', LogoutView.as_view(), name='logout'),

    path('asset_numbers/<int:project>/', AssetNumbersView.as_view(), name='asset_numbers'),
    path('change_asset_status/<int:id>/', AssetChangeStatus.as_view(), name='change_asset_status'),

    path('admin/', admin.site.urls),
    path('', include(router.urls)),

    path('userinfo/', CurrentUserView.as_view(), name='userInfo'),
    
    path('form_numbers/', FormNumberView.as_view(), name='form_numbers'),

    path('project_numbers/', ProjectNumberView.as_view(), name='project_numbers'),
    path('recent_projects/', RecentProjectsView.as_view(), name='recent_projects'),
    path('change_form_status/<int:id>/', ChangeFormStatus.as_view(), name='change_form_status'),
    path('change_project_status/<int:id>/', ChangeProjectStatus.as_view(), name='change_project_status'),
    path('responses_by_project/<int:project>/<int:form>/', ResponsesByProject.as_view(), name='responses_by_project'),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

