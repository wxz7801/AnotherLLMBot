from src.config_loader import config  # 导入 config对象
from src.k_llm.models import chat_model
from src.k_llm.prompt_templates import rag_cat_girl, cat_girl

from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


class ChatBot():
    def __init__(self):
        self.name = "ChatBot"
        self.output_parser = StrOutputParser()
        use_rag = config["use_rag"]


        if use_rag:
            from src.k_llm.rag import retriever, format_docs

            prompt_template = rag_cat_girl
            # prompt_template = hub.pull("rlm/rag-prompt")
            self.chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt_template 
                | chat_model 
                | self.output_parser
            )
        else:
            prompt_template = cat_girl
            self.chain = prompt_template | chat_model | self.output_parser
    
    def reply(self, user_input):
        # 调用 invoke 方法生成响应
        try:
            invoke_response = self.chain.invoke(user_input)
            message = invoke_response.split("</think>")[-1].split('\n')[-1]
            return message
        except Exception as e:
            return "发生错误:", e

chat_bot = ChatBot()