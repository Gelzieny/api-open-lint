#!/bin/bash
cd /home/gelzieny.martins/meu_projeto
source .venv/bin/activate
uvicorn manage:app --host 0.0.0.0 --port 8096  
deactivate