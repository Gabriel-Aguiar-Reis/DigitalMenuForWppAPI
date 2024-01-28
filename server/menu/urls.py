from django.urls import path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

from .views import (
    AddQtyToIngredient,
    AddToCart,
    AddUniqueToCart,
    CalculateTotalOrderPrice,
    CampaignDetail,
    CampaignList,
    ClearCart,
    HealthCheck,
    IngredientDetail,
    IngredientList,
    PhotoDetail,
    PhotoList,
    ProductDetail,
    ProductList,
    RemoveFromCart,
    RemoveQtyFromIngredient,
    TypeDetail,
    TypeList,
    ViewCart,
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
    path(
        'healthcheck/',
        HealthCheck.as_view(),
        name='HealthCheck'
    ),
    
    path(
        'campaigns/<uuid:pk>/',
        CampaignDetail.as_view(),
        name='CampaignDetail'
    ),
    path(
        'campaigns/',
        CampaignList.as_view(),
        name='CampaignList'
    ),
    
    path(
        'cart/clear/',
        ClearCart.as_view(), 
        name='ClearCart'
    ),
    path(
        'cart/calculate_total_order_price/',
        CalculateTotalOrderPrice.as_view(),
        name='CalculateTotalOrderPrice'
    ),
    path(
        'cart/view/',
        ViewCart.as_view(),
        name='ViewCart'
    ),
    
    path(
        'cart/products/<uuid:pk>/ingredients/<uuid:ingredient_pk>/add_qty/<int:qty_added>/',
        AddQtyToIngredient.as_view(),
        name='AddQtyToIngredient'
    ),
    path(
        'cart/products/<uuid:pk>/ingredients/<uuid:ingredient_pk>/remove_qty/<int:qty_removed>/',
        RemoveQtyFromIngredient.as_view(),
        name='RemoveQtyFromIngredient'
    ),
    
    path(
        'cart/products/<uuid:pk>/add/<int:units>/',
        AddToCart.as_view(),
        name='AddToCart',
    ),
    path(
        'cart/products/<uuid:pk>/remove/<int:units>/',
        RemoveFromCart.as_view(),
        name='RemoveFromCart',
    ),
    
    path(
        'cart/products/<uuid:pk>/add/<int:units>/<uuid:order_p_id>',
        AddUniqueToCart.as_view(),
        name='AddUniqueToCart',
    ),
    
    path(
        'ingredients/<uuid:pk>',
        IngredientDetail.as_view(),
        name='IngredientDetail'
    ),
    path(
        'ingredients/',
        IngredientList.as_view(),
        name='IngredientList'
    ),
    
    path(
        'photos/<uuid:pk>/',
        PhotoDetail.as_view(),
        name='PhotoDetail'
    ),
    path(
        'photos/',
        PhotoList.as_view(),
        name='PhotoList'
    ),
    
    path(
        'products/<uuid:pk>/',
        ProductDetail.as_view(),
        name='ProductDetail'
    ),
    path(
        'products/',
        ProductList.as_view(),
        name='ProductList'
    ),
    
    
    path(
        'types/<uuid:pk>/',
        TypeDetail.as_view(),
        name='TypeDetail'
    ),
    path(
        'types/',
        TypeList.as_view(),
        name='TypeList'
    ),
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
