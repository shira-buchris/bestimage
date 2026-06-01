import cv2
import numpy as np
from insightface.app import FaceAnalysis
from scipy.spatial.distance import cosine
import os
from openpyxl import Workbook
from collections import defaultdict 
from Chadut.chadut import blur_score, is_blurry, analyze_blur 
# import folder2
import ClassId

from insightface.app import FaceAnalysis
from scipy.spatial.distance import cosine


# אתחול המודל
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=-1, det_size=(640, 640))


THRESHOLD = 0.45
known_faces = {}
face_counter = 0
# counts={}
# priority={}
counts = defaultdict(lambda: [0, 0])
#פתיחת קובץ אקסל לשמירת הנתונים

wb = Workbook()
ws = wb.active  # גיליון אחד בלבד

# ws.title = "נתונים"

# כותרות לעמודות
ws["A1"] = "ID"
ws["B1"] = "מס' מופעים"
ws["C1"] = "עדיפות"

# # דוגמה לנתונים
# ws.append(["א", "ב", "ג"])
# ws.append(["ד", "ה", "ו"])



def get_unique_id(new_embedding):
    global face_counter
    for face_id, saved_embedding in known_faces.items():
        dist = cosine(new_embedding, saved_embedding)
        if dist < THRESHOLD:
            return face_id
    
    face_counter += 1
    new_id = face_counter 
    known_faces[new_id] = new_embedding
    return new_id


#טעינת המודל
app = FaceAnalysis(name='buffalo_l')
app.prepare(ctx_id=0)


dict_person={}
def get_embedding(face_img):
    faces = app.get(face_img)

    if len(faces) == 0:
        return None

    return faces[0].embedding
def ser_fiq_score(face_img, runs=20, noise_std=0.01):
    base_emb = get_embedding(face_img)

    if base_emb is None:
        return 100

    similarities = []

    for _ in range(runs):
        # הוספת רעש קטן לתמונה
        noise = np.random.normal(0, noise_std, face_img.shape).astype(np.uint8)
        noisy_img = cv2.add(face_img, noise)

        emb = get_embedding(noisy_img)

        if emb is None:
            continue

        sim = 1 - cosine(base_emb, emb)
        similarities.append(sim)

    if len(similarities) == 0:
        return 0

    # יציבות = ממוצע הדמיון
    return float(np.mean(similarities))

def fun1(image_path):

    # img_path = os.path.join(folder_path, filename)
    img = cv2.imread(image_path)
    # זיהוי פנים
    faces = app.get(img)
    print(f"נמצאו {len(faces)} פנים בתמונה.\n")
    #יצירת אוביקט מסוג תמונה
    # מכניסה את הנתונים
    numFaces= len(faces)
    
    if numFaces > 0:
        for face in faces:
            # זיהוי ה-ID הייחודי
            person_id = get_unique_id(face.embedding)
            #יצירת אוביקט מסוג בנ"א
            # הכנסת הנתונים המתאימים-ID,רשימת תמונות בהם מופיע-להכניס את התמונה הנוכחית לרשימה,
            # לבדוק גיל-? כרגע לא
            # לתת עדיפות בתכונה באוביקט
            x1, y1, x2, y2 = face.bbox.astype(int)
            face_img = img[y1:y2, x1:x2]
            display_img = img.copy()
            max_height = 800
            if display_img.shape[0] > max_height:
                ratio = max_height / display_img.shape[0]
                display_img = cv2.resize(display_img, (0,0), fx=ratio, fy=ratio)
            
            cv2.imshow('Face Recognition Scan', display_img)
            #בדיקת איכות של הבנא בתמונה
            score = ser_fiq_score(face_img)
            print("1111111111111",score,id)
    
    
            #בדיקת חיוך
            #בדיקת מבט
fun1(r"C:\myproject\Photos\2\859A8658.JPG")
    