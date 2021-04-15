import json 
import boto3
import random

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
    image_bytes = BytesIO(request.body)
   
    image = Image.open(image_bytes)
    
    
    pred = inf.predict(np.asarray(image))  
    con = float((pred[2].max()))
    confidence = (f"{con:.0%}")
  
    rand = 'abcdefghijklmnopqrstuvwxyz1234567890'

    s3.Bucket('cassava-classifier').put_object(Key=opts[pred[0][0]], Body=image_bytes)
    opts = {
        "0": "Cassava Bacterial Blight (CBB)",
        "1": "Cassava Brown Streak Disease (CBSD)",
        "2": "Cassava Green Mottle (CGM)",
        "3": "Cassava Mosaic Disease (CMD)",
        "4": "Healthy",
    }
    image.close()
    return JsonResponse(opts[pred[0][0]] + ' ' + confidence ,safe=False)


