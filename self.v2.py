from time import sleep
from pytz import timezone 
from re import sub,search
from random import choice
from datetime import datetime 
from pydub import AudioSegment

import requests, subprocess, platform, os

from pyrogram import (Client, idle, filters)
from pyrogram.raw.types import InputUserSelf
from pyrogram.raw.functions.users import GetFullUser
from pyrogram.raw.functions.contacts import GetBlocked
# from pyrogram.raw.functions.contacts import get_blocked
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardMarkup, InlineKeyboardButton)

print("started client")

bot = Client("Helper")
app = Client("iran")    
spotifyToken = "BQDC0pWsarxwBkXTPXsVHOCACbEBYjh1yyVIMvp-k1KwIyAAsfI5bANHEhHAzNorj_aEvwfNZ0jSUtiJe9-3fNEolyPu208CxgiQrTCiWjWeqU11dvZVhrJOa8b0mEJtzY8GhkwON3OgqaVUZOK3ZOBnvzKKc2Pqp8yv9qoRVr_MbokRK7F8Mm4xwIKMg-HfzBTq5zKSGZHE3nc"

numberFont = [
    ":","0","1","2","3","4","5","6","7","8","9"
    ]

numberFonts = [
[":","0","1","2","3","4","5","6","7","8","9"],
[":","𝟶","𝟷","𝟸","𝟹","𝟺","𝟻","𝟼","𝟽","𝟾","𝟿"],
[":","⓪","①","②","③","④","⑤","⑥","⑦","⑧","⑨"],
[":","⓿","❶","❷","❸","❹","❺","❻","❼","❽","❾"],
[":","𝟘","𝟙","𝟚","𝟛","𝟜","𝟝"," 𝟞","𝟟","𝟠","𝟡"],
[":","𝟬","𝟭","𝟮","𝟯","𝟰","𝟱","𝟲","𝟳","𝟴","𝟵"],
[":","０","１","２","３","４","５","６","７","８","９"],
[":","❬0❭","❬1❭","❬2❭","❬3❭","❬4❭","❬5❭","❬6❭","❬7❭","❬8❭","❬9❭"],
[":","─𝟎","─𝟏","─𝟐","─𝟑","─𝟒","─𝟓","─𝟔","─𝟕","─𝟖","─𝟗"],
[":","𝟎","𝟏","𝟐","𝟑","𝟒","𝟓","𝟔","𝟕","𝟖","𝟗"],i
[":","҉0","҉1","҉2","҉3","҉4","҉5","҉6","҉7","҉8","҉9"],
[":","𝟎","𝟏","𝟐","𝟑","𝟒","𝟓","𝟔","𝟕","𝟖","𝟗"],
[":","ꝋ","ᛑ","ᘖ","ᙣ","ᔦ","Ƽ","ᑳ","ᒣ","ზ","ᖗ"],
[":","𝒪","ﾉ","ϩ","Ӡ","५","Ƽ","Ϭ","7","𝟠","९"],
[":","۰","۱","۲","۳","۴","۵","۶","۷","۸","۹"],
[":","₀","₁","₂","₃","₄","₅","₆","₇","₈","₉"],
[":","⁰","¹","²","³","⁴","⁵","⁶","⁷","⁸","⁹"]
]

# with app:
#     offset = 0
#     limit = 10
#     blocked_contacts = app.invoke(GetBlocked(offset=offset, limit=limit))
    
#     print("Blocked Users:")
#     for user in blocked_contacts.users:
#         print(f"ID: {user.id}, Username: {getattr(user, 'username', None)}, Name: {user.first_name} {user.last_name}")

STN = ""
STB = ""
SAB = ""
BSL = ""
FONT = 0

def time(index: None):
    numbers = datetime.now(timezone("Asia/Tehran")).strftime("%H:%M")
    if index == None :
        FontNumberType = choice(numberFonts)
    else :
        FontNumberType = numberFonts[int(index)]
        
    for char in numbers :
        numbers = numbers.replace(char , FontNumberType[int(numberFont.index(str(char)))])
    return numbers

def IRTime():
    IRT = datetime.now()  
    return IRT

def rollEditor(text): 
    MEMBER = sub("MEMBER", "Member👤", text) 
    ADMIN = sub("ADMINISTRATOR", "Administrator💠", MEMBER) 
    OWNER = sub("OWNER", "Creator🔱", ADMIN) 
    DEVELOPER = sub("DEVELOPER", "Owner of BOT👨‍💻", OWNER) 
    return DEVELOPER

def get_current_track():
    def ms2min(ms):
        total_seconds = int(ms / 1000)
        minutes = int(total_seconds / 60)
        seconds = int(total_seconds - minutes * 60)
        return '{}:{:02}'.format(minutes, seconds)

    try:
        response = requests.get(
            'https://api.spotify.com/v1/me/player/currently-playing',
            headers={
                'Authorization': f'Bearer {spotifyToken}'
            }
        )
        json_resp = response.json()
        type = json_resp['currently_playing_type']
        if type == 'track':
            track_name = json_resp['item']['name']
            artists = [artist for artist in json_resp['item']['artists']]
            artist_names = ', '.join([artist['name'] for artist in artists])
            duration_ms = json_resp['item']['duration_ms']
            progress_ms = json_resp['progress_ms']

            current_track_info = {
                'track_name': track_name,
                'artists': artist_names,
                'duration': ms2min(duration_ms),
                'progress': ms2min(progress_ms),
            }
            
        else:
            current_track_info = {
                'track_name': 'ads',
                'artists': 'unknown',
                'duration': '00',
                'progress': '00',
            }
        return current_track_info
    except Exception as e:
        return {'error': str(e)}

def ping(host):
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", host]
    try:
        output = subprocess.check_output(command, stderr=subprocess.STDOUT, universal_newlines=True)
        
        if platform.system().lower() == "windows":
            match = search(r"Average = (\d+)ms", output)
            
        else:
            match = search(r"time=(\d+.?\d*) ms", output)
        response_time = match.group(1) if match else "Unknown"
        return True, response_time, output
    
    except subprocess.CalledProcessError as e:
        return False, "N/A", e.output

def sendVoice(url, output_filename):
    """Download a file from a URL and convert it from MP3 to OGG format."""
    try:
        # Download the file
        response = requests.get(url, stream=True)
        response.raise_for_status()
        temp_filename = f"{output_filename}.mp3"

        with open(temp_filename, "wb") as file:
            for chunk in response.iter_content(chunk_size=1024):
                file.write(chunk)

        audio = AudioSegment.from_mp3(temp_filename)
        audio.export(f"{output_filename}.ogg", format="ogg")

        os.remove(temp_filename)

        print(f"File downloaded and converted to {output_filename}")
    except Exception as e:
        print(f"An error occurred: {e}")

def getBio():
    with app :
        Allinformation = app.invoke(
            GetFullUser(
                id=InputUserSelf()
            )
        )
        if Allinformation.full_user.about == None:
            bio = ""
            lenght = 0
        else:
            bio = Allinformation.full_user.about
            lenght = len(bio)
        return {"bio":bio,"lenght":lenght}

with app:
    global ID
    GetID = app.get_me()
    ID = GetID.id
    print(f"user id saved . \n user id : {ID}")
    app.send_message("me" , text=
            f"╔═══ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴀʟᴇʀᴛ‌ ══\n"+
            f"║✓ ᴀᴄᴄᴇꜱꜱ ꜱᴜᴄᴄᴇꜱꜱ \n"+
            f"║» ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ɪɴʟɪɴᴇ ᴍᴏᴅᴇ ! \n"\
            f"╚═══════ ᴇɴᴅ  ══════ \n")

with bot:
    global BID
    GetBID = bot.get_me()
    BID = GetBID.username
    print(f"user id saved . \n user id : {ID}")
    bot.send_message(ID , text=
            f"╔═══ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴀʟᴇʀᴛ‌ ══\n"+
            f"║✓ ᴀᴄᴄᴇꜱꜱ ꜱᴜᴄᴄᴇꜱꜱ \n"+
            f"║» ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇ ɪɴʟɪɴᴇ ᴍᴏᴅᴇ ! \n"\
            f"╚═══════ ᴇɴᴅ  ══════ \n")
    

@bot.on_message(filters.command("start", prefixes="/"))
def echo(client, message):
    bot.send_message(
        message.chat.id,
        f"ʜᴇʟʟᴏ {message.from_user.first_name} ɪ'ᴍ ᴀ ꜱᴇʟꜰ ʜᴇʟᴘᴇʀ ꜱᴏ ɪ ᴄᴏᴜʟᴅɴ'ᴛ ᴅᴏ ᴀɴʏ ꜱᴘᴇᴄɪᴀʟ ᴛʜɪɴɢꜱ ʙᴜᴛ ɪꜰ ʏᴏᴜʀ ꜱᴇʟꜰ ɪꜱ ᴄᴏɴɴᴇᴄᴛᴇᴅ ᴛᴏ ᴛʜɪꜱ ʙᴏᴛ ʏᴏᴜ ᴄᴀɴ ᴜꜱᴇʀ ᴛʜɪꜱ ᴏᴘᴛɪᴏɴꜱ \n",
        reply_markup=InlineKeyboardMarkup(
            [
                [ 
                    InlineKeyboardButton( 
                        "ᴏᴘᴇɴ ᴘᴀɴᴇʟ",
                        switch_inline_query_current_chat="panel",
                        
                    )
                ],[
                    InlineKeyboardButton( 
                        "ᴏᴘᴇɴ ᴍᴜꜱɪᴄ ꜰɪɴᴅᴇʀ",
                        switch_inline_query_current_chat="[write music name]",
                        
                    )
                ],[
                    InlineKeyboardButton( 
                        "𝒞𝓇𝑒𝒶𝓉𝑜𝓇 & 𝒹𝑒𝓋𝑒𝓁𝑜𝓅𝑒𝓇",
                        url="t.me/Amiro_im",
                        
                    )
                ]
            ]
        )
    )
    
