from app import app
from app import tiling as tile #calling file tiling.py from folder app as tile
from app import mLearning as ml #calling file mLearning.py from folder app as ml
from flask import render_template
import os, os.path
import torch

# calling class from file .py and save it to a variable

tiling = tile.Tiling() #calling class Tiling from tiling.py, and save it to a variable named tiling
models = ml.Model() #calling class Model from mLearning.py, and save it to a variable named models
directory = tile.select_dir() #calling class select_dir from tiling.py, and save it to a variable named directory

@app.route("/home")
def index():
    return render_template("index.html")

"""
endpoint for image tiling
input: a folder contain files of WP
"""
@app.route("/tile")
def tiling_images():
    path_in=directory.folder()
    base_path=directory.folder()
    if len(path_in)==0 and len(base_path)==0:
        return"specify the input and output path correctly"
    else:
        path2 = os.listdir(path_in)
        last_path=os.path.basename(base_path)
        if os.path.exists("G:/My Drive/"+last_path)==True:
            return"output folder you specified: "+str(base_path) +" already exist in google drive"
        else:
            for f in path2:
                if os.path.isdir(f):
                    return"input directory must only contain .tiff image file"
                else:
                    tiling.make_tile(path_in,base_path)
                    return "the results is ready on G:/My Drive/"+str(last_path)
    
"""
endpoint for boredpile detection
input: a folder contain tiling folders every WP
"""
@app.route("/model")
def model():
    #calling our model
    model_path = "G:/My Drive/best (5).pt" #insert model file path located in drive
    model = torch.hub.load('ultralytics/yolov5', 'custom', model_path)  # default
    
    #define in directpries to get image_path and out directories to save the result
    path_in = directory.folder()
    path_out = directory.folder()

    if len(path_in)==0 and len(path_out)==0:
        return"specify the input and output path correctly"
    else:
        pathh=os.listdir(path_in)
        
        for n in range(len(pathh)):
            base=os.path.basename(pathh[n])
            filename=os.path.splitext(base)[0]
            image_path= path_in+'/'+filename
            models.count_wpshp(n, filename,image_path,path_out,model)
            
        return "the results is ready on "+str(path_out)

"""
endpoint for roof detection
"""
@app.route("/roof")
def roof_model():
    #calling our model
    model_path = "G:/My Drive/roof-weights/v4-90.pt" #insert model file path located in drive
    model = torch.hub.load('ultralytics/yolov5', 'custom', model_path)  # default
    
    
    #define in directpries to get image_path and out directories to save the result
    path_in = directory.folder()
    path_out = directory.folder()

    if len(path_in)==0 and len(path_out)==0:
        return"specify the input and output path correctly"
    else:
        pathh=os.listdir(path_in)
        
        for n in range(len(pathh)):
            base=os.path.basename(pathh[n])
            filename=os.path.splitext(base)[0]
            image_path= path_in+'/'+filename
            models.count_wpshp(n, filename,image_path,path_out,model)
            
        return "the results is ready on "+str(path_out)