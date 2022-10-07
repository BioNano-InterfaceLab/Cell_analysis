import os
import cv2
import numpy as np

BinarizationThreshold = 5
MaxCountourArea= 500
MinCountourArea= 15


path = "F:/RBC_Deformation_NP_10_19_2021/10_24_2021/Old_2"
output_directory="F:/RBC_Deformation_NP_10_19_2021/10_24_2021/Old_2_Processed"

background=cv2.imread(path + "/" + (sorted(os.listdir(path)))[0])
background = cv2.cvtColor(background, cv2.COLOR_BGR2GRAY)
background_blur = cv2.GaussianBlur(background, (5, 5), 5)


#diff= []
current=0
    
for f in sorted(os.listdir(path)):
  if f.endswith(".tiff"):
    frame = cv2.imread(path + "/" + f)
    frame=cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    frame_blured = cv2.GaussianBlur(frame, (5, 5), 5)
    frame_delta = cv2.absdiff(frame_blured, background_blur)
    frame_thresh = cv2.threshold(frame_delta, BinarizationThreshold, 255, cv2.THRESH_BINARY)[1]
    #erode_kernel = np.ones((5, 5), 'uint8')
    #frame_erode = cv2.morphologyEx(frame_thresh, cv2.MORPH_OPEN, erode_kernel)
    cnts, hierarchy = cv2.findContours(frame_thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    #background_blur=frame_blured

    for c in cnts:
        (x_i, y_i, w_i, h_i) = cv2.boundingRect(c)
        if cv2.contourArea(c) > MinCountourArea:
            #cv2.imshow('frame',frame)
            cv2.imwrite(output_directory + "/" + f, frame_thresh)
            #k = cv2.waitKey(30) & 0xff
            #if k == 27:
               # break
           
    if len(cnts)==0 and current % 5000 == 0:
           background_blur=frame_blured
    #diff1 = np.sum(frame_thresh)
    #diff.append(diff1)
    current=current+1
    if current % 5000 == 0:
       print(current)


    
#diff= np.delete(diff, 0, 0)