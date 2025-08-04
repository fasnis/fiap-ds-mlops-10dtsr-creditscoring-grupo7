import streamlit as st
import requests
import json

# Configuração da página
st.set_page_config(page_title="Consulta de Score - QuantumFinance", layout="centered") 
st.title("Consulta de Score de Crédito")
st.markdown("Preencha os dados do cliente para obter o score estimado.")

# Informação sobre quais features são usadas
st.info("📝 **Modelo simplificado:** Este modelo utiliza apenas 4 campos principais para predição de score de crédito.")

# Função simulada (mock) para prever o score
def mock_score_prediction(data):
    if data["Annual_Income"] > 80000 and data["Monthly_Inhand_Salary"] > 7000:
        return 900, "Muito Baixo"
    elif data["Annual_Income"] > 40000:
        return 700, "Baixo"
    else:
        return 500, "Moderado"

# Função para chamada real da API (exemplo com requests)
def call_real_api(data_dict):
    url = "https://y5fnbkvuc7.execute-api.us-east-1.amazonaws.com/prod/predict"
    headers = {
        "x-api-key": "Q5KZwt1B9c48VPynBfLUl6URsGBQxA5s3aE0QYMz",
        "Content-Type": "application/json"
    }

    # The model expects exactly 4 features in this order:
    # Age, Annual_Income, Monthly_Inhand_Salary, Num_Bank_Accounts
    feature_values = [
        data_dict["Age"], 
        data_dict["Annual_Income"], 
        data_dict["Monthly_Inhand_Salary"], 
        data_dict["Num_Bank_Accounts"]
    ]
    payload = {"data": feature_values}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        # Parse the nested response structure
        if result.get("statusCode") == 200:
            body = json.loads(result.get("body", "{}"))
            raw_prediction = body.get("prediction", 0)
            
            # Convert the raw prediction to a credit score range (300-850)
            # Normalize and map to credit score range
            # Assuming the raw prediction represents some form of creditworthiness
            if raw_prediction > 100000:
                score = 800 + min(50, (raw_prediction - 100000) / 10000)  # High range 800-850
            elif raw_prediction > 50000:
                score = 650 + (raw_prediction - 50000) / 1000  # Mid-high range 650-800
            elif raw_prediction > 20000:
                score = 500 + (raw_prediction - 20000) / 600   # Mid range 500-650
            else:
                score = 300 + raw_prediction / 100  # Low range 300-500
            
            score = max(300, min(850, int(score)))  # Ensure score is within valid range
            
            if score > 700:
                risco = "Baixo"
            elif score > 500:
                risco = "Médio"
            else:
                risco = "Alto"

            return score, risco
        else:
            return 0, f"Erro na API: {result.get('body', 'Unknown error')}"

    except Exception as e:
        return 0, f"Erro na API: {e}"

# Formulário manual
st.subheader("Preenchimento Manual")

with st.form("manual_input"):
    Age = st.number_input("Idade", min_value=18, max_value=100, value=33)
    Annual_Income = st.number_input("Renda Anual (R$)", min_value=0, max_value=500000, value=50000)
    Monthly_Inhand_Salary = st.number_input("Salário Mensal (R$)", min_value=0.0, max_value=100000.0, value=4166.0)
    Num_Bank_Accounts = st.number_input("Nº de Contas Bancárias", min_value=0, max_value=20, value=3)

    submitted = st.form_submit_button("Consultar Score")

    if submitted:
        input_data = {
            "Age": Age,
            "Annual_Income": Annual_Income,
            "Monthly_Inhand_Salary": Monthly_Inhand_Salary,
            "Num_Bank_Accounts": Num_Bank_Accounts
        }

        with st.spinner("Consultando score..."):
            #score, risco = mock_score_prediction(input_data)
            # SUBSTITUIR POR CHAMADA REAL DA API
            score, risco = call_real_api(input_data)
        st.success("Consulta realizada com sucesso!")
        st.markdown(f"""
        ### Resultado:
        - **Score de Crédito:** {score}  
        - **Nível de Risco:** {risco}
        """)
