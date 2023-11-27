import pygame
import os

BASE_IMAGE_PATH = 'data/images/'
BASE_DATA_PATH = 'data/'

def loadImage(path):
    image = pygame.image.load(BASE_IMAGE_PATH + path).convert_alpha()
    return image

def loadFromData(path):
    file = (BASE_DATA_PATH + path)
    return file

def getImageData(path, scale):
    thisDictionary = {}
    for folder in os.listdir(BASE_IMAGE_PATH + path):
        folderPath = os.path.join(BASE_IMAGE_PATH + path, folder)
        filesInFolder = os.listdir(folderPath)
        filePaths = []
        for file in filesInFolder:
            filePath = os.path.join(folderPath, file)
            filePaths.append(filePath)
        thisDictionary[folder] = filePaths
    thisDictionary.update(sortImageData(thisDictionary, scale))
    if len(thisDictionary.keys()) > 1:
        return thisDictionary
    else:
        returnedList = list(thisDictionary.values())[0]
        return returnedList

def sortImageData(images, scale):
    sortedItems = {}
    for folder, folderImages in images.items():
        sortedItems.update({folder : sorted(folderImages, key=lambda x: int(x.split('_')[-1].split('.')[0]))})
    loadedAndScaled = loadAndScaleImages(sortedItems, scale)
    return loadedAndScaled

def loadAndScaleImages(images, scale):
    loadedAndScaled = {}
    for folder, folderImages in images.items():
        updatedFolder = []
        for image in folderImages:
            loadedImage = pygame.image.load(image).convert_alpha()
            if scale is None:
                updatedFolder.append(loadedImage)
            else:
                calculatedSize = (loadedImage.get_width() * scale, loadedImage.get_height() * scale)
                scaledImage = pygame.transform.scale(loadedImage, calculatedSize)
                updatedFolder.append(scaledImage)
        loadedAndScaled.update({folder : updatedFolder})
    return loadedAndScaled
