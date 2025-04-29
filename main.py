from fastapi import FastAPI
from api.__init__ import api_router
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  #Permite qualquer origem
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    #from pyngrok import ngrok, conf
    PORT = 8000

    #conf.get_default().auth_token = NGROK_TOKEN

    #public_url = ngrok.connect(PORT)
    #print(f"🔗 NGROK TÚNEL ATIVO: {public_url}")

    uvicorn.run(app, host="0.0.0.0", port=PORT)
