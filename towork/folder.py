import cv2
import numpy as np
from insightface.app import FaceAnalysis
from scipy.spatial.distance import cosine
import os
from openpyxl import Workbook

# אתחול המודל
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=-1, det_size=(640, 640))

THRESHOLD = 0.45
known_faces = {}
face_counter = 0

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
    new_id = f"ID_{face_counter}"
    known_faces[new_id] = new_embedding
    return new_id

def draw_on_image(img, bbox, label):
    # המרת קואורדינטות למספרים שלמים
    x1, y1, x2, y2 = bbox.astype(int)
    
    # הגדרת צבע (ירוק) ועובי קו
    color = (0, 255, 0)
    thickness = 2
    
    # ציור המלבן סביב הפנים
    cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
    
    # כתיבת ה-ID מעל המלבן
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 0.8
    # רקע שחור לטקסט כדי שיהיה קריא
    cv2.rectangle(img, (x1, y1 - 30), (x1 + 100, y1), color, -1)
    cv2.putText(img, label, (x1, y1 - 10), font, font_scale, (255, 255, 255), thickness)

def process_and_show(folder_path):
    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(folder_path, filename)
            img = cv2.imread(img_path)
            if img is None: continue
            
            # זיהוי פנים
            faces = app.get(img)
            
            for face in faces:
                # זיהוי ה-ID הייחודי
                person_id = get_unique_id(face.embedding)
                #הוספת שורה חדשה לאקסל
                
                
                # ציור על התמונה
                draw_on_image(img, face.bbox, person_id)
            
            # הצגת התמונה בחלון
            # אם התמונה גדולה מדי למסך, נקטין אותה לתצוגה בלבד
            display_img = img.copy()
            max_height = 800
            if display_img.shape[0] > max_height:
                ratio = max_height / display_img.shape[0]
                display_img = cv2.resize(display_img, (0,0), fx=ratio, fy=ratio)
            
            cv2.imshow('Face Recognition Scan', display_img)
            
            # המתנה למקש: הקש על כל מקש למעבר לתמונה הבאה, או 'q' ליציאה
            key = cv2.waitKey(0)
            if key == ord('q'):
                break
                
    cv2.destroyAllWindows()
wb.save("קובץ_3_עמודות.xlsx")

# הרצה (שנה את הנתיב לתיקייה שלך)
process_and_show(r"C:\myproject\Photos\2")