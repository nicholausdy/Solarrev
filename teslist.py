import os
lat = -6.21151
lon = 106.74293
def isPreprocessFileExist(lat,lon):
    os.chdir('./preprocess_image')
    filelist = os.listdir('.')
    print(filelist)
    lat = str(lat)
    lon = str(lon)
    isImg = findString(filelist,'img',lat,lon)
    isImgClear = findString(filelist,'imgclear',lat,lon)
    print(isImg)
    print(isImgClear)
    return (isImg and isImgClear) 

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
   

print(isPreprocessFileExist(lat,lon))

       