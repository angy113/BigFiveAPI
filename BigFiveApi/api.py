from rest_framework.viewsets import ModelViewSet

from .serializers import SurveySerializer
from .models import Survey

class SurveyViewSet(ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer