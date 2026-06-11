import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'

import numpy as np
import shutil
from pathlib import Path

# from tensorflow.python.keras.applications.mobilenet import MobileNet, preprocess_input
# from tensorflow.python.keras.preprocessing import image as process_image
# from tensorflow.python.keras.utils import Sequence
# from tensorflow.python.keras.layers import GlobalAveragePooling2D
# from tensorflow.python.keras import Model

# from tensorflow.keras.applications.mobilenet import MobileNet, preprocess_input
# from tensorflow.keras.preprocessing import image as process_image
# from tensorflow.keras.utils import Sequence
# from tensorflow.keras.layers import GlobalAveragePooling2D
# from tensorflow.keras import Model

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
        '''Define a pre-trained MobileNet model.

        Args:
            output_layer: the number of layer that output.

        Returns:
            Class of keras model with weights.
        '''
        base_model = MobileNet(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
        output = base_model.layers[output_layer].output
        output = GlobalAveragePooling2D()(output)
        model = Model(inputs=base_model.input, outputs=output)
        return model

    @staticmethod
    def preprocess_image(path,model1):
        '''Process an image to numpy array.

        Args:
            path: the path of the image.

        Returns:
            Numpy array of the image.
        '''
        img = process_image.load_img(path, target_size=(224, 224))
        x = process_image.img_to_array(img)
        x = np.expand_dims(x, axis=0)
        # x = Model.predict(x)
        x = preprocess_input(x)
        x = model1.predict(x)

        x=x.flatten()
        # print("22222222222222222222222222",x)
        return x


    @staticmethod
    def cosine_distance(input1, input2,nativ1,nativ2):
        '''Calculating the distance of two inputs.

        The return values lies in [-1, 1]. `-1` denotes two features are the most unlike,
        `1` denotes they are the most similar.

        Args:
            input1, input2: two input numpy arrays.

        Returns:
            Element-wise cosine distances of two inputs.
        '''
        #return
        # np.dot(input1, input2) / (np.linalg.norm(input1) * np.linalg.norm(input2))
        # base = r"C:\myproject\PhotosWedding\1234"
        # new_path = os.path.join(base, nativ1)
        # destination=new_path


        source=nativ2
                                                                                                                    # '''כאן השינוי'''
        Dimion=np.dot(input1, input2.T) / (np.linalg.norm(input1) * np.linalg.norm(input2))#np.dot(input1, input2.T) / \
                #np.dot(np.linalg.norm(input1, axis=1, keepdims=True), \
                        #np.linalg.norm(input2.T, axis=0, keepdims=True))
        print("dimion:",Dimion)
        print("11111111111111111111111111",Dimion)
        if Dimion>0.851:
            #וכאן הוספה למערך
            destination= nativ1
            course= nativ2
            parent_dir = Path(nativ1).parent
            destination = parent_dir / Path(course).name
            shutil.move(course, destination)
            dest = destination

            # new_path =

            # parent_dir = Path(new_path).parent
            # print("88888888888888888",parent_dir,source)
            # parent_dir.mkdir(exist_ok=True)
            # shutil.move(source,parent_dir)
            # destination=parent_dir/os.path.basename(nativ1)
            # dest=destination

        else:


            # arrImage= []
            # arrImage.append()
            # DeepModel.arrPozot.append(1)
            parent_dir= Path(nativ1).parent
            parent_dir= Path(parent_dir).parent
            new_folder=parent_dir / str(DeepModel.i)
            new_folder.mkdir(exist_ok=True)
            dest = new_folder / Path(nativ2).name
            counter = 1
            while dest.exists():
                dest = new_folder / f"{counter}_{Path(nativ2).name}"
                counter += 1
            shutil.move(nativ2, dest)
            DeepModel.i += 1 

            

            DeepModel.arrtmunaBepoza = []
            DeepModel.arrtmunaBepoza.append((DeepModel.moneLamilonArashi)-1) 
            objPoza = Posa(DeepModel.moneLearrPozot, new_folder, DeepModel.arrtmunaBepoza )
            # במקום זה: 
            # DeepModel.arrPozot[DeepModel.moneLearrPozot].append(objPoza)
            # DeepModel.arrPozot.append(DeepModel.arrtmunaBepoza)
            # את זה: 
            DeepModel.arrPozot.append(objPoza)
            
            DeepModel.moneLearrPozot += 1



        return Dimion, dest

    # def new_cosine_distance(path_folder):
    #     dimion=
    def extract_feature(self, generator):
        '''Extract deep feature using MobileNet model.

        Args:
            generator: a predict generator inherit from `keras.utils.Sequence`.

        Returns:
            The output features of all inputs.
        '''
        features = self._model.predict_generator(generator)
        return features



class DataSequence(Sequence):
    '''Predict generator inherit from `keras.utils.Sequence`.'''
    def __init__(self, paras, generation, batch_size=32):
        self.list_of_label_fields = []
        self.list_of_paras = paras
        self.data_generation = generation
        self.batch_size = batch_size
        self.__idx = 0

    def __len__(self):
        '''The number of batches per epoch.'''
        return int(np.ceil(len(self.list_of_paras) / self.batch_size))

    def __getitem__(self, idx):
        '''Generate one batch of data.'''
        paras = self.list_of_paras[idx * self.batch_size : (idx+1) * self.batch_size]
        batch_x, batch_fields = self.data_generation(paras)

        if idx == self.__idx:
            self.list_of_label_fields += batch_fields
            self.__idx += 1

        return np.array(batch_x)
model = DeepModel()


#print(model.cosine_distance(model.preprocess_image(r"C:\myproject\PhotosWedding\859A8696.JPG",model._model),model.preprocess_image(r"C:\myproject\PhotosWedding\1234\859A8682.JPG",model._model),r"C:\myproject\PhotosWedding\859A8696.JPG",r"C:\myproject\PhotosWedding\1234\859A8682.JPG"))




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

    objectImage = ImageData(DeepModel.moneLamilonArashi, current_path,  score=0.0, participants=participants) #???????????צריך חדות של תמונה ובהירות?
    DeepModel.milonAtmunotArashi[DeepModel.moneLamilonArashi] = objectImage    # image1 
    DeepModel.moneLamilonArashi += 1 
    print(f"Created folder {folder} and copied first image")

    # לולאה על שאר הקובץ
    for j in range(1, len(lines)):
        image2 = lines[j] 
        Lafun = cv2.imread(image2)
        participants = process_and_show(None, Lafun, str(image2))

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

        objectImage = ImageData(DeepModel.moneLamilonArashi, image1_copy_path,  score=0.0, participants=participants ) #???????????צריך חדות של תמונה ובהירות?
        DeepModel.milonAtmunotArashi[DeepModel.moneLamilonArashi] = image2  
        DeepModel.moneLamilonArashi += 1
        print(result)

        # הזזה קדימה
        # image1_copy_path = image2







zimonAll(r"C:\myproject\PhotosWedding\1234",model)




# import os
# import numpy as np
# import shutil
# from pathlib import Path

# from tensorflow.keras.applications.mobilenet import MobileNet, preprocess_input
# from tensorflow.keras.preprocessing import image as process_image
# from tensorflow.keras.layers import GlobalAveragePooling2D
# from tensorflow.keras import Model


# class DeepModel:
#     i = 2

#     def __init__(self):
#         self._model = self._define_model()
#         print("Loading MobileNet...")

#     @staticmethod
#     def _define_model(output_layer=-1):
#         base_model = MobileNet(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
#         output = base_model.layers[output_layer].output
#         output = GlobalAveragePooling2D()(output)
#         return Model(inputs=base_model.input, outputs=output)

#     @staticmethod
#     def preprocess_image(path, model):
#         if not os.path.exists(path):
#             print("Missing file:", path)
#             return None

#         img = process_image.load_img(path, target_size=(224, 224))
#         x = process_image.img_to_array(img)
#         x = np.expand_dims(x, axis=0)
#         x = preprocess_input(x)

#         x = model.predict(x)
#         return x.flatten()

#     @staticmethod
#     def cosine_distance(v1, v2):
#         return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))


# def zimonAll(path_folder, model):
#     output_file = "images.txt"
#     image_extensions = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"}

#     # יצירת קובץ נתיבים
#     with open(output_file, "w", encoding="utf-8") as f:
#         for root, _, files in os.walk(path_folder):
#             for file in files:
#                 if os.path.splitext(file)[1].lower() in image_extensions:
#                     f.write(os.path.join(root, file) + "\n")

#     print("Saved to images.txt")

#     # קריאה מהקובץ
#     with open(output_file, "r", encoding="utf-8") as f:
#         lines = [line.strip() for line in f if line.strip()]

#     if len(lines) < 2:
#         print("Not enough images")
#         return

#     # תמונה ראשונה
#     image1 = lines[0]

#     # תיקייה ראשונה
#     folder = "1"
#     os.makedirs(folder, exist_ok=True)

#     shutil.copy(image1, os.path.join(folder, os.path.basename(image1)))

#     print("Created folder 1")

#     # מעבר על שאר התמונות
#     for i in range(1, len(lines)):
#         image2 = lines[i]

#         vec1 = model.preprocess_image(image1, model._model)
#         vec2 = model.preprocess_image(image2, model._model)

#         if vec1 is None or vec2 is None:
#             image1 = image2
#             continue

#         similarity = model.cosine_distance(vec1, vec2)

#         print(f"{image1} <-> {image2} = {similarity}")

#         image1 = image2


# # הפעלה
# model = DeepModel()
#zimonAll(r"C:\myproject\Photos", model)