# biblioteca que tenha interface web (flask)
import pickle
import pandas as pd
from flask             import Flask, request, Response
from rossmann.Rossmann import Rossmann 

# Loading model
model = pickle.load(open("/Users/raquelrocha/Documents/ProjetosComunidadeDS/DSProducao/model/model_rossmann2.pkl","rb"))

# Initialize API
app = Flask(__name__)

# criar a rota, url que irá receber dados as requests
@app.route("/rossmann/predict", methods = ["POST"]) # pode ser Post(recebe metodos que envia algum dado para receber) ou Get( pede alguma coisa)
def rossmann_predict():
    test_json = request.get_json() #aqui pegaremos o dado, por isso usamos get

    # teste se está funcionando o teste_jason
    if test_json: # there is data
        if isinstance (test_json, dict): #unique example
            test_raw = pd.DataFrame (test_json, index = [0]) # assim funciona para apenas 1 linha e json
        
        else: #multiple example
            test_raw = pd.DataFrame (test_json, columns = test_json[0].keys()) #se houver várias linhas será dessa forma
    
        # Instantiate Rossmann Class (criar uma cópia daquela classe)
        # fazendo isso temos acesso a todos os métodos que implementou na classe
        pipeline = Rossmann()
    
        #data cleaning
        df1 = pipeline.data_cleaning(test_raw) # test_raw pq queremos os dados originas e não o transformado
        
        #feature engineering
        df2 = pipeline.feature_engineering(df1)
        
        #data preparation
        df3 = pipeline.data_preparation(df2)
        
        #prediction
        df_response = pipeline.get_prediction(model, test_raw, df3)
        
        return df_response
    
    else:
        return Response("{}", status = 200, minetype = "application/json")
    
# para funcionar a API temos que fazer um IF
if __name__ == "__main__":
    app.run("0.0.0.0") #numeração é o localhost (rodando na minha maquina)
    
