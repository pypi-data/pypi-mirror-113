import os 

current_file_path = os.getcwd()
AI_Model_path = os.path.join(current_file_path,'AI_model')

'''
確認現在的路徑與要下載的檔案路徑
print(f"current_file_path: {current_file_path}")
print(f"AI_Model_path:{AI_Model_path}")
'''


def create_dir(dirpath):
    os.mkdir(dirpath)

def check_dir(dirpath):
    return os.path.isdir(dirpath)

def check_file(filepath):
    return os.path.isfile(filepath)

if check_dir(AI_Model_path)==False:
    create_dir(AI_Model_path)
    import requests    
    url = 'https://976658e65208.ngrok.io/static/AI_Model/HMC_svr_model.pkl'
    res = requests.get(url)
    with open(AI_Model_path+'/HMC_svr_model.pkl','wb') as f:
        f.write(res.content)
        f.close()

else:
    pass
