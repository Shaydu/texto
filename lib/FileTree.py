import subprocess
import os
import glob
from VideoAnalyzer import VideoAnalyzer

class FileTree:

     @staticmethod
     def outputTree(filePath):
         if(os.path.isdir(filePath)):
             out = subprocess.check_output(["tree","-lhat", filePath])

             vidExt = ['.avi', '.mkv','.m4v','.mp4']
             
             dirs =  os.listdir(filePath)
             for filename in dirs:
                filename2, fileExt = os.path.splitext(filename)
                print("loop filext" + fileExt)
                print("loop filename" + filename)
                if(fileExt in vidExt):
                     out += "Stream info: " + VideoAnalyzer.getVideoSize(filePath + "/" + filename) + "\n"
  
         else:
             out = subprocess.check_output(["ls","-lhat", filePath]) + "\n"
             out += VideoAnalyzer.getVideoSize(filePath)
         print("returning " + out)
         return out

ft = FileTree()

#print ft.outputTree("/mnt/media/complete/Antichrist.Criterion.Collection.UNCUT.Edition.2009.BluRay.720p.DTS.x264-CHD/")              
#print ft.outputTree("/mnt/media/complete/Wedding.m4v")              
