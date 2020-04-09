import data_preprocess as preprocess
import data_process 
import cv2
import numpy as np
import matplotlib.pyplot as plt
import os
from PIL import Image
import io
import base64
import json

def savePreprocessImageHandler(lat,lon):
    try:
        img = preprocess.imgwhite(lat,lon)
        imgclear = preprocess.imgfull(lat,lon)
        img = np.asarray(img)
        imgclear = np.asarray(imgclear)
        W,H = 768, 768
        center =(W/2,W/2)
        scale = 1
        M = cv2.getRotationMatrix2D(center, -30, scale)
        img= cv2.warpAffine(img, M, (W, H))
        imgclear= cv2.warpAffine(imgclear, M, (W, H))
        filename_img = 'img+'+str(lat)+'+'+str(lon)+'+'+'.png'
        filename_imgclear = 'imgclear+'+str(lat)+'+'+str(lon)+'+'+'.png'  
        cv2.imwrite(filename_img,img)
        cv2.imwrite(filename_imgclear,imgclear)
        res =  {"status":"success"}
    except:
        res = {"status":"failed","reason":"image not saved due to error in preprocessing"}
    finally:
        print(res)
        return res

def findString(l,s,lat,lon):
    for i in range(len(l)):
        splitted_file = l[i].split('+')
        if (splitted_file[0]==s):
            if((splitted_file[1] == lat) and (splitted_file[2] == lon)):
                res = True
                break
            else:
                res = False
    return res

def isPreprocessFileExist(lat,lon):
    #os.chdir('./preprocess_image')
    filelist = os.listdir('.')
    print(filelist)
    lat = str(lat)
    lon = str(lon)
    isImg = findString(filelist,'img',lat,lon)
    isImgClear = findString(filelist,'imgclear',lat,lon)
    print(isImg)
    print(isImgClear)
    return (isImg and isImgClear) 

def loadPreprocessImageHandler(lat,lon):
    try:
        os.chdir('./preprocess_image')
        if (not(isPreprocessFileExist(lat,lon))):
            print('Writing')
            res = savePreprocessImageHandler(lat,lon) 
        print('Loading')
        filename_img = 'img+'+str(lat)+'+'+str(lon)+'+'+'.png'
        filename_imgclear = 'imgclear+'+str(lat)+'+'+str(lon)+'+'+'.png'
        img = cv2.imread(filename_img)
        imgclear = cv2.imread(filename_imgclear)
        res = {"status":"success"} 
        print(res)
        return img,imgclear
    except:
        print({"status":"failed","reason":"image loading failed"}) 
    finally:
        os.chdir('..')

def getsolarPanels(lat,lon):
    try:
        print(os.listdir('.'))
        img,imgclear = loadPreprocessImageHandler(lat,lon)
        house,L,R,U,D = data_process.gethouse(img)
        panel1, panel2, panel3, panel4, p1,p2,p3,p4 = data_process.getsolarpanelsystem(house,L,R,U,D)
        return panel1, panel2, panel3, panel4, p1,p2,p3,p4
    except:
        print({"status":"failed","reason":"image loading failed"}) 

def getsolarPanelArea(p1,p2,p3,p4):
    return p1+p2+p3+p4

def getimage(filepath):
    image = open(filepath,'rb')
    image_read = image.read()
    image_64_bytes = base64.b64encode(image_read)
    image_64_string = image_64_bytes.decode('ascii') 
    return image_64_string

#call this function for server
def getsolarPanelPlacement(lat,lon):
    try:
        img, imgclear = loadPreprocessImageHandler(lat,lon)
        panel1, panel2, panel3, panel4, p1,p2,p3,p4 = getsolarPanels(lat,lon)
        pic = cv2.addWeighted(imgclear, 0.9, panel1+panel2+panel3+panel4,0.1,0)
        pic = Image.fromarray(pic,"RGB")
        os.chdir('./solar_img')
        filepath = 'solar+'+str(lat)+'+'+str(lon)+'+'+'.png'
        pic.save(filepath)
        print('Success')
        print(filepath)
        return getimage(filepath)
    except:
        res = {"status":"failed","reason":"image loading failed"}
        print(res)
        return res
    finally:
        print('Finally')
        os.chdir('..')

