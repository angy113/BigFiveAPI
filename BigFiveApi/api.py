from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from .serializers import SurveySerializer
from .models import Survey

import numpy as np

from tensorflow import keras
from sklearn.preprocessing import LabelEncoder


class SurveyViewSet(ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    def create(self, request, *args, **kwargs):
        super().create(request,*args, **kwargs)
        requestNumphyArray = np.fromiter(request.data.values(), dtype=int)
        arrayAnswers = requestNumphyArray[0:50] / 5

        def reduceTimes(t): return 60000 if t > 60000 else t
        vfunc = np.vectorize(reduceTimes)
        arrayTimes = vfunc(requestNumphyArray[50:100])
        arrayTimes = arrayTimes / 60000

        requestNumphyArray = np.append(arrayAnswers, arrayTimes)
        array = np.array([requestNumphyArray])
        model = keras.models.load_model('./ann_model.h5')
        prediction = model.predict(array)

        # Prediccion
        pred = []

        for i in prediction:
            pred.append(np.where(i == np.amax(i))[0][0])

        # Load label encoder
        encoder = LabelEncoder()
        encoder.classes_ = np.load('./classes.npy', allow_pickle=True)
        return Response(encoder.inverse_transform([pred])[0], status=HTTP_201_CREATED)
