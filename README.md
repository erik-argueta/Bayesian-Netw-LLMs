# Bayesian Network with LLMs
Program Authors:  
* Erik Argueta  
* Jerico Avila  
* Jose Cervantes

## How to Initialize
* If using uv, run the following within the project's home directory:  
`uv pip install -r requirements.txt`

* If using pip, run the following in within the project's home directory:  
`pip install -r requirements.txt`

## NRP API Key
This project reads the NRP LLM key from your local environment, not from source code.

1. Copy the example environment file:  
`cp .env.example .env`

2. Edit `.env` and replace `your_nrp_api_key_here` with your real NRP API key.

3. Run the GUI or tests normally. `diagnostics.py` loads `.env` automatically.

The real `.env` file is ignored by git. Do not commit private API keys.

## Python .venv
Please don't forget to create your venv as `.venv`  
Otherwise, please include the venv within .gitignore  

## Branching  
Please work in a different branch until you're ready to merge with main.  
Please notify the group when a push has been made on the main branch.  
