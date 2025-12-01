import os
from dotenv import load_dotenv

def load_env_var(varname:str)->str:

    load_dotenv()
    value=os.getenv(varname)
    if value is None:
        raise ValueError(f"Environment variable {varname} not found.")
    return value


DATA_DIR=load_env_var('DATA_DIR')
COLLECTION_NAME=load_env_var('COLLECTION_NAME')
EMBEDDER_MODEL_NAME=load_env_var('EMBEDDER_MODEL_NAME')
GEN_MODEL_NAME=load_env_var('GEN_MODEL_NAME')
QDRANT_HOST=load_env_var('QDRANT_HOST')
QDRANT_PORT=int(load_env_var('QDRANT_PORT'))
QDRANT_DATA_FOLDER=load_env_var('QDRANT_DATA_FOLDER')
QDRANT_COLLECTION_NAME=load_env_var('QDRANT_COLLECTION_NAME')
USE_GPU=bool(int(load_env_var('USE_GPU')))
