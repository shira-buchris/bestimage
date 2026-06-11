import cv2

#חישוב לפלסיאן
def laplacian(face): 
    GrayImage= cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    laplacianImage= cv2.Laplacian(GrayImage, cv2.CV_64F).var() 
    # laplacianImage1= cv2.Laplacian(GrayImage, cv2.CV_64F)
    # laplacianImage1 = cv2.convertScaleAbs(laplacianImage1) 

    return   laplacianImage  