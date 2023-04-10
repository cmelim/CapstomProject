from flask import Flask, render_template, request,  redirect, url_for
import joblib
import os
import pandas as pd
import numpy as np
import csv
import subprocess
import ipaddress
from os.path import join, dirname, realpath


HOST_NAME = "localhost"
HOST_PORT = 80
 
app = Flask(__name__)

#app.config['UPLOAD_FOLDER'] = 'C:\\CapstomProject\\static\\files'

UPLOAD_FOLDER = 'static/files'
MODEL_FOLDER = 'models'
app.config['UPLOAD_FOLDER'] =  UPLOAD_FOLDER

model_KNN = joblib.load(os.path.dirname(__file__)+'\models\KNN_trained_model.pkl')
model_AB_trained_model= joblib.load(os.path.dirname(__file__)+'\models\AB_trained_model.pkl')
model_DT_trained_model = joblib.load(os.path.dirname(__file__)+'\models\DT_trained_model.pkl')
model_GB_trained_model = joblib.load(os.path.dirname(__file__)+'\models\GB_trained_model.pkl')
model_LG_trained_model = joblib.load(os.path.dirname(__file__)+'\models\LG_trained_model.pkl')
#model_NB_trained_model = joblib.load(os.path.dirname(__file__)+'\models\NB_trained_model.pkl')
model_LGBM_trained_model = joblib.load(os.path.dirname(__file__)+'\models\LGBM_trained_model.pkl')
model_RF_trained_model = joblib.load(os.path.dirname(__file__)+'\models\RF_trained_model.pkl')
model_SVM_trained_model = joblib.load(os.path.dirname(__file__)+'\models\SVM_trained_model.pkl')




@app.route('/')
def home():
    #return render_template('form.html')
    return render_template('uploadFile.html')
 
@app.route('/predict', methods=['POST'])
def predict():
    input_data = [float(x) for x in request.form.values()]
    #prediction[] = "Caca" #model.predict([input_data])
    prediction= [1, 2, 3] 
    return render_template('result.html', prediction=prediction[0])


# Get the uploaded files
@app.route("/", methods=['POST'])
def uploadFiles():
      valuesForm =request.form.values()
      opctionSelect = request.form.get('selecctalgoritm')
      print('os.path.dirname(__file__) ------ 0 ',os.path.dirname(__file__))
      
      totalRows =0
      totalMalicuisRows = 0
      predictionModelName= getModelStringName(int(opctionSelect))
      title = predictionModelName + " Model Training Results" 
      # get the uploaded file
      #print ("uploadFiles POST !!!!")
      uploaded_file = request.files['file']
      print (uploaded_file.filename)
      if uploaded_file.filename != '':
           file_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
          # set the file path
           uploaded_file.save(file_path)
           listIpMalicius,totalRows = parseCSV(file_path,int(opctionSelect))
           totalMalicuisRows = len(listIpMalicius)
          # save the file
           rows = []
           #print("file_path es ",file_path)
           with open(file_path) as file2:
            reader = csv.reader(file2)   
             
            return render_template("TableResponse.html", listIpMalicius=listIpMalicius, file_path=file_path,totalRows=totalRows, totalMalicuisRows=len(listIpMalicius),predictionModelName=predictionModelName,title=title )
      #return redirect(url_for('index'))

