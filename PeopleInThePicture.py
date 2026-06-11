# . ייבואים  
safModel = 0.45 

import cv2
from insightface.app import FaceAnalysis
from scipy.spatial.distance import cosine
from chadut import laplacian
from ClassIdInImage import ClassIdInImage
from smileEndEyes import process_frame, smile 
from ClassId import ClassId 
import mediapipe.python.solutions.face_mesh as mp_face_mesh 
import os

from tryTestModel import predict_one_image 

# אתחול המודל
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])                           #אם זה לא עצמים בתנועה- זה בסדר.
app.prepare(ctx_id=-1, det_size=(640, 640))

THRESHOLD = safModel                                                                                    # !! לשנות לקובץ חיצוני!!!קבוע!!
person = {}
face_counter = 0

# ייחודי ID 
def get_unique_id(new_embedding):
    global face_counter
    for face_id, person_class in person.items():
        dist = cosine(new_embedding, person_class.embedding)
        if dist < THRESHOLD:
            return face_id

    face_counter += 1
    new_id = face_counter
    person[new_id] = ClassId(person_id = new_id, embedding = new_embedding)

    return new_id


# . חיתוך פנים  
def Face_cutting(img, face): 
    x1, y1, x2, y2 = face.bbox.astype(int)

    h, w = img.shape[:2]

    face_width = x2 - x1
    face_height = y2 - y1

    padding_x = int(face_width * 0.15)
    padding_y = int(face_height * 0.15)

    x1 = max(0, x1 - padding_x)
    y1 = max(0, y1 - padding_y)
    x2 = min(w, x2 + padding_x)
    y2 = min(h, y2 + padding_y)

    return img[y1:y2, x1:x2]

# . מדידת איכות  
def Quality_measurement(face_img, numFaces, person_id): 

    cadut = laplacian(face_img)
    print("Sharpness:", cadut, "id",person_id)

    with mp_face_mesh.FaceMesh() as face_mesh:
        _, eyes = process_frame(face_img, face_mesh)
        
    if eyes is None:
        eyes = 0.00

    print("Eyes:", eyes)
    smiling = predict_one_image(face_img)    #smile(face_img)                                                                         #לשלוח לפונקציה שתחשב את זה. 

    if smiling is None:
        smiling = 0.00
    print("smile:", smiling)

    PriorityInImage = ( cadut*0.6 + eyes*0.13 + smiling*0.27 )/ numFaces                                   #...כאן אמורה להיות הנוסחה של המוצלחות כפול עדיפות חלקי מספר המשתתפים או נוסחה חלופית. לא בדיוק

    return cadut, eyes, smiling, PriorityInImage  

# טיפול באדם 
def One_face(face, img, nativ, numFaces, arrLabena): 
    person_id = get_unique_id(face.embedding)
    person[person_id].add_count()
    person[person_id].add_priority(1/numFaces)
    person[person_id].add_image(nativ)                                                                            # ? את הנתיב ? לא את הקוד
    face_img = Face_cutting(img, face)

    cadut, eyes, smiling, PriorityInImage = Quality_measurement(face_img, numFaces, person_id) 

    # 1. יצירת תיקיית בדיקה (אם היא עדיין לא קיימת במחשב)
    output_dir = "debug_faces"
    os.makedirs(output_dir, exist_ok=True)
    # 2. ניקח עותק של פרצוף האדם הנוכחי כדי לא להרוס את המקור
    debug_img = face_img.copy()
    # 3. נכתוב על גבי התמונה את הנתונים שהמחשב חישב עבורו
    # נשים טקסט קטן בצבע ירוק בפינה השמאלית העליונה
    cv2.putText(debug_img, f"ID: {person_id}", (5, 15), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
    cv2.putText(debug_img, f"Smile: {smiling:.3f}", (5, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
    cv2.putText(debug_img, f"Eyes: {eyes:.3f}", (5, 45), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0, 255, 0), 1)
    # 4. נשמור את התמונה לקובץ בתוך התיקייה, השם יכלול את ה-ID שלו
    file_name = f"{output_dir}/face_id_{person_id}.jpg"
    cv2.imwrite(file_name, debug_img)
    # ==========================================
    arachimToBena = ClassIdInImage(person_id, cadut, eyes, smiling, PriorityInImage)
    arrLabena.append(arachimToBena) 


# עיבוד התמונה
def Processing_image(img, nativ):
    faces = app.get(img)
    print(f"נמצאו {len(faces)} פנים בתמונה.\n")
    numFaces= len(faces)
    arrLabena = []
    if numFaces > 0:
        for face in faces:
            One_face(face, img, nativ, numFaces, arrLabena)

    else:
        print("תמונה ללא פנים")

    return arrLabena


# img = cv2.imread(r"C:\myproject\EyesAndSmile\AGB_7880.JPG")

# Processing_image(
#     img,
#     r"C:\myproject\EyesAndSmile\AGB_7880.JPG"
#     )
