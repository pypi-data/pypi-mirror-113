from cv2 import cv2 as cv
import numpy as np
import time
import math
from AI_model import *
import pandas as pd

def showimg_by_path(image_path):
    image = cv.imread(image_path)
    cv.imshow('',image)
    cv.waitKey()
    cv.destroyAllWindows()

def showimg_by_ndarray(img_array):
    cv.imshow('',img_array)
    cv.waitKey()
    cv.destroyAllWindows()

def showimg_binary_img(img_array,threshold):
    gray = cv.cvtColor(img_array,cv.COLOR_BGR2GRAY)
    ret, binary = cv.threshold(gray,threshold,255,cv.THRESH_BINARY)
    cv.imshow('',binary)
    cv.waitKey()
    cv.destroyAllWindows()


def HSV(img_array):
    return cv.cvtColor(img_array,cv.COLOR_BGR2HSV)

def HLS(img_array):
    return cv.cvtColor(img_array,cv.COLOR_BGR2HLS)

def Lab(img_array):
    return cv.cvtColor(img_array,cv.COLOR_BGR2Lab)

def YCrCb(img_array):
    return cv.cvtColor(img_array,cv.COLOR_BGR2YCrCb)

def calculator_HMC(img_path):
    o = cv.imread(img_path)
    _shape = o.shape
    image_name='test'

    if o.shape[0]<o.shape[1]:
        print('此為橫向照片，不符合規格')

    elif o.shape[0]>o.shape[1]:
        o = cv.resize(o,(720,1280))
        _shape = o.shape
        print('調整圖檔大小：',_shape)

    total_area = o.shape[0]*o.shape[1]

    gray = cv.cvtColor(o,cv.COLOR_BGR2GRAY)
    ret , binary = cv.threshold(gray,160,255,cv.THRESH_BINARY)
    binary[1225:1250,75:500] = 255

    copy = o.copy()
    contours,hierarchy = cv.findContours(binary,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)
    copy = cv.drawContours(copy,contours,-1,(0,255,0),2)

    n = len(contours)

    copy = o.copy()

    coordinate_x_list=[]
    coordinate_y_list=[]

    e=0

    vertex = []
    total_area = o.shape[0] * o.shape[1]
    print("總面積:",total_area)

    for i in range(n):
        M = cv.moments(contours[i])
        area = M['m00']
        area_percentage = area/total_area
        if area_percentage > 0.003 and area_percentage < 0.010:
            cx = int(M['m10']/M['m00'])#三角形的x範圍  800-2200
            cy = int(M['m01']/M['m00'])#三角形的y範圍  0-3800
            if cx / o.shape[1] <0.7 and cx / o.shape[1] > 0.4 and cy / o.shape[0] < 0.25 and cy / o.shape[0] > 0.1:
                e += 1
                length = area**(1/2)
                cut = copy[cy-int(length*1.3):cy+int(length*10.4),cx-int(length*4.1):cx+int(length*0.7)]
                for coordinate in contours[i]:
                    coordinate_x_list.append(coordinate.flatten()[0])
                    coordinate_y_list.append(coordinate.flatten()[1])

    if e==0:
        print('未偵測到黑色校正色版')
    elif e!=0:
        print("偵測到黑色校正色版的數量：",e)

    vertex.append(tuple([np.min(coordinate_x_list),np.min(coordinate_y_list)]))
    vertex.append(tuple([np.min(coordinate_x_list),np.max(coordinate_y_list)]))
    vertex.append(tuple([np.max(coordinate_x_list),np.min(coordinate_y_list)]))
    vertex.append(tuple([np.max(coordinate_x_list),np.max(coordinate_y_list)]))
    print(vertex[0],vertex[1],vertex[2],vertex[3])

    v1 = vertex[0]
    v2 = vertex[1]
    v3 = vertex[2]
    v4 = vertex[3]

    #讀取校正板
    black_ck,gray_ck,white_ck,ck_value_list = read_checker(cut,image_name)

    #Gamma校正
    constrast_mean_list,constrast_quartile_list = constrast_correction(cut,image_name,black_ck,gray_ck,white_ck)

    #Gamma校正
    gamma_img = gamma_correction(cut,image_name,gray_ck)

    #光暈處理
    Halation_img = halation_removal(gamma_img,image_name)
    v1 = (0,0)
    v2 = (0,Halation_img.shape[0])
    v3 = (Halation_img.shape[1],0)
    v4 = (Halation_img.shape[1],Halation_img.shape[0])

    #擷取ROI
    ROI_2 = ROI_cropped(Halation_img,image_name,v1,v2,v3,v4)

    #去除背景
    removal_bg = bluerubber_removal(ROI_2,image_name)

    #去除陰影
    shadow_img = shadow_removal(removal_bg,image_name)

    #計算CIs
    mean_list,quartile_list = CIs_calculator(shadow_img,image_name)

    mean_list = mean_list + constrast_mean_list + ck_value_list
    print(mean_list)
    #估算HMC
    HMC = HMC_estimate(mean_list)

    #估算FR
    #fertility = Fertility(quartile_list)
    fertility = 50
    #估算GC
    rice_spiceies=1
    #print(rice_spiceies)
    #grain_counter = Grain_Counter(mean_list,fertility,rice_spiceies,shadow_img,image_name)
    grain_counter = 100

    return _shape,HMC,fertility,grain_counter

