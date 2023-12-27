from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import (
    CampaignDetail,
    CampaignList,
    HealthCheckView,
    PhotoDetail,
    PhotoList,
    ProductDetail,
    ProductList,
    TypeDetail,
    TypeList,
)

schema_view = get_schema_view(
    openapi.Info(
        title='MenuSunCookies API',
        default_version='v1',
        description='This is a MenuSunCookies API swagger.',
        terms_of_service='https://www.google.com/policies/terms/',
        contact=openapi.Contact(email='lugafeagre@gmail.com'),
        license=openapi.License(name='BSD License'),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path('healthcheck/', HealthCheckView.as_view(), name='HealthCheckView'),
    path(
        'campaigns/<uuid:pk>', CampaignDetail.as_view(), name='CampaignDetail'
    ),
    path('campaigns/', CampaignList.as_view(), name='CampaignList'),
    path('photos/<uuid:pk>', PhotoDetail.as_view(), name='PhotoDetail'),
    path('photos/', PhotoList.as_view(), name='PhotoList'),
    path('products/<uuid:pk>', ProductDetail.as_view(), name='ProductDetail'),
    path('products/', ProductList.as_view(), name='ProductList'),
    path('types/<uuid:pk>', TypeDetail.as_view(), name='TypeDetail'),
    path('types/', TypeList.as_view(), name='TypeList'),
]

urlpatterns += [
    path(
        '<format>/',
        schema_view.without_ui(cache_timeout=0),
        name='schema-json',
    ),
    path(
        '',
        schema_view.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui',
    ),
    path(
        'redoc/',
        schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc',
    ),
]