@app.on_message(filters.command("panel", prefixes=".")& filters.me)
def panel(client, message):
    
    inlineResults = app.get_inline_bot_results(BID,"panel")
    
    app.delete_messages(message.chat.id,
                        message.id)
    
    app.send_inline_bot_result(
        message.chat.id,
        inlineResults.query_id,
        inlineResults.results[0].id)

@app.on_message(filters.command("help", prefixes=".")& filters.me)
def echo(client, message):
        # iranTimeHM = f"{IRTime().hour}:{IRTime().minute}:{IRTime().second}" 
        # WithFont = fontEditor(iranTimeHM) 
        app.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=
        f"\n╔═══ command ════" +
        f"\n║⚉ ᴏᴘᴇɴ ꜱᴇʟꜰ ᴘᴀɴᴇʟ =><code>@[BOT USERNAME] panel</code>" +
        f"\n║⚉ <code></code>" +
        f"\n╠═══ ᴜꜱᴇʀ ɪɴꜰᴏ ════" +
        f"\n║⚉ ɢᴇᴛ ᴜꜱᴇʀ ɪɴꜰᴏ => <code>.info [REPLAY IN MESSAGE OR USER ID OR @USERNAME]</code>" +
        f"\n║⚉ ɢᴇᴛ ᴜꜱᴇʀ ɪɴꜰᴏ => <code>.user [REPLAY IN MESSAGE OR USER ID OR @USERNAME]</code>" +
        f"\n║⚉ ɢᴇᴛ ᴀᴄᴄ ɪɴꜰᴏ => <code>.accinfo</code>" +
        f"\n╠═══ ʙᴀɴ / ᴜɴʙᴀɴ ════" +
        f"\n║⚉ ʙᴀɴ ᴜꜱᴇʀ => <code>.ban [REPLAY IN MESSAGE OR USER ID OR @USERNAME]</code>" +
        f"\n║⚉ ᴜɴʙᴀɴ ᴜꜱᴇʀ => => <code>.unban  [REPLAY IN MESSAGE OR USER ID OR @USERNAME]</code>" +
        f"\n╠═══ ᴛᴀɢ ════" +
        f"\n║⚉ ᴛᴀɢ ᴇᴠᴇʀʏᴏɴᴇ => <code>.tag</code>" +
        f"\n║⚉ ᴛᴀɢ ᴀᴅᴍɪɴꜱ => <code>.tagadmin</code>" +
        f"\n║⚉ ᴛᴀɢ ᴍᴇᴍʙᴇʀꜱ => <code>.tagmember</code>" +
        f"\n╠═══ ᴅᴀᴛᴇ ════" +
        f"\n║⚉ ɢᴇᴛ ᴅᴀᴛᴇ ɪɴꜰᴏ => <code>.date</code>" +
        f"\n╠═══ ꜱᴘᴀᴍ ════" +
        f"\n║⚉ ꜱᴘᴀᴍ ᴛᴇxᴛ => <code> .spam [NUBMER (less than 100) ] t:[TEXT]</code>" +
        f"\n║⚉ ꜱᴘᴀᴍ ᴛᴀɢ => <code>.uspam [USER ID] [NUBMER (less than 100) ] t:[TEXT]</code>" +
        f"\n╠═══ ꜰᴜɴ ════" +
        f"\n║⚉ ɢᴇᴛ ɪɴꜱᴛᴀɢʀᴀᴍ ᴘᴀɢᴇ ɪɴꜰᴏ => <code>.iginfo [PAGE USERNAME]</code>" +
        f"\n║⚉ ꜱᴇɴᴅ ᴀ ᴠᴏɪᴄᴇ => <code>.voice [TEXT]</code>" +
        f"\n╚═════ ᴇɴᴅ ═══════" +
        f"\n")

@bot.on_inline_query()
def answer(client, inline_query):
    global ID
    userID = inline_query.from_user.id
    if(userID == ID):
        if ( inline_query.query == "panel" or inline_query.query == "Panel" or inline_query.query == "PANEL"):
            inline_query.answer(
                results=[
                    InlineQueryResultArticle(
                        title="Panel",
                        input_message_content=InputTextMessageContent(
                            "ꜱᴇᴛᴛɪɴɢ ᴘᴀɴᴇʟ ꜰᴏʀ **ꜱᴇʟꜰ** \n ɪɴ ᴛʜɪꜱ ᴘᴀʀᴛ ʏᴏᴜ ᴄᴀɴ ᴄᴏɴᴛʀᴏʟ ʏᴏᴜʀ ꜱᴇʟꜰ ʙʏ ᴄʟɪᴄᴋ ᴏɴ ʙᴜᴛᴛᴏɴ"
                        ),
                        description=f"ʜᴇʟʟᴏ {inline_query.from_user.first_name} ʜᴇʀᴇ ɪꜱ ʏᴏᴜʀ ꜱᴇʟꜰ ᴄᴏɴᴛʀᴏʟ ᴘᴀɴᴇʟ",
                        reply_markup=InlineKeyboardMarkup(
                            [
                                [InlineKeyboardButton(
                                    
                                    text="ꜱᴇʟꜰ ᴛɪᴍᴇ ɴᴀᴍᴇ",
                                    callback_data="n0"             
                                ),
                                InlineKeyboardButton(
                                    text="ᴛᴜʀɴ ᴏɴ",
                                    callback_data="STNon"
                                ),
                                InlineKeyboardButton(
                                    text="ᴛᴜʀɴ ᴏꜰꜰ",
                                    callback_data="STNoff"
                                )],
                                [InlineKeyboardButton(
                                    text="ꜰᴏɴᴛ'ꜱ | ᴘᴀɢᴇ 1",
                                    callback_data="None"             
                                )],
                                [
                                    InlineKeyboardButton(
                                    text=time(0),
                                    callback_data=f"font_0"             
                                ),
                                InlineKeyboardButton(
                                    text=time(1),
                                    callback_data=f"font_1" 
                                )],
                                [
                                    InlineKeyboardButton(
                                    text=time(2),
                                    callback_data=f"font_2"             
                                ),
                                InlineKeyboardButton(
                                    text=time(3),
                                    callback_data=f"font_3" 
                                )],
                                [
                                    InlineKeyboardButton(
                                    text=time(4),
                                    callback_data=f"font_4"             
                                ),
                                InlineKeyboardButton(
                                    text=time(5),
                                    callback_data=f"font_5" 
                                )],
                                [
                                    InlineKeyboardButton(
                                    text=time(6),
                                    callback_data=f"font_6"             
                                ),
                                InlineKeyboardButton(
                                    text=time(7),
                                    callback_data=f"font_7" 
                                )],
                                [
                                    InlineKeyboardButton(
                                    text=time(8),
                                    callback_data=f"font_8"             
                                ),
                                InlineKeyboardButton(
                                    text=time(9),
                                    callback_data=f"font_9" 
                                )],
                                [
                                    InlineKeyboardButton(
                                    text=time(10),
                                    callback_data=f"font_10"             
                                ),
                                InlineKeyboardButton(
                                    text=time(11),
                                    callback_data=f"font_11" 
                                )],
                                [InlineKeyboardButton(
                                    text="ᴘᴀɢᴇ'ꜱ",
                                    callback_data="none"             
                                )],
                                [InlineKeyboardButton(
                                    text="1 ✓",
                                    callback_data="page1"             
                                ),
                                InlineKeyboardButton(
                                    text="2",
                                    callback_data="page2"
                                ),
                                InlineKeyboardButton(
                                    text="3",
                                    callback_data="page3"             
                                ),
                                InlineKeyboardButton(
                                    text="4",
                                    callback_data="page4"             
                                ),
                                InlineKeyboardButton(
                                    text="5",
                                    callback_data="page5"             
                                ),
                                InlineKeyboardButton(
                                    text="6",
                                    callback_data="page6"             
                                )]

                            ]
                        )
                    )
                ],
                cache_time=1
            )
        # elif (inline_query.query != "panel" or inline_query.query != "Panel" or inline_query.query != "PANEL"):
            # musicName = inline_query.query
            # global BID
            # MusicApi = requests.get(f"https://api.deezer.com/search?q={musicName}&limit=15")
            # musics = MusicApi.json()
            # buttons = []
            # for item in musics["data"]:
            #     buttons.append(
            #         [InlineKeyboardButton(
            #         text=item["title"] ,
            #         callback_data="musiccallback_"+str(item["id"])
            #         )]
            # )
            # ReplayMarkup = InlineKeyboardMarkup(buttons)
            # inline_query.answer(
            #     results=[
            #         InlineQueryResultArticle(
            #             title="ᴍᴜꜱɪᴄ",
            #             input_message_content=InputTextMessageContent(
            #                 f"ʀᴇꜱᴜʟᴛꜱ ꜰᴏʀ {musicName} :"
            #             ),
            #             description=f"ᴜꜱᴇ @{BID} [ᴍᴜꜱɪᴄ ɴᴀᴍᴇ] ᴛᴏ ꜱʜᴏᴡ 10 ᴛᴏᴘ ᴍᴜꜱɪᴄ'ꜱ",
            #             reply_markup=ReplayMarkup
            #         )
            #     ],
            #     cache_time=1
            # )       
        else:
            pass
    elif (userID != ID):
        # global BID
        inline_query.answer(
            results=[
                 InlineQueryResultArticle(
                title="ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ",
                input_message_content=InputTextMessageContent(
                    "ᴘʟᴇᴀꜱᴇ ᴏᴘᴇɴ ᴛʜᴇ ʙᴏᴛ ꜰɪʀꜱᴛ ꜰᴏʀ **ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ**!"
                ),
                url=f"https://t.me/{BID}?start",
                description=f"ᴘʟᴇᴀꜱᴇ ᴏᴘᴇɴ ᴛʜᴇ ʙᴏᴛ ꜰɪʀꜱᴛ ꜰᴏʀ **ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ**! \n ɪꜰ ᴛʜᴇ ɪɴʟɪɴᴇ ᴍᴏᴅᴇ ɪꜱ ɴᴏᴛ ᴡᴏʀᴋɪɴɢ ꜱᴛᴀʀᴛ ᴀɢᴀɪɴ \n ɪꜰ ʏᴏᴜ ꜱᴛᴀʀᴛᴇᴅ ᴀʟʀᴇᴀᴅʏ ɪɢɴᴏʀᴇ ᴛʜɪꜱ ᴍᴇꜱꜱᴀɢᴇ",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(
                            "ᴄʟɪᴄᴋ ᴛᴏ ᴏᴘᴇɴ »",
                            url=f"https://t.me/{BID}?start"
                        )]
                    ]
                )
            )
            ],
            cache_time=1
        )
    else: 
        pass     

