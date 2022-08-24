from matplotlib import pyplot as plt
from groupingLetters import *
from readImage import Read
import numpy as np
import matplotlib.patches as patches
import timeit

imagePath = "scene2/ryoungt_13.08.2002/dPICT0047.JPG"
'''getting original image'''
originalImage = Read.getImage(imagePath)
'''getting image as grayscale'''
grayImage = Read.getImageAsGrayScale(imagePath)
'''calculating gradient directions'''
gradientDirections = Read.getGradientDirections(grayImage) 
'''detecting edge pixels'''
edgeImage = Read.get_edges(grayImage) 

direction = 1

starttime = timeit.default_timer()

SW_Map = Read.initialize_SW_Map(edgeImage)


def SWT_apply_parallel(arr):

    start , end =  arr[0], arr[len(arr)-1]

    parallelEdgeImage = edgeImage[start:end]
    parallelGradientDirections = gradientDirections[start:end]
    parallelSW_Map = SW_Map[start:end]
    
    edgePointRows, edgePointCols =  np.nonzero(parallelEdgeImage) 

    rays = [] 

    for pos in list(zip(edgePointRows,edgePointCols)):

        startGradient = parallelGradientDirections[pos]  

        startX = np.cos(startGradient)
        startY = np.sin(startGradient)

        steps = 1

        ray = [(pos)]
        
        while  True: # TODO:  FIND A VALUE TO LIMIT STROKE WIDTH
            x_q = np.int32(round(pos[1] + (direction * startX * steps)))
            y_q = np.int32(round(pos[0] + (direction * startY * steps)))

            steps = steps + 1

            if not (0 <= x_q < parallelEdgeImage.shape[1] and 0 <= y_q < parallelEdgeImage.shape[0]):
                break
            
            ray.append((y_q, x_q))

            if parallelEdgeImage[y_q, x_q] > 0:
    
                strokeW = np.sqrt( (x_q - pos[1]) ** 2 + (y_q - pos[0]) ** 2)

                theta = np.abs(np.abs(startGradient - parallelGradientDirections[y_q, x_q]) - np.pi)

                if theta <= np.pi / 2:
                    for ry, rx in ray:
                        parallelSW_Map[ry, rx] = min(parallelSW_Map[ry, rx], strokeW)
                    rays.append(ray) 
                break
            
                
    for ray in rays:
        median = np.median([parallelSW_Map[y, x] for (y, x) in ray])
        for (y, x) in ray:
            parallelSW_Map[y, x] = min(median, parallelSW_Map[y, x]) 

    parallelSW_Map[parallelSW_Map == np.Infinity] = 0
 

    return parallelSW_Map


    


 



