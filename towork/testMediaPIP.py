import cv2
import mediapipe as mp

# MediaPipe Face Mesh (רשת פנים)
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles

# נתיב לתמונה (שני: תשני כאן)
image_path = "face.jpg"

# קריאת תמונה
image = cv2.imread(image_path)

if image is None:
    raise ValueError("לא נמצאה תמונה בנתיב שציינת")

# המרת צבע ל-RGB (נדרש ל-MediaPipe)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

with mp_face_mesh.FaceMesh(
    static_image_mode=True,
    max_num_faces=1,
    refine_landmarks=True,
    min_detection_confidence=0.5
) as face_mesh:

    results = face_mesh.process(image_rgb)

    image_out = image.copy()

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:

            # רשת משולשים (mesh = רשת)
            mp_drawing.draw_landmarks(
                image=image_out,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style()
            )

            # קווי מתאר (עיניים/פה/לסת)
            mp_drawing.draw_landmarks(
                image=image_out,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_CONTOURS,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_contours_style()
            )

# הצגת תמונה
cv2.imshow("Face Mesh", image_out)
cv2.waitKey(0)
cv2.destroyAllWindows()

# שמירה (אופציונלי)
cv2.imwrite("output_mesh.jpg", image_out)