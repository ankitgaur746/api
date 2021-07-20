import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from pydantic import BaseModel 
import base64
import cv2
import predict
import numpy as np


class Image64(BaseModel):
    img: str
class Image64Respone(BaseModel):
    damage: str
    part:str
#intialize web app / pi
app = FastAPI()

# Allows cors for everyone **Ignore**
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)
# pip install -e detectron2_repo

# Redirects base url to docs goto /redoc for fancy documentation 
@app.get("/")
def main():
    return RedirectResponse(url="/docs")

# POST request for Name Write
@app.post("/ai", response_model=Image64Respone)
def post_name(img_base64:Image64):
    img = base64.b64decode(img_base64.img); 
    npimg = np.fromstring(img, dtype=np.uint8); 
    source = cv2.imdecode(npimg, 1)
    b1, b2 = predict.predict(source)
    return {'damage':base64.b64encode(b1), 'part':base64.b64encode(b2)}



if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8081)