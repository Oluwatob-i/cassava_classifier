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
    recommendation_for = (request.get_full_path()).split('?')[-1].split('=')[-1].lower()
    context = {}
    opts = {
        "cbb": "Cassava Bacterial Blight (CBB)",
        "cbsd" : "Cassava Brown Streak Disease (CBSD)",
        "cgm": "Cassava Green Mottle (CGM)",
        "cmd": "Cassava Mosaic Disease (CMD)"
    }
    descriptions = {
        "cbb": "Small, angular, brown, water-soaked lesions between leaf veins on lower surfaces of leaves; leaf blades turning brown as lesion expands; lesions may have a yello halo; lesions coalesce to form large necrotic patches; defoliation occurs with leaf petioles remaining in horizontal position as leaves drop; dieback of shoots; brown gum may be present on stems, leaves and petioles",
        "cbsd" : "Yellowin along veins on lower/older leaves ~ 3 months after planting",
        "cgm": "Yellow stipping of leaves; chlorotic spots on leaves; chlorosis of entire leaves; if infestation is very high then leaves may be stunted and deformed; terminal leaves may die and drop from plant; pest responsible is a tiny green mite",
        "cmd": "Discolored pale green, yellow or white mottled leaves which may be distorted with a reduced size; in highly susceptible cassava cultivars plant growth may be stunted, resulting in poor root yield and low quality stem cuttings. Note that infected plants can express a range of symptoms and the exact symptoms depend on the species of virus and the strain as well as the environmental conditions and and the sensitivity of the cassava host."
    }
    recommendations = {
        "cbb": ["Rotate cassava crop with non-host; plow crop debris into soil after harvest or remove and burn it; prune infected parts from plant; propagate cuttings only from healthy plants; intercrop cassava with corn (maize) and melon"],
        "cbsd" : ["Disease diagnosis: The first and foremost important aspect is to identify the disease correctly. Cassava brown streak disease varies in symptoms which made it difficult to identify in the field. It makes further complicated if both cassava brown streak and cassava mosaic diseases occur together. There are few techniques like serological and molecular methods are used to identify the virus in laboratory but have their limitations. Planting materials: Use only healthy and disease free cuttings for planting. Resistant cultivars: Plant cassava varieties that are more tolerant of brown streak virus such as Garukunsubire and Seruruseke. Roguing and sanitation: Remove and destroy any plants which are symptomatic of the disease including alternative hosts. Early Harvesting of tubers: Harvest crop early to avoid severe losses due to necrosis of tubers. Follow proper plant quarantine practices to avoid spread of virus to new region. Control insect vector: Whiteflies can be controlled by encouraging beneficial insects in the field like spiders, ladybird beetles etc. Use yellow sticky traps to monitor infestation of whiteflies. Spraying insecticidal soaps under leaf surface to kill flies."],
        "cgm": ["Plant tolerant cassava varieties where possible; plant at the beginning of the rainy season to encourage vigorous growth which allows plant to tolerate attack; intercropping with crops such as cowpea may reduce damage; introductions of the predatory mite Typhlodromalus aripo have been very successful at controlling the green spider mite in many regions of Africa" ],
        "cmd": ["Varieties of cassava resistant to the virus are available in many countries, most traditional varieties of cassava grown in Africa are susceptible to the virus, seek advice from an agricultural extension on suitable varieties for your region (see below). Do not plant cuttings from plants with symptoms of disease; inspect plants regularly for symptoms of disease and remove and destroy any showing symptoms. Infected plants should be uprooted ('rouged'). Replace with disease resistant varieties such as 'Rwizihiza', 'Ndamirabana', 'Cyizere', 'Seruruseke', 'Mavoka', 'Garukunsubire' and 'Mbakungahaze'. There is no agrochemical agent or organic treatment for this disease. There are both control strategies for the whitefly vector."]
    }
    if recommendation_for in opts.keys():
        context = {
            'image': f'/static/images/{recommendation_for}.jpg',
            'full_name': opts[recommendation_for],
            'description': descriptions[recommendation_for],
            'recommendations': recommendations[recommendation_for]
        }
    return render(request, 'recommendation.html', context)

def get_image(request):
    image_bytes = BytesIO(request.body)
    image = Image.open(image_bytes)  
    image = image.resize((128,128)) 
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


    s3.Bucket('cassava-classifier').put_object(Key=(image_name ), Body=request.body, ContentType='image/jpeg')
    image.close()

   
    return JsonResponse({'pred': opts[pred[0][0]], 'confidence': confidence}  if pred[0] else ''  ,safe=False)


