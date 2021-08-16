from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from .serializers import SurveySerializer
from .models import Survey

import numpy as np
import json

from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import LabelEncoder

class SurveyViewSet(ModelViewSet):
    queryset = Survey.objects.all()
    serializer_class = SurveySerializer

    @action(detail=False, methods=['post'])
    def predict (self, request, pk = None):
        
        res = json.loads(request.data)
        array1 = np.fromiter(res.values(),dtype=int)
        arrayAnswers = array1[0:50] / 50

        reduceTimes = lambda t: 60000 if t>60000 else t
        vfunc = np.vectorize(reduceTimes)
        arrayTimes=vfunc(array1[50:100])
        arrayTimes = arrayTimes / 60000
        
        array1 = np.append(arrayAnswers,arrayTimes)
        array = np.array([array1])
        model = keras.models.load_model('/home/ann_model.h5')
        prediction = model.predict(array)

        # Prediccion 
        pred = []

        for i in prediction:    
            pred.append(np.where(i == np.amax(i))[0][0])

        # Load label encoder 
        encoder = LabelEncoder()
        encoder.classes_ = np.load('/home/classes.npy', allow_pickle=True)
        return Response(encoder.inverse_transform([pred])[0])