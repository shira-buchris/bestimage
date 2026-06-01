import cv2
import numpy as np
from insightface.app import FaceAnalysis

# שלב 1: אתחול המודל
# buffalo_l הוא המודל הכבד והמדויק ביותר (מומלץ לתמונות סטודיו)
# ctx_id=0 אומר להשתמש בכרטיס מסך, ctx_id=-1 אומר להשתמש במעבד (CPU)
app = FaceAnalysis(name='buffalo_l', providers=['CPUExecutionProvider'])
app.prepare(ctx_id=-1, det_size=(640, 640))

def analyze_studio_photo(image_path):
    # שלב 2: טעינת התמונה מהדיסק
    img = cv2.imread(image_path)
    if img is None:
        print("לא ניתן לטעון את התמונה")
        return

    # שלב 3: הרצת המודל (גילוי, יישור וחילוץ מאפיינים בשורה אחת)
    faces = app.get(img)
   
    print(f"נמצאו {len(faces)} פנים בתמונה.\n")

    dominant_face = None
    max_area = 0

    # שלב 4: מעבר על כל דמות שזוהתה וניתוח הנתונים
    for i, face in enumerate(faces):
        # א. המזהה הייחודי (Embedding) - וקטור של 512 מספרים
        # זה ה-ID שאיתו תשווי לתמונות אחרות
        face_id_vector = face.embedding
       
        # ב. מיקום הפנים (Bounding Box)
        bbox = face.bbox.astype(int) # [x1, y1, x2, y2]
       
        # ג. נקודות ציון (Landmarks) - עיניים, אף, פה
        landmarks = face.kps
       
        # ד. חישוב דומיננטיות לפי שטח הפנים בתמונה
        width = bbox[2] - bbox[0]
        height = bbox[3] - bbox[1]
        area = width * height
       
        print(f"--- דמות {i+1} ---")
        print(f"מיקום בפריים: {bbox}")
        print(f"גודל פנים (שטח): {area} פיקסלים")
        print(f"חתימה דיגיטלית (ID) - 5 המספרים הראשונים: {face_id_vector[:5]}")
       
        # בדיקה האם זו הדמות הכי גדולה (דומיננטית)
        if area > max_area:
            max_area = area
            dominant_face = {
                'id': i+1,
                'vector': face_id_vector,
                'bbox': bbox
            }

    # שלב 5: סיכום התוצאות
    if dominant_face:
        print("\n==============================")
        print(f"הדמות הדומיננטית שזוהתה: דמות מספר {dominant_face['id']}")
        print(f"מיקום: {dominant_face['bbox']}")
        print("==============================")

# הרצת הפונקציה על תמונה
analyze_studio_photo(r"C:\myproject\IMG_6610.JPG")