@bot.on_callback_query()
def answer(client, callback_query):
    global app
    global ID , STN , STB ,STB ,BSL ,FONT
    CQData = callback_query.data
    if(callback_query.from_user.id == ID):
        if(CQData == "page1"):
            bot.edit_inline_reply_markup(
                inline_message_id = callback_query.inline_message_id,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(
                            
                            text="ꜱᴇʟꜰ ᴛɪᴍᴇ ɴᴀᴍᴇ",
                            callback_data="n0"             
                        ),
                        InlineKeyboardButton(
                            text="ᴛᴜʀɴ ᴏɴ",
                            callback_data="STNon"
                        ),
                        InlineKeyboardButton(
                            text="ᴛᴜʀɴ ᴏꜰꜰ",
                            callback_data="STNoff"
                        )],
                        [InlineKeyboardButton(
                            text="ꜰᴏɴᴛ'ꜱ | ᴘᴀɢᴇ 1",
                            callback_data="None"             
                        )],
                        [
                            InlineKeyboardButton(
                            text=time(0),
                            callback_data=f"font_0"             
                        ),
                        InlineKeyboardButton(
                            text=time(1),
                            callback_data=f"font_1" 
                        )],
                        [
                            InlineKeyboardButton(
                            text=time(2),
                            callback_data=f"font_2"             
                        ),
                        InlineKeyboardButton(
                            text=time(3),
                            callback_data=f"font_3" 
                        )],
                        [
                            InlineKeyboardButton(
                            text=time(4),
                            callback_data=f"font_4"             
                        ),
                        InlineKeyboardButton(
                            text=time(5),
                            callback_data=f"font_5" 
                        )],
                        [
                            InlineKeyboardButton(
                            text=time(6),
                            callback_data=f"font_6"             
                        ),
                        InlineKeyboardButton(
                            text=time(7),
                            callback_data=f"font_7" 
                        )],
                        [
                            InlineKeyboardButton(
                            text=time(8),
                            callback_data=f"font_8"             
                        ),
                        InlineKeyboardButton(
                            text=time(9),
                            callback_data=f"font_9" 
                        )],
                        [
                            InlineKeyboardButton(
                            text=time(10),
                            callback_data=f"font_10"             
                        ),
                        InlineKeyboardButton(
                            text=time(11),
                            callback_data=f"font_11" 
                        )],
                        [InlineKeyboardButton(
                            text="ᴘᴀɢᴇ'ꜱ",
                            callback_data="none"             
                        )],
                        [InlineKeyboardButton(
                            text="1 ✓",
                            callback_data="page1"             
                        ),
                        InlineKeyboardButton(
                            text="2",
                            callback_data="page2"
                        ),
                        InlineKeyboardButton(
                            text="3",
                            callback_data="page3"             
                        ),
                        InlineKeyboardButton(
                            text="4",
                            callback_data="page4"             
                        ),
                        InlineKeyboardButton(
                            text="5",
                            callback_data="page5"             
                        ),
                        InlineKeyboardButton(
                            text="6",
                            callback_data="page6"             
                        )]
                    ]
                ),
            )
        elif(CQData == "page2"):
            bot.edit_inline_reply_markup(
                inline_message_id = callback_query.inline_message_id,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(    
                            text="ꜱᴇʟꜰ ᴛɪᴍᴇ ɴᴀᴍᴇ",
                            callback_data="n0"             
                        ),
                        InlineKeyboardButton(
                            text="ᴛᴜʀɴ ᴏɴ",
                            callback_data="STNon"
                        ),
                        InlineKeyboardButton(
                            text="ᴛᴜʀɴ ᴏꜰꜰ",
                            callback_data="STNoff"
                        )],
                        [InlineKeyboardButton(
                            text="ꜰᴏɴᴛ'ꜱ | ᴘᴀɢᴇ 2",
                            callback_data="None"             
                        )],
                        [InlineKeyboardButton(
                            text="ʀᴀɴᴅᴏᴀᴍ ⮓",
                            callback_data=f"font_None"             
                        )],
                        [InlineKeyboardButton(
                            text=time(12),
                            callback_data=f"font_12" 
                        )],
                        [InlineKeyboardButton(
                            text=time(13),
                            callback_data=f"font_13"             
                        )],
                        [InlineKeyboardButton(
                            text=time(14),
                            callback_data=f"font_14" 
                        )],
                        [InlineKeyboardButton(
                            text=time(15),
                            callback_data=f"font_15"             
                        )],
                        [InlineKeyboardButton(
                            text=time(16),
                            callback_data=f"font_16" 
                        )],
                        [InlineKeyboardButton(
                            text="ᴘᴀɢᴇ'ꜱ",
                            callback_data="none"             
                        )],
                        [InlineKeyboardButton(
                            text="1",
                            callback_data="page1"             
                        ),
                        InlineKeyboardButton(
                            text="2 ✓",
                            callback_data="page2"
                        ),
                        InlineKeyboardButton(
                            text="3",
                            callback_data="page3"             
                        ),
                        InlineKeyboardButton(
                            text="4",
                            callback_data="page4"             
                        ),
                        InlineKeyboardButton(
                            text="5",
                            callback_data="page5"             
                        ),
                        InlineKeyboardButton(
                            text="6",
                            callback_data="page6"             
                        )]
                    ]
                ),
            )
        elif(CQData == "page3"):
            bot.edit_inline_reply_markup(
                inline_message_id = callback_query.inline_message_id,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(
                            text="ʙɪᴏ | ᴘᴀɢᴇ 1",
                            callback_data="None"             
                        )],
                        [InlineKeyboardButton(
                            text="~",
                            callback_data="None"             
                        )],
                        [InlineKeyboardButton(          
                            text="ꜱᴇʟꜰ ᴛɪᴍᴇ ʙɪᴏ",
                            callback_data="n0"             
                        ),
                        InlineKeyboardButton(
                            text="ᴛᴜʀɴ ᴏɴ",
                            callback_data="STBon"
                        ),
                        InlineKeyboardButton(
                            text="ᴛᴜʀɴ ᴏꜰꜰ",
                            callback_data="STBoff"
                        )],
                        [InlineKeyboardButton(
                            text="ᴍᴀɪɴ ʙɪᴏ",
                            callback_data=f"None"             
                        ),
                        InlineKeyboardButton(
                            text="ᴛᴜʀɴ ᴏɴ",
                            callback_data=f"bio_mainBio_on" 
                        ),
                        InlineKeyboardButton(
                            text="ᴛᴜʀɴ ᴏꜰꜰ",
                            callback_data=f"bio_mainBio_off"             
                        )],
                        [InlineKeyboardButton(
                            text="ᴍᴀɪɴ + ᴛɪᴍᴇ ʙɪᴏ",
                            callback_data=f"None"             
                        ),
                        InlineKeyboardButton(
                            text="ᴛᴜʀɴ ᴏɴ",
                            callback_data=f"bio_mainBioAndTime_on" 
                        ),
                        InlineKeyboardButton(
                            text="ᴛᴜʀɴ ᴏꜰꜰ",
                            callback_data=f"bio_mainBioAndTime_off"             
                        )],
                        [InlineKeyboardButton(
                            text="ʀᴀɴᴅᴏᴀᴍ ʙɪᴏ",
                            callback_data=f"None"             
                        ),
                        InlineKeyboardButton(
                            text="ᴛᴜʀɴ ᴏɴ",
                            callback_data=f"bio_randomBio_on" 
                        ),
                        InlineKeyboardButton(
                            text="ᴛᴜʀɴ ᴏꜰꜰ",
                            callback_data=f"bio_randomBio_off"             
                        )],
                        [InlineKeyboardButton(
                            text="ꜱᴘᴏᴛɪꜰʏ ʟɪꜱᴛᴇɴɪɴɢ ᴏɴ ʙɪᴏ",
                            callback_data=f"None"             
                        ),
                        InlineKeyboardButton(
                            text="ᴛᴜʀɴ ᴏɴ",
                            callback_data=f"bio_spotify_on" 
                        ),
                        InlineKeyboardButton(
                            text="ᴛᴜʀɴ ᴏꜰꜰ",
                            callback_data=f"bio_spotify_off"             
                        )],
                        [InlineKeyboardButton(
                            text="~",
                            callback_data="None"             
                        )],
                        [InlineKeyboardButton(
                            text="ᴘᴀɢᴇ'ꜱ",
                            callback_data="none"             
                        )],
                        [InlineKeyboardButton(
                            text="1",
                            callback_data="page1"             
                        ),
                        InlineKeyboardButton(
                            text="2",
                            callback_data="page2"
                        ),
                        InlineKeyboardButton(
                            text="3 ✓",
                            callback_data="page3"             
                        ),
                        InlineKeyboardButton(
                            text="4",
                            callback_data="page4"             
                        ),
                        InlineKeyboardButton(
                            text="5",
                            callback_data="page5"             
                        ),
                        InlineKeyboardButton(
                            text="6",
                            callback_data="page6"             
                        )]
                    ]
                )
            )
        elif(CQData == "bio_spotify_off"):
            BSL = 0
            app.update_profile(last_name=f" ")
            callback_query.answer(
                f"╔═══ ꜱᴇʟꜰ ɪɴꜰᴏ‌ ════╗\n"+
                f"║⚉ ꜱᴘᴏᴛɪꜰʏ ʟɪꜱᴛᴇɴɪɴɢ\n"+
                f"║✓ ᴛᴜʀɴ ᴏꜰꜰ  \n"+
                f"╚══════ ᴇɴᴅ  ════╝ \n",
                show_alert=True)         
        elif(CQData == "bio_spotify_on"):
            BSL = 1
            callback_query.answer(
                f"╔═══ ꜱᴇʟꜰ ɪɴꜰᴏ‌ ════╗\n"+
                f"║⚉ ꜱᴘᴏᴛɪꜰʏ ʟɪꜱᴛᴇɴɪɴɢ \n"+
                f"║✓ ᴛᴜʀɴ ᴏɴ  \n"+
                f"╚══════ ᴇɴᴅ  ════╝ \n",
                show_alert=True)         
            while BSL == 1:
                try:
                    track_info = get_current_track()
                    if 'error' not in track_info:
                        print(f"{track_info['track_name']} By {track_info['artists']} | {track_info['progress']}/{track_info['duration']}")
                        app.update_profile(bio=f"𝑳𝒊𝒔𝒕𝒆𝒏𝒊𝒏𝒈 𝒕𝒐 {track_info['track_name']} 𝑩𝒚 {track_info['artists']} | {track_info['progress']}/{track_info['duration']}")
                        sleep(5)
                    else:
                        print(track_info)
                        sleep(30)
                except Exception as e:
                    print(e)
                    app.send_message("me",text=
                        f"╔═══ ᴀʟᴇʀᴛ‌ ══\n"+
                        f"║✓ ᴛʜᴇʀᴇ ᴡᴀꜱ ꜱᴏᴍᴇ ᴇʀʀᴏʀꜱ: \n"+
                        f"║» {e} \n"\
                        f"╚═══════ ᴇɴᴅ  ══════ \n")
        elif(CQData == "STNoff"):
            STN = 0
            app.update_profile(last_name=f" ")
            callback_query.answer(
                f"╔═══ ꜱᴇʟꜰ ɪɴꜰᴏ‌ ════╗\n"+
                f"║⚉ ꜱᴇʟꜰ ᴛɪᴍᴇ ɴᴀᴍᴇ \n"+
                f"║✓ ᴛᴜʀɴ ᴏꜰꜰ  \n"+
                f"╚══════ ᴇɴᴅ  ════╝ \n",
                show_alert=True)         
        elif(CQData == "STNon"):
            if STN == 0 or STN == "":
                STN = 1
                callback_query.answer(
                    f"╔═══ ꜱᴇʟꜰ ɪɴꜰᴏ‌ ════╗\n"+
                    f"║⚉ ꜱᴇʟꜰ ᴛɪᴍᴇ ɴᴀᴍᴇ \n"+
                    f"║✓ ᴛᴜʀɴ ᴏɴ  \n"+
                    f"╚══════ ᴇɴᴅ  ════╝ \n",
                    show_alert=True) 
                while STN == 1:
                    if FONT == None:
                        
                        if (IRTime().second == 00) :
                            print(time(index=choice(range(len(numberFonts) - 1))))
                            app.update_profile(last_name=time(index=time(choice(range(len(numberFonts) - 1)))))
                        sleep(1)
                        print(IRTime().second)
                    else:
                        if (IRTime().second == 00) :
                            app.update_profile(last_name=time(FONT))
                        print(IRTime().second)
                        sleep(1)
            else:
                STN = 1
                callback_query.answer(
                    f"╔═══ ꜱᴇʟꜰ ɪɴꜰᴏ‌ ════╗\n"+
                    f"║⚉ ꜱᴇʟꜰ ᴛɪᴍᴇ ɴᴀᴍᴇ \n"+
                    f"║✓ ᴡᴀꜱ ᴏɴ  \n"+
                    f"╚══════ ᴇɴᴅ  ════╝ \n",
                    show_alert=True)                  
        elif(CQData == "STBoff"):
            STB = 0
            app.update_profile(bio=f" ")
            callback_query.answer(
                f"╔═══ ꜱᴇʟꜰ ɪɴꜰᴏ‌ ════╗\n"+
                f"║⚉ ꜱᴇʟꜰ ᴛɪᴍᴇ ʙɪᴏ \n"+
                f"║✓ ᴛᴜʀɴ ᴏꜰꜰ  \n"+
                f"╚══════ ᴇɴᴅ  ════╝ \n",
                show_alert=True)                   
        elif(CQData == "STBon"):
            if STB == 0 or STB == "":
                STB = 1
                callback_query.answer(
                    f"╔═══ ꜱᴇʟꜰ ɪɴꜰᴏ‌ ════╗\n"+
                    f"║⚉ ꜱᴇʟꜰ ᴛɪᴍᴇ ʙɪᴏ \n"+
                    f"║✓ ᴛᴜʀɴ ᴏɴ  \n"+
                    f"╚══════ ᴇɴᴅ  ════╝ \n",
                    show_alert=True) 
                while STB == 1:
                    if FONT == None:
                        if (IRTime().second == 00) :
                            print(time(index=time(choice(range(len(numberFonts) - 1)))))
                            app.update_profile(bio=time(index=time(choice(range(len(numberFonts) - 1)))))
                        sleep(1)
                        print(IRTime().second)
                        
                    else:
                        print(IRTime().second)
                        if (IRTime().second == 00) :
                            app.update_profile(bio=time(FONT))
                        sleep(1)
                        # print("Bio => "+time(FONT))
                        # sleep(1)
            else:
                STB = 1
                callback_query.answer(
                    f"╔═══ ꜱᴇʟꜰ ɪɴꜰᴏ‌ ════╗\n"+
                    f"║⚉ ꜱᴇʟꜰ ᴛɪᴍᴇ ʙɪᴏ \n"+
                    f"║✓ ᴡᴀꜱ ᴏɴ  \n"+
                    f"╚══════ ᴇɴᴅ  ════╝ \n",
                    show_alert=True)                 
       
       
        elif(CQData == "bio_randomBio_off"):
            SAB = 0
            app.update_profile(bio=f" ")
            callback_query.answer(
                f"╔═══ ꜱᴇʟꜰ ɪɴꜰᴏ‌ ════╗\n"+
                f"║⚉ ꜱᴇʟꜰ ᴀᴜᴛᴏ ʙɪᴏ \n"+
                f"║✓ ᴛᴜʀɴ ᴏꜰꜰ  \n"+
                f"╚══════ ᴇɴᴅ  ════╝ \n",
                show_alert=True)                   
        
        elif(CQData == "bio_randomBio_on"):
            if SAB == 0 or SAB == "":
                SAB = 1
                callback_query.answer(
                    f"╔═══ ꜱᴇʟꜰ ɪɴꜰᴏ‌ ════╗\n"+
                    f"║⚉ ꜱᴇʟꜰ ᴀᴜᴛᴏ ʙɪᴏ \n"+
                    f"║✓ ᴛᴜʀɴ ᴏɴ  \n"+
                    f"╚══════ ᴇɴᴅ  ════╝ \n",
                    show_alert=True) 
                while SAB == 1:
                    if FONT == None:
                        if (IRTime().second == 00) :
                            print(time(index=time(choice(range(len(numberFonts) - 1)))))
                            app.update_profile(bio=time(index=time(choice(range(len(numberFonts) - 1)))))
                        sleep(1)
                        print(IRTime().second)
                        
                    else:
                        print(IRTime().second)
                        if (IRTime().second == 00) :
                            app.update_profile(bio=time(FONT))
                        sleep(1)
                        # print("Bio => "+time(FONT))
                        # sleep(1)
            else:
                SAB = 1
                callback_query.answer(
                    f"╔═══ ꜱᴇʟꜰ ɪɴꜰᴏ‌ ════╗\n"+
                    f"║⚉ ꜱᴇʟꜰ ᴀᴜᴛᴏ ʙɪᴏ \n"+
                    f"║✓ ᴡᴀꜱ ᴏɴ  \n"+
                    f"╚══════ ᴇɴᴅ  ════╝ \n",
                    show_alert=True)     
       
        elif(CQData == "font_0"): 
            FONT = 0
            
            callback_query.answer(
            f"╔═══ ᴛɪᴍᴇ ꜰᴏɴᴛ ɪɴꜰᴏ‌ ══\n"+
            f"║✓ ꜰᴏɴᴛ ᴄʜᴀɴɢᴇᴅ \n"+
            f"║⚉ ᴇxᴀᴍᴘʟᴇ :{time(index=FONT)}\n"+
            f"╚═══════ ᴇɴᴅ  ══════ \n",
            show_alert=True)
            # while FONT == 0  and STN == 1 :
            #     if (IRTime().second == 00) :
            #         app.update_profile(bio=time(index=FONT))
            # sleep(1)
        elif(CQData == "font_1"):
            FONT = 1
            
            callback_query.answer(
            f"╔═══ ᴛɪᴍᴇ ꜰᴏɴᴛ ɪɴꜰᴏ‌ ══\n"+
            f"║✓ ꜰᴏɴᴛ ᴄʜᴀɴɢᴇᴅ \n"+
            f"║⚉ ᴇxᴀᴍᴘʟᴇ :{time(index=FONT)}\n"+
            f"╚═══════ ᴇɴᴅ  ══════ \n",
            show_alert=True)
            # while FONT == 1  and STN == 1 :
            #     if (IRTime().second == 00) :
            #         app.update_profile(last_name=time(index=FONT))
            #     sleep(1)
        elif(CQData == "font_2"): 
            FONT = 2
            
            callback_query.answer(
            f"╔═══ ᴛɪᴍᴇ ꜰᴏɴᴛ ɪɴꜰᴏ‌ ══\n"+
            f"║✓ ꜰᴏɴᴛ ᴄʜᴀɴɢᴇᴅ \n"+
            f"║⚉ ᴇxᴀᴍᴘʟᴇ :{time(index=FONT)}\n"+
            f"╚═══════ ᴇɴᴅ  ══════ \n",
            show_alert=True)
            # while FONT == 2  and STN == 1 :
            #     if (IRTime().second == 00) :
            #         app.update_profile(last_name=time(index=FONT))
            #     sleep(1)         
        elif(CQData == "font_3"): 
            FONT = 3
            
            callback_query.answer(
            f"╔═══ ᴛɪᴍᴇ ꜰᴏɴᴛ ɪɴꜰᴏ‌ ══\n"+
            f"║✓ ꜰᴏɴᴛ ᴄʜᴀɴɢᴇᴅ \n"+
            f"║⚉ ᴇxᴀᴍᴘʟᴇ :{time(index=FONT)}\n"+
            f"╚═══════ ᴇɴᴅ  ══════ \n",
            show_alert=True)
            # while FONT == 3  and STN == 1 :
            #     if (IRTime().second == 00) :
            #         app.update_profile(last_name=time(index=FONT))
            #     sleep(1)   
        elif(CQData == "font_4"): 
            FONT = 4
            
            callback_query.answer(
            f"╔═══ ᴛɪᴍᴇ ꜰᴏɴᴛ ɪɴꜰᴏ‌ ══\n"+
            f"║✓ ꜰᴏɴᴛ ᴄʜᴀɴɢᴇᴅ \n"+
            f"║⚉ ᴇxᴀᴍᴘʟᴇ :{time(index=FONT)}\n"+
            f"╚═══════ ᴇɴᴅ  ══════ \n",
            show_alert=True)
            # while FONT == 4  and STN == 1 :
            #     if (IRTime().second == 00) :
            #         app.update_profile(last_name=time(index=FONT))
            #     sleep(1)
        elif(CQData == "font_5"): 
            FONT = 5
            
            callback_query.answer(
            f"╔═══ ᴛɪᴍᴇ ꜰᴏɴᴛ ɪɴꜰᴏ‌ ══\n"+
            f"║✓ ꜰᴏɴᴛ ᴄʜᴀɴɢᴇᴅ \n"+
            f"║⚉ ᴇxᴀᴍᴘʟᴇ :{time(index=FONT)}\n"+
            f"╚═══════ ᴇɴᴅ  ══════ \n",
            show_alert=True)
            # while FONT == 5  and STN == 1 :
            #     if (IRTime().second == 00) :
            #         app.update_profile(last_name=time(index=FONT))
            #     sleep(1)
        elif(CQData == "font_6"): 
            FONT = 6
            
            callback_query.answer(
            f"╔═══ ᴛɪᴍᴇ ꜰᴏɴᴛ ɪɴꜰᴏ‌ ══\n"+
            f"║✓ ꜰᴏɴᴛ ᴄʜᴀɴɢᴇᴅ \n"+
            f"║⚉ ᴇxᴀᴍᴘʟᴇ :{time(index=FONT)}\n"+
            f"╚═══════ ᴇɴᴅ  ══════ \n",
            show_alert=True)
            # while FONT == 6  and STN == 1 :
            #     if (IRTime().second == 00) :
            #         app.update_profile(last_name=time(index=FONT))
            #     sleep(1)          
        elif(CQData == "font_7"): 
            FONT = 7
            
            callback_query.answer(
            f"╔═══ ᴛɪᴍᴇ ꜰᴏɴᴛ ɪɴꜰᴏ‌ ══\n"+
            f"║✓ ꜰᴏɴᴛ ᴄʜᴀɴɢᴇᴅ \n"+
            f"║⚉ ᴇxᴀᴍᴘʟᴇ :{time(index=FONT)}\n"+
            f"╚═══════ ᴇɴᴅ  ══════ \n",
            show_alert=True)
            # while FONT == 7  and STN == 1 :
            #     if (IRTime().second == 00) :
            #         app.update_profile(last_name=time(index=FONT))
            #     sleep(1)
        elif(CQData == "font_8"): 
            FONT = 8
            
            callback_query.answer(
            f"╔═══ ᴛɪᴍᴇ ꜰᴏɴᴛ ɪɴꜰᴏ‌ ══\n"+
            f"║✓ ꜰᴏɴᴛ ᴄʜᴀɴɢᴇᴅ \n"+
            f"║⚉ ᴇxᴀᴍᴘʟᴇ :{time(index=FONT)}\n"+
            f"╚═══════ ᴇɴᴅ  ══════ \n",
            show_alert=True)
            # while FONT == 8  and STN == 1 :
            #     if (IRTime().second == 00) :
            #         app.update_profile(last_name=time(index=FONT))
            #     sleep(1)
        elif(CQData == "font_9"): 
            FONT = 9
            
            callback_query.answer(
            f"╔═══ ᴛɪᴍᴇ ꜰᴏɴᴛ ɪɴꜰᴏ‌ ══\n"+
            f"║✓ ꜰᴏɴᴛ ᴄʜᴀɴɢᴇᴅ \n"+
            f"║⚉ ᴇxᴀᴍᴘʟᴇ :{time(index=FONT)}\n"+
            f"╚═══════ ᴇɴᴅ  ══════ \n",
            show_alert=True)
            # while FONT == 9  and STN == 1 :
            #     if (IRTime().second == 00) :
            #         app.update_profile(last_name=time(index=FONT))
            #     sleep(1)
        elif(CQData == "font_10"): 
            FONT = 10
            
            callback_query.answer(
            f"╔═══ ᴛɪᴍᴇ ꜰᴏɴᴛ ɪɴꜰᴏ‌ ══\n"+
            f"║✓ ꜰᴏɴᴛ ᴄʜᴀɴɢᴇᴅ \n"+
            f"║⚉ ᴇxᴀᴍᴘʟᴇ :{time(index=FONT)}\n"+
            f"╚═══════ ᴇɴᴅ  ══════ \n",
            show_alert=True)
            # while FONT == 10  and STN == 1 :
            #     if (IRTime().second == 00) :
            #         app.update_profile(last_name=time(index=FONT))
            #     sleep(1)
        elif(CQData == "font_11"): 
            FONT = 11 
            
            callback_query.answer(
            f"╔═══ ᴛɪᴍᴇ ꜰᴏɴᴛ ɪɴꜰᴏ‌ ══\n"+
            f"║✓ ꜰᴏɴᴛ ᴄʜᴀɴɢᴇᴅ \n"+
            f"║⚉ ᴇxᴀᴍᴘʟᴇ :{time(index=FONT)}\n"+
            f"╚═══════ ᴇɴᴅ  ══════ \n",
            show_alert=True)
            # while FONT == 11  and STN == 1 :
            #     if (IRTime().second == 00) :
            #         app.update_profile(last_name=time(index=FONT))
            #     sleep(1)
        elif(CQData == "font_12"): 
            FONT = 12
            
            callback_query.answer(
            f"╔═══ ᴛɪᴍᴇ ꜰᴏɴᴛ ɪɴꜰᴏ‌ ══\n"+
            f"║✓ ꜰᴏɴᴛ ᴄʜᴀɴɢᴇᴅ \n"+
            f"║⚉ ᴇxᴀᴍᴘʟᴇ :{time(index=FONT)}\n"+
            f"╚═══════ ᴇɴᴅ  ══════ \n",
            show_alert=True)
            # while FONT == 12  and STN == 1 :
            #     if (IRTime().second == 00) :
            #         app.update_profile(last_name=time(index=FONT))
            #     sleep(1)
        elif(CQData == "font_13"): 
            FONT = 13
            
            callback_query.answer(
            f"╔═══ ᴛɪᴍᴇ ꜰᴏɴᴛ ɪɴꜰᴏ‌ ══\n"+
            f"║✓ ꜰᴏɴᴛ ᴄʜᴀɴɢᴇᴅ \n"+
            f"║⚉ ᴇxᴀᴍᴘʟᴇ :{time(index=FONT)}\n"+
            f"╚═══════ ᴇɴᴅ  ══════ \n",
            show_alert=True)
            # while FONT == 13  and STN == 1 :
            #     if (IRTime().second == 00) :
            #         app.update_profile(last_name=time(index=FONT)) 
            #     sleep(1)
        elif(CQData == "font_14"): 
            FONT = 14
            
            callback_query.answer(
            f"╔═══ ᴛɪᴍᴇ ꜰᴏɴᴛ ɪɴꜰᴏ‌ ══\n"+
            f"║✓ ꜰᴏɴᴛ ᴄʜᴀɴɢᴇᴅ \n"+
            f"║⚉ ᴇxᴀᴍᴘʟᴇ :{time(index=FONT)}\n"+
            f"╚═══════ ᴇɴᴅ  ══════ \n",
            show_alert=True)
            # while FONT == 14  and STN == 1 :
            #     if (IRTime().second == 00) :
            #         app.update_profile(last_name=time(index=FONT))
            #     sleep(1)
        elif(CQData == "font_15"): 
            FONT = 15
            
            callback_query.answer(
            f"╔═══ ᴛɪᴍᴇ ꜰᴏɴᴛ ɪɴꜰᴏ‌ ══\n"+
            f"║✓ ꜰᴏɴᴛ ᴄʜᴀɴɢᴇᴅ \n"+
            f"║⚉ ᴇxᴀᴍᴘʟᴇ :{time(index=FONT)}\n"+
            f"╚═══════ ᴇɴᴅ  ══════ \n",
            show_alert=True)
            # while FONT == 15  and STN == 1 :
            #     if (IRTime().second == 00) :
            #         app.update_profile(last_name=time(index=FONT))
            #     sleep(1)      
        elif(CQData == "font_16"): 
            FONT = 16
            
            callback_query.answer(
            f"╔═══ ᴛɪᴍᴇ ꜰᴏɴᴛ ɪɴꜰᴏ‌ ══\n"+
            f"║✓ ꜰᴏɴᴛ ᴄʜᴀɴɢᴇᴅ \n"+
            f"║⚉ ᴇxᴀᴍᴘʟᴇ :{time(index=FONT)}\n"+
            f"╚═══════ ᴇɴᴅ  ══════ \n",
            show_alert=True)
            # while FONT == 16  and STN == 1 :
            #     if (IRTime().second == 00) :
            #         app.update_profile(last_name=time(index=FONT))
            #     sleep(1)
        elif(CQData == "font_None"): 
            FONT = None
            
            callback_query.answer(
            f"╔═══ ᴛɪᴍᴇ ꜰᴏɴᴛ ɪɴꜰᴏ‌ ══\n"+
            f"║✓ ꜰᴏɴᴛ ᴄʜᴀɴɢᴇᴅ \n"+
            f"║⚉ ʀᴀɴᴅᴏᴍ\n"+
            f"╚═══════ ᴇɴᴅ  ══════ \n",
            show_alert=True)
            # while FONT == None  and STN == 1 :
            #     if (IRTime().second == 00) :
            #         app.update_profile(last_name=time(index=FONT))
            #     sleep(1)
        elif(CQData == "close"):
            chat_id = callback_query.message.chat.id
            app.delete_messages(chat_id=chat_id ,message_ids=callback_query.message.id)
        else:
            callback_query.answer(
            f"╔═══ ᴇʀʀᴏʀ ══\n"+
            f"║✓ ᴄᴏᴍɪɴɢ ꜱᴏᴏɴ! \n"+
            f"╚═══════ ᴇɴᴅ  ══════ \n",)
    else:
        callback_query.answer(
            f"╔═══ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴀʟᴇʀᴛ‌ ══\n"+
            f"║✓ ᴀᴄᴄᴇꜱꜱ ᴅᴇɴɪᴇᴅ \n"+
            f"║» ɪᴛ'ʟʟ ʙᴇ ʙᴇᴛᴛᴇʀ ɪꜰ \n"
            f"║» ʏᴏᴜ ꜱᴛᴀʏ ɪɴ ʏᴏᴜʀ ʟɪᴍɪᴛꜱ.\n"
            f"╚═══════ ᴇɴᴅ  ══════ \n",
        show_alert=True)
        app.send_message("me" , text=
            f"╔═══ ᴠᴇʀɪꜰɪᴄᴀᴛɪᴏɴ ᴀʟᴇʀᴛ‌ ══\n"+
            f"║✓ ᴀᴄᴄᴇꜱꜱ ᴅᴇɴɪᴇᴅ \n"+
            f"║» <a href='tg://openmessage?user_id={callback_query.from_user.id}'>{callback_query.from_user.first_name } </a> ᴛʀʏ ᴛᴏ ᴜꜱᴇ ᴘᴀɴᴇʟ.\n"
            f"║» ɪᴅ : <code>{callback_query.from_user.id }</code>\n"
            f"║» ᴜꜱᴇʀɴᴀᴍᴇ : @{callback_query.from_user.username }\n"
            f"╚═══════ ᴇɴᴅ  ══════ \n",)

