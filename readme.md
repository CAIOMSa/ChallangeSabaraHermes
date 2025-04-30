
# 🏥 HermesApi

**Hermes** é uma API desenvolvida com FastAPI para auxiliar no atendimento clínico de pacientes, incluindo classificação de imagens médicas com IA, controle de etapas do atendimento, diagnósticos automatizados e controle de estoque.

---

## 📌 Funcionalidades principais

- 📷 Classificação de imagens médicas com IA (modelo TensorFlow)
- 🧾 Diagnóstico e geração de conclusões com explicações textuais (skLearn)
- 🩺 Controle de fila de atendimento por etapas
- 🗂 Armazenamento local de imagens médicas
- 🛏️ Gestão de pacientes, convênios, quartos e estoque
- 🌐 API RESTful com documentação interativa

---

## 📁 Estrutura de Diretórios

**Hexagonal Architecture Simplificada**

```
.
├── api/                   # Endpoints (controladores)
├── banco_de_imagens/     # Armazenamento das imagens
├── database/             # Conexão com SQL Server
├── dtos/                 # Modelos de dados (DTOs - Pydantic)
├── models/               # ORM e modelos de IA
├── services/             # Lógica de negócio
├── utils/                # Funções utilitárias
├── conf.py               # Configurações globais
├── main.py               # Entrada principal da API
└── readme.md             # Documentação do projeto
```

---
## 📊 Diagrama de Arquitetura

## ⚙️ Requisitos e Instalação

**Versão recomendada do Python:** 3.9

### 📦 Instalação dos pacotes

```bash
pip install fastapi
pip install pyodbc
pip install numpy==1.26.4
pip install tensorflow
pip install scikit-learn
pip install pandas
pip install pydantic
pip install uvicorn
pip install python-multipart
pip install pyngrok
```

---
## 🛢 Banco de Dados
### [Modelo pronto para rodar no docker](https://drive.google.com/drive/folders/1mLNyrJprF_lPm-jrlBFLvafd8gqKT574?usp=drive_link)  **executar com o bash 
```bash
docker-compose up -d
```

---
### [Instalar o ODBC](https://learn.microsoft.com/pt-br/sql/connect/odbc/download-odbc-driver-for-sql-server?view=sql-server-ver16) e configura-lo caso necessário

## ▶️ Como iniciar o sistema

### 🔥 Permissão no firewall (Windows)

```bash
netsh advfirewall firewall add rule name="FastAPI" dir=in action=allow protocol=TCP localport=8000
```

### 🚀 Executar o programa

```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 📡 Endpoints da API

Acesse a documentação interativa em:

[http://127.0.0.8:8000/docs](http://127.0.0.8:8000/docs)
