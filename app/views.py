import json 
import boto3

from PIL import Image
from io import BytesIO
from django.shortcuts import render
from django.http import JsonResponse

from fastai.vision.all import *

import boto3

s3 = boto3.resource('s3')


# Create your views here.

inf = load_learner('/home/ubuntu/export.pkl')

def home(request):
    return render(request,'home.html')

def get_image(request):
  
    image = Image.open(BytesIO(request.body))
    
    pred = inf.predict(np.asarray(image))
    
    con = float((pred[2].max()))
    confidence = (f"{con:.0%}")
    print(confidence)
    opts = {
        "0": "Cassava Bacterial Blight (CBB)",
        "1": "Cassava Brown Streak Disease (CBSD)",
        "2": "Cassava Green Mottle (CGM)",
        "3": "Cassava Mosaic Disease (CMD)",
        "4": "Healthy",
    }
    return JsonResponse(opts[pred[0][0]] + ' ' + confidence ,safe=False)