@app.on_message(filters.command("spam", prefixes=".")& filters.me)
def echo(client, message):
    spamTotal = eval(message.text.split(" ")[1])
    spamText = message.text.split("t:")[1]
    if spamTotal > 100 :
        app.edit_message_text(chat_id=message.chat.id,
        message_id=message.id, 
        text=
        f"╔═══ ᴇʀʀᴏʀ ɪɴꜰᴏ‌ ════ \n"+
        f"║✗ ᴛʜᴇ ʟɪᴍɪᴛ ꜰᴏʀ ꜱᴘᴀᴍ ɪꜱ 100 \n"+
        f"║⚉ ʏᴏᴜʀ ᴠᴀʟᴜᴇ : {spamTotal}\n"+
        f"╚═════ ᴇɴᴅ ════════ \n")

    else :
        app.edit_message_text(chat_id=message.chat.id,
        message_id=message.id, 
        text=
        f"╔═══ ꜱᴘᴀᴍ ɪɴꜰᴏ‌ ════ \n"+
        f"║✓ ꜱᴘᴀᴍ ꜱᴛᴀʀᴛ\n"+
        f"║⚉ {spamTotal} ᴛɪᴍᴇꜱ ᴏɴ {spamText}\n"+
        f"╚═════ ᴇɴᴅ ═══════ \n")
        for x in range(spamTotal):
            app.send_message(message.chat.id , text=f"{x + 1}/{spamTotal} | {spamText}")

