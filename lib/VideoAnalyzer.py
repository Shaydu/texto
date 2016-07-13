import subprocess
from subprocess import call
import logging
import shlex
import json
import pprint
import re
import os 

class VideoAnalyzer:

   def getDimensions(self, filePath):
       #@todo need to call ffprobe command and return output
       probeCmd = "ffprobe -v error -of flat=s=_ -select_streams v:0 -show_entries stream=height,width " 
       #ffprobe -v error -show_entries stream=width,height \  -of default=noprint_wrappers=1 input.mp4

       # function to find the resolution of the input video file

       print "checking " + filePath
       print probeCmd + filePath
       ls_output = subprocess.check_output(["ffprobe", "-v", "error", "-select_streams","v:0", "-show_entries", "stream=width,height", "-of", "default=noprint_wrappers=1", filePath])
       print ls_output


   def findVideoResolution(self, pathToInputVideo):
	    cmd = "ffprobe -v error -print_format json -select_streams v:0"
	    args = shlex.split(cmd)
	    args.append(pathToInputVideo)
	    # run the ffprobe process, decode stdout into utf-8 & convert to JSON
	    ffprobeOutput = subprocess.check_output(args).decode('utf-8')
	    ffprobeOutput = json.loads(ffprobeOutput)
            pprint.pprint(ffprobeOutput)
	    # find height and width
	    height = ffprobeOutput['streams'][0]['height']
	    width = ffprobeOutput['streams'][0]['width']

	    return height + "x" + width
   @staticmethod		       
   def getVideoSize(pathtovideo):
        pattern = re.compile(r'Stream.*Video.*([0-9]{3,})x([0-9]{3,})')
        p = subprocess.Popen(['ffmpeg', '-i', pathtovideo],
				 stdout=subprocess.PIPE,
				 stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        match = pattern.search(stderr)
	if match:
		x, y = map(int, match.groups()[0:2])
	else:
		x = y = 0
	
        return str(x) + "x" +  str(y)

   

#va = VideoAnalyzer()
#print va.getVideoSize("/mnt/media/complete/Wedding.m4v")

#va.getDimensions("/mnt/media/complete/Wedding.m4v")
#print va.findVideoResolution("/mnt/media/completealert/Away Days (2016).mp4")
