# Usa uma imagem oficial do Python 
FROM python:3.11  

# Define o diretório de trabalho dentro do contêiner 
WORKDIR /app  

# Copia os arquivos do projeto para dentro do contêiner 
COPY . /app  

# Instala as dependências do projeto
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Baixa o modelo de linguagem do spaCy 
RUN python -m spacy download pt_core_news_sm  

# Expõe a porta do Streamlit 
EXPOSE 8501  

# Comando para rodar o aplicativo 
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]