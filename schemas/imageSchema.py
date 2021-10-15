def imageEntity(item) -> dict:
    return {
        "id": str(item['_id']),
        "images": item['images'],
        "codeProduit": str(item['codeProduit'])
    }


def imagesEntity(entity) -> list:
    return [imageEntity(item) for item in entity]
