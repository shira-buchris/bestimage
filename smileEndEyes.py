import cv2    
import mediapipe as mp 
import numpy as np
list = [187,61,291,411]
list2 = [] 
def smile(imgFace):
    list2 = [] 
    #גישה למספרים קבועים במדיה פיפ
    fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, refine_landmarks=True)
    # קריאת התמונה בצורה שתומכת בעברית ובכל השפות (numpy עוקף את הבעיה של OpenCV)
    results = fm.process(cv2.cvtColor(imgFace, cv2.COLOR_BGR2RGB))
    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            h, w, _ = imgFace.shape
            for t in list:
                lm = face_landmarks.landmark[t] 
                x = int(lm.x * w)
                y = int(lm.y * h)
                list2.append([x, y])
            if len(list2) < 4:   # ← add this
                return None
 
    #הלחיים - קטן
    difference = abs(list2[0][0] - list2[1][0])
    difference += abs(list2[2][0] - list2[3][0])
    #השפתיים - גדול
    difference2 = abs(list2[1][0] - list2[2][0])
    print(difference)
    print(difference2)

    return difference 

# import cv2
# import mediapipe as mp
# import numpy as np
# list = [187,61,291,411]
# list2 = []

# def smile(imgFace):
#     #גישה למספרים קבועים במדיה פיפ
#     # mp_face_mesh = mp.solutions.face_mesh
#     crop_width = imgFace.shape[1]
#     fm = mp.solutions.face_mesh.FaceMesh(static_image_mode=True, refine_landmarks=True)
#     results = fm.process(cv2.cvtColor(imgFace, cv2.COLOR_BGR2RGB))
#     if results.multi_face_landmarks:
#         for face_landmarks in results.multi_face_landmarks:
#             h, w, _ = imgFace.shape
#             for t in list:
#                 lm = face_landmarks.landmark[t]
#                 x = int(lm.x * w)
#                 y = int(lm.y * h)
#                 list2.append([x, y])

#     #הלחיים - קטן
#     difference = abs(list2[0][0] - list2[1][0])
#     difference += abs(list2[2][0] - list2[3][0])
#     smile_ratio = difference / (crop_width + 1e-6)
#     print("smile_ratio", smile_ratio) 
#     return smile_ratio 



import math # חישובים מתמטיים
import cv2 # עיבוד תמונה ומצלמה
import mediapipe as mp # זיהוי פנים ועיניים
import json # לקריאת המערך נקודות
import mediapipe.python.solutions.face_mesh as mp_face_mesh
# ייבוא מודולים של MediaPipe
# mp_face_mesh = mp.solutions.face_mesh  

# פונקציה לחישוב EAR (Eye Aspect Ratio)
def ear(eye_landmarks):
    A = math.dist(eye_landmarks[1], eye_landmarks[5])
    B = math.dist(eye_landmarks[2], eye_landmarks[4])
    C = math.dist(eye_landmarks[0], eye_landmarks[3])
    return (A + B) / (2.0 * (C + 1e-6)) # הוספת 1e-6 כדי למנוע חלוקה באפס

# קריאת מערכי נקודות מקובץ JSON
with open("eye_landmarks.json", "r") as f:
    landmarks_data = json.load(f)

right_eye_indices = landmarks_data["right_eye"] # עין ימין
left_eye_indices = landmarks_data["left_eye"] # עין שמאל


# פונקציה שמטפלת בפריים בודד
def process_frame(frame, face_mesh):
    avg_ear = None
    try:
        # המרת צבעים ל RGB
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(frame_rgb)
        if not results.multi_face_landmarks:
            print("אזהרה: לא זוהו פנים בפריים הנוכחי.")

        # אתחול הערכים
        right_status, left_status = None, None
        face_landmarks = None

        # במקרה שנמצאו נקודות פנים
        if results.multi_face_landmarks:
            for face_landmarks in results.multi_face_landmarks:

                # חישוב EAR לעין ימין
                right_eye = [(face_landmarks.landmark[i].x,
                              face_landmarks.landmark[i].y)
                              for i in right_eye_indices]
                right_ear = ear(right_eye)

                # חישוב EAR לעין שמאל
                left_eye = [(face_landmarks.landmark[i].x,
                             face_landmarks.landmark[i].y)
                             for i in left_eye_indices]
                left_ear = ear(left_eye)

                avg_ear = (right_ear + left_ear) / 2

                openness_threshold = 0.22
                print(f"עין ימין: {'פתוחה' if right_ear > openness_threshold else 'סגורה'}")
                print(f"עין שמאל: {'פתוחה' if left_ear > openness_threshold else 'סגורה'}")

        return frame, avg_ear

    except Exception as e: # במקרה של שגיאה
        print(f"Error processing frame: {e}")
        return frame, None 

print("System initialized successfully!")

# # זימון הפונקציה על פריים מהמחשב
# frame, avg_ear = process_frame(
#     cv2.imread(r"C:\myproject\EyesAndSmile\AGB_7880.JPG"),
#     mp_face_mesh.FaceMesh() 
# )

# print(f"Average EAR: {avg_ear:.3f}")