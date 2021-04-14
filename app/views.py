import json 
from PIL import Image
from io import BytesIO
from django.shortcuts import render
from django.http import JsonResponse

from fastai.vision.all import *

# Create your views here.

inf = load_learner('/home/azureuser/export.pkl')

def home(request):
    return render(request,'home.html')

def get_image(request):
  
    image = Image.open(BytesIO(request.body))
  
    pred = inf.predict(np.asarray(image))
    print(pred)
    opts = {
        "0": "Cassava Bacterial Blight (CBB)",
        "1": "Cassava Brown Streak Disease (CBSD)",
        "2": "Cassava Green Mottle (CGM)",
        "3": "Cassava Mosaic Disease (CMD)",
        "4": "Healthy",
    }
    return JsonResponse(opts[pred[0][0]],safe=False)


