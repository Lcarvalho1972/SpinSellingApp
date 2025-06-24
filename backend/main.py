from fastapi import FastAPI

# Instanciar o app
app = FastAPI(
    title="SpinSellingApp",
    description="API para gerar roteiros de vendas baseados no SPIN Selling",
    version="0.1.0"
)

# Rota de teste
@app.get("/")
def read_root():
    return {"message": "SpinSellingApp API rodando com sucesso ??"}
