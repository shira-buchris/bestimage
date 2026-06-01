from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

# כאן תייבאי את הקוד שלך
# from main_process import process_folder

app = FastAPI()

class ProcessRequest(BaseModel):
    folder_path: str

@app.post("/process")
def process_images(request: ProcessRequest):
    try:
        folder_path = request.folder_path

        # כאן תפעילי את הפונקציה הראשית שלך
        # result_path = process_folder(folder_path)

        result_path = folder_path + "_results"  # זמני לבדיקה

        return {
            "success": True,
            "result_path": result_path,
            "message": "Processing completed successfully"
        }

    except Exception as e:
        return {
            "success": False,
            "result_path": None,
            "message": str(e)
        }

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000) 