from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
from superlinked.server import create_app

def create_app_with_cors() -> FastAPI:
    app = create_app()
    
    # Get CORS settings from environment variables
    origins = os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")
    methods = os.getenv("CORS_ALLOW_METHODS", "GET,POST,OPTIONS").split(",")
    headers = os.getenv("CORS_ALLOW_HEADERS", "*").split(",")
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=methods,
        allow_headers=headers,
    )
    
    return app

if __name__ == "__main__":
    import uvicorn
    app = create_app_with_cors()
    uvicorn.run(app, host="0.0.0.0", port=8080) 