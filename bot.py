import time
from datetime import datetime, timedelta
from pytz import timezone
from pyrogram import Client          # cbgram installs itself under the name "pyrogram"
from config import Config
from aiohttp import web
from route import web_server
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ----------------------------------------
# 𝐌𝐀𝐃𝐄 𝐁𝐘 𝐀𝐁𝐇𝐈
# 𝐓𝐆 𝐈𝐃 : @𝐂𝐋𝐔𝐓𝐂𝐇𝟎𝟎𝟖
# 𝐀𝐍𝐘 𝐈𝐒𝐒𝐔𝐄𝐒 𝐎𝐑 𝐀𝐃𝐃𝐈𝐍𝐆 𝐌𝐎𝐑𝐄 𝐓𝐇𝐈𝐍𝐆𝐬 𝐂𝐀𝐍 𝐂𝐎𝐍𝐓𝐀𝐂𝐓 𝐌𝐄
# ----------------------------------------

# Removed for cbgram:
#   import pyromod.listen                      -> cbgram has built-in listen()/ask()
#   pyrogram.utils.MIN_CHANNEL_ID = ...        -> cbgram already accepts new channel ids

PORT = Config.PORT


class Bot(Client):
    def __init__(self):
        super().__init__(
            name="rexbots",
            api_id=Config.API_ID,
            api_hash=Config.API_HASH,
            bot_token=Config.BOT_TOKEN,
            workers=32,                      # cbgram default is min(32, cpus + 4); 200 was far too many
            plugins={"root": "plugins"},
            sleep_threshold=15,
        )
        self.start_time = time.time()

    async def start(self):
        await super().start()
        me = await self.get_me()
        self.mention = me.mention
        self.username = me.username
        self.uptime = Config.BOT_UPTIME

        if Config.WEBHOOK:
            app = web.AppRunner(await web_server())
            await app.setup()
            await web.TCPSite(app, "0.0.0.0", PORT).start()

        print(f"{me.first_name} Is Started.....✨️")

        uptime_seconds = int(time.time() - self.start_time)
        uptime_string = str(timedelta(seconds=uptime_seconds))

        for chat_id in [Config.LOG_CHANNEL, Config.SUPPORT_CHAT]:
            try:
                curr = datetime.now(timezone("Asia/Kolkata"))
                date = curr.strftime('%d %B, %Y')
                time_str = curr.strftime('%I:%M:%S %p')
                await self.send_photo(
                    chat_id=chat_id,
                    photo=Config.START_PIC,
                    caption=(
                        "**I ʀᴇsᴛᴀʀᴛᴇᴅ ᴀɢᴀɪɴ !**\n\n"
                        f"ɪ ᴅɪᴅɴ'ᴛ sʟᴇᴘᴛ sɪɴᴄᴇ: `{uptime_string}`"
                    ),
                    reply_markup=InlineKeyboardMarkup(
                        [[InlineKeyboardButton("ᴜᴘᴅᴀᴛᴇs", url="https://t.me/cantarellabots")]]
                    )
                )
            except Exception as e:
                print(f"Failed to send message in chat {chat_id}: {e}")

    # Needed because start() is overridden as async: run() then awaits self.stop(),
    # and without an async override cbgram's wrapped stop() returns None -> TypeError on SIGTERM.
    async def stop(self, *args):
        await super().stop()
        print("Bot stopped.")


Bot().run()
