# -*- coding: UTF-8 -*-
import sys
import os.path
import json
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))

from pprint import pprint
from shotgun_api3 import Shotgun
import subprocess as sp

sg = Shotgun("your_site_url", "script_name", "script_key")

src = "path to movie file"
dst, ext = os.path.splitext(os.path.basename(src))

version_id = 7228
img = 'a.jpg'

command = ['ffmpeg',
            '-y',
            '-i', src,
            '-f', 'mp4',
            '-vcodec', 'libx264',
            '-pix_fmt', 'yuv420p',
            '-vf', "scale=trunc((a*oh)/2)*2:720",
            '-g', '30', 
            '-b:v', '2000k', 
            '-vprofile', 'high',
            '-bf', '0',
            '-strict', 'experimental',
            '-acodec', 'aac',
            '-ab', '160k',
            '-ac', '2', 
            dst + '.mp4']
pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)

# 另外一种通过subprocess进行转换 mp4
# vcodec = "-vcodec libx264 -pix_fmt yuv420p -vf 'scale=trunc((a*oh)/2)*2:720' -g 30 -b:v 2000k -vprofile high -bf 0"
# acodec = "-strict experimental -acodec aac -ab 160k -ac 2"
# subprocess.call(['ffmpeg', '-i', src, vcodec, acodec,'-f mp4', dst + '.mp4'])

command = ['ffmpeg',
            '-y',
            '-i', src,
            '-f', 'webm',
            '-vcodec', 'libvpx',
            '-pix_fmt', 'yuv420p',
            '-vf', "scale=trunc((a*oh)/2)*2:720",
            '-g', '30', 
            '-b:v', '2000k', 
            '-vpre', '720p',
            '-quality', 'realtime',
            '-cpu-used', '0',
            '-qmin', "10",
            "-qmax", "42",
            '-acodec', 'libvorbis',
            '-aq', '60',
            '-ac', '2', 
            dst + '.webm']
pipe = sp.Popen(command, stdout=sp.PIPE, bufsize=10**8)

# 另外一种通过subprocess进行转换 webm
# vcodec = "-pix_fmt yuv420p -vcodec libvpx -vf 'scale=trunc((a*oh)/2)*2:720' -g 30 -b:v 2000k -vpre 720p -quality realtime -cpu-used 0 -qmin 10 -qmax 42"
# acodec = "-acodec libvorbis -aq 60 -ac 2"
# subprocess.call(['ffmpeg', '-i', src, vcodec, acodec,'-f webm', dst + '.webm'])

# 序列帧转换参数
# vcodec = "-r frame_count/seconds -i src_file -f image2 thumb_files-%02d.jpeg"

# 将转码完成的mp4，webm上传到Shotgun审看的字段
upload_mp4=sg.upload('Version', version_id, 'sample.mp4','sg_uploaded_movie_mp4')
# print(upload_mp4)
upload_webm=sg.upload('Version', version_id, 'sample.webm','sg_uploaded_movie_webm')
# print(upload_webm)

# 上传缩率图，和filmstrip
upload_thumb=sg.upload_thumbnail("Version", version_id, img)
# print(upload_thumb)
upload_film_thumb=sg.upload_filmstrip_thumbnail("Version", version_id, img)
# print(upload_film_thumb)