import urllib.request
print("מתחיל להוריד את המודל, זה עשוי לקחת כמה שניות...")
url = "https://github.com/onnx/models/raw/main/validated/vision/classification/mobilenet/model/mobilenetv2-7.onnx"
urllib.request.urlretrieve(url, "mobilenet.onnx")
print("הקובץ mobilenet.onnx ירד בהצלחה ויושב בתיקייה!")