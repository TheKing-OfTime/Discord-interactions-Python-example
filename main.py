import requests
import discord
from discord.ext import commands
from scr.Lib import TOKENS


bot = commands.Bot(command_prefix="t!")


TOKEN = TOKENS[0]

channel_id = 453272494724349963

def SlashCommand(name:str, description:str, options:list, default_permission:bool= True):
    payload = {
        "name": str(name),
        "description": str(description),
    }
    if options is not None:
        payload["options"] = options

    if default_permission is False:
        payload["default_permission"] = False
    return payload

def SlashCommandOption(type_:int, name, description, required:bool = False, choices:list=None, options:list=None):
    payload = {
        "type": type_,
        "name": name,
        "description": description
    }
    if required is True:
        payload["required"] = True
    if choices is not None:
        payload["choices"] = choices
    if options is not None:
        payload["options"] = options

    return payload

def Button(text, style, url = None, disabled=False, custom_id="click_button_default"):
    payload = {
        "type": 2,
        "label": str(text),
        "style": int(style),
    }
    if url is not None:
        payload["url"] = str(url)
    else:
        payload["custom_id"] = str(custom_id)

    if bool(disabled):
        payload["disabled"] = True
    return payload

def ActionRaw(lst:list):
    payload = {
        "type": 1,
        "components": lst
    }
    return payload

def SelectMenu(custom_id:str, placeholder:str = None, mix_values:int = 1, max_values:int = 1, options:list = None):
    payload = {
        "type": 3,
        "custom_id": str(custom_id),
        "placeholder": placeholder,
        "mix_values": mix_values or 1,
        "max_values": max_values or 1,
        "options": options
    }
    return payload

def SelectOption(label:str, value:str, default:bool = False, description:str = None, e_id:str = None, e_name:str = None):
    payload = {
        'label': label,
        'value': value,
        'default': default,
        'description': description,
        'emoji': {
            'name': e_name,
            'id': e_id
        }
    }
    return payload

def ContextCommand():
    """
    Coming soon
    """
    pass

async def CreateSlashCommand(name:str, description:str, options:list, default_permission:bool = True):
    r = requests.request("POST", f"https://discord.com/api/v9/applications/{bot.user.id}/commands", json =
        SlashCommand(name, description, options, default_permission),
        headers = {
            "Authorization": f"Bot {TOKEN}",
            "Content-Type": "application/json"
        })
    print(r.status_code, "\n", r.content)

async def toggle_role(member:discord.Member, values, arg = '1'):
    roles_to_add = []
    lst = []
    for role in member.guild.roles:
        if str(role.colour) == "#4dc1e9" or str(role.colour) == "#c7a6fb" or str(role.colour) == "#3498db":
            lst.append(role)
        lst.sort()

    if arg == '1':
        lst = lst[:24]
    else: lst = lst[25:]


    roles_to_remove = lst

    for role_id in values:
        role = member.guild.get_role(int(role_id))
        if role not in member.roles:
            roles_to_add.append(role)
            roles_to_remove.remove(role)
        else:
            roles_to_remove.remove(role)

    for role in roles_to_remove:
        if role not in member.roles:
            roles_to_remove.remove(role)

    await member.add_roles(*roles_to_add, reason="По требованию пользователя")
    await member.remove_roles(*roles_to_remove, reason="По требованию пользователя")