def parseCSV(filePath,modelToCall):
      blockingIP=[]
      # CVS Column Names
      print ("================  COLUM NAMES =================")      
      col_names = ['Flow ID','Src IP','Src Port','Dst IP','Dst Port','Protocol','Timestamp','Flow Duration','Tot Fwd Pkts','Tot Bwd Pkts','TotLen Fwd Pkts','TotLen Bwd Pkts','Fwd Pkt Len Max','Fwd Pkt Len Min','Fwd Pkt Len Mean','Fwd Pkt Len Std','Bwd Pkt Len Max','Bwd Pkt Len Min','Bwd Pkt Len Mean','Bwd Pkt Len Std','Flow Byts/s','Flow Pkts/s','Flow IAT Mean','Flow IAT Std','Flow IAT Max','Flow IAT Min','Fwd IAT Tot','Fwd IAT Mean','Fwd IAT Std','Fwd IAT Max','Fwd IAT Min','Bwd IAT Tot','Bwd IAT Mean','Bwd IAT Std','Bwd IAT Max','Bwd IAT Min','Fwd PSH Flags','Bwd PSH Flags','Fwd URG Flags','Bwd URG Flags','Fwd Header Len','Bwd Header Len','Fwd Pkts/s','Bwd Pkts/s','Pkt Len Min','Pkt Len Max','Pkt Len Mean','Pkt Len Std','Pkt Len Var','FIN Flag Cnt','SYN Flag Cnt','RST Flag Cnt','PSH Flag Cnt','ACK Flag Cnt','URG Flag Cnt','CWE Flag Count','ECE Flag Cnt','Down/Up Ratio','Pkt Size Avg','Fwd Seg Size Avg','Bwd Seg Size Avg','Fwd Byts/b Avg','Fwd Pkts/b Avg','Fwd Blk Rate Avg','Bwd Byts/b Avg','Bwd Pkts/b Avg','Bwd Blk Rate Avg','Subflow Fwd Pkts','Subflow Fwd Byts','Subflow Bwd Pkts','Subflow Bwd Byts','Init Fwd Win Byts','Init Bwd Win Byts','Fwd Act Data Pkts','Fwd Seg Size Min','Active Mean','Active Std','Active Max','Active Min','Idle Mean','Idle Std','Idle Max','Idle Min','Label']

      # Use Pandas to parse the CSV file
      csvData = pd.read_csv(filePath,names=col_names, header=None)
      # Loop through the Rows
      data = 1
      totalRows = len(csvData)
      input_data =[]
      
      for i,row in csvData.iterrows():
        #   Column            Non-Null Count  Dtype  
        #---  ------            --------------  -----  
        #0   Src IP            386 non-null    object   Ok
        #1   Dst IP            386 non-null    object   OK
        #2   Protocol          386 non-null    int64    OK
        #3   Pkt Len Min       386 non-null    float64  OK
        #4   Bwd Pkt Len Std   386 non-null    float64  OK
        #5   Pkt Len Std       386 non-null    float64  OK
        #6   Bwd Seg Size Avg  386 non-null    float64  OK
        #7   Bwd Pkt Len Mean  386 non-null    float64  OK
        #8   Bwd Pkt Len Max   386 non-null    float64  OK
        #9   Pkt Len Max       386 non-null    float64  OK
        #10  Bwd Pkt Len Min   386 non-null    float64  OK
        #11  Pkt Len Mean      386 non-null    float64
        #12  Pkt Len Var       386 non-null    float64
        #13  Pkt Size Avg      386 non-null    float64
        #14  Fwd IAT Std       386 non-null    float64
        #15  Idle Max          386 non-null    float64
       
        if(i>0):
            input_data = [int(ipaddress.IPv4Address(row['Src IP'])),int(ipaddress.IPv4Address(row['Dst IP'])),
                          int(float(row['Protocol'])),
                          int(float(row['Pkt Len Min'])),int(float(row['Bwd Pkt Len Std'])),int(float(row['Pkt Len Std'])),
                          int(float(row['Bwd Seg Size Avg'])),int(float(row['Bwd Pkt Len Mean'])),int(float(row['Bwd Pkt Len Max'])),
                          int(float(row['Pkt Len Max'])),int(float(row['Bwd Pkt Len Min'])),int(float(row['Pkt Len Mean'])),
                          int(float(row['Pkt Len Var'])),int(float(row['Pkt Size Avg'])),int(float(row['Fwd IAT Std']))]
            #print("[",i,"]", input_data, "\n")
            
            #prediction = model_KNN.predict([input_data])
            if(modelToCall == 0):
                prediction = model_KNN.predict([input_data])
            elif(modelToCall == 1):    
                prediction = model_AB_trained_model.predict([input_data])
            elif(modelToCall == 2):    
                prediction = model_DT_trained_model.predict([input_data])
            elif(modelToCall == 3):    
                prediction = model_GB_trained_model.predict([input_data])
            elif(modelToCall == 4):
                prediction = model_LG_trained_model.predict([input_data])
            #elif(modelToCall == 5):
            #    prediction = model_NB_trained_model.predict([input_data])
            elif(modelToCall == 6):
                prediction = model_LGBM_trained_model.predict([input_data])
            elif(modelToCall == 7):
                prediction = model_RF_trained_model.predict([input_data])
            else:
                prediction = model_SVM_trained_model.predict([input_data])
            #print("Prediction *****    :",prediction)           
            
            if(prediction[0] == 1):
                       
                # ansibleBlockIp(row['Src IP']) 
                #Change info format to snumber to ip string
                input_data[0] =row['Src IP']
                input_data[1] =row['Dst IP']              
                blockingIP.append(input_data)

        #data = i
        input_data = []
      #listIpTobloq(blockingIP)         
      return blockingIP,totalRows
