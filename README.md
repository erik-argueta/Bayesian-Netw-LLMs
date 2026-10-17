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

The client uses `https://ellm.nrp-nautilus.io/v1`, model `gpt-oss`, and
`client.chat.completions.create(...)`.

Set the key in your terminal or `~/.bashrc`:

```bash
export NRP_API_KEY="your_nrp_api_key_here"
```

If you edited `~/.bashrc`, reload it with `source ~/.bashrc`. Start the GUI
from that same terminal:

```bash
python diagnostics_gui.py
```

Use an NRP-issued key for this endpoint. Colab's `userdata` is replaced by
`os.environ["NRP_API_KEY"]` for local use. The code does not load `.env` files.
Do not commit private API keys.

The prompt requests JSON containing `diagnosis` and `probability`. Pydantic
validates the returned JSON locally; this does not assume that the NRP endpoint
supports OpenAI's server-side Structured Outputs options.

## Python .venv
Please don't forget to create your venv as `.venv`  
Otherwise, please include the venv within .gitignore  

## Branching  
Please work in a different branch until you're ready to merge with main.  
Please notify the group when a push has been made on the main branch.  