def getenergyAllRoofs(lat,lon):
    try:
        roof1,roof2,roof3,roof4 = data_process.getdata(lat,lon)
        panel1,panel2,panel3,panel4,p1,p2,p3,p4 = getsolarPanels(lat,lon)
        eperday,epermonth,eperyear = data_process.allroofs(p1,p2,p3,p4,roof1,roof2,roof3,roof4)
        return round(eperday),round(epermonth),round(eperyear)
    except:
        res = {"status":"failed","reason":"data processing failed"}
        print(res)
        return res

def getenergyOneRoof(lat,lon):
    try:
        img, imgclear = loadPreprocessImageHandler(lat,lon)
        roof1,roof2,roof3,roof4 = data_process.getdata(lat,lon)
        panel1,panel2,panel3,panel4,p1,p2,p3,p4 = getsolarPanels(lat,lon)
        bestroofindex,e1perday,e1permonth,e1peryear = data_process.oneroof(p1,p2,p3,p4,roof1,roof2,roof3,roof4)
        os.chdir('./solar_img')
        if bestroofindex == 1:
            pic = cv2.addWeighted(imgclear, 0.9, panel1,0.1,0)
            pic = Image.fromarray(pic,"RGB")
            filename = str(bestroofindex) +'+solar+'+str(lat)+'+'+str(lon)+'+'+'.png'
            pic.save(filename)
            bestroof = filename
        elif bestroofindex == 2:
            pic = cv2.addWeighted(imgclear, 0.9, panel2,0.1,0)
            pic = Image.fromarray(pic,"RGB")
            filename = str(bestroofindex) +'+solar+'+str(lat)+'+'+str(lon)+'+'+'.png'
            pic.save(filename)
            bestroof = filename
        elif bestroofindex == 3:
            pic = cv2.addWeighted(imgclear, 0.9, panel3,0.1,0)
            pic = Image.fromarray(pic,"RGB")
            filename = str(bestroofindex) +'+solar+'+str(lat)+'+'+str(lon)+'+'+'.png'
            pic.save(filename)
            bestroof = filename
        elif bestroofindex == 4:
            pic = cv2.addWeighted(imgclear, 0.9, panel4,0.1,0)
            pic = Image.fromarray(pic,"RGB")
            filename = str(bestroofindex) +'+solar+'+str(lat)+'+'+str(lon)+'+'+'.png'
            pic.save(filename)
            bestroof = filename
        return getimage(bestroof),round(e1perday,2),round(e1permonth,2),round(e1peryear,2)
    except:
        res = {"status":"failed","reason":"data processing failed"}
        print(res)
        return res
    finally:
        os.chdir('..')

def getAllInfo(lat,lon):
    try:
        SolarPanelPlacement = getsolarPanelPlacement(lat,lon)
        TotalEnergyPerDay, TotalEnergyPerMonth, TotalEnergyPerYear  = getenergyAllRoofs(lat,lon) 
        BestRoofPlacement, BestRoofEnergyPerDay, BestRoofEnergyPerMonth, BestRoofEnergyPerYear = getenergyOneRoof(lat,lon)
        res = {"status":200,"SolarPanelPlacement":SolarPanelPlacement,"TotalEnergyPerDay":TotalEnergyPerDay,"TotalEnergyPerMonth":TotalEnergyPerMonth,"TotalEnergyPerYear":TotalEnergyPerYear,"BestRoofPlacement":BestRoofPlacement,"BestRoofEnergyPerDay":BestRoofEnergyPerDay,"BestRoofEnergyPerMonth":BestRoofEnergyPerMonth,"BestRoofEnergyPerYear":BestRoofEnergyPerYear}
    except:
        res = {"status":500, "reason":"Internal server error"}
    finally:
        os.chdir('/home/ec2-user/Solarrev')
        return json.dumps(res)





