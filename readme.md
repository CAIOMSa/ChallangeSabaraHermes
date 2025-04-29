FastAPI pip install fastapi
Pyodbc pip install pyodbc
Numpy v(1.26.4) pip install numpy tF
TensorFlow pip install tensorflow tF
Sklearn pip install scikit-learn tF
Pandas pip install pandas tF
pydantic pip install pydantic
uvicorn pip install uvicorn
pip install python-multipart
pip install pyngrok

netsh advfirewall firewall add rule name="FastAPI" dir=in action=allow protocol=TCP localport=8000
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
http://127.0.0.8:8000/docs

OBSERVACOES:

Tailwind Twin IntelliSense

SITE PARA BASE DE DADOS DE IMAGENS:
https://medpix.nlm.nih.gov/search?allen=true&allt=true&alli=true&query=radiographic
https://datasetsearch.research.google.com/

DIAGNOSTIC:
REVER FLUXO E LIGAÇÃO COM MODELOS

GERAL:
ATIVAR NGROK!!!!!!!