@app.on_message(filters.command("uspam", prefixes=".")& filters.me)
def echo(client, message):
    spamUID = message.text.split(" ")[1]
    spamTotal = eval(message.text.split(" ")[2])
    spamText = message.text.split("t:")[1]
    if spamTotal > 100 :
        app.edit_message_text(chat_id=message.chat.id,
        message_id=message.id, 
        text=        
        f"╔═══ ᴇʀʀᴏʀ ɪɴꜰᴏ‌ ════ \n"+
        f"║✗ ᴛʜᴇ ʟɪᴍɪᴛ ꜰᴏʀ ꜱᴘᴀᴍ ɪꜱ 100 \n"+
        f"║⚉ ʏᴏᴜʀ ᴠᴀʟᴜᴇ : {spamTotal}\n"+
        f"╚═════ ᴇɴᴅ ═══════ \n")
    else :
        app.edit_message_text(chat_id=message.chat.id,
        message_id=message.id, 
        text=
        f"╔═══ ꜱᴘᴀᴍ ɪɴꜰᴏ‌ ════ \n"+
        f"║✓ ꜱᴘᴀᴍ ꜱᴛᴀʀᴛ\n"+
        f"║⚉ {spamTotal} ᴛɪᴍᴇꜱ ᴏɴ <a href='tg://user?id={spamUID}'>ᴛʜɪꜱ ᴜꜱᴇʀ</a>\n"+
        f"╚═════ ᴇɴᴅ ═══════ \n")
        for x in range(spamTotal):
            app.send_message(message.chat.id , text=f"{x + 1}/{spamTotal} | <a href='tg://user?id={spamUID}'>{spamText}</a>")

