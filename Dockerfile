# Use a imagem base oficial do AWS Lambda Python (versão 3.10 neste exemplo)
FROM public.ecr.aws/lambda/python:3.10

# Copiar dependências do Python
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt

# Copiar código da função e artefatos do modelo para o diretório do Lambda
COPY app.py ${LAMBDA_TASK_ROOT}
COPY models/model.pkl ${LAMBDA_TASK_ROOT}/models/
COPY models/model_metadata.json ${LAMBDA_TASK_ROOT}/models/

# Definir o comando de inicialização (handler do Lambda)
CMD [ "app.handler" ]