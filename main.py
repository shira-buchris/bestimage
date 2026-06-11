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

from PeopleInThePicture import Processing_image
from priority import priorityAfter 
import cv2
from Classimage import ImageData 
from ClassPoza import Posa 

import sys


if len(sys.argv) > 1:
    folder_path = sys.argv[1] 

madadDimion = 0.851 

arrForFirstOne= []
arrPozot = []            #מערך הפוזות של כל התמונות שבתוכו יש לכל פוזה מערך? של הקוד של התמונה הזו במילון התמונות הראשי.

class DeepModel():
    '''MobileNet deep model.'''
    i=2
    milonAtmunotArashi = {}  
    moneLamilonArashi = 1
    arrtmunaBepoza = []      # המערך שיתחדש לכל פוזה בכל פעם עם התמונה והקוד שלה במילון הראשי ויכנס לתוך arrPozot.
    #moneLmilon = 2          # משתנה בכל פעם איפה להכניס את התמונה בתוך arrtmunaBepoza
    degelLepam1 = True  
    moneLearrPozot = 0  

    def __init__(self):
        self._model = self._define_model()
        # self.i = 1

        print('Loading MobileNet.')
        print()

    # .(לתמונה הכללית)(cnn) MobileNet יצירת מודל
    @staticmethod
    def _define_model(output_layer=-1):
        base_model = MobileNet(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        output = base_model.layers[output_layer].output
        output = GlobalAveragePooling2D()(output)
        model = Model(inputs=base_model.input, outputs=output)
        return model 

    # .והפעלתו . MobileNet המרת התמונה לפורמט
    @staticmethod
    def preprocess_image(path,model1):
        img = process_image.load_img(path, target_size=(224, 224))
        x = process_image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        # x = Model.predict(x)
        x = preprocess_input(x)
        x = model1.predict(x)

        x=x.flatten()
        return x 

    # .דימיון קוסינוס לתמונות
    @staticmethod
    def cosinus_dimion (input1, input2 ):
        Dimion=np.dot(input1, input2.T) / (np.linalg.norm(input1) * np.linalg.norm(input2))  
        return Dimion 
    
    # חלוקה נכונה לתיקיות
    @staticmethod
    def Division_into_folders(input1, input2, nativ1,nativ2):
        source=nativ2
        Dimion= model.cosinus_dimion(input1, input2)
        print("dimion:",Dimion)
        if Dimion>madadDimion:
            parent_dir = Path(nativ1).parent
            destination = parent_dir / Path(source).name
            shutil.move(source, destination)
            dest = destination 
        else:
            parent_dir= Path(nativ1).parent
            parent_dir= Path(parent_dir).parent
            new_folder=parent_dir / str(DeepModel.i)
            new_folder.mkdir(exist_ok=True)
            dest = new_folder / Path(source).name
            counter = 1
            while dest.exists():
                dest = new_folder / f"{counter}_{Path(source).name}"
                counter += 1
            shutil.move(source, dest)
            DeepModel.i += 1 

            DeepModel.arrtmunaBepoza = []
            DeepModel.arrtmunaBepoza.append((DeepModel.moneLamilonArashi)-1) 
            objPoza = Posa(DeepModel.moneLearrPozot, new_folder, DeepModel.arrtmunaBepoza )
            arrPozot.append(objPoza)
            DeepModel.moneLearrPozot += 1

        return Dimion, dest

model = DeepModel()

# .txt קבלת הנתיב ויצירת  
def get_all_images(path_folder):
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
    return lines 

def read_image_unicode(path):
    data = np.fromfile(path, dtype=np.uint8)
    return cv2.imdecode(data, cv2.IMREAD_COLOR)

# .טיפול בתמונה הראשונה  (כולל מבנת)
def first_image(image1):
    Lafun = read_image_unicode(image1) 
    if Lafun is None:
        raise ValueError(f"לא הצלחתי לקרוא את התמונה הראשונה: {image1}")
    participants = Processing_image( Lafun, str(image1))

    folder = "1"
    os.makedirs(folder, exist_ok=True)

    DeepModel.arrtmunaBepoza = []
    DeepModel.arrtmunaBepoza.append(1)

    objPoza = Posa(
        DeepModel.moneLearrPozot,
        Path(folder),
        DeepModel.arrtmunaBepoza
    )

    arrPozot.append(objPoza)

    DeepModel.moneLearrPozot += 1
    # DeepModel.arrtmunaBepoza.append(1)
    # arrPozot.append(DeepModel.arrtmunaBepoza)
    image1_copy_path = os.path.join(folder, os.path.basename(image1))
    shutil.move(image1, image1_copy_path) 
    current_path=image1_copy_path 

    print(f"Created folder {folder} and copied first image")

    objectImage = ImageData(DeepModel.moneLamilonArashi, current_path,  score=0.0, participants=participants) #???????????צריך חדות של תמונה ובהירות?
    DeepModel.milonAtmunotArashi[DeepModel.moneLamilonArashi] = objectImage    # image1 
    DeepModel.moneLamilonArashi += 1 
    return current_path

# . טיפול בשאר התמונות 
def image(image2, image1_copy_path, model):                                                                                   # ? צריך לשלוח את המשתנים השני והשלישי  
    Lafun = read_image_unicode(image2)

    if Lafun is None:
        raise ValueError(f"לא הצלחתי לקרוא את התמונה: {image2}")
    participants = Processing_image(Lafun, str(image2))
    
    
        # חישוב דמיון
    result = DeepModel.Division_into_folders(
        DeepModel.preprocess_image(image1_copy_path, model._model),
        DeepModel.preprocess_image(image2, model._model),
        image1_copy_path,
        image2
    )

    _, new_path = result
    if new_path is not None:
        image1_copy_path = str(new_path)
    else:
        image1_copy_path = image2 

    objectImage = ImageData(DeepModel.moneLamilonArashi, image1_copy_path,  score=0.0, participants=participants)                       #???????????צריך חדות של תמונה ובהירות?
    DeepModel.milonAtmunotArashi[DeepModel.moneLamilonArashi] = objectImage   
    DeepModel.moneLamilonArashi += 1 
    print(result)

    return image1_copy_path 

# הפעלת כל הפונקציות
def zimonAll(path_folder):
    
    lines = get_all_images(path_folder) 
    if not lines:
        return
    image1_copy_path = first_image(lines[0])

    # לולאה על שאר הקובץ
    for j in range(1, len(lines)):
        image1_copy_path = image(lines[j], image1_copy_path, model)   

    selected_image = priorityAfter(arrPozot ,path_folder, DeepModel.milonAtmunotArashi)
    print(selected_image) 

# zimonAll(r"C:\myproject\PhotosWedding\1234")
zimonAll(r"C:\myproject\debug_faces")   #r"C:\myproject\PhotosWedding\1234"folder_path