@app.on_message(filters.command("ban", prefixes=".")& filters.group & filters.me)
def echo(client, message):
    if message.reply_to_message :
        member = app.get_chat_member(message.chat.id ,message.reply_to_message.from_user.id)
        app.ban_chat_member(message.chat.id ,message.reply_to_message.from_user.id),
        app.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=
        f"╔═══ ʙᴀɴ ɪɴꜰᴏ‌ ════ \n"+
        f"║⚉ ᴜꜱᴇʀ <a href='tg://user?id={message.reply_to_message.from_user.id}'>{message.reply_to_message.from_user.first_name}</a> \n"+
        f"║✓ ʙᴀɴ ʙʏ <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> \n"
        f"╚═════ ᴇɴᴅ ═══════ \n"
        )
    elif message.text.split(" ")[1] :
        uid = message.text.split(" ")[1]
        member = app.get_chat_member(message.chat.id ,uid)
        app.ban_chat_member(message.chat.id ,member.user.id),
        app.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=
        f"╔═══ ʙᴀɴ ɪɴꜰᴏ‌ ════ \n"+
        f"║⚉ ᴜꜱᴇʀ <a href='tg://user?id={member.user.id}'>{member.user.first_name}</a> \n"+
        f"║✓ ʙᴀɴ ʙʏ <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> \n"
        f"╚═════ ᴇɴᴅ ═══════ \n"
        )
    elif message.text.split(" @")[1] :
        username = message.text.split(" @")[1]
        member = app.get_chat_member(message.chat.id ,username)
        app.ban_chat_member(message.chat.id ,member.user.id),
        app.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=
        f"╔═══ ʙᴀɴ ɪɴꜰᴏ‌ ════ \n"+
        f"║⚉ ᴜꜱᴇʀ <a href='tg://user?id={member.user.id}'>{member.user.first_name}</a>> \n"+
        f"║✓ ʙᴀɴ ʙʏ <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> \n"
        f"╚═════ ᴇɴᴅ ═══════ \n"
        )

@app.on_message(filters.command("unban", prefixes=".")& filters.group & filters.me)
def echo(client, message):
    if message.reply_to_message :
        member = app.get_chat_member(message.chat.id ,message.reply_to_message.from_user.id)
        app.unban_chat_member(message.chat.id ,message.reply_to_message.from_user.id),
        app.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=
        f"╔═══ ᴜɴʙᴀɴ ɪɴꜰᴏ‌ ════ \n"+
        f"║⚉ ᴜꜱᴇʀ <a href='tg://user?id={message.reply_to_message.from_user.id}'>{message.reply_to_message.from_user.first_name}</a> \n"+
        f"║✓ ᴜɴʙᴀɴ ʙʏ <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> \n"
        f"╚═════ ᴇɴᴅ ═══════ \n"
        )
    elif message.text.split(" ")[1] :
        uid = message.text.split(" ")[1]
        member = app.get_chat_member(message.chat.id ,uid)
        app.unban_chat_member(message.chat.id ,member.user.id),
        app.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=
        f"╔═══ ᴜɴʙᴀɴ ɪɴꜰᴏ‌ ════ \n"+
        f"║⚉ ᴜꜱᴇʀ <a href='tg://user?id={member.user.id}'>{member.user.first_name}</a> \n"+
        f"║✓ ᴜɴʙᴀɴ ʙʏ <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> \n"
        f"╚═════ ᴇɴᴅ ═══════ \n"
        )
    elif message.text.split(" @")[1] :
        username = message.text.split(" @")[1]
        member = app.get_chat_member(message.chat.id ,username)
        app.unban_chat_member(message.chat.id ,member.user.id),
        app.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=
        f"╔═══ ᴜɴʙᴀɴ ɪɴꜰᴏ‌ ════ \n"+
        f"║⚉ ᴜꜱᴇʀ <a href='tg://user?id={member.user.id}'>{member.user.first_name}</a>> \n"+
        f"║✓ ᴜɴʙᴀɴ ʙʏ <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name}</a> \n"
        f"╚═════ ᴇɴᴅ ═══════ \n"
        )

