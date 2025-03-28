from src.chat_bot import chat_bot
from src.topic_identifier import topic_identifier


def main():
    while True:
        print("欢迎使用聊天机器人！输入内容与模型对话，输入 /bye 退出。")
        user_input = input("用户: ")
        if user_input.strip().lower() == "/bye":
            print("再见！")
            break

        # 调用 invoke 方法生成响应
        try:
            answer = chat_bot.reply(user_input)
            print("模型:", answer)
        except Exception as e:
            print("发生错误:", e)


if __name__ == "__main__":
    main()
