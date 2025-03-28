import random
from src.chat_bot import chat_bot

from pydantic import BaseModel
from nonebot import logger


class Config(BaseModel):
    """Plugin Config Here"""


from nonebot import on_command, on
from nonebot.rule import to_me
from nonebot.adapters import Message
from nonebot.params import EventMessage

weather = on_command("天气", rule=to_me(), aliases={"weather", "查天气"}, priority=10, block=True)

@weather.handle()
async def handle_function():
    # await weather.send("天气是...")
    await weather.finish("天气是...")

any_message = on(rule=to_me(), priority=20, block=True)

@any_message.handle()
async def handle_any_message(args: Message = EventMessage()):
    # 创建一个0-1之间的随机数
    reply_chance = random.random()
    print(reply_chance)
    if reply_chance < 0.5:
        await any_message.finish()

    content = args.extract_plain_text()
    logger.info(content)
    try:
        reply = chat_bot.reply(content)
    except Exception as e:
        logger.error(e)
    await any_message.finish(reply)