# import cv2 

# cv2. Laplacian ( תמונה, cv2.CV_64F ) . var ()
import cv2
import numpy as np


def laplacian_variance(image: np.ndarray) -> float:
    """
    מחשב רמת חדות לפי Variance of Laplacian.

    החזר גבוה = תמונה חדה
    החזר נמוך = תמונה מטושטשת
    """
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    lap = cv2.Laplacian(gray, cv2.CV_64F)
    return lap.var()


def is_blurry(image: np.ndarray, threshold: float = 80.0) -> bool:
    """
    מחזיר האם התמונה מטושטשת לפי threshold.

    ברירת מחדל: 80 (ניתן לכיול לפי הדאטה שלך)
    """
    score = laplacian_variance(image)
    return score < threshold


def blur_score(image: np.ndarray) -> float:
    """
    wrapper נוח לקבלת ציון חדות בלבד
    """
    return laplacian_variance(image)


def analyze_blur(image: np.ndarray, threshold: float = 80.0) -> dict:
    """
    מחזיר גם ציון וגם החלטה.
    שימושי לדיבוג / לוגים
    """
    score = laplacian_variance(image)

    return {
        "score": float(score),
        "is_blurry": bool(score < threshold),
        "threshold": threshold
    }