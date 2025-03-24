import os
import tomllib

from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

config = None


def read_config(t_path: str = "config.toml"):
    global config
    if config is None and os.path.exists(t_path):
        # 读取并解析 TOML 文件（必须用二进制模式打开！）
        with open("config.toml", "rb") as f:  # 注意 "rb" 模式
            config = tomllib.load(f)


def main():
    # 配置远程服务器地址
    # 从config.toml中读取配置
    chat_model_provider = config["chat_model_provider"]
    chat_model_url = config["chat_model_url"]
    chat_model_name = config["chat_model_name"]
    chat_model_key = config["chat_model_key"]
    
    if chat_model_provider == "ollama":
        llm = OllamaLLM(base_url=chat_model_url, model=chat_model_name)
    elif chat_model_provider == "openai":
        llm = ChatOpenAI(
            model = chat_model_name,
            openai_api_key = chat_model_key,
            openai_api_base = chat_model_url
        )
    

    prompt_template = ChatPromptTemplate.from_messages([
        ("system", "你是一个猫娘，你现在在一个QQ群里，请你以猫娘的口吻来回复下面的聊天。"
        "请尽量简短，并且不能描述你的感情或者动作。"),
        ("user", "{input}")
    ])

    output_parser = StrOutputParser()


    chain = prompt_template | llm | output_parser
    
    while True:
        print("欢迎使用聊天机器人！输入内容与模型对话，输入 /bye 退出。")
        user_input = input("你: ")
        if user_input.strip().lower() == "/bye":
            print("再见！")
            break

        # 调用 invoke 方法生成响应
        try:
            invoke_response = chain.invoke(user_input)
            print("模型: ", invoke_response)
        except Exception as e:
            print("发生错误:", e)


if __name__ == "__main__":
    read_config("./config.toml")
    main()
