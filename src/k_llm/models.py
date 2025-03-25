from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from src.config_loader import config

def get_chat_model():
    # 从config.toml中读取配置
    chat_model_provider = config["chat_model_provider"]
    chat_model_url = config["chat_model_url"]
    chat_model_name = config["chat_model_name"]
    chat_model_key = config["chat_model_key"]

    if chat_model_provider == "ollama":
        llm = ChatOllama(base_url=chat_model_url, model=chat_model_name)
    elif chat_model_provider == "openai":
        llm = ChatOpenAI(
            model = chat_model_name,
            openai_api_key = chat_model_key,
            openai_api_base = chat_model_url
        )
    
    return llm

def get_embedding_model():
    emb_model_provider = config["emb_model_provider"]
    emb_model_url = config["emb_model_url"]
    emb_model_name = config["emb_model_name"]
    emb_model_key = config["emb_model_key"]
    
    if emb_model_provider == "ollama":
        embeddings = OllamaEmbeddings(base_url=emb_model_url, model=emb_model_name)
    elif emb_model_provider == "openai":
        embeddings = OpenAIEmbeddings(
            model = emb_model_name,
            openai_api_key = emb_model_key,
            openai_api_base = emb_model_url
        )
    
    return embeddings

chat_model = get_chat_model()
embedding_model = get_embedding_model()