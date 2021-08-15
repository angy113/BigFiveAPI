from django.db import router
from .api import SurveyViewSet
from rest_framework.routers import DefaultRouter
router = DefaultRouter()
# router.
# router.register('admin/', admin.site.urls)
# router.register('', welcome)
router.register('', SurveyViewSet)
urlpatterns =   router.urls