def parseCSVCallModel(filePath,modelToCall):
      blockingIP=[]     
      col_names = ['Flow ID','Src IP','Src Port','Dst IP','Dst Port','Protocol','Timestamp','Flow Duration','Tot Fwd Pkts','Tot Bwd Pkts','TotLen Fwd Pkts','TotLen Bwd Pkts','Fwd Pkt Len Max','Fwd Pkt Len Min','Fwd Pkt Len Mean','Fwd Pkt Len Std','Bwd Pkt Len Max','Bwd Pkt Len Min','Bwd Pkt Len Mean','Bwd Pkt Len Std','Flow Byts/s','Flow Pkts/s','Flow IAT Mean','Flow IAT Std','Flow IAT Max','Flow IAT Min','Fwd IAT Tot','Fwd IAT Mean','Fwd IAT Std','Fwd IAT Max','Fwd IAT Min','Bwd IAT Tot','Bwd IAT Mean','Bwd IAT Std','Bwd IAT Max','Bwd IAT Min','Fwd PSH Flags','Bwd PSH Flags','Fwd URG Flags','Bwd URG Flags','Fwd Header Len','Bwd Header Len','Fwd Pkts/s','Bwd Pkts/s','Pkt Len Min','Pkt Len Max','Pkt Len Mean','Pkt Len Std','Pkt Len Var','FIN Flag Cnt','SYN Flag Cnt','RST Flag Cnt','PSH Flag Cnt','ACK Flag Cnt','URG Flag Cnt','CWE Flag Count','ECE Flag Cnt','Down/Up Ratio','Pkt Size Avg','Fwd Seg Size Avg','Bwd Seg Size Avg','Fwd Byts/b Avg','Fwd Pkts/b Avg','Fwd Blk Rate Avg','Bwd Byts/b Avg','Bwd Pkts/b Avg','Bwd Blk Rate Avg','Subflow Fwd Pkts','Subflow Fwd Byts','Subflow Bwd Pkts','Subflow Bwd Byts','Init Fwd Win Byts','Init Bwd Win Byts','Fwd Act Data Pkts','Fwd Seg Size Min','Active Mean','Active Std','Active Max','Active Min','Idle Mean','Idle Std','Idle Max','Idle Min','Label']
      # Use Pandas to parse the CSV file
      csvData = pd.read_csv(filePath,names=col_names, header=None)
      # Loop through the Rows
      data = 1
      input_data =[]      
      for i,row in csvData.iterrows(): 
        #---  ------            --------------  -----  
        #0   Src IP            386 non-null    object   Ok
        #1   Dst IP            386 non-null    object   OK
        #2   Protocol          386 non-null    int64    OK
        #3   Pkt Len Min       386 non-null    float64  OK
        #4   Bwd Pkt Len Std   386 non-null    float64  OK
        #5   Pkt Len Std       386 non-null    float64  OK
        #6   Bwd Seg Size Avg  386 non-null    float64  OK
        #7   Bwd Pkt Len Mean  386 non-null    float64  OK
        #8   Bwd Pkt Len Max   386 non-null    float64  OK
        #9   Pkt Len Max       386 non-null    float64  OK
        #10  Bwd Pkt Len Min   386 non-null    float64  OK
        #11  Pkt Len Mean      386 non-null    float64
        #12  Pkt Len Var       386 non-null    float64
        #13  Pkt Size Avg      386 non-null    float64
        #14  Fwd IAT Std       386 non-null    float64
        #15  Idle Max          386 non-null    float64
        
        if(i>0):
            #ipFrom = convertIPtoMOdel(row['Src IP'])
            print("-------------------------------------------->  ",row['Src IP'].apply(lambda x: int(ipaddress.IPv4Address(x))))
            input_data = [int(ipaddress.IPv4Address(row['Src IP'])),int(ipaddress.IPv4Address(row['Dst IP'])),
                          int(float(row['Protocol'])),
                          int(float(row['Pkt Len Min'])),int(float(row['Bwd Pkt Len Std'])),int(float(row['Pkt Len Std'])),
                          int(float(row['Bwd Seg Size Avg'])),int(float(row['Bwd Pkt Len Mean'])),int(float(row['Bwd Pkt Len Max'])),
                          int(float(row['Pkt Len Max'])),int(float(row['Bwd Pkt Len Min'])),int(float(row['Pkt Len Mean'])),
                          int(float(row['Pkt Len Var'])),int(float(row['Pkt Size Avg'])),int(float(row['Fwd IAT Std']))]
            if(modelToCall == 0):
                prediction = model_KNN.predict([input_data])
            elif(modelToCall == 1):    
                prediction = model_AB_trained_model.predict([input_data])
            elif(modelToCall == 2):    
                prediction = model_DT_trained_model.predict([input_data])
            elif(modelToCall == 3):    
                prediction = model_GB_trained_model.predict([input_data])
            elif(modelToCall == 4):
                prediction = model_LG_trained_model.predict([input_data])
            elif(modelToCall == 5):
                prediction = model_NB_trained_model.predict([input_data])
            elif(modelToCall == 6):
                prediction = model_LGBM_trained_model.predict([input_data])
            elif(modelToCall == 7):
                prediction = model_RF_trained_model.predict([input_data])
            else:
                prediction = model_SVM_trained_model.predict([input_data])            

            prediction = model_KNN.predict([input_data])
            print("Prediction     :",prediction)  
            if(prediction[0] == 1):
                print("row['Src IP'] ",row['Src IP'])
                ansibleBlockIp(row['Src IP'])
                blockingIP = blockingIP + [row['Src IP']]        
        input_data = []
      listIpTobloq(blockingIP)  
      #print(data)
      return blockingIP
