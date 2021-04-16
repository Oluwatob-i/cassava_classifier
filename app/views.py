import json 
import boto3
import random
import os
import pwd

from PIL import Image
from io import BytesIO
from django.shortcuts import render
from django.http import JsonResponse

from fastai.vision.all import *

import boto3

s3 = boto3.resource('s3')


# Create your views here.
sys_username = pwd.getpwuid( os.getuid() )[ 0 ]
inf = load_learner(f'/home/{sys_username}/export.pkl')

def home(request):
    return render(request,'home.html')

def recommendation(request):

    return render(request, 'recommendation.html')

def get_image(request):
    image_bytes = BytesIO(request.body)
    image = Image.open(image_bytes)   

    pred = inf.predict(np.asarray(image))  
    confidence = float((pred[2].max()))
    confidence = (f"{confidence:.0%}")
   
    opts = {
        "0": "Cassava Bacterial Blight (CBB)",
        "1": "Cassava Brown Streak Disease (CBSD)",
        "2": "Cassava Green Mottle (CGM)",
        "3": "Cassava Mosaic Disease (CMD)",
        "4": "Healthy",
    }
    rand = 'abcdefghijklmnopqrstuvwxyz1234567890'
    rand = (random.sample(rand, 10))
    if not pred[0]:
        image_name =  'no_prediction'+  '/' +  ''.join(rand) +  '.jpg'

    else:
        image_name =  opts[pred[0][0]] +  '/' +  ''.join(rand) + f'-{(confidence.split("%")[0])}' + '.jpg'


    #s3.Bucket('cassava-classifier').put_object(Key=(image_name ), Body=request.body, ContentType='image/jpeg')
    image.close()

   
    return JsonResponse({'pred': opts[pred[0][0]], 'confidence': confidence}  if pred[0] else ''  ,safe=False)


