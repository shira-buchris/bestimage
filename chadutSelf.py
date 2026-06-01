# import cv2
# import numpy as np
# import tensorflow as tf
# import matplotlib.pyplot as plt

# #חישוב לפלסיאן
# def laplacian(face): 
#     #חישוב חדות
#     GrayImage= cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
#     cv2.imshow("image", GrayImage); cv2.waitKey(0); cv2.destroyAllWindows()
#     laplacianImage= cv2.Laplacian(GrayImage, cv2.CV_64F).var()
#     laplacianImage1= cv2.Laplacian(GrayImage, cv2.CV_64F)#.var()

#     laplacianImage1 = cv2.convertScaleAbs(laplacianImage1) 
#     cv2.imshow("Laplacian", laplacianImage1)
#     # is_blurry= laplacianImage < 200                                      #!!!!!!!קבוע!!!!!!להעביר לקובץ חיצוני!!!!!
#     # התייחסות לרעש 
    

#     #חישוב בהירות 
#     #צריך לבדוק אם ואיך
#     return   laplacianImage   #,is_blurry



# img= cv2.imread(r"C:\myproject\Photos\2\AGB_7758.JPG")
# laplacian(img)







import cv2
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt

#חישוב לפלסיאן
def laplacian(face): 
    #חישוב חדות
    GrayImage= cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
    # cv2.imshow("image", GrayImage); cv2.waitKey(0); cv2.destroyAllWindows()
    laplacianImage= cv2.Laplacian(GrayImage, cv2.CV_64F).var()
    laplacianImage1= cv2.Laplacian(GrayImage, cv2.CV_64F)#.var()

    laplacianImage1 = cv2.convertScaleAbs(laplacianImage1) 
    # cv2.imshow("Laplacian", laplacianImage1)
    # is_blurry= laplacianImage < 200                                      #!!!!!!!קבוע!!!!!!להעביר לקובץ חיצוני!!!!!
    # התייחסות לרעש 
    

    #חישוב בהירות 
    #צריך לבדוק אם ואיך
    return   laplacianImage   #,is_blurry
