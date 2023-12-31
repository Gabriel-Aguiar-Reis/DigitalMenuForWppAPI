from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import (
    AddIngredient,
    AddQtyToIngredient,
    AddToCart,
    CampaignDetail,
    CampaignList,
    ClearCart,
    GetIngredient,
    HealthCheck,
    ListIngredients,
    PhotoDetail,
    PhotoList,
    ProductDetail,
    ProductList,
    RemoveFromCart,
    TypeDetail,
    TypeList,
    ViewCart,
    RemoveIngredient,
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
    path('healthcheck/', HealthCheck.as_view(), name='HealthCheck'),
    path(
        'campaigns/<uuid:pk>/', CampaignDetail.as_view(), name='CampaignDetail'
    ),
    path('campaigns/', CampaignList.as_view(), name='CampaignList'),
    path('cart/clear/', ClearCart.as_view(), name='ClearCart'),
    path('cart/view/', ViewCart.as_view(), name='ViewCart'),
    path('photos/<uuid:pk>/', PhotoDetail.as_view(), name='PhotoDetail'),
    path('photos/', PhotoList.as_view(), name='PhotoList'),
    path('products/<uuid:pk>/', ProductDetail.as_view(), name='ProductDetail'),
    path('products/<uuid:pk>/ingredients/', ListIngredients.as_view(), name='ListIngredients'),
    path('products/<uuid:pk>/add_ingredient/<str:name>/<str:price>/', AddIngredient.as_view(), name='AddIngredient'),
    path('products/<uuid:pk>/ingredients/<uuid:ingredient_pk>/add_qty/<int:qty_added>/', AddQtyToIngredient.as_view(), name='AddQtyToIngredient'),
    path('products/<uuid:pk>/ingredients/<uuid:ingredient_pk>/remove/', RemoveIngredient.as_view(), name='RemoveIngredient'),
    path('products/<uuid:pk>/ingredients/<uuid:ingredient_pk>/get/', GetIngredient.as_view(), name='GetIngredient'),
    path(
        'products/<uuid:pk>/add/<int:units>/',
        AddToCart.as_view(),
        name='AddToCart',
    ),
    path(
        'products/<uuid:pk>/remove/<int:units>/',
        RemoveFromCart.as_view(),
        name='RemoveFromCart',
    ),
    path('products/', ProductList.as_view(), name='ProductList'),
    path('types/<uuid:pk>/', TypeDetail.as_view(), name='TypeDetail'),
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
