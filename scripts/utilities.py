import pygame
import os
from PIL import Image
BASE_IMAGE_PATH = 'data/images/'
BASE_DATA_PATH = 'data/'

def getPath(path, shouldLoad, shouldScale, scaleTo):
    dataPath = BASE_DATA_PATH + path

    def loadOrScale(fileContainer):
        if shouldLoad and shouldScale:
            return loadImages(fileContainer, shouldScale, scaleTo)
        elif shouldLoad:
            return loadImages(fileContainer, shouldScale, scaleTo)
        else:
            return fileContainer

    if os.path.exists(dataPath):
        def pathJoiner(pathTo, theFile):
            joinedPath = os.path.join(pathTo, theFile)
            return joinedPath

        if os.path.isdir(dataPath):
            returnType = 'list'
            folderFilePaths = {}
            filePaths = []
            for file in os.listdir(dataPath):
                pathToFile = pathJoiner(dataPath, file)
                if os.path.isdir(pathToFile):
                    files = []
                    returnType = 'dictionary'
                    for subFile in os.listdir(pathToFile):
                        pathToSubFile = pathJoiner(pathToFile, subFile)
                        files.append(pathToSubFile)
                    folderFilePaths.update({file: sortImages(files)})
                else:
                    filePaths.append(pathToFile)
            if returnType == 'list':
                return loadOrScale(sortImages(filePaths))
            else:
                return loadOrScale(sortImages(folderFilePaths))
        elif os.path.isfile(dataPath):
            return loadOrScale(dataPath)
    else:
        print(f'\nPath {dataPath} does not exist, please check the path.\n')

def sortImages(images):
    try:
        if isinstance(images, list):
            sortedList = sorted(images, key=lambda x: int(x.split('_')[-1].split('.')[0]))
            return sortedList
        elif isinstance(images, dict):
            for container, containerImages in images.items():
                images.update({container: sorted(containerImages, key=lambda x: int(x.split('_')[-1].split('.')[0]))})
            return images

    except TypeError:
        print(f'\nThing: \n {images} \n is not of type list or dict, or something else went wrong.\n')

def loadImages(images, shouldScale, scaleTo):
    def checkTransparency(thisImage):
        with Image.open(thisImage, mode='r') as openImage:
            if openImage.mode != 'RGBA':
                return False
            return True

    try:
        if isinstance(images, list):
            for index, image in enumerate(images):
                if shouldScale:
                    if checkTransparency(image):
                        images[index] = scaleImages(pygame.image.load(image).convert_alpha(), scaleTo)
                    else:
                        images[index] = scaleImages(pygame.image.load(image).convert(), scaleTo)
                else:
                    if checkTransparency(image):
                        images[index] = pygame.image.load(image).convert_alpha()
                    else:
                        images[index] = pygame.image.load(image).convert()
            return images
        elif isinstance(images, dict):
            for container, containerImages in images.items():
                for index, image in enumerate(containerImages):
                    if shouldScale:
                        if checkTransparency(image):
                            containerImages[index] = scaleImages(pygame.image.load(image).convert_alpha(), scaleTo)
                        else:
                            containerImages[index] = scaleImages(pygame.image.load(image).convert(), scaleTo)
                    else:
                        if checkTransparency(image):
                            containerImages[index] = pygame.image.load(image).convert_alpha()
                        else:
                            containerImages[index] = pygame.image.load(image).convert()
            return images
        else:
            if shouldScale:
                if checkTransparency(images):
                    return scaleImages(pygame.image.load(images).convert_alpha(), scaleTo)
                else:
                    return scaleImages(pygame.image.load(images).convert(), scaleTo)
            else:
                if checkTransparency(images):
                    return pygame.image.load(images).convert_alpha()
                else:
                    return pygame.image.load(images).convert()

    except pygame.error:
        print(f'\nThing: \n {images} \n is not an image, or something else went wrong.\n')

def scaleImages(images, scaleTo):
    try:
        if isinstance(images, list):
            for index, image in enumerate(images):
                images[index] = pygame.transform.scale(image, (image.get_width() * scaleTo, image.get_height() * scaleTo))
            return images
        elif isinstance(images, dict):
            for container, containerImages in images.items():
                for index, image in enumerate(containerImages):
                    containerImages[index] = pygame.transform.scale(image, (image.get_width() * scaleTo, image.get_height() * scaleTo))
            return images
        else:
            return pygame.transform.scale(images, (images.get_width() * scaleTo, images.get_height() * scaleTo))
    except pygame.error:
        print(f'\nThing: \n {images} \n is not scalable, or something else went wrong.\n')
