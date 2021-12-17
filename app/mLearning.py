
from PIL import Image
import os, os.path
import pandas as pd
import shutil
import rasterio


class Model:

  def count_wpshp(self,n,filename,image_path,path_out,model,threshold=0.3):
    """
    inputs = TIFF file with coordinates, threshold
    outputs = CSV of lat long of object detected for GIS shp file

    """
    
    
    print(filename) 
    print(image_path)
    
    model.conf = threshold
    imgs = [] # contains all images in dir
    geos = [] # contains tiff coords in dir
    path = image_path
    valid_images = [".jpg",".gif",".png",".tga",".tif",".tiff"]
    total = []
    
    print("starting first for"+str(n))
    files = os.listdir(path)
    df = pd.DataFrame((files), columns =['nama file'])
    
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        
        
        imgs.append(Image.open(os.path.join(path,f))) #opens images 
        geos.append(rasterio.open(os.path.join(path,f))) # gets coordinates of tiff
    
    print("starting second for"+str(n))
    
    for img,geo in zip(imgs,geos) : #iterate over two list/tuple in parallel
      
      results = model(img) #inputs image to model
      
      boredpile_ds = results.pandas().xyxy[0] #outputs a pandas df with cols of coordinates, class of object and confidence score
    
      # Below we reapply the coordinates extracted from the tif files to our xmin,xmax,ymin,ymax to convert to latlong

      boredpile_ds["xmin"], boredpile_ds["ymin"] = geo.transform * (boredpile_ds.xmin,boredpile_ds.ymin) # transforms coordinates to geoloc
      boredpile_ds["xmax"], boredpile_ds["ymax"] = geo.transform * (boredpile_ds.xmax, boredpile_ds.ymax) # same as above
      boredpile_ds =boredpile_ds[['name','class','xmin', 'ymin', 'xmax','ymax','confidence']] # removes unneeded columns
      
      total.append(boredpile_ds) #we need to appends result of each object (here in pandas df) to a list so to get one giant df
      
    print("starting concat"+str(n))
    total = pd.concat(total,ignore_index=True) #concatanate to list of results df to one big dataframe
    total.to_csv(path_out+'/'+filename+".csv") #download csv of our shp file location