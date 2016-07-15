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

   @staticmethod
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
        #pattern = re.compile(r'Stream.*Video.*([0-9]{3,4})x([0-9]{3,4})')
        pattern = re.compile(r'Stream.*(Video.*)')
        p = subprocess.Popen(['ffmpeg', '-i', pathtovideo],
				 stdout=subprocess.PIPE,
				 stderr=subprocess.PIPE)
        stdout, stderr = p.communicate()
        match = pattern.search(stderr)
	
        if match:
                pprint.pprint(match.groups())
		return match.groups()[0]
                #x, y = map(int, match.groups()[0:2])
	else:
		x = y = 0
	
        return str(x) + "x" +  str(y)

   

#va = VideoAnalyzer()
#print va.getVideoSize("/mnt/media/complete/Goodfellas.1990.BluRay.1080p.H264.AAC-RARBG.mp4")
#print va.getVideoSize("/mnt/media/complete/Indiana.Jones.And.The.Raiders.Of.The.Lost.Ark.1981.1080p.BluRay.x264.YIFY.mp4")

#va.getDimensions("/mnt/media/complete/Wedding.m4v")
#print va.findVideoResolution("/mnt/media/complete/the.summit.2012.docu.dvdrip.x264-debtvid.mkv")