def  ansibleBlockIp(ip_address):
    print("Bloque de ip windows ip_address ",ip_address)
    playbook_in = 'C:\CapstomProject\playbook.yml'
    cmd = ['ansible-playbook', playbook_in, '-e', 'ip_address={}'.format(ip_address)]
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout, stderr = p.communicate()
    if p.returncode == 0:
        print('El playbook se ha ejecutado correctamente.')
    else:
        print('Ha ocurrido un error al ejecutar el playbook: {}'.format(stderr.decode()))

def listIpTobloq(listip):
    for ip in listip:
        print(ip)
        #ansibleBlockIp(ip)
        #blockingIP = blockingIP + [ip]
        #(ip)

def getModelStringName(modelToCall):
    print("*****************   getModelStringName",modelToCall)
    if(modelToCall == 0):
        return 'KNN'
    elif(modelToCall == 1):
        return 'AB'
    elif(modelToCall == 2):
        return 'DT'
    elif(modelToCall == 3):
        return 'GB'
    elif(modelToCall == 4):
        return 'LG'
    elif(modelToCall == 5):
        return 'NB'
    elif(modelToCall == 6):
        return 'LGBM'
    elif(modelToCall == 7):
        return 'RF'
    else:
        return 'SVM'

if __name__ == '__main__':
    app.run(debug=True)