@app.on_message(filters.command("info", prefixes=".")& filters.me)
def echo(client, message): 
    if message.reply_to_message :
        status = ""
        member = app.get_chat_member(message.chat.id ,message.reply_to_message.from_user.id)
        StatusMember = str(member.status).split("ChatMemberStatus.")[1]
        if message.reply_to_message.from_user.id == 905259902:
            status += rollEditor("DEVELOPER")
        else:
            status += rollEditor(StatusMember)
        app.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=
            f"\n╔═══ ᴄʜᴀᴛ ɪɴꜰᴏ‌ ════" +
            f"\n║⚉ ᴍᴇꜱꜱᴀɢᴇ ɴᴜᴍʙᴇʀ‌ {message.reply_to_message.id}" +
            f"\n║⚉ ᴄʜᴀᴛ ɴᴀᴍᴇ‌ : <code>{message.chat.title or message.chat.first_name}</code>" +
            f"\n║⚉ ᴄʜᴀᴛ ɪᴅ‌ : <code>{message.chat.id}</code>" +
            f"\n╠═══ ᴜꜱᴇʀ ɪɴꜰᴏ ════" +
            f"\n║⚉ ᴜꜱᴇʀ ɴᴀᴍᴇ ‌: <a href='tg://user?id={message.reply_to_message.from_user.id}'>{message.reply_to_message.from_user.first_name } </a>" +
            f"\n║⚉ ᴜꜱᴇʀ ɪᴅ‌ : <code>{message.reply_to_message.from_user.id}</code>" +
            f"\n║⚉ ᴜꜱᴇʀ ᴜꜱᴇʀɴᴀᴍᴇ : <code>@{message.reply_to_message.from_user.username}</code>" +
            f"\n║⚉ ᴜꜱᴇʀ ꜱᴛᴀᴛᴜꜱ : {status}" +
            # f"\n║⚉ ᴛɪᴍᴇ : <code>{WithFont}</code>" +
            f"\n╚═════ ᴇɴᴅ ═══════" +
            f"\n"
            )
    elif message.text.split(" ")[1] :
        uid = message.text.split(" ")[1]
        status = ""
        member = app.get_chat_member(message.chat.id ,uid)
        StatusMember = str(member.status).split("ChatMemberStatus.")[1]
        if message.reply_to_message.from_user.id == 905259902:
            status += rollEditor("DEVELOPER")
        else:
            status += rollEditor(StatusMember)
        app.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=
            f"\n╔═══ ᴄʜᴀᴛ ɪɴꜰᴏ‌ ════" +
            f"\n║⚉ ᴍᴇꜱꜱᴀɢᴇ ɴᴜᴍʙᴇʀ‌ {message.id}" +
            f"\n║⚉ ᴄʜᴀᴛ ɴᴀᴍᴇ‌ : <code>{message.chat.title or message.chat.first_name}</code>" +
            f"\n║⚉ ᴄʜᴀᴛ ɪᴅ‌ : <code>{message.chat.id}</code>" +
            f"\n╠═══ ᴜꜱᴇʀ ɪɴꜰᴏ ════" +
            f"\n║⚉ ᴜꜱᴇʀ ɴᴀᴍᴇ ‌: <a href='tg://user?id={member.user.id}'>{member.user.first_name }</a>" +
            f"\n║⚉ ᴜꜱᴇʀ ɪᴅ‌ : <code>{uid}</code>" +
            f"\n║⚉ ᴜꜱᴇʀ ᴜꜱᴇʀɴᴀᴍᴇ : <code>@{member.user.username}</code>" +
            f"\n║⚉ ᴜꜱᴇʀ ꜱᴛᴀᴛᴜꜱ : {status}" +
            # f"\n║⚉ ᴛɪᴍᴇ : <code>{WithFont}</code>" +
            f"\n╚═════ ᴇɴᴅ ═══════" +
            f"\n"
            )
    elif message.text.split(" @")[1] :
        username = message.text.split(" @")[1]
        status = ""
        member = app.get_chat_member(message.chat.id ,username)
        StatusMember = str(member.status).split("ChatMemberStatus.")[1]
        if message.reply_to_message.from_user.id == 905259902:
            status += rollEditor("DEVELOPER")
        else:
            status += rollEditor(StatusMember)
        app.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=
            f"\n╔═══ ᴄʜᴀᴛ ɪɴꜰᴏ‌ ════" +
            f"\n║⚉ ᴍᴇꜱꜱᴀɢᴇ ɴᴜᴍʙᴇʀ‌ {message.id}" +
            f"\n║⚉ ᴄʜᴀᴛ ɴᴀᴍᴇ‌ : <code>{message.chat.title or message.chat.first_name}</code>" +
            f"\n║⚉ ᴄʜᴀᴛ ɪᴅ‌ : <code>{message.chat.id}</code>" +
            f"\n╠═══ ᴜꜱᴇʀ ɪɴꜰᴏ ════" +
            f"\n║⚉ ᴜꜱᴇʀ ɴᴀᴍᴇ ‌: <a href='tg://user?id={member.user.id}'>{member.user.first_name }</a>" +
            f"\n║⚉ ᴜꜱᴇʀ ɪᴅ‌ : <code>{member.user.id}</code>" +
            f"\n║⚉ ᴜꜱᴇʀ ᴜꜱᴇʀɴᴀᴍᴇ : <code>@{member.user.username}</code>" +
            f"\n║⚉ ᴜꜱᴇʀ ꜱᴛᴀᴛᴜꜱ : {status}" +
            # f"\n║⚉ ᴛɪᴍᴇ : <code>{WithFont}</code>" +
            f"\n╚═════ ᴇɴᴅ ═══════" +
            f"\n"
            )

@app.on_message(filters.command("user", prefixes=".")& filters.me)
def echo(client, message):
    # iranTimeHM = f"{IRTime().hour}:{IRTime().minute}:{IRTime().second}" 
    # WithFont = fontEditor(iranTimeHM) 
    if message.reply_to_message :
        member = app.get_users(message.reply_to_message.from_user.id)
        app.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=
            f"\n╔═══ ᴄʜᴀᴛ ɪɴꜰᴏ‌ ════" +
            f"\n║⚉ ᴍᴇꜱꜱᴀɢᴇ ɴᴜᴍʙᴇʀ‌ {message.reply_to_message.id}" +
            f"\n║⚉ ᴄʜᴀᴛ ɴᴀᴍᴇ‌ : <code>{message.chat.title or message.chat.first_name}</code>" +
            f"\n║⚉ ᴄʜᴀᴛ ɪᴅ‌ : <code>{message.chat.id}</code>" +
            f"\n╠═══ ᴜꜱᴇʀ ɪɴꜰᴏ ════" +
            f"\n║⚉ ᴜꜱᴇʀ ɴᴀᴍᴇ ‌: <a href='tg://user?id={member.id}'>{member.first_name } </a>" +
            f"\n║⚉ ᴜꜱᴇʀ ɪᴅ‌ : <code>{member.id}</code>" +
            f"\n║⚉ ᴜꜱᴇʀ ᴜꜱᴇʀɴᴀᴍᴇ : <code>@{member.username}</code>" +
            # f"\n║⚉ ᴛɪᴍᴇ : <code>{WithFont}</code>" +
            f"\n╚═════ ᴇɴᴅ ═══════" +
            f"\n"
            )
    elif message.text.split(" @")[1] :
        username = message.text.split(" @")[1]
        member = app.get_users(username)
        print(member)
        app.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=
            f"\n╔═══ ᴄʜᴀᴛ ɪɴꜰᴏ‌ ════" +
            f"\n║⚉ ᴍᴇꜱꜱᴀɢᴇ ɴᴜᴍʙᴇʀ‌ {message.id}" +
            f"\n║⚉ ᴄʜᴀᴛ ɴᴀᴍᴇ‌ : <code>{message.chat.title or message.chat.first_name}</code>" +
            f"\n║⚉ ᴄʜᴀᴛ ɪᴅ‌ : <code>{message.chat.id}</code>" +
            f"\n╠═══ ᴜꜱᴇʀ ɪɴꜰᴏ ════" +
            f"\n║⚉ ᴜꜱᴇʀ ɴᴀᴍᴇ ‌: <a href='tg://user?id={member.id}'>{member.first_name }</a>" +
            f"\n║⚉ ᴜꜱᴇʀ ɪᴅ‌ : <code>{member.id}</code>" +
            f"\n║⚉ ᴜꜱᴇʀ ᴜꜱᴇʀɴᴀᴍᴇ : <code>@{member.username}</code>" +
            # f"\n║⚉ ᴛɪᴍᴇ : <code>{WithFont}</code>" +
            f"\n╚═════ ᴇɴᴅ ═══════" +
            f"\n"
            )
    elif message.text.split(" ")[1] :
        uid = message.text.split(" ")[1]
        member = app.get_users(uid)
        app.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=
            f"\n╔═══ ᴄʜᴀᴛ ɪɴꜰᴏ‌ ════" +
            f"\n║⚉ ᴍᴇꜱꜱᴀɢᴇ ɴᴜᴍʙᴇʀ‌ {message.id}" +
            f"\n║⚉ ᴄʜᴀᴛ ɴᴀᴍᴇ‌ : <code>{message.chat.title or message.chat.first_name}</code>" +
            f"\n║⚉ ᴄʜᴀᴛ ɪᴅ‌ : <code>{message.chat.id}</code>" +
            f"\n╠═══ ᴜꜱᴇʀ ɪɴꜰᴏ ════" +
            f"\n║⚉ ᴜꜱᴇʀ ɴᴀᴍᴇ ‌: <a href='tg://user?id={member.id}'>{member.first_name }</a>" +
            f"\n║⚉ ᴜꜱᴇʀ ɪᴅ‌ : <code>{uid}</code>" +
            f"\n║⚉ ᴜꜱᴇʀ ᴜꜱᴇʀɴᴀᴍᴇ : <code>@{member.username}</code>" +
            # f"\n║⚉ ᴛɪᴍᴇ : <code>{WithFont}</code>" +
            f"\n╚═════ ᴇɴᴅ ═══════" +
            f"\n"
            )
        
