import json
import logging
import joblib  # ou pickle, dependendo de como o modelo foi salvo

# Configuração básica de logging
logging.basicConfig(level=logging.INFO)

# Carregando o modelo e metadados na inicialização do container:
model = joblib.load("model/model.pkl")
with open("model/model_metadata.json", "r") as f:
    metadata = json.load(f)
logging.info("Modelo carregado com sucesso.")
# (Opcional: você pode usar dados de `metadata`, ex: imprimir versão do modelo)
if "model_version" in metadata:
    logging.info(f"Versão do modelo: {metadata['model_version']}")

# Função handler do Lambda
def handler(event, context):
    """
    Manipulador Lambda que será chamado em cada requisição.
    """
    try:
        # Se o evento vier do API Gateway, o corpo estará em event['body']
        body = json.loads(event['body'])
    except (KeyError, TypeError):
        # Caso event já seja um dicionário (ex.: chamada direta/local)
        body = event

    # Log da entrada recebida
    logging.info(f"Entrada recebida: {body}")

    # **Pré-processamento**: prepare os dados de entrada para o modelo
    # Supondo que o JSON de entrada tenha um campo "data" contendo as features
    input_data = body.get("data")
    # Exemplo: converter para formato esperado pelo modelo (lista dentro de lista para uma amostra)
    # Aqui assumimos que input_data já é uma lista/array de valores numéricos
    data_for_prediction = [input_data]

    # (Você pode adicionar passos de normalização, codificação, etc., conforme necessário usando metadata)

    # **Inferência**: use o modelo carregado para prever resultados
    prediction = model.predict(data_for_prediction)
    output = prediction.tolist()  # converter numpy array para list, se necessário

    # Log da saída produzida
    logging.info(f"Predição gerada: {output}")

    # Monta a resposta HTTP (formato compatível com Lambda Proxy Integrations)
    response = {
        "statusCode": 200,
        "body": json.dumps({"prediction": output[0]})
    }
    return response
