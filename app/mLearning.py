
from PIL import Image
import os, os.path
import pandas as pd
import shutil
import rasterio
import gdal
import glob
from pydub import AudioSegment
from pydub.utils import make_chunks
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
global path4

path4  = "G:/My Drive/"

class Select_Dir:
  """
  function for generate a dialog for select folder
  """
  def folder(self):
    win = Tk()
    
    # Define the geometry
    win.geometry("250x250")
    
    # Create a label and a Button to Open the dialog
    path = filedialog.askdirectory(title="Select a Folder")
    
    win.destroy()
    return path


class Tiling:
  """
  this function will generate tile of image, and store every images in one folder
  input: path_in, path_out
  all the outputs will be moved to google drive automatically, once the tiling process done
  """
  def make_tile(self, path_in, base_path):
    #specify size of tiling
    tile_size_x = 500
    tile_size_y = 500
    
    #specify path of images we need to tile
    in_path = path_in
    baseDir = base_path
    input_filename = os.listdir(in_path) # all filenames stored in variable

    #this is a loop for tiling every image in one directory
    for n in range(len(input_filename)):
      base = os.path.basename(input_filename[n])
      nama = os.path.splitext(base)[0]
      path = in_path+ '/'+ str(input_filename[n])
      
      ds = gdal.Open(path)
      band = ds.GetRasterBand(1)
      xsize = band.XSize
      ysize = band.YSize

      #creating directory before tiling
      path1 = baseDir + '/' + str(nama)
      os.makedirs(path1)
      print(path1)

      #create tiling
      for i in range(0, xsize, tile_size_x):
        for j in range(0, ysize, tile_size_y):
          com_string = "gdal_translate -of GTIFF -srcwin " + str(i) + ", " \
                        + str(j) + ", " + str(tile_size_x) + ", " \
                        + str(tile_size_y) + " " + str(in_path+'/')\
                        + str(input_filename[n]) + " " + str(path1+'/')\
                        + str(nama)+ "_" + str(i) + "_" + str(j) + ".tiff"
          
          os.system(com_string)
          print(com_string)
    print("moving to drive..")
    shutil.move(baseDir, path4)


class Model:

  def count_wpshp(self, n, filename, image_path, path_out, model, threshold=0.3):
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
    valid_images = [".jpg", ".gif", ".png", ".tga", ".tif", ".tiff"]
    total = []
    
    print("starting first for"+str(n))
    files = os.listdir(path)
    df = pd.DataFrame((files), columns =['nama file'])
    
    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]
        if ext.lower() not in valid_images:
            continue
        
        imgs.append(Image.open(os.path.join(path, f))) #opens images 
        geos.append(rasterio.open(os.path.join(path, f))) # gets coordinates of tiff
    
    print("starting second for"+str(n))
    
    """
    - iterate over two list/tuple in parallel
    - inputs image to model
    - outputs a pandas df with cols of coordinates, 
      class of object and confidence score
    - Below we reapply the coordinates extracted from the tif files 
      to our xmin,xmax,ymin,ymax to convert to latlong
    """

    for img,geo in zip(imgs, geos) : 
      results = model(img) 
      boredpile_ds = results.pandas().xyxy[0] 
    
      # transforms coordinates to geoloc
      boredpile_ds["xmin"], boredpile_ds["ymin"] = geo.transform * (boredpile_ds.xmin, boredpile_ds.ymin) 
      boredpile_ds["xmax"], boredpile_ds["ymax"] = geo.transform * (boredpile_ds.xmax, boredpile_ds.ymax)

      # removes unneeded columns 
      boredpile_ds = boredpile_ds[[
                    'name', 'class', 'xmin',
                    'ymin', 'xmax', 'ymax', 
                    'confidence'
                    ]] 
      
      #appends result of each object (here in pandas df) to a list so to get one giant df
      total.append(boredpile_ds)
      
    print("starting concat" + str(n))
    total = pd.concat(total, ignore_index = True) #concatanate to list of results df to one big dataframe
    total.to_csv(path_out + '/' + filename + ".csv") #download csv of our shp file location