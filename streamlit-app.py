import streamlit as st
import requests

# Configuração da página
st.set_page_config(page_title="Consulta de Score - QuantumFinance", layout="centered") 
st.title("Consulta de Score de Crédito")
st.markdown("Preencha os dados do cliente para obter o score estimado.")

# Função simulada (mock) para prever o score
def mock_score_prediction(data):
    if data["Annual_Income"] > 80000 and data["Monthly_Inhand_Salary"] > 7000:
        return {"credit_score": "900", "risco": "Muito Baixo"}
    elif data["Annual_Income"] > 40000:
        return {"credit_score": "700", "risco": "Baixo"}
    else:
        return {"credit_score": "500", "risco": "Moderado"}

# Função para chamada real da API (exemplo com requests)
def call_real_api(data_dict):
    import requests

    url = "https://y5fnbkvuc7.execute-api.us-east-1.amazonaws.com/prod/predict"
    headers = {
        "x-api-key": "Q5KZwt1B9c48VPynBfLUl6URsGBQxA5s3aE0QYMz",
        "Content-Type": "application/json"
    }

    payload = {"data": list(data_dict.values())}

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()

        score = result.get("credit_score", 0)

        if score > 700:
            risco = "Baixo"
        elif score > 500:
            risco = "Médio"
        else:
            risco = "Alto"

        return score, risco

    except Exception as e:
        return None, f"Erro na API: {e}"
# Lista de campos esperados
expected_fields = [
    "Age", "Annual_Income", "Monthly_Inhand_Salary", "Num_Bank_Accounts", "Num_Credit_Card", "Interest_Rate",
    "Num_of_Loan", "Delay_from_due_date", "Num_of_Delayed_Payment", "Changed_Credit_Limit",
    "Num_Credit_Inquiries", "Credit_Utilization_Ratio", "Total_EMI_per_month", 
    "Amount_invested_monthly", "Monthly_Balance", "Credit_History_Age_Months"
]

# Upload CSV
st.subheader("Opção 1: Upload de Arquivo CSV")
uploaded_file = st.file_uploader("Faça upload do arquivo CSV com os dados dos clientes", type=["csv"])

if uploaded_file:
    try:
        df = pd.read_csv(uploaded_file)

        if not set(expected_fields).issubset(df.columns):
            st.error("O CSV deve conter as colunas esperadas no formato correto.")
        else:
            with st.spinner("Processando..."):
                #df[["credit_score", "risco"]] = df.apply(mock_score_prediction, axis=1, result_type="expand")
                #SUBSTITUIR POR CHAMADA REAL DA API
                df[["credit_score", "risco"]] = df.apply(lambda row: call_real_api(row.to_dict()), axis=1, result_type="expand")

            st.success("Dados processados com sucesso!")
            st.dataframe(df[expected_fields + ["credit_score", "risco"]])

            csv_result = df.to_csv(index=False).encode("utf-8")
            st.download_button("Baixar resultado", csv_result, "resultado_score.csv", "text/csv")

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")

# Separador
st.markdown("---")

# Formulário manual
st.subheader("Opção 2: Preenchimento Manual")

with st.form("manual_input"):
    Age = st.number_input("Idade", 18, 100, 33)
    Annual_Income = st.number_input("Renda Anual (R$)", 0, 500000, 50000)
    Monthly_Inhand_Salary = st.number_input("Salário Mensal (R$)", 0.0, 100000, 4166)
    Num_Bank_Accounts = st.number_input("Nº de Contas Bancárias", 0, 20, 3)
    Num_Credit_Card = st.number_input("Nº de Cartões de Crédito", 0, 10, 2)
    Interest_Rate = st.number_input("Taxa de Juros (%)", 0.0, 50.0, 12.5)
    Num_of_Loan = st.number_input("Nº de Empréstimos", 0, 20, 2)
    Delay_from_due_date = st.number_input("Dias de Atraso Médio", 0, 100, 15)
    Num_of_Delayed_Payment = st.number_input("Qtd. Pagamentos em Atraso", 0, 50, 8)
    Changed_Credit_Limit = st.number_input("Variação no Limite de Crédito (%)", -100.0, 100.0, 10.5)
    Num_Credit_Inquiries = st.number_input("Nº Consultas de Crédito", 0, 20, 3)
    Credit_Utilization_Ratio = st.number_input("Utilização do Crédito (%)", 0.0, 100.0, 30.5)
    Total_EMI_per_month = st.number_input("EMI Total Mensal (R$)", 0.0, 20000.0, 850.0)
    Amount_invested_monthly = st.number_input("Investimento Mensal (R$)", 0.0, 10000.0, 200.0)
    Monthly_Balance = st.number_input("Saldo Médio Mensal (R$)", -10000.0, 10000.0, 500.0)
    Credit_History_Age_Months = st.number_input("Histórico de Crédito (meses)", 0, 360, 180)

    submitted = st.form_submit_button("Consultar Score")

    if submitted:
        input_data = {
            "Age": Age,
            "Annual_Income": Annual_Income,
            "Monthly_Inhand_Salary": Monthly_Inhand_Salary,
            "Num_Bank_Accounts": Num_Bank_Accounts,
            "Num_Credit_Card": Num_Credit_Card,
            "Interest_Rate": Interest_Rate,
            "Num_of_Loan": Num_of_Loan,
            "Delay_from_due_date": Delay_from_due_date,
            "Num_of_Delayed_Payment": Num_of_Delayed_Payment,
            "Changed_Credit_Limit": Changed_Credit_Limit,
            "Num_Credit_Inquiries": Num_Credit_Inquiries,
            "Credit_Utilization_Ratio": Credit_Utilization_Ratio,
            "Total_EMI_per_month": Total_EMI_per_month,
            "Amount_invested_monthly": Amount_invested_monthly,
            "Monthly_Balance": Monthly_Balance,
            "Credit_History_Age_Months": Credit_History_Age_Months
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
