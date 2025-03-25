import os
from src.config_loader import config  # 导入 config对象
from src.k_llm.models import chat_model
from src.k_llm.prompt_templates import rag_cat_girl, cat_girl

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


def main():
    output_parser = StrOutputParser()
    use_rag = config["use_rag"]


    if use_rag:
        from src.k_llm.rag import retriever, format_docs

        # retrieved_docs = retriever.invoke("你好")
        # print(len(retrieved_docs))
        # print(retrieved_docs[0].metadata)
        # input("按回车键继续...")

        prompt_template = rag_cat_girl
        # prompt_template = hub.pull("rlm/rag-prompt")
        chain = (
            {"context": retriever | format_docs, "question": RunnablePassthrough()}
            | prompt_template 
            | chat_model 
            | output_parser
        )
    else:
        prompt_template = cat_girl
        chain = prompt_template | chat_model | output_parser
    
    while True:
        print("欢迎使用聊天机器人！输入内容与模型对话，输入 /bye 退出。")
        user_input = input("你: ")
        if user_input.strip().lower() == "/bye":
            print("再见！")
            break

        # 调用 invoke 方法生成响应
        try:
            invoke_response = chain.invoke(user_input)
            message = invoke_response.split("</think>")[-1].split('\n')[-1]
            print("模型:", message)
        except Exception as e:
            print("发生错误:", e)


if __name__ == "__main__":
    main()
