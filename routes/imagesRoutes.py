from config.db import connection
from typing import List
from fastapi import APIRouter, UploadFile, File, Request, Form
import shutil
import os
from os import path, remove
from PIL import Image
from models.images import Images
from schemas.imageSchema import imageEntity, imagesEntity
import requests
from bson.objectid import ObjectId
from uuid import uuid4
import random
import string


images = APIRouter()


@images.get('/getImages')
async def getImagesAll():
    return imagesEntity(connection.hwanitdb.images.find())


@images.post("/addImages/{produitId}")
async def add_images(produitId: str, images: List[UploadFile] = File(...),
                     nom: str = Form(...),
                     description: str = Form(...),
                     prix: float = Form(...),
                     id_categorie: int = Form(...),
                     id_brand: int = Form(...),
                     quantitie: int = Form(...),
                     id_hanout: str = Form(...),
                     token: str = Form(...)
                     ):
    idX = str(uuid4())

    dirLarge = "./images/produit/" + produitId + "/l"
    dirMinimum = "./images/produit/" + produitId + "/m"
    dirSmall = "./images/produit/" + produitId + "/s"

    if not os.path.exists("./images/produit/" + produitId):
        os.makedirs(dirLarge)
        os.makedirs(dirMinimum)
        os.makedirs(dirSmall)
    imagesNames = []
    for image in images:

        letters = string.ascii_lowercase
        fileNameHash = ''.join(random.choice(letters)
                               for i in range(10)) + '.jpg'

        imagesNames.append(fileNameHash)

        with open(dirLarge + "/" + fileNameHash, "wb") as buffer:
            shutil.copyfileobj(image.file, buffer)

            imgM = Image.open(open(dirLarge + "/" + fileNameHash, 'rb'))

            imgMM = imgM.resize((300, 300), Image.ANTIALIAS)
            imgS = imgM.resize((100, 100), Image.ANTIALIAS)

            imgMM.save(os.path.join(dirMinimum + "/",
                                    fileNameHash), 'JPEG', quality=90)
            imgS.save(os.path.join(dirSmall + "/", fileNameHash),
                      'JPEG', quality=90)

    datainMongo = {
        '_id': idX,
        "codeProduit": produitId,
        "images": imagesNames
    }
    connection.hwanitdb.images.insert_one(datainMongo)
    data = {'_id': produitId,
            'nom': nom,
            'description': description,
            'prix': prix,
            'id_categorie': id_categorie,
            'quantitie': quantitie,
            'id_hanout': id_hanout,
            'id_brand': id_brand,
            'thumbnail': imagesNames[0],
            'idInMongo': idX
            }

    reponse = requests.post(
        'http://127.0.0.1:9005/api/addProduit', data)

    return reponse.json()


@images.get('/getImagesById/{imageid}')
async def getImageById(imageid):

    return connection.hwanitdb.images.find_one({"_id": imageid})


@images.delete('/deleteImages/{idProduit}/{imageId}')
async def deleteById(imageId, idProduit):
    pathX = "./images/produit/"
    if os.path.join(pathX, idProduit + '/'):
        try:
            shutil.rmtree(os.path.join(pathX, idProduit))
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))
    res = connection.hwanitdb.images.delete_one({"_id": imageId})

    return "deleted"
