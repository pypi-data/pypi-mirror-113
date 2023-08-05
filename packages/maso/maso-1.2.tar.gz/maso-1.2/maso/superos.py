import os 

def create_dir(dirpath):
    os.mkdir(dirpath)

def check_dir(dirpath):
    return os.path.isdir(dirpath)

def check_file(filepath):
    return os.path.isfile(filepath)

if check_dir('./AI_model')==False:
    create_dir('./AI_model')
    import requests    
    url = 'https://976658e65208.ngrok.io/static/AI_Model/HMC_svr_model.pkl'
    res = requests.get(url)
    with open('./AI_model/HMC_svr_model.pkl','wb') as f:
        f.write(res.content)
        f.close()

