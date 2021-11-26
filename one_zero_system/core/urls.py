from rest_framework import routers

from .views import *

router = routers.DefaultRouter()
router.register('products', ProductViewSet)

urlpatterns = []

urlpatterns += router.urls