#=======================================================================讀取校正板===========================================================================

def read_checker(image,image_name):
    start_time = time.time()
    print('{}_讀取校正板'.format(image_name))
    ck_value_list = []
    o = image
    gray = cv.cvtColor(o,cv.COLOR_BGR2GRAY)
    ret , binary = cv.threshold(gray,160,255,cv.THRESH_BINARY)
    contours,hierarchy = cv.findContours(binary,cv.RETR_LIST,cv.CHAIN_APPROX_SIMPLE)

    copy = o.copy()
    n = len(contours)
    font=cv.FONT_HERSHEY_SIMPLEX
    checker_position=[]
    q=0
    total_area = o.shape[0] * o.shape[1]
    print('\nROI(I)總面積:',total_area)

    for i in range(n):
        M = cv.moments(contours[i])

        area = M['m00']
        area_percentage = area / total_area
        if area_percentage > 0.016 and area_percentage < 0.023:#這邊設定校正色板的輪廓面積範圍***1291之後的
            cx = int(M['m10']/M['m00'])#校正板x範圍 450-1050
            cy = int(M['m01']/M['m00'])#校正板y範圍 900-3200
            if cx / o.shape[1] > 0.8 and cx / o.shape[1] < 0.9 and cy / o.shape[0] > 0.05 and cy / o.shape[0] < 0.4:
                checker_position.append((cx,cy))
                cv.putText(copy,"checker"+str(i),(cx,cy),font,1,(0,0,255),3)#p=每個像素幾公分
                q+=1

    checker_position.sort(key = lambda s: s[1])
    print("偵測到的校正板個數%d"%(q))

    if q==2:
        checker_position.insert(1,(int((checker_position[0][0]+checker_position[1][0])/2),int((checker_position[0][1]+checker_position[1][1])/2)))

    if q!=3:
        print("******************圖片%s，沒有偵測到三個校正板*************************"%(image_name))
    print("校正板的中心點位置list:",checker_position)

    print('校正板中心點位置=\n',checker_position)

    g=checker_position[0]
    black_ck = o[g[1]-30:g[1]+30,g[0]-30:g[0]+30]

    g=checker_position[1]
    gray_ck = o[g[1]-30:g[1]+30,g[0]-30:g[0]+30]

    g=checker_position[2]
    white_ck = o[g[1]-30:g[1]+30,g[0]-30:g[0]+30]

    black_value = np.mean(black_ck)
    gray_value = np.mean(gray_ck)
    white_value = np.mean(white_ck)

    ck_value_list.append(black_value)
    ck_value_list.append(gray_value)
    ck_value_list.append(white_value)

    end_time = time.time()
    print("處理的時間{}秒".format(round(end_time-start_time,2)))
    return black_ck,gray_ck,white_ck,ck_value_list

#=======================================================================對比校正===========================================================================