@app.on_message(filters.command("accinfo", prefixes=".")& filters.me)
def echo(client, message):
    # iranTimeHM = f"{IRTime().hour}:{IRTime().minute}:{IRTime().second}" 
    # WithFont = fontEditor(iranTimeHM) 
    app.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=
        f"\n╔═══ ᴄʜᴀᴛ ɪɴꜰᴏ‌ ════" +
        f"\n║⚉ ᴍᴇꜱꜱᴀɢᴇ ɴᴜᴍʙᴇʀ‌ {message.id}" +
        f"\n║⚉ ᴄʜᴀᴛ ɴᴀᴍᴇ‌ : <code>{message.chat.title or message.chat.first_name}</code>" +
        f"\n║⚉ ᴄʜᴀᴛ ɪᴅ‌ : <code>{message.chat.id}</code>" +
        f"\n╠═══ ᴜꜱᴇʀ ɪɴꜰᴏ ════" +
        f"\n║⚉ ᴜꜱᴇʀ ɴᴀᴍᴇ ‌: <a href='tg://user?id={message.from_user.id}'>{message.from_user.first_name } </a>" +
        f"\n║⚉ ᴜꜱᴇʀ ɪᴅ‌ : <code>{message.from_user.id}</code>" +
        f"\n║⚉ ᴜꜱᴇʀ ᴜꜱᴇʀɴᴀᴍᴇ : <code>@{message.from_user.username}</code>" +
        # f"\n║⚉ ᴛɪᴍᴇ : <code>{WithFont}</code>" +
        f"\n╚═════ ᴇɴᴅ ═══════" +
        f"\n"
    )
    
@app.on_message(filters.command("tag", prefixes=".")& filters.me)
def echo(client, message):
    app.get_chat_members(message.chat.id)
    members = "╔═══ ᴍᴇᴍʙᴇʀ'ꜱ‌ ════ \n"
    LastNameNone = ""
    for member in app.get_chat_members(message.chat.id):
        members += f"║⚉ <a href='tg://user?id={member.user.id}'>{member.user.first_name}{member.user.last_name or LastNameNone}</a> \n"
    app.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=members)

@app.on_message(filters.command("tagadmin", prefixes=".")& filters.me)
def echo(client, message):
    LastNameNone = ""
    admins = "╔═══ admin'ꜱ‌ ════ \n"
    for member in app.get_chat_members(message.chat.id):
        StatusMember = str(member.status).split("ChatMemberStatus.")[1]
        if StatusMember == "ADMINISTRATOR" or StatusMember == "OWNER":
            admins += f"║⚉ {member.user.first_name}{member.user.last_name or LastNameNone}\n"

    app.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=admins)

@app.on_message(filters.command("tagmember", prefixes=".")& filters.me)
def echo(client, message):
    LastNameNone = ""
    memberONLY = "╔═══ ᴍᴇᴍʙᴇʀ'ꜱ‌ ════ \n"
    for member in app.get_chat_members(message.chat.id):
        StatusMember = str(member.status).split("ChatMemberStatus.")[1]
        if StatusMember == "MEMBER":
            memberONLY += f"║⚉ {member.user.first_name}{member.user.last_name or LastNameNone}\n"

    app.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=memberONLY)

@app.on_message(filters.command("ping", prefixes=".")& filters.me)
def echo(client, message):
    
    if len(message.text.split(" ")) == 1 :
        link = "api.telegram.org"
    else :
        link = message.text.split(" ")[1]
    
    reachable, response_time, response = ping(link)
        
    app.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=        
        f"╔═══ ꜱᴇʀᴠᴇʀ ɪɴꜰᴏ‌ ════ \n"+
        f"║⚉ ᴡᴇʙꜱɪᴛᴇ: {link} \n"+
        f"║⚉ ᴘɪɴɢ: {response_time} ᴍꜱ \n"+
        f"╚═════ ᴇɴᴅ ═══════ \n")

@app.on_message(filters.command("date", prefixes=".") &filters.me)
def echo(client, message):
    DateReq = requests.get("https://api.demiro.me/date-info/").json()
    date = DateReq['results_date'][0]
    ToDay = date["todayEN"] +" | " + date['todayFA']  
    Month = date["monthEN"] +" | " + date['monthFA']  
    Session = date["Seasonsen"] +" | " + date['Seasonsfa']  
    AnimalOfYear = date['Animal']
    DaysPast = date['past']
    DaysRemaining = date['remaining']
    # MorA = date["morning-or-afternonEN"] + " | " + ["morning-or-afternonFA"]
    fullDate =  date["dateen"] +" | 14" + date['datefa']  
    
    justTime = f"{IRTime().hour}:{IRTime().minute}:{IRTime().second}" 
    app.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=
                          f"╔═ ᴅᴀᴛᴇ ɪɴꜰᴏ‌ ══ \n"+
                          f"║⚉ ᴛᴏᴅᴀʏ : {ToDay}\n"+
                          f"║⚉ ᴍᴏɴᴛʜ : {Month}\n"+
                          f"║⚉ ꜱᴇꜱꜱɪᴏɴ : {Session}\n"+
                          f"║⚉ ᴀɴɪᴍᴀʟ ᴏꜰ ʏᴇᴀʀ : {AnimalOfYear}\n" +
                          f"║⚉ ᴅᴀʏ'ꜱ ᴘᴀꜱᴛ : {DaysPast}\n"+
                          f"║⚉ ᴅᴀʏ'ꜱ ʀᴇᴍᴀɪɴɪɴɢ : {DaysRemaining}\n"+
                          f"║⚉ ᴛɪᴍᴇ : {justTime}\n"+
                        #   f"║⚉ {MorA}\n"+
                          f"║⚉ ᴅᴀᴛᴇ : {fullDate}\n"+
                          f"╚═════ ᴇɴᴅ ═══════ \n"
                          )
    
@app.on_message(filters.command("iginfo", prefixes=".") &filters.me)
def echo(client, message):
    accid = message.text.split(" ")[1]
    license = "9RsXKcMzRy5zB1Dg3abwLXlzhgSLrc5fMFfUUCrzb85nV9zp7eYh"
    igreq = requests.get(f"https://api2.haji-api.ir/instainfo/?license={license}&text={accid}").json()
    acc = igreq["result"][0]
    bio = acc["biography"]
    name = acc["full_name"]
    username = acc["username"]
    links = ""
    for link in acc["bio_links"]:
        linkUrl = link["url"]
        linkTitle = link["title"] 
        links += f"║⚉ ʟɪɴᴋ'ꜱ : <a href='{linkUrl}'>{linkTitle}</a> \n"
    is_privet = acc["is_private"]
    followers = acc["follower_count"]
    followeings =  acc["following_count"]
    posts = acc["media_count"]
    app.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=
                          f"╔═ ɪɴꜱᴛᴀɢʀᴀᴍ ᴀᴄᴄᴏᴜɴᴛ ɪɴꜰᴏ‌ ══ \n"+
                          f"║⚉ ɴᴀᴍᴇ : {name}\n"+
                          f"║⚉ ᴜꜱᴇʀɴᴀᴍᴇ : {username}\n"+
                          f"║⚉ ʙɪᴏ : {bio}\n"+
                          f"║⚉ ꜰᴏʟʟᴏᴡᴇʀ'ꜱ : {followers}\n" +
                          f"║⚉ ꜰᴏʟʟᴏᴡɪɴɢ'ꜱ : {followeings}\n"+
                          f"║⚉ ᴘᴏꜱᴛ'ꜱ : {posts}\n"+
                          f"║⚉ ɪꜱ ᴘʀɪᴠᴀᴛᴇ : {is_privet}\n"+
                          f"{links}"+
                          f"╚═════ ᴇɴᴅ ═══════ \n"
                          )

@app.on_message(filters.command("voice", prefixes=".")& filters.me)
def echo(client, message):
    app.delete_messages(message.chat.id , message.id)
    text = message.text.split(".voice")[1]
    ReqVoice = requests.get(f"https://api.irateam.ir/create-voice/?text={text}&Character=FaridNeural").json()
    Voice = ReqVoice['results']['url']
    
    sendVoice(Voice,text)
    
    if message.reply_to_message :
        app.send_voice(message.chat.id , f"{text}.ogg" , reply_to_message_id=message.reply_to_message.id)
        os.remove(f"{text}.ogg")
        
    else :
        app.send_voice(message.chat.id , f"{text}.ogg" )
        os.remove(f"{text}.ogg")
        
@app.on_message(filters.command("spotifytoken", prefixes="")& filters.me)
def echo(client, message):
    global spotifyToken
    spotifyToken2 = message.text.split("spotifytoken")[1]
    app.edit_message_text(chat_id=message.chat.id, message_id=message.id, text=
                          f"Spotify Token Updated From\n <code>{spotifyToken}</code> to \n <code>{spotifyToken2}</code>")
    spotifyToken = spotifyToken2



app.start()
bot.start()

idle()

print("started!")
