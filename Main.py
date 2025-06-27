import asyncio
from telethon import TelegramClient, events, functions
from telethon.sessions import StringSession
import random

# Dost ka API aur session
api_id = 22718643
api_hash = "5b7eb1cd80f5090705d73d17ada7d729"
session_string = "1BVtsOKsBu6964Nx4cjCtCPJ70hn9wV--CXk7nwZmHmyWvPebEqEVbCuKioqia8i8ogOywFwXYEwyfR5d4Q-KKtaIP8KQb7qUv-sx5HNvPs-gS4wqWm4d2UYMhz_bM5cDGbeGwGsUjpvmoeM3PWppaHfofs76_t8Q-MkymtE472WWk58IMp533QbdwDfFzWi4i1zX1LYrgCtqy3o6OkzSsm9r2RD2umyYce1eYDoJHLl_4CFa5YIFRQB0M85Nv5MKZi5r8AnKmGdcknAQkSoppsH6RxK7LPm8QGO9Z1rJtR8f0lQeAs8fdfwvPA6jSzJpuapc1EmxLoQAl8XLv4rAke47yc52jKw="

OWNER_ID = 7285681667  # Dost ka Telegram ID

CRYPTO_ADDRESSES = {
    ".btc": "16eiD5bGe2u7MvNMG9uzvG5NEJvVKLpuzW",
    ".eth": "0xcd936fadde7436dc6a7ff2c02830ab69f2444c50",
    ".ton": "EQD5mxRgCuRNLxKxeOjG6r14iSroLF5FtomPnet-sgP5xNJb\nMEMO: 111939307",
    ".ltc": "LNeLQpEjmH87ctjDdZpmcvAWt5d1Pn9eVd",
    ".sol": "3YHbxsJFLqXTAsxnkKCN1T48Gt2h33qxbtg9EUfty9Sv",
    ".usdt": "0xcd936fadde7436dc6a7ff2c02830ab69f2444c50"
}

client = TelegramClient(StringSession(session_string), api_id, api_hash)


@client.on(events.NewMessage(outgoing=True, pattern=r'^\.\w+'))
async def handler(event):
    if event.sender_id != OWNER_ID:
        return

    cmd = event.raw_text.strip().lower()
    try:
        if cmd in CRYPTO_ADDRESSES:
            await event.reply(f"{CRYPTO_ADDRESSES[cmd]}")
        elif cmd == ".rec":
            await event.reply("✅ I’ve received your funds. Please hold on while I process your payment.\nThank you for your patience!")
        elif cmd == ".block":
            entity = await client.get_entity(event.chat_id)
            await client(functions.contacts.BlockRequest(id=entity.id))
            await event.reply("⛔ User Blocked.")
        elif cmd == ".unblock":
            entity = await client.get_entity(event.chat_id)
            await client(functions.contacts.UnblockRequest(id=entity.id))
            await event.reply("✅ User Unblocked.")
        elif cmd == ".lock":
            await client.edit_permissions(event.chat_id, send_messages=False)
            await event.reply("🔒 Group Locked.")
        elif cmd == ".clear":
            await client.delete_dialog(event.chat_id)
            await event.respond("🧹 Chat Cleared.")
        elif cmd == ".close":
            await event.reply("☠️ Leaving & deleting group...")
            await asyncio.sleep(2)
            await client.delete_dialog(event.chat_id)
        elif cmd == ".mm":
            me = await client.get_me()
            group_title = f"Cesive MM - {random.randint(1000, 9999)}"
            await client(functions.messages.CreateChatRequest(
                users=[me],
                title=group_title
            ))
            await event.reply(f"✅ MM Group Created: {group_title}")
        elif cmd == ".id":
            reply = await event.get_reply_message()
            target = reply.sender_id if reply else event.chat_id
            await event.reply(f"🆔 ID: {target}")
        elif cmd == ".userinfo":
            reply = await event.get_reply_message()
            user = await client.get_entity(reply.sender_id if reply else event.chat_id)
            msg = f"👤 **User Info:**\n"
            msg += f"• Name: {user.first_name or ''} {user.last_name or ''}\n"
            msg += f"• Username: @{user.username}\n" if user.username else ""
            msg += f"• ID: {user.id}\n"
            msg += f"• Bio: {getattr(user, 'bot_info_description', 'Not available')}"
            await event.reply(msg)

    except Exception as e:
        await event.reply(f"⚠️ Error: {e}")

    await asyncio.sleep(2)
    await event.delete()


async def main():
    print("🔐 Logging in...")
    await client.start()
    print("✅ Selfbot is running 24/7.")
    await client.run_until_disconnected()


client.loop.run_until_complete(main())
