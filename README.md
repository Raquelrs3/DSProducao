# Previsão de Vendas das Lojas Rossmann
![Rossmann_capa](https://user-images.githubusercontent.com/98356094/156845692-d2aaf2be-b4f1-43df-a7ee-2b9a719a5c80.jpeg)

Este é um projeto realizado com dados públicos disponibilizados pela empresa na plataforma do [KAGGLE](https://www.kaggle.com/c/rossmann-store-sales).


## 1. Problema de Negócio
O CFO da empresa, por meio de uma reunião com os gerentes de loja, requisitou a eles que trouxessem uma previsão diária de vendas das próximas seis semanas.


## 2. Entendimento do Negócio
#### Motivação
o CFO requisitou essa solução durante uma reunião de resultados mensais.

#### Causa Raiz do Problema
Investimento em reforma das lojas.

#### Quem é o Stakeholder
o CFO da Rossmann.

#### Formato da Solução
* Vendas diárias em R$, nas próximas 6 semanas,
* Problema de predição,
* Time series, regressão...,
* Predições acessadas via celular.
 
 
## 3. Metodologia de Desenvolvimento do Projeto
 O projeto foi desenvolvido através da técnica CRISP-DM
 * Versão END-TO_END da solução,
 * Velocidade na entrega de valor,
 * Mapeamento de todos os possíveis problems.


##### Passo 01 - Descrição dos dados: Conhecimento dos dados, tipos, métricas estatísticas para identificar outliers, analise das métricas estatísticas e ajustes em features do dataset (preenchimento de NA's).


##### Passo 02 - Feature Engineering: Desenvolvimento de mapa mental para analisar o fenômeno, as variáveis e os principais aspectos que impactam cada uma delas. 


##### Passo 03 - Filtragem dos dados: Filtragem das linhas e excluir as colunas que não são relevantes para o modelo ou não fazem parte do escopo do negócio. EX: Dias em que as lojas estavam fevhadas ou inoperantes.


##### Passo 04 - Análise Exploratória dos dados: Exploração dos dados para encontrar insights.


##### Passo 05 - Preparação dos dados: Preparação para as aplicações de modelos de machine learning.


##### Passo 06 - Seleção de Features: Seleção dos melhores atributos para treinar o modelo. Utilizamos o algoritmo Boruta para essa seleção.


##### Passo 07 - Modelagem de Machine Learning: Foram realizados testes e treinamentos de alguns modelos de machine learning, para possibilitar a comparação da performance e escolha do modelo ideal para o projeto. Foi utilizada a técnica de Cross Validation para garantir a performance real sobre os dados selecionados.


##### Passo 08 - Hyperparameter Fine Tunning: Análise pelo método Random Search, em cima do algoritmo escolhido XBoost, para escolha dos melhores valores de cada parâmetro do modelo.


##### Passo 09 - Tradução e interpretação de erros: Aqui entendemos a performance do modelo para comunicar ao CFO quanto em dinheiro o modelo retornará à empresa. Foram usadas as métricas: MAE (Mean Absolute Error), MAPE (Mean Absolute Percentage Error) e RMSE (Root Mean Squared Error).


##### Passo 10 - Deploy do modelo em produção: Publicação em um ambiente de nuvem. Foi escolhida a plataforma Heroku.


##### Passo 11 - Bot do Telegram: Aqui realizamos a criação do bot no Telegram, o qual possibilita a consulta das previsões em tempo real.


## 4. Entendendo os Dados
* Dados disponibilizados pela empresa na plataforma do [Kaggle](https://www.kaggle.com/c/rossmann-store-sales) 

| VARIÁVEL  |  DEFINIÇÃO  |
| ------------------- | ------------------- |
|  Id	 |  Um Id que representa uma tupla (Store, Date) dentro do conjunto de testes
|  Store |  Um ID exclusivo para cada loja 
|Sales	|O volume de negócios para um determinado dia.|
|Customers	|O número de clientes em um determinado dia.|
|Open|Um indicador para saber se a loja estava aberta: 0 = fechado, 1 = aberto|
|State Holiday	|Indica um feriado estadual. Normalmente todas as lojas, com poucas exceções, estão fechadas nos feriados estaduais. Observe que todas as escolas estão fechadas nos feriados e fins de semana. a = feriado, b = feriado da páscoa, c = natal, 0 = nenhum.|
|School Holiday	|Indica se a (Loja, Data) foi afetada pelo fechamento de escolas públicas.|
|Store Type	|Diferencia entre 4 modelos de loja diferentes: a, b, c, d|
|Assortment	|Descreve um nível de sortimento: a = básico, b = extra, c = estendido.|
|Competition Distance|Distância em metros até a loja concorrente mais próxima.|
|Competition Open Since [Month/Year]	|Fornece o ano e o mês aproximados em que o concorrente mais próximo foi aberto.|
|Promo|Indica se uma loja está executando uma promoção naquele dia.|
|Promo2|Promo2 é uma promoção contínua e consecutiva para algumas lojas: 0 = a loja não está participando, 1 = a loja está participando.|
|Promo2 Since[Year/Week]	|Descreve o ano e a semana do calendário em que a loja começou a participar do Promo2|
|Promo Interval	|Descreve os intervalos consecutivos em que a Promo2 é iniciada, nomeando os meses em que a promoção é iniciada novamente. Por exemplo, "fevereiro, maio, agosto, novembro" significa que cada rodada começa em fevereiro, maio, agosto, novembro de qualquer ano para essa loja.|


## 5. Principais Insights

**Hipótese 1**
Lojas com maior sortimentos deveriam vender mais.
falso lojas com maior sortimento(assortment) vendem menos.

![Hipotese1 0](https://user-images.githubusercontent.com/98356094/156849829-138a0461-4e1b-439f-9894-8d5705d2c208.jpg)
![Hipotese1 1](https://user-images.githubusercontent.com/98356094/156849711-63eb4fe8-6ac6-413e-88ce-358cb0ae254e.jpg)
![Hipotese1 2](https://user-images.githubusercontent.com/98356094/156849731-b2ec2960-4fa7-491a-bb8d-c9f19c6312a0.jpg)


**Hipótese 2**
Lojas com promoções ativas por mais tempo deveriam vender mais.
falso lojas com promoções ativas por mais tempo vendem menos, depois de um certo periodo de promoção.

![Hipotese2 0](https://user-images.githubusercontent.com/98356094/156849766-a14e9a77-883f-4018-bd3d-1a29f5d84b52.jpg)


**Hipótese 3**
Lojas com competidores mais próximos deveriam vender menos.
falso lojas com competidores mais próximos vendem mais.

![Hipotese3 0](https://user-images.githubusercontent.com/98356094/156849795-af360416-d086-4981-aed1-a7663b1fea77.jpg)


## 6. Performance do Modelo

A estratégia foi usar modelos lineares com o propósito de relacionar duas variáveis (resposta e explicativa) e também modelos não lineares que permitem ajustes de relações mais complexas. Desta forma, respectivamente, podemos determinar se as médias dos grupos são diferentes e as causas de variação para entender o comportamento dessas variáveis, como também, fazer predições fora do domínio observado de uma variável(x).

Para a realização desta etapa do projeto, foram aplicados os seguintes modelos:

* Modelos Lineares
* Média,
* Linear Regression,
* Linear Regression Regularized.
* Modelos Não Lineares
* Random Forest Regressor,
* XGBoost Regressor.


### Comparação da performance dos modelos

![Screen Shot 2022-03-04 at 18 41 23](https://user-images.githubusercontent.com/98356094/156845864-023e007d-e6db-4b7d-8781-2a01a7d215c7.png)


### Performance final do modelo escolhido após Hyperparameter Fine Tuning

![Screen Shot 2022-03-04 at 18 41 12](https://user-images.githubusercontent.com/98356094/156845917-e240bc38-1e36-44d2-83bf-c56e8e4cd7a2.png)


## 7. Resultado Final
Obtivemos bons resultados na previsão de vendas, o qual o CFO da empresa terá acesso por meio de um BOT pelo TELEGRAM.
A performance do modelo pode ser constatada na análise da relação entre as vendas e as predições:

![MachineLearningPerformance](https://user-images.githubusercontent.com/98356094/156846108-a02dafa3-2c7b-455e-ad34-3e5b43add4fc.jpg)


Grande parte das lojas tiveram valores do erro MAPE próximo do erro modelo proposto.
MAPE erro 0.095

![BusinessPerformance](https://user-images.githubusercontent.com/98356094/156846172-c910cded-5774-4323-86f7-9838b7b0804b.jpg)


Seguem os resultados do modelo conforme o melhor e o pior cenário
 
![Screen Shot 2022-03-04 at 18 40 54](https://user-images.githubusercontent.com/98356094/156845965-cabfb56d-7281-44e7-bbbf-04f0750c22e3.png)


## - Conclusão
 
As vendas para as próximas seis semanas estão sendo projetadas com sucesso. Sendo assim, o CFO poderá consultar em tempo real e de qualquer lugar as predições das vendas, por meio do Bot do telegram, podendo extrair informações do rendimento das lojas para melhor decisão sobre o budget necessãrio para as reformas de suas filiais.


**Como funciona o BOT:**
**Para acessar os resultados da previsão de vendas das lojas, basta acessar sua conta do telegram e enviar uma mensagem com o número da loja.**
**Ex: /22, /57, /100. [Clique aqui](https://t.me/rossmannr_bot) para fazer o teste**
