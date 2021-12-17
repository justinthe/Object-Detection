import os, gdal
import glob
import os.path
import shutil
from pydub import AudioSegment
from pydub.utils import make_chunks


#Import the Tkinter library
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

class select_dir:
  """
  function for generate a dialog for select folder
  """
  def folder(self):
    win= Tk()
    #Define the geometry
    win.geometry("250x250")
    #Create a label and a Button to Open the dialog
    path= filedialog.askdirectory(title="Select a Folder")
    win.destroy()
    return path



class Tiling:
  """
  this function will generate tile of image, and store every images in one folder
  input: path_in, path_out
  all the outputs will be moved to google drive automatically, once the tiling process done
  """
  def make_tile(self,path_in, base_path):
    #specify size of tiling
    tile_size_x = 500
    tile_size_y = 500
    
    #specify path of images we need to tile
    in_path = path_in
    baseDir = base_path
    input_filename = os.listdir(in_path) # all filenames stored in variable

    #this is a loop for tiling every image in one directory
    for n in range(len(input_filename)):
      base=os.path.basename(input_filename[n])
      nama=os.path.splitext(base)[0]
      path = in_path+ '/'+str(input_filename[n])
      
      ds = gdal.Open(path)
      band = ds.GetRasterBand(1)
      xsize=band.XSize
      ysize=band.YSize

      #creating directory before tiling
      
      path1=baseDir+'/'+str(nama)
      os.makedirs(path1)
      print(path1)

      #create tiling
      for i in range(0, xsize, tile_size_x):
        for j in range(0, ysize, tile_size_y):
          com_string = "gdal_translate -of GTIFF -srcwin " + str(i)+ ", " + str(j) + ", " + str(tile_size_x) + ", " + str(tile_size_y) + " " + str(in_path+'/') + str(input_filename[n]) + " " + str(path1+'/') + str(nama)+ "_" + str(i) + "_" + str(j) + ".tiff"
          os.system(com_string)
          print(com_string)
    print("moving to drive..")
    shutil.move(baseDir, "G:/My Drive")