class Main(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.command()
    async def test(self, ctx: commands.Context):
        requests.request("POST", f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
                                    json =

                                        {
                                            "content": "Are you satisfied?",
                                            "components":
                                            [
                                                ActionRaw([
                                                    Button("Да", 3, custom_id="click_yes" ),
                                                    Button("Нет", 4, custom_id="click_no" )
                                                ])
                                            ]
                                         }
                                    ,
                                    headers = { "Authorization": f"Bot {TOKEN}",
                                                "Content-Type": "application/json"})

    @commands.command(aliases=["ts"])
    async def test_s(self, ctx: commands.Context):
        requests.request("POST", f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
                                    json =

                                    {
                                        "content": "Select test",
                                        "components":
                                            [
                                                ActionRaw(
                                                    [
                                                        SelectMenu("Select_menu", "Select it!", max_values=3, options=
                                                            [
                                                                SelectOption("1", "value_1", False, "Select your first choice!", "764938637862371348", "done_2"),
                                                                SelectOption("2", "value_2", False, "Select your second choice!", "764938637862371348", "done_2"),
                                                                SelectOption("3", "value_3", False, "Select your third choice!", "764938637862371348", "done_2")
                                                            ]
                                                        )
                                                    ]
                                                )
                                            ]
                                    }
                                    ,
                                    headers = { "Authorization": f"Bot {TOKEN}",
                                                "Content-Type": "application/json"})

    @commands.command(aliases=["r"])
    async def role(self, ctx, arg = "1", ephemerial=False):
        lst = []
        options1 = []
        options2 = []
        e_name = None
        e_id = None
        roles_to_clearing = []

        if type(ctx) is not commands.Context:
            channel_id = ctx['channel_id']
            guild = await bot.fetch_guild(ctx['guild_id'])
            member = await guild.fetch_member(ctx['member_id'])
        else:
            channel_id = ctx.channel.id
            guild = ctx.guild
            member = ctx.author

        for role in guild.roles:
            if str(role.colour) == "#4dc1e9" or str(role.colour) == "#c7a6fb" or str(role.colour) == "#3498db":
                lst.append(role)
            lst.sort()

        for role in lst:
            if str(role.colour) == "#4dc1e9":
                e_name = "game"
                e_id = "850363704742903819"
            elif str(role.colour) == "#3498db":
                e_name = "ganre"
                e_id = "850363722487955486"
            elif str(role.colour) == "#c7a6fb":
                e_name = "forts"
                e_id = "869133402631188521"

            if not ctx["clearing"]:
                is_have = role in member.roles
            else:
                if role in member.roles:
                    roles_to_clearing.append(role)
                is_have = False

            if len(options1) < 25:
                options1.append(SelectOption(role.name, role.id, e_name=e_name, e_id=e_id, default = is_have))
            else:
                options2.append(SelectOption(role.name, role.id, e_name=e_name, e_id=e_id, default = is_have))

        if ctx["clearing"]:
            await member.remove_roles(*roles_to_clearing, reason="По требованию пользователя")

        json = {
            "content": f"Игровые роли (Страница {arg} из 2)",
            "components": [ActionRaw([
                SelectMenu(
                    f"role_selection {arg}",
                    "Выберите любые интересующие вас роли",
                    max_values=len(options1 if arg == "1" else options2),
                    options=options1 if arg == "1" else options2
                )
            ]),
            ActionRaw([
                Button("Сбросить роли", 4, custom_id = f"clear_roles {arg}")
            ])],
            "flags": 64 if ephemerial else None

        }

        if type(ctx) is commands.Context:

            response = requests.request("POST", f"https://discord.com/api/v9/channels/{channel_id}/messages",
                                        json = json
                                        ,
                                        headers = { "Authorization": f"Bot {TOKEN}",
                                                    "Content-Type": "application/json"})
            print(response.status_code, response.content if response.status_code != 200 else "")
        else:
            return json

    @commands.command()
    async def vote(self, ctx: commands.Context, *, text:str):
        requests.request("POST", f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
                                    json =

                                    {
                                        "content": text,
                                        "components":
                                            [
                                                ActionRaw([
                                                    Button("Да", 3, custom_id="click_yes" ),
                                                    Button("Нет", 4, custom_id="click_no" )
                                                ])
                                            ]
                                    }
                                    ,
                                    headers = { "Authorization": f"Bot {TOKEN}",
                                                "Content-Type": "application/json"})


    @commands.command()
    async def button(self, ctx: commands.Context, text, style, disabled=False, arg=None):

        if style != "5":
            _id = arg
            url=None
        else:
            _id = "click_button_default"
            url=arg

        requests.request("POST", f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
                                    json =

                                    {
                                        "content": "Button",
                                        "components":
                                            [
                                                ActionRaw([
                                                    Button(text, style, url, disabled, _id)
                                                ])
                                            ]
                                    }
                                    ,
                                    headers = { "Authorization": f"Bot {TOKEN}",
                                                "Content-Type": "application/json"})

    @commands.command()
    async def demo(self, ctx: commands.Context):
        requests.request("POST", f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
                                    json =

                                    {
                                        "content": "Демонстрация",
                                        "components":
                                            [
                                                ActionRaw([
                                                    Button("Blurple", 1, custom_id="Blurple_clicked"),
                                                    Button("Grey", 2, custom_id="Gray_clicked"),
                                                    Button("Green", 3, custom_id="Green_clicked"),
                                                    Button("Red", 4, custom_id="Red_clicked"),
                                                    Button("Link", 5, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
                                                ]),
                                                ActionRaw([
                                                    Button("Blurple", 1, custom_id="Blurple_clicked", disabled=True),
                                                    Button("Grey", 2, custom_id="Gray_clicked", disabled=True),
                                                    Button("Green", 3, custom_id="Green_clicked", disabled=True),
                                                    Button("Red", 4, custom_id="Red_clicked", disabled=True),
                                                    Button("Link", 5, url="https://www.youtube.com/watch?v=dQw4w9WgXcQ", disabled=True)
                                                ])
                                            ]
                                    }
                                    ,
                                    headers = { "Authorization": f"Bot {TOKEN}",
                                                "Content-Type": "application/json"})

    @commands.command(aliases=["createSC"])
    @commands.check(commands.is_owner())
    async def CreateSlashCommand(self, ctx, name, *, description):
        await CreateSlashCommand(name, description, [SlashCommandOption(4, "страница", "Выберите страницу", choices=[{"name": "1", "value": 1}, {"name": "2", "value": 2}]),
                                                     SlashCommandOption(8, "роль", "Выберите конкретную роль")
                                                     ])
        await ctx.send("done")


    @commands.Cog.listener()
    async def on_ready(self):
        print("ready")

    @commands.Cog.listener()
    async def on_socket_response(self, msg):
        if msg["t"] == 'INTERACTION_CREATE':

            interaction_id      = msg["d"]["id"]
            interaction_token   = msg["d"]["token"]
            interaction_type    = msg["d"]["type"]
            print(msg["d"]["data"])

            json_ = None
            content = None
            type_ = 4
            data_ = None
            print(interaction_type)

            if interaction_type == 3:
                component_type  = msg["d"]["data"]["component_type"]
                member_id       = msg["d"]["member"]["user"]["id"]
                guild_id        = msg["d"]["guild_id"]
                channel_id  = msg["d"]["channel_id"]

                if component_type == 2:

                    button_id = msg["d"]["data"]['custom_id']

                    if button_id == "click_yes":
                        content = "Голос учтён!"

                        print(self.bot.get_user(member_id) or await self.bot.fetch_user(member_id), "Да")

                        json_ = {
                            "type": 7,
                            "data": {
                                "flags": 64,
                                "components":
                                [
                                    ActionRaw([
                                        Button("Да", 3, custom_id="click_yes", disabled = True),
                                        Button("Нет", 2, custom_id="click_no", disabled = True )
                                    ])
                                ]

                            }
                        }

                    elif button_id == "click_no":
                        content = "Голос учтён!"
                        print(self.bot.get_user(member_id) or await self.bot.fetch_user(member_id), "Нет")
                        json_ = {
                            "type": 7,
                            "data": {
                                "flags": 64,
                                "components":
                                [
                                    ActionRaw([
                                        Button("Да", 2, custom_id="click_yes", disabled = True),
                                        Button("Нет", 4, custom_id="click_no", disabled = True )
                                    ])
                                ]

                            }
                        }

                    elif button_id == "click_button_default":
                        content = "Clicked!"

                    elif button_id.startswith("clear_roles"):
                        value = button_id.split(' ')[1]
                        data_ = await self.role({"guild_id": guild_id, "channel_id": channel_id, "member_id": member_id, "clearing": True}, value, ephemerial=True)
                        type_ = 7
                        content = False

                    else:
                        content = f"Clicked! ID = {button_id}"

                elif component_type == 3:
                    values = msg["d"]["data"]["values"]
                    selection_id = msg["d"]["data"]["custom_id"]
                    if selection_id.startswith("role_selection"):
                        value = selection_id.split(' ')[1]
                        content = f"Выбранные роли установленны"
                        guild = await bot.fetch_guild(guild_id)
                        member = await guild.fetch_member(member_id)
                        url = f"https://discord.com/api/v9/interactions/{interaction_id}/{interaction_token}/callback"
                        r = requests.post(url, json={
                            "data":{
                                "content" : content,
                                "flags": 64,
                            },
                            "type": 4
                        })
                        content = None

                        await toggle_role(member, values, value)
                    else:
                        content = f"You have chosen these selections: {values}"
                    print(content)
            elif interaction_type == 2:
                guild_id    = msg["d"]["guild_id"]
                member_id   = msg["d"]["member"]["user"]["id"]
                channel_id  = msg["d"]["channel_id"]
                name        = msg["d"]["data"]["name"]
                if name == "ping":
                    content = f"`{round(bot.latency * 1000, 2)}`"
                if name == "role":
                    try:
                        value = msg["d"]["data"]["options"][0]["value"]
                    except:
                        value = '1'
                    data_ = await self.role({"guild_id": guild_id, "channel_id": channel_id, "member_id": member_id, "clearing": False}, value, ephemerial=True)
                    type_ = 4
                    content = False

            url = f"https://discord.com/api/v9/interactions/{interaction_id}/{interaction_token}/callback"
            if not data_:
                data = {
                    "content": content,
                    "flags": 64
                }
            else:
                data = data_

            if content is not None:

                if json_ is None:
                    json_ = {
                        "type": type_,
                        "data": data
                    }
                r = requests.post(url, json=json_)
                print(r.content)


bot.add_cog(Main(bot))
bot.run(TOKEN)
