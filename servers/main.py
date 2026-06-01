# .ייבואים 
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1' 
import numpy as np
import shutil
from pathlib import Path 

from keras.applications.mobilenet import MobileNet, preprocess_input
from keras.preprocessing import image as process_image
from keras.utils import Sequence
from keras.layers import GlobalAveragePooling2D
from keras import Model

from folder2 import process_and_show
import cv2
from Classimage import ImageData 
from ClassPoza import Posa 

arrForFirstOne= []
class DeepModel():
    '''MobileNet deep model.'''
    i=2
    milonAtmunotArashi = {}  
    moneLamilonArashi = 1
    arrPozot = []         #מערך הפוזות של כל התמונות שבתוכו יש לכל פוזה מערך? של הקוד של התמונה הזו במילון התמונות הראשי.
    arrtmunaBepoza = []          # המערך שיתחדש לכל פוזה בכל פעם עם התמונה והקוד שלה במילון הראשי ויכנס לתוך arrPozot.
    #moneLmilon = 2          # משתנה בכל פעם איפה להכניס את התמונה בתוך arrtmunaBepoza
    degelLepam1 = True  
    moneLearrPozot = 0  

    def __init__(self):
        self._model = self._define_model()
        # self.i = 1

        print('Loading MobileNet.')
        print()

    @staticmethod
    def _define_model(output_layer=-1):



def zimonAll(path_folder,model):
    output_file="images.txt"
    txt_path=output_file


    image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"}

    with open(output_file, "w", encoding="utf-8") as f:
        for root, _, files in os.walk(path_folder):
            for file in files:
                if os.path.splitext(file)[1].lower() in image_extensions:
                    full_path = os.path.join(root, file)
                    f.write(full_path + "\n")
    print(f"Saved to {output_file}")
    # קריאת כל השורות
    with open(txt_path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f if line.strip()]
    if len(lines) < 2:
        print("Not enough images")
        return

    # image1 = שורה ראשונה
    image1 = lines[0] 
    # זימון ליצירת המבני נתונים לכל האנשים בתמונה. 
    Lafun = cv2.imread(image1)
    participants = process_and_show(None, Lafun, str(image1))
    objectImage = ImageData(DeepModel.moneLamilonArashi, image1,  score=0.0, participants=participants) #???????????צריך חדות של תמונה ובהירות?
    DeepModel.milonAtmunotArashi[DeepModel.moneLamilonArashi] = objectImage    # image1 
    DeepModel.moneLamilonArashi += 1 
    # יצירת תיקייה בשם 1
    folder = "1"
    os.makedirs(folder, exist_ok=True)

    # הכנסת image1 לתיקייה
    #DeepModel.dictmunaBepoza[1]= image1
    DeepModel.arrtmunaBepoza.append(1)
    DeepModel.arrPozot.append(DeepModel.arrtmunaBepoza)

    image1_copy_path = os.path.join(folder, os.path.basename(image1))
    # shutil.copy(image1, image1_copy_path)                                       #?למה זה העתקה ולא העברה
    shutil.move(image1, image1_copy_path)                                      
    current_path=image1_copy_path
    print(f"Created folder {folder} and copied first image")

    # לולאה על שאר הקובץ
    for j in range(1, len(lines)):
        image2 = lines[j] 
        Lafun = cv2.imread(image2)
        participants = process_and_show(None, Lafun, str(image2))
        objectImage = ImageData(DeepModel.moneLamilonArashi, image2,  score=0.0, participants=participants ) #???????????צריך חדות של תמונה ובהירות?
        DeepModel.milonAtmunotArashi[DeepModel.moneLamilonArashi] = image2  
        DeepModel.moneLamilonArashi += 1
        # זימון ליצירת המבני נתונים לכל האנשים בתמונה. 
        # Lafun = cv2.imread(image2)
        # process_and_show(None, Lafun, str(image2))
        # חישוב דמיון
        result = model.cosine_distance(
            model.preprocess_image(image1_copy_path, model._model),
            model.preprocess_image(image2, model._model),
            image1_copy_path,
            image2
        )
        _, new_path = result

        if new_path is not None:
            image1_copy_path = str(new_path)
        else:
            image1_copy_path = image2
        print(result)

        # הזזה קדימה
        # image1_copy_path = image2







zimonAll(r"C:\myproject\PhotosWedding\1234",model)
