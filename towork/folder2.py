import cv2
import numpy as np
from insightface.app import FaceAnalysis
from scipy.spatial.distance import cosine
import os
import matplotlib.pyplot as plt 
from openpyxl import Workbook
from collections import defaultdict
from chadutSelf import laplacian
from ClassId import ClassId
# from smileEndEyes import analyze_eyes
from ClassIdInImage import ClassIdInImage
from smileEndEyes import process_frame, smile 
from ClassId import ClassId 
import mediapipe.python.solutions.face_mesh as mp_face_mesh 


# אתחול המודל
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])         #אם זה לא עצמים בתנועה- זה בסדר.
app.prepare(ctx_id=-1, det_size=(640, 640))


THRESHOLD = 0.45                                                         # !! לשנות לקובץ חיצוני!!!קבוע!!
person = {}
face_counter = 0
# counts={}
# priority={}
counts = defaultdict(lambda: [0, 0])
#פתיחת קובץ אקסל לשמירת הנתונים

#מילון בני האדם. 
milonBnea = {} 


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

# def draw_eyes(img, kps):
#     import cv2

#     for i, eye in enumerate(kps[:2]):  # רק עיניים
#         x, y = int(eye[0]), int(eye[1])

#         cv2.circle(img, (x, y), 5, (0, 0, 255), -1)
#         cv2.putText(img, f"E{i+1}", (x+5, y-5),
#                     cv2.FONT_HERSHEY_SIMPLEX, 0.6,
#                     (0, 0, 255), 2)

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


def draw_on_image(img, bbox, label):
#     # המרת קואורדינטות למספרים שלמים
    x1, y1, x2, y2 = bbox.astype(int)
    face_img = img[y1:y2, x1:x2]
#     # הגדרת צבע (ירוק) ועובי קו
    color = (0, 255, 0)
    thickness = 5

#     # ציור המלבן סביב הפנים
    cv2.rectangle(img, (x1, y1), (x2, y2), color, thickness)
    #...מכאן אני מתחילה חדות. לא בדיוק כאן
    face_image= img[y1:y2,x1:x2]

#     # כתיבת ה-ID מעל המלבן
    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
#     # רקע שחור לטקסט כדי שיהיה קריא
    cv2.rectangle(img, (x1, y1 - 30), (x1 + 100, y1), color, -1)
    cv2.putText(img, str(label), (x1, y1 - 10), font, font_scale, (255, 255, 255), thickness)

def process_and_show(folder_path,img, nativ):
    # for filename in os.listdir(folder_path):
    #     if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
    #         img_path = os.path.join(folder_path, filename)
    #         img = cv2.imread(img_path)
            # if img is None: continue

    # זיהוי פנים
    faces = app.get(img)
    print(f"נמצאו {len(faces)} פנים בתמונה.\n")
    #יצירת אוביקט מסוג תמונה
    # מכניסה את הנתונים
    numFaces= len(faces)
    # יצירת מערך לכל הבנ"א שבתמונה
    arrLabena = []
    if numFaces > 0:
        for face in faces:
            # זיהוי ה-ID הייחודי
            person_id = get_unique_id(face.embedding)
            person[person_id].add_count()
            person[person_id].add_priority(1/numFaces)
            person[person_id].add_image(nativ)
        
            #ID = ClassId(person_id)

            # הכנסת הנתונים המתאימים-ID,רשימת תמונות בהם מופיע-להכניס את התמונה הנוכחית לרשימה,
            # לבדוק גיל-? כרגע לא
            # לתת עדיפות בתכונה באוביקט
            x1, y1, x2, y2 = face.bbox.astype(int)
            face_img = img[y1:y2, x1:x2]
            print("---------------Eyes-----------") 
            #smileEyes(face_img)
            #result = analyze_eyes(face_img)
            #עכשיו שמתי בסימן שאלה. 
            # result = analyze_eyes(img, face)
            # print(result)


            blurry = laplacian(face_img)
            print("Sharpness:", blurry, "id",person_id)

            # eyes = 0.5  #process_frame(face_img)
            with mp_face_mesh.FaceMesh() as face_mesh:
                _, eyes = process_frame(face_img, face_mesh)
            if eyes is None:
                eyes = 0.00
            print("Eyes:", eyes)

            smiling = smile(face_img)     #לשלוח לפונקציה שתחשב את זה. 
            if smiling is None:
                smiling = 0.00
            PriorityInImage = ( blurry*0.6 + eyes*0.13 + smiling*0.27 )/ numFaces #...כאן אמורה להיות הנוסחה של המוצלחות כפול עדיפות חלקי מספר המשתתפים או נוסחה חלופית. לא בדיוק

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



            #יצירת אוביקט מסוג בנ"א בתמונה
            arachimToBena = ClassIdInImage(person_id, blurry, eyes, smiling, PriorityInImage)
            arrLabena.append(arachimToBena) 
            #העלאת המונה במילון
            #counts[person_id][0] += 1
            #העלאת העדיפות
            #counts[person_id][1] += (1 / numFaces)
            # ציור על התמונה
            # draw_on_image(img, face.bbox, person_id)
            # draw_eyes(img, face.kps)
    else:
        print("תמונה ללא פנים")

    return arrLabena
    # הצגת התמונה בחלון
    # אם התמונה גדולה מדי למסך, נקטין אותה לתצוגה בלבד
    # # display_img = img.copy()
    # # max_height = 800
    # # if display_img.shape[0] > max_height:
    # #     ratio = max_height / display_img.shape[0]
    # #     display_img = cv2.resize(display_img, (0,0), fx=ratio, fy=ratio)

    # # cv2.imshow('Face Recognition Scan', display_img) 
#  מ
#     # img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

#     # plt.figure(figsize=(12, 8))
#     # plt.imshow(img_rgb)
#     # plt.axis('off')
#     # plt.title("Detected Faces")
#     # plt.show()
    # cv2.namedWindow("Faces", cv2.WINDOW_NORMAL)
    # cv2.imshow("Faces", img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # return arrLabena 

    # המתנה למקש: הקש על כל מקש למעבר לתמונה הבאה, או 'q' ליציאה
    # key = cv2.waitKey(0)
    # if key == ord('q'):
    #    break

    # cv2.destroyAllWindows()
    # for person_id, person_obj in person.items():
    #     print(person_id, person_obj)
    #for person_id, total_count in counts.items():
    #    ws.append([person_id, total_count[0],total_count[1]])
    #wb.save("קובץ_3_עמודות.xlsx")


# הרצה (שנה את הנתיב לתיקייה שלך)
# process_and_show(r"C:\myproject\PhotosWedding\1234") 

img = cv2.imread(r"C:\myproject\EyesAndSmile\AGB_7880.JPG")

process_and_show(
    None,
    img,
    r"C:\myproject\EyesAndSmile\AGB_7880.JPG"
    )