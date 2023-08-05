import joblib #jbolib模块
import requests 
import os

def HMC_estimate(X):
    #读取Model
    path = os.path.dirname(__file__)
    SVR = joblib.load(path+'/AI_model/HMC_svr_model.pkl')

    X = [X]
    #测试读取后的Model
    SVR_prediction = SVR.predict(X)

    HMC_ = round(SVR_prediction[0],2)
    print('含水量%s％w.b.'%(str(HMC_)))

    return HMC_
