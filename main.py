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

async def toggle_role(member:discord.Member, role:discord.Role):
    if role in member.roles:
        await member.remove_roles(role, reason="По требованию пользователя")
    else:
        await member.add_roles(role, reason="По требованию пользователя")

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
    async def role(self, ctx: commands.Context, arg = "1"):
        lst = []
        options1 = []
        options2 = []
        e_name = None
        e_id = None
        for role in ctx.guild.roles:
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

            if len(options1) < 25:
                options1.append(SelectOption(role.name, role.id, e_name=e_name, e_id=e_id))
            else:
                options2.append(SelectOption(role.name, role.id, e_name=e_name, e_id=e_id))

        response = requests.request("POST", f"https://discord.com/api/v9/channels/{ctx.channel.id}/messages",
                                    json =

                                    {
                                        "content": f"Игровые роли (Страница {arg} из 2)",
                                        "components": [ActionRaw([
                                            SelectMenu(
                                                "role_selection",
                                                "Выберите любые интересующие вас роли",
                                                max_values=len(options1 if arg == "1" else options2),
                                                options=options1 if arg == "1" else options2
                                            )
                                        ])]

                                    }
                                    ,
                                    headers = { "Authorization": f"Bot {TOKEN}",
                                                "Content-Type": "application/json"})
        print(response.status_code, response.content if response.status_code != 200 else "")

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
        await CreateSlashCommand(name, description, None, SlashCommandOption(4, "Страница", "Выберите страницу", choices=[{"name": 1, "value": "1"}, {"name": 2, "value": "2"}]))
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

            json_ = None
            content = None
            type_ = 4
            print(interaction_type)

            if interaction_type == 3:
                component_type  = msg["d"]["data"]["component_type"]
                member_id       = msg["d"]["member"]["user"]["id"]
                message_id      = msg["d"]["message"]["id"]
                message_content = msg["d"]["message"]["content"]
                guild_id        = msg["d"]["guild_id"]
                channel_id      = msg["d"]["message"]["channel_id"]



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

                    else:
                        content = f"Clicked! ID = {button_id}"

                elif component_type == 3:
                    values = msg["d"]["data"]["values"]
                    selection_id = msg["d"]["data"]["custom_id"]
                    if selection_id == "role_selection":
                        content = f"Выбранные роли установленны"
                        guild = await bot.fetch_guild(guild_id)
                        member = await guild.fetch_member(member_id)
                        for role in values:
                            role = guild.get_role(int(role))
                            await toggle_role(member, role)
                    else:
                        content = f"You have chosen these selections: {values}"
            elif interaction_type == 2:
                name = msg["d"]["data"]["name"]
                if name == "ping":
                    content = f"`{round(bot.latency * 1000, 2)}`"
                if name == "role":
                    pass

            url = f"https://discord.com/api/v9/interactions/{interaction_id}/{interaction_token}/callback"
            if content is not None:

                if json_ is None:
                    json_ = {
                        "type": type_,
                        "data": {
                            "content": content,
                            "flags": 64,

                        }
                    }
                requests.post(url, json=json_)


bot.add_cog(Main(bot))
bot.run(TOKEN)