def constrast_correction(o,image_name,black,gray,white):
    start_time = time.time()
    print('{}_對比校正'.format(image_name))

    img = o.copy()
    print(img.dtype)
    Bb,Bg,Br = cv.split(black)
    Wb,Wg,Wr = cv.split(white)

    B_r = np.array(Br).flatten()
    B_g = np.array(Bg).flatten()
    B_b = np.array(Bb).flatten()

    W_r = np.array(Wr).flatten()
    W_g = np.array(Wg).flatten()
    W_b = np.array(Wb).flatten()

    print(B_r.min(),B_g.min(),B_b.min())
    print(W_r.max(),W_g.max(),W_b.max())


    img_bl = np.zeros(img.shape)
    img_w = np.zeros(img.shape)

    img_bl[:,:,0] = B_b.min()
    img_bl[:,:,1] = B_g.min()
    img_bl[:,:,2] = B_r.min()

    img_w[:,:,0] = W_b.max()
    img_w[:,:,1] = W_g.max()
    img_w[:,:,2] = W_r.max()


    #result_img = img
    result_img = 255*(img-img_bl)/(img_w-img_bl)
    print(result_img.dtype)

    path = './constrast.png'
    cv.imwrite(path,result_img)
    result_img = cv.imread('./constrast.png')
    import os 
    os.remove(path)

    #Gamma校正
    gamma_img = gamma_correction(result_img,image_name,gray)

    #光暈處理
    Halation_img = halation_removal(gamma_img,image_name)

    v1 = (0,0)
    v2 = (0,Halation_img.shape[0])
    v3 = (Halation_img.shape[1],0)
    v4 = (Halation_img.shape[1],Halation_img.shape[0])
    print(Halation_img.dtype)

    #擷取ROI
    ROI_2 = ROI_cropped(Halation_img,image_name,v1,v2,v3,v4)
#    print(ROI_2.shape)
    print(ROI_2)
    print(ROI_2.shape)
    print(ROI_2.dtype)
    ROI_2 = ROI_2.astype(np.dtype('uint8'))


    #去除背景
    removal_bg = bluerubber_removal(ROI_2,image_name)


    #去除陰影
    shadow_img = shadow_removal(removal_bg,image_name)

    #計算CIs
    mean_list,quartile_list = CIs_calculator(shadow_img,image_name)

    end_time = time.time()
    print("處理的時間{}秒".format(round(end_time-start_time,2)))

    return mean_list,quartile_list
#=======================================================================gamma校正===========================================================================

def gamma_correction(image,image_name,gray):
    start_time = time.time()
    print('{}_Gamma校正'.format(image_name))
    B,G,R = cv.split(gray)
    
    r1 = math.log10(119)/math.log10(R.mean())
    r2 = math.log10(119)/math.log10(G.mean())
    r3 = math.log10(119)/math.log10(B.mean())

    o = image
    img = o.copy()
    img[:,:,2] = 255*((img[:,:,2]/255)**r1)
    img[:,:,1] = 255*((img[:,:,1]/255)**r2)
    img[:,:,0] = 255*((img[:,:,0]/255)**r3)

    end_time = time.time()
    print("處理的時間{}秒".format(round(end_time-start_time,2)))
    return img

#=======================================================================光暈去除===========================================================================

def halation_removal(image,image_name):
    start_time = time.time()
    print('{}_光暈去除'.format(image_name))
    o = image
    img = o.copy()
    
#    print(img[0,0])
#    print(np.std(img[0,0]))
    img[np.std(img[:,:])<35]=0

    different = cv.subtract(o, img)
    end_time = time.time()
    print("處理的時間{}秒".format(round(end_time-start_time,2)))
    return img


#=======================================================================截取ROI===========================================================================

def ROI_cropped(image,image_name,v1,v2,v3,v4):
    start_time = time.time()
    print('{}截取ROI'.format(image_name))
    ROI_vertex_x=[v1[0],v2[0],v3[0],v4[0]]
    ROI_vertex_x.sort()
    ROI_vertex_y=[v1[1],v2[1],v3[1],v4[1]]
    ROI_vertex_y.sort()
    o = image
    img = o.copy()

    imCrop = img[ROI_vertex_y[0]:ROI_vertex_y[3],ROI_vertex_x[0]:ROI_vertex_x[3]-130]
#    print(imCrop.shape)
    end_time = time.time()
    print("處理的時間{}秒".format(round(end_time-start_time,2)))
    return imCrop

#=======================================================================去除藍繩與白三角====================================================================

