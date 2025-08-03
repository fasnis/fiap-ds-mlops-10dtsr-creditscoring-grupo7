import json
import logging
import joblib
import pickle
import os
import numpy as np

logging.basicConfig(level=logging.INFO)

# Diretório onde fica o modelo
MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")

# Carrega modelo (tentando joblib e pickle)
model = None
metadata = {}

try:
    try:
        model = joblib.load(os.path.join(MODEL_DIR, "model.pkl"))
        logging.info("Modelo carregado com sucesso (joblib).")
    except Exception as e_joblib:
        logging.warning(f"Falha ao carregar com joblib: {e_joblib}. Tentando pickle...")
        with open(os.path.join(MODEL_DIR, "model.pkl"), "rb") as f:
            model = pickle.load(f)
        logging.info("Modelo carregado com sucesso (pickle).")

    with open(os.path.join(MODEL_DIR, "model_metadata.json"), "r") as f:
        metadata = json.load(f)
    logging.info("Metadados carregados com sucesso.")
    if "model_version" in metadata:
        logging.info(f"Versão do modelo: {metadata['model_version']}")

except FileNotFoundError as e:
    logging.error(f"Arquivo de modelo ou metadados não encontrado: {e}")
    raise
except Exception as e:
    logging.error(f"Erro ao carregar o modelo: {e}")
    raise


def handler(event, context):
    """
    Função handler do AWS Lambda ou teste local.
    """
    try:
        # Detecta se está vindo do API Gateway (body é string)
        if isinstance(event, dict) and "body" in event:
            body = json.loads(event["body"])
        else:
            body = event

        logging.info(f"Entrada recebida: {body}")

        # Pega os dados da entrada
        input_data = body.get("data")
        if input_data is None:
            raise ValueError("Campo 'data' não encontrado na requisição.")

        # Converte para numpy array para facilitar reshape
        input_array = np.array(input_data, dtype=float)

        # Ajusta forma da entrada
        expected_features = getattr(model, "n_features_in_", None)
        if expected_features is not None and input_array.ndim == 1:
            if input_array.shape[0] != expected_features:
                logging.warning(
                    f"Ajustando entrada: modelo espera {expected_features} features, "
                    f"mas recebeu {input_array.shape[0]}"
                )
            input_array = input_array.reshape(1, -1)  # (1, n_features)
        elif input_array.ndim == 0:
            # Caso entrada seja um valor único
            input_array = input_array.reshape(1, 1)

        # Faz a predição
        prediction = model.predict(input_array)
        output = prediction.tolist()

        logging.info(f"Predição gerada: {output}")

        # Resposta compatível com API Gateway
        return {
            "statusCode": 200,
            "body": json.dumps({"prediction": output[0]})
        }

    except Exception as e:
        logging.error(f"Erro ao processar requisição: {e}")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": str(e)})
        }


# Teste local
if __name__ == "__main__":
    evento_teste = {
        "data": [1.0, 2.5, 3.3, 4.7]  # entrada de teste
    }
    print(handler(evento_teste, None))
