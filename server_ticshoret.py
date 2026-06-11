import os
import sys
import traceback
from fastapi import FastAPI
from pydantic import BaseModel

# =========================
# חיבור לתיקיית הקוד שלך
# =========================

current_dir = os.path.dirname(os.path.abspath(__file__))

# אם הקוד שלך בתיקייה אחרת, שנה כאן:
project_code_path = current_dir

if project_code_path not in sys.path:
    sys.path.append(project_code_path)

# כאן תייבא את הפונקציה/מחלקה המרכזית שלך
# דוגמה:
# from main_pipeline import run_analysis

app = FastAPI()


class AnalyzeRequest(BaseModel):
    path: str


@app.get("/")
def home():
    return {"status": "ok", "message": "Python FastAPI server is running"}


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    try:
        input_path = request.path

        if not os.path.exists(input_path):
            return {
                "status": "error",
                "message": f"Path not found: {input_path}"
            }

        # =========================
        # כאן מחברים לקוד האמיתי שלך
        # =========================

        # לדוגמה זמנית לבדיקה:
        result = {
            "selected_images": [],
            "output_folder": input_path,
            "message": "Analysis completed successfully"
        }

        # אחר כך תחליף לזה, למשל:
        # result = run_analysis(input_path)

        return {
            "status": "success",
            "data": result
        }

    except Exception as e:
        traceback.print_exc()
        return {
            "status": "error",
            "message": str(e)
        }


@app.post("/shutdown")
def shutdown():
    return {"status": "success", "message": "Shutdown endpoint received"}