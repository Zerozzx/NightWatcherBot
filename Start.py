from khl import Bot, Message,EventTypes,Event
from khl.command import Rule
from khl.card import CardMessage, Card,Module,Element,Types,Struct
import logging,json,random
from datetime import datetime,timedelta

# init Bot
with open('Config/Token.json','r',encoding='utf-8') as TokenFile:
    config = json.load(TokenFile)

bot = Bot(token=config['token'])

# register command, send `/hello` in channel to invoke
@bot.command(name='hello')
async def world(msg: Message):
    await msg.reply('world!')

@bot.command(name='人工智障')
async def AI(msg: Message):
    await msg.reply("给爷爬！")

@bot.command(name='掷骰子')
async def roll(msg:Message, t_min:int, t_max:int, n:int=1):
    result = [random.randint(t_min, t_max) for i in range(n)]
    await msg.reply(f'你的点数:{result}',True, is_temp = True)
    await msg.ctx.channel.send(f'你的点数:{result}', temp_target_id=msg.author.id)

# register event
@bot.on_event(EventTypes.UPDATED_MESSAGE)
async def update_reminder(b:Bot,event:Event):
    channel = await b.fetch_public_channel(event.body['channel_id'])
    updated_at = datetime.fromtimestamp(event.body['updated_at'] /1000)
    await b.send(channel, f'消息 {event.body["msg_id"]} 在 {updated_at} 时被更新')

async def delete_catcher(b:Bot, event:Event):
    channel = await b.fetch_public_channel(event.body['channel_id'])
    await b.send(channel,f'消息 {event.body["msg_id"]} 被删除了...')

bot.add_event_handler(EventTypes.DELETED_MESSAGE,delete_catcher)

# 条件命令
# register command and add a rule
# invoke this via saying `/hello @{bot_name}` in channel
@bot.command(name='你好', rules=[Rule.is_bot_mentioned(bot)])
async def Hi(msg: Message, mention_str: str):
    await msg.reply(f'你好！，你正在@ {mention_str}')

# is_mention_all = 任何用户被 @
@bot.command(rules=[Rule.is_mention_all])
async def ISee(msg: Message, mention_str: str):
    await msg.reply(f'我看到了！你在@{mention_str}！')

# 自定义 Rule，如果消息中有 “才艺” 两个字
def my_rule(msg: Message) -> bool:
    return msg.content.find('才艺') != -1
# 使用自定义 Rule
# this command can only be triggered with msg that contains 'khl' such as /test_mine khl-go
@bot.command(name='测试自定义规则', rules=[my_rule])
async def test_mine(msg: Message, comment: str):
    await msg.reply(f'yes! {comment} can trigger this command')

# 卡片消息
@bot.command()
async def minimalCard(msg: Message):
    cm = CardMessage(Card())
    await msg.reply(cm)

@bot.command()
async def card(msg: Message):
    c = Card(Module.Header('CardMessage'), Module.Section('convenient to convey structured information'))
    cm = CardMessage(c)  # Card can not be sent directly, need to wrapped with a CardMessage
    await msg.reply(cm)

# button example, build a card in a single statement
# btw, short code without readability is not recommended
@bot.command()
async def button(msg: Message):
    await msg.reply(
        CardMessage(
            Card(
                Module.Header('An example for button'),
                Module.Context('Take a pill, take the choice'),
                Module.ActionGroup(
                    # RETURN_VAL type(default): send an event when clicked, see print_btn_value() defined at L58
                    Element.Button('Truth', 'RED', theme=Types.Theme.DANGER),
                    Element.Button('Wonderland', 'BLUE', Types.Click.RETURN_VAL)),
                Module.Divider(),
                Module.Section(
                    'another kind of button, user will goto the link when clicks the button:',
                    # LINK type: user will open the link in browser when clicked
                    Element.Button('link button', 'https://github.com/TWT233/khl.py', Types.Click.LINK)))))

@bot.command()
async def countdown(msg: Message):
    cm = CardMessage()

    c1 = Card(Module.Header('Countdown example'), color='#5A3BD7')  # color=(90,59,215) is another available form
    c1.append(Module.Divider())
    c1.append(Module.Countdown(datetime.now() + timedelta(hours=1), mode=Types.CountdownMode.SECOND))
    cm.append(c1)

    c2 = Card(theme=Types.Theme.DANGER)  # priority: color > theme, default: Type.Theme.PRIMARY
    c2.append(Module.Section('the DAY style countdown'))
    c2.append(Module.Countdown(datetime.now() + timedelta(hours=1), mode=Types.CountdownMode.DAY))
    cm.append(c2)  # A CardMessage can contain up to 5 Cards

    await msg.reply(cm)

# struct example
@bot.command()
async def struct(msg: Message):
    await msg.reply(CardMessage(Card(Module.Section(Struct.Paragraph(3, 'a', 'b', 'c')))))

# 当用户单机了按钮后输出内容
@bot.on_event(EventTypes.MESSAGE_BTN_CLICK)
async def print_btn_value(_: Bot, e: Event):
    print(f'''{e.body['user_info']['nickname']} took the {e.body['value']} pill''')

# 观测回应
@bot.on_event(EventTypes.ADDED_REACTION)
async def reaction_reminder(b:Bot,event:Event):
    # fetch channel of the REACTION event
    channel = await b.fetch_public_channel(event.body['channel_id']) 
    # send a messge to inform user at current channel
    await b.send(channel,f"you add reaction{event.body['emoji']['id']}") 

# everything done, go ahead now!
logging.basicConfig(level='INFO')
bot.run()
# now invite the bot to a server, and send '/hello' in any channel
# (remember to grant the bot with read & send permissions)