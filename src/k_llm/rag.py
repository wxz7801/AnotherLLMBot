import os
from langchain_chroma import Chroma
from langchain_community.document_loaders import DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

from k_llm.models import embedding_model

# 获取检索器
def get_retriever():
    chroma_db_path="./chroma_db"

    # 检查是否存在持久化的 Chroma 数据库
    if os.path.exists(chroma_db_path):
        print("检测到已存在的 Chroma 数据库，正在加载...")
        vector_storage = Chroma(persist_directory=chroma_db_path, embedding_function=embedding_model)
    else:
        print("未检测到 Chroma 数据库，开始加载文档并创建向量存储...")
        # 加载文档
        loader = DirectoryLoader("./knowledge")
        documents = loader.load()
        print(f"加载了 {len(documents)} 个文档。")

        # 分词器
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=500, chunk_overlap=20, add_start_index=True
        )
        all_splits = text_splitter.split_documents(documents)
        print(f"分割了 {len(all_splits)} 个文档。")

        # 创建向量存储
        vector_storage = Chroma.from_documents(all_splits, embedding_model, persist_directory=chroma_db_path)
        print("向量存储已创建并保存到磁盘。")

    #　配置检索器
    retriever = vector_storage.as_retriever(search_type="similarity_score_threshold", 
                                            search_kwargs={"score_threshold": 0.3}, 
                                            )   
    return retriever

retriever = get_retriever()
