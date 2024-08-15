import uvicorn
from fastapi import FastAPI
from pyngrok import ngrok
from app.main import app 
if __name__ == "__main__":
    # Open a ngrok tunnel to the HTTP server
    public_url = ngrok.connect(8000)
    print(f" * Public URL: {public_url}")

    # Start the FastAPI app
    uvicorn.run(app, host="0.0.0.0", port=8000)