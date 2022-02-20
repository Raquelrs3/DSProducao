#Aqui estamos fazendo a rossmann class limpando os dados  do passo 1, 2, 3, 5 e 6
#pegamos todas as transformações
import pickle
import inflection
import pandas as pd
import numpy as np
import math
import datetime

class Rossmann(object):
    def __init__(self): # construtor para ser a primeira função a rodar
        self.home_path="/Users/raquelrocha/Documents/ProjetosComunidadeDS/DSProducao/" #caminho do projeto, precisa pois ao rodar os codigos abaixo, que não está com o caminho completo ao subir não irá reconhecer
        self.competition_distance_scaler   = pickle.load( open( self.home_path + 'parameter/competition_distance_scaler.pkl', 'rb') ) # self.home_path +  para concatenar
        self.competition_time_month_scaler = pickle.load( open( self.home_path + 'parameter/competition_time_month_scaler.pkl', 'rb') )
        self.promo_time_week_scaler        = pickle.load( open( self.home_path + 'parameter/promo_time_week_scaler.pkl', 'rb') )
        self.year_scaler                   = pickle.load( open( self.home_path + 'parameter/year_scaler.pkl', 'rb') )
        self.store_type_scaler             = pickle.load( open( self.home_path + 'parameter/store_type_scaler.pkl', 'rb') )

        
        
    # aqui chamo o método data_cleaning abro o df1, ele passa a função e retorna um df1 limpo
    def data_cleaning(self, df1):
        
        ## 1.1 Rename Columns
        cols_old = ['Store', 'DayOfWeek', 'Date', 'Open', 'Promo',
                    'StateHoliday', 'SchoolHoliday', 'StoreType', 'Assortment',
                    'CompetitionDistance', 'CompetitionOpenSinceMonth',
                    'CompetitionOpenSinceYear', 'Promo2', 'Promo2SinceWeek',
                    'Promo2SinceYear', 'PromoInterval'] #Sales, tira da lista pois é ele que queremos prever e Customers pois não temos como prever esses dados
        # função para deixar a lista em minúsculo e em snakecase(_)
        snakecase = lambda x: inflection.underscore (x)
        cols_new = list(map(snakecase, cols_old))

        #rename
        df1.columns = cols_new

        ## 1.3 Data Types

        # mudar a data de object para forma de data
        df1["date"] = pd.to_datetime(df1["date"])


        ## 1.5 Fillout NA (Substituindo os dados faltantes)

        #competition_distance colocar 0 no lugar de NA Lambda é assim pq só tem 1 coluna
        df1["competition_distance"] = df1["competition_distance"].apply (lambda x:200000.0 if math.isnan(x) else x)

        #competition_open_since_month aqui aplica assim pq tem mais de uma coluna para analisar (por isso o Axis:1, se fosse axis 0 seria ao longo da linha)
        df1["competition_open_since_month"] = df1.apply(lambda x: x["date"].month if math.isnan( x["competition_open_since_month"]) else x["competition_open_since_month"], axis=1)

        #competition_open_since_year
        df1["competition_open_since_year"] = df1.apply(lambda x: x["date"].year if math.isnan( x["competition_open_since_year"]) else x["competition_open_since_year"], axis=1)

        #promo2_since_week
        df1["promo2_since_week"] = df1.apply(lambda x: x["date"].week if math.isnan( x["promo2_since_week"]) else x["promo2_since_week"], axis=1)

        #promo2_since_year
        df1["promo2_since_year"] = df1.apply(lambda x: x["date"].year if math.isnan( x["promo2_since_year"]) else x["promo2_since_year"], axis=1)


        #promo_interval Inplace=True faz a modificação direto na coluna e Fillna vai preencher com 0
        month_map={1:"Jan", 2:"Fev", 3:"Mar", 4:"Apr", 5:"May", 6:"Jun", 7:"Jul", 8:"Aug", 9:"Sep", 10:"Oct", 11:"Nov", 12:"Dec"}

        df1["promo_interval"].fillna(0, inplace=True)

        #Mapeia a o dicionario dentro da coluna (para saber se está dentro da promoção, se 0 não participa da promoção se 1 participa)
        df1["month_map"] = df1["date"].dt.month.map(month_map)

        df1["is_promo"] = df1[["promo_interval", "month_map"]].apply(lambda x: 0 if x["promo_interval"] == 0 else 1 if x["month_map"] in x["promo_interval"].split(",") else 0, axis=1)


        ## 1.6 Change data Types (Estatística Descritiva)

        #competition
        df1["competition_open_since_month"] = df1["competition_open_since_month"].astype(int)
        df1["competition_open_since_year"] = df1["competition_open_since_year"].astype(int)

        #promo
        df1["promo2_since_week"] = df1["promo2_since_week"].astype(int)
        df1["promo2_since_year"] = df1["promo2_since_year"].astype(int)

        return df1
    

    def feature_engineering(self, df2):
    
    
        # Variáveis a ser derivadas da variavel original Date 
        # year 
        df2["year"] = df2["date"].dt.year

        # month
        df2["month"] = df2["date"].dt.month

        # day
        df2["day"] = df2["date"].dt.day

        # week of year
        df2["week_of_year"] = df2["date"].dt.weekofyear

        # year week (%Y ano, %W semana)
        df2["year_week"] = df2["date"].dt.strftime("%Y-%W")


        # competition since (esta em duas linhas nos dados, devemos juntar elas em uma só) day=1 para coeaçar no dia 1, considerando o mês como um todo
        # método "datetime.datetime( year=x["competition_open_since_year"], month=x["competition_open_since_month"], day=1)"
        # função em cima do método acima "df2.apply(lambda x: datetime.datetime( year=x["competition_open_since_year"], month=x["competition_open_since_month"], day=1)"
        # se der problema de datetime not define, só importar o datetime
        df2["competition_since"] = df2.apply( lambda x: datetime.datetime( year=x["competition_open_since_year"], month=x["competition_open_since_month"], day=1 ), axis=1 )
        # diferença das duas (para conseguir o mês, P.S. subtrai o date comm o q vc quer)
        df2["competition_time_month"] = ((df2["date"] - df2["competition_since"])/30).apply( lambda x: x.days).astype(int)

        # promo since (juntar as duas informações(precisam estar como string),semana e o ano, e depois transformar no mês) (-) é para dar espaço entre as duas informações
        df2["promo_since"] = df2["promo2_since_year"].astype(str) + "-" + df2["promo2_since_week"].astype(str)
        # transformar novamente em data , (x + "-1", "%Y-%W-%w") = formato de resultadoano, semana do ano, semana de domingo a domingo (o w minúsculo)
        df2["promo_since"] = df2["promo_since"].apply(lambda x: datetime.datetime.strptime (x + "-1", "%Y-%W-%w") - datetime.timedelta(days=7))
        #subtrai as duas datas (subtrai o date comm o q vc quer)
        df2["promo_time_week"]=((df2["date"] - df2["promo_since"])/7).apply(lambda x: x.days).astype(int)

        # assortment, usar o apply para colocar em todas as linhas a função lambda, (a=basic, b=extra, c=extended (informações pegas no kaggle))
        df2["assortment"] = df2["assortment"].apply(lambda x: "basic" if x =="a" else "extra" if x =="b" else "extended")

        # state holiday usar o apply para colocar em todas as linhas a função lambda, (a=public holiday, b=easter holiday, c=christmas (informações pegas no kaggle))
        df2["state_holiday"] = df2["state_holiday"].apply(lambda x: "public_holiday" if x =="a" else "easter_holiday" if x =="b" else "christmas" if x=="c" else "regular_day")
        

        # 3.0 Filtragem de Variáveis (Passo 3) Aula11
        ## 3.1 Filtragem das linhas
        ### começa com esse para diminuir volume dos dados que irá trabalhar.
        #p.s aqui trocar os df3 por df2
        # o que iremos filtrar ("open" != 0 "sales" > 0)
        df2 = df2[df2["open"] != 0] # aqui deletou a condição sales

        ## 3.2 Seleção das colunas
        #o que não queremos ("customers", "open", "promo_interval", "month_map")
        cols_drop = ["open","promo_interval", "month_map"] # aqui deletou costumers da lista
        # deletar (classe pandas "drop")
        df2 = df2.drop(cols_drop,axis=1)
        
        return df2
    
    
    def data_preparation(self, df5):

        ## 5.2 Rescaling
        ## trocar todos os rs. mms por self + nome competition time month e restante
        # competition distance
        df5["competition_distance"] = self.competition_distance_scaler.fit_transform( df5[["competition_distance"]].values ) #encontra os parametros da fórmula e aplica nos dados

        # competition time month
        df5["competition_time_month"] = self.competition_time_month_scaler.fit_transform( df5[["competition_time_month"]].values ) #encontra os parametros da fórmula e aplica nos dados

        # promo time week
        df5["promo_time_week"] = self.promo_time_week_scaler.fit_transform( df5[["promo_time_week"]].values ) #encontra os parametros da fórmula e aplica nos dados

        # year
        df5["year"] = self.year_scaler.fit_transform( df5[["year"]].values ) #encontra os parametros da fórmula e aplica nos dados


        ### 5.3.1 Encoding
        # state_holiday - One Hot Encoding
        df5 = pd.get_dummies( df5, prefix=["state_holiday"], columns=["state_holiday"])

        # store_type - Label Encoding
        df5['store_type'] = self.store_type_scaler.fit_transform ( df5["store_type"])

        # assortment - Ordinal Encoding
        assortment_dict = {"basic":1, "extra":2, "extended":3}
        df5["assortment"] = df5["assortment"].map(assortment_dict)

        ### 5.3.3 Nature Transformation

        # month
        df5["month_sin"] = df5["month"].apply(lambda x: np.sin(x * (2. * np.pi/12)))
        df5["month_cos"] = df5["month"].apply(lambda x: np.cos(x * (2. * np.pi/12)))

        # day
        df5["day_sin"] = df5["day"].apply(lambda x: np.sin(x * (2. * np.pi/30)))
        df5["day_cos"] = df5["day"].apply(lambda x: np.cos(x * (2. * np.pi/30)))

        # week of year
        df5["week_of_year_sin"] = df5["week_of_year"].apply(lambda x: np.sin(x * (2. * np.pi/52)))
        df5["week_of_year_cos"] = df5["week_of_year"].apply(lambda x: np.cos(x * (2. * np.pi/52)))

        # day of week
        df5["day_of_week_sin"] = df5["day_of_week"].apply(lambda x: np.sin(x * (2. * np.pi/7)))
        df5["day_of_week_cos"] = df5["day_of_week"].apply(lambda x: np.cos(x * (2. * np.pi/7)))
        
        cols_selected = ['store','promo','store_type','assortment','competition_distance','competition_open_since_month',
                         'competition_open_since_year','promo2','promo2_since_week','promo2_since_year','competition_time_month',
                         'promo_time_week','day_of_week_sin','day_of_week_cos','month_sin','month_cos','day_sin','day_cos',
                         'week_of_year_sin','week_of_year_cos']
        
        print(f"Shape df5: {df5[cols_selected].shape}") # para saber o número de colunas do df5

        return df5[cols_selected]
    
    def get_prediction(self, model, original_data, test_data):
        # prediction
        print(f"Shape test_data: {test_data.shape}") # testar o shape tesr_data
        pred = model.predict(test_data)
        
        # join pred into the original data (para retornar os dados originais)
        original_data["prediction"] = np.expm1(pred)
        
        return original_data.to_json(orient="records", date_format="iso") # transformar em json para subir via API, ISO é para não bagunçar a data
    

