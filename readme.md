FastAPI pip install fastapi
Pyodbc pip install pyodbc
Numpy v(1.26.4) pip install numpy 
TensorFlow pip install tensorflow 
Sklearn pip install scikit-learn 
Pandas pip install pandas 
pydantic pip install pydantic
uvicorn pip install uvicorn
pip install python-multipart
pip install pyngrok

netsh advfirewall firewall add rule name="FastAPI" dir=in action=allow protocol=TCP localport=8000
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
http://127.0.0.8:8000/docs
