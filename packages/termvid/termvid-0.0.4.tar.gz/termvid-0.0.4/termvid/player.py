#!/usr/bin/env python3
import cv2
import sys
import time
import frame
import blessed

term = blessed.Terminal()

box = frame.HDFrame((0, 0), (term.width, term.height))
fileid = 0

if len(sys.argv) > 1:
	fileid = sys.argv[1]

cap = cv2.VideoCapture(fileid)

while True:
	_, data = cap.read()
	box.draw(data)
	time.sleep(0.01)