def bluerubber_removal(image,image_name):
    start_time = time.time()
    print('{}_去除背景與綠葉'.format(image_name))
    o = image
    img = o.copy()

    copy = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
    copy[:,:]=2*img[:,:,1]-img[:,:,0]-img[:,:,2]

    hsv = cv.cvtColor(img,cv.COLOR_BGR2HSV)
    H,S,V = cv.split(hsv)
#    img[H[:,:]>40] = 0

    ret, mask1 = cv.threshold(copy,200,255,cv.THRESH_BINARY_INV)
    zero_img = np.zeros(img.shape,np.uint8)
    img = cv.add(zero_img,img,mask=mask1)

    b,g,r = cv.split(img)
    gap = r - b
    img[gap[:,:]<35] = 0
    gap = b - r
    img[gap[:,:]<35] = 0
    gap = g - b
    img[gap[:,:]<35] = 0
    gap = b - g
    img[gap[:,:]<35] = 0


    img[b[:,:]>170] = 0

    img[int(img.shape[0]*0.85):,int(img.shape[1]*0.8):] = 0
    end_time = time.time()
    print("處理的時間{}秒".format(round(end_time-start_time,2)))

    return img

#=======================================================================去除陰影===========================================================================

def shadow_removal(image,image_name):
    start_time = time.time()
    print('{}_去除陰影'.format(image_name))
    o = image
    img = o.copy()
    gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)

    img[gray[:,:]<120]=0
    end_time = time.time()
    print("處理的時間{}秒".format(round(end_time-start_time,2)))
    return img

#=======================================================================計算CIs===========================================================================

def CIs_calculator(image,image_name):
    start_time = time.time()
    print('{}_計算CIs'.format(image_name))
    paddy_image = image

    total=0
    black=0
    lower=0
    real=0
    NDI_pixel=[]
    GI_pixel=[]
    RGRI_piexl=[]
    new=[]
    
    for i in range(1,int(paddy_image.shape[0])):
        for j in range(1,int(paddy_image.shape[1])):
            a=paddy_image[i,j,0]#B
            b=paddy_image[i,j,1]#G
            c=paddy_image[i,j,2]#R
            total+=1
            if a==0 or b==0 or c==0:
                black+=1
            elif a<30 and b<30 and c<30:
                lower+=1
            else:
                #print(paddy_image[i,j])
                new.append(paddy_image[i,j])
                NDI_pixel.append((float(b)-float(c))/(float(b)+float(c)))#NDI = (G-R)/(G+R)
                GI_pixel.append(float(b)/float(c))#GI = G/R
                RGRI_piexl.append(float(c)/float(b))#RGRI = R/G
                real+=1

    a = math.ceil(len(new)**0.5)

    if a**2>len(new):
        i=a**2-len(new)#平方後的總像素與現在總像素的差值

        for j in range(0,i):
            new.append(np.array([127,127,127],dtype=np.uint8))
    b = len(new)#新的矩陣像素數量
    new_image = np.zeros((a,a,3),dtype=np.uint8)
    new = np.full([1,b,3],new)
    c = new.shape#更新後的矩陣像素數量
    d = new_image.shape#空矩陣的像素數量  要跟上面一樣

    new_image = new.reshape(a,a,3)

    NDI = np.full([1,len(NDI_pixel)],NDI_pixel)
    GI = np.full([1,len(GI_pixel)],GI_pixel)
    RGRI = np.full([1,len(RGRI_piexl)],RGRI_piexl)

    #計算平均值
    RGB = np.mean(np.mean(new_image,axis=1),axis=0)
    HSV = np.mean(np.mean(cv.cvtColor(new_image,cv.COLOR_BGR2HSV),axis=1),axis=0)
    HLS = np.mean(np.mean(cv.cvtColor(new_image,cv.COLOR_BGR2HLS),axis=1),axis=0)
    Lab = np.mean(np.mean(cv.cvtColor(new_image,cv.COLOR_BGR2Lab),axis=1),axis=0)
    YCC = np.mean(np.mean(cv.cvtColor(new_image,cv.COLOR_BGR2YCrCb),axis=1),axis=0)
    NDI = np.mean(NDI,axis=1)
    GI = np.mean(GI,axis=1)
    RGRI = np.mean(RGRI,axis=1)

    mean_list = [RGB[2],RGB[1],RGB[0],HSV[0],HSV[1],HSV[2],HLS[1],HLS[2],Lab[0],Lab[1],Lab[2],YCC[0],YCC[1],YCC[2],NDI[0],GI[0],RGRI[0]]

    #計算四分位數
    b,g,r = cv.split(new_image)
    B = np.percentile(b,[25,50,75])
    G = np.percentile(g,[25,50,75])
    R = np.percentile(r,[25,50,75])
