import uvicorn
from fastapi import FastAPI, File, UploadFile, Form
from io import BytesIO
from fastapi.middleware.cors import CORSMiddleware
import os
from PIL import Image

from prediction import read_image, preprocess, predict_by_path

app = FastAPI()

# Configurasi CORS jika sekiranya tidak dibutuhkan
# bisa di comment saja badan code dibawah ini
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# nama folder 'flagImages' merupakan folder
# untuk menyimpan gambar flag dari user
flagImageFolder = 'flagImages'

# Cek keberadaan folder 'flagImages', jika tidak ada
# akan dibuat
if flagImageFolder not in os.listdir():
    os.mkdir(flagImageFolder)

# List folder dalam folder 'flagImages'
listFlagDir = os.listdir(flagImageFolder)

@app.get('/index')
async def hello_world():
    return "hello world"

@app.post('/api/predict')
async def predict_image(file: bytes = File(...)):
    # Read Image
    # image = load_gambar_by_path(file)
    image = read_image(file)
    
    image2 = preprocess(image)
    # Predictions Image with Model
    predictions = predict_by_path(image2)
    print(predictions)
    return predictions

@app.post("/predict/flag_image")
async def flag_image(file: UploadFile = File(...), label: str = Form(default="label")):
    '''
    Menyimpan gambar flag sesuai directory pada parameter input label
    attributes:
        - file  : Object file gambar, dapat diakses sebagai byte object dengan
                  method read()
        - label : string nama forlder, sesuai nama label gambar yang diberikan
                  format penamaan adalah sebagai berikut :
                  {kondisi odp (good/bad)}_odp_{jenis odp}_{posisi odp (luar/dalam)}
                  contoh input label : good_odp_pedestal_dalam
    '''
    image = Image.open(BytesIO(await file.read()))
    currentFlagFolder = flagImageFolder+'/'+label+"/"

    if label not in listFlagDir:
        os.mkdir(currentFlagFolder)   

    count = len(os.listdir(currentFlagFolder))+1
    image.save(currentFlagFolder + str(count) + '.jpg')

if __name__ == "__main__":
    uvicorn.run(app, port=8080, host='0.0.0.0')