#    print(B,G,R)
    H1,S1,V1 = cv.split(cv.cvtColor(new_image,cv.COLOR_BGR2HSV))
    H2,L2,S2 = cv.split(cv.cvtColor(new_image,cv.COLOR_BGR2HLS))
    L3,a3,b3 = cv.split(cv.cvtColor(new_image,cv.COLOR_BGR2Lab))
    Y,Cr,Cb = cv.split(cv.cvtColor(new_image,cv.COLOR_BGR2YCrCb))

    #計算H統計值
    h = pd.Series(H1.flatten())
    #峰值
    h_skew = h.skew()
    #偏值
    h_kurt = h.kurt()
    #平均值
    h_mean = h.mean()
    #標準差
    h_std = h.std()

    #計算H前兩個波峰的x1,y1,x2,y2
    HSV = cv.cvtColor(new_image,cv.COLOR_BGR2HSV)
    H = cv.calcHist([HSV],[0],None,[50],[1,50])

    H = H.flatten()
    max_H = np.max(H)
    n = len(H)
    max_x_point=[]
    max_y_point=[]
    for i in range(1,n-1):
        if H[i-1]<H[i] and H[i+1]<H[i] and H[i]>500:
            max_x_point.append(i)
            max_y_point.append(H[i])

    print("最高點x位置：",max_x_point)
    print("最高點y位置：",max_y_point)

    n = len(max_x_point)
    ratio=[]
    print('波峰的數量：',n)
    if n>1:
        if max_y_point[0]<max_y_point[1]:
            ratio.append(0)
        elif max_y_point[0]>max_y_point[1]:
            ratio.append(1)
        else:
            ratio.append(1)

    elif n==1:
        ratio.append(1)

    #計算H_sharp_ratio
    H_sharp_ratio=0
    if n>1:
        H_sharp_ratio = (max_y_point[0]/(max_y_point[0]+max_y_point[1]))*100
    elif n==1:
        H_sharp_ratio = 90

    H1 = np.percentile(H1,[25,50,75])
    S1 = np.percentile(S1,[25,50,75])
    V1 = np.percentile(V1,[25,50,75])
    H2 = np.percentile(H2,[25,50,75])
    L2 = np.percentile(L2,[25,50,75])
    S2 = np.percentile(S2,[25,50,75])
    L3 = np.percentile(L3,[25,50,75])
    a3 = np.percentile(a3,[25,50,75])
    b3 = np.percentile(b3,[25,50,75])
    Y = np.percentile(Y,[25,50,75])
    Cr = np.percentile(Cr,[25,50,75])
    Cb = np.percentile(Cb,[25,50,75])
    NDI = np.percentile(NDI,[25,50,75])
    GI = np.percentile(GI,[25,50,75])
    RGRI = np.percentile(RGRI,[25,50,75])
    end_time = time.time()
    print("處理的時間{}秒".format(round(end_time-start_time,2)))

    quartile_list = [
        H_sharp_ratio,
        h_skew,h_kurt,h_mean,h_std,
        R[0],R[1],R[2],
        G[0],G[1],G[2],
        B[0],B[1],B[2],
        H1[0],H1[1],H1[2],
        S1[0],S1[1],S1[2],
        V1[0],V1[1],V1[2],
        H2[0],H2[1],H2[2],
        L2[0],L2[1],L2[2],
        S2[0],S2[1],S2[2],
        L3[0],L3[1],L3[2],
        a3[0],a3[1],a3[2],
        b3[0],b3[1],b3[2],
        Y[0],Y[1],Y[2],
        Cr[0],Cr[1],Cr[2],
        Cb[0],Cb[1],Cb[2],
        NDI[0],NDI[1],NDI[2],
        GI[0],GI[1],GI[2],
        RGRI[0],RGRI[1],RGRI[2]        
    ]
    return mean_list,quartile_list