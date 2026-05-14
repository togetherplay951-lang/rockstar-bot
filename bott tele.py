from imapclient import IMAPClient
import pyzmail
import re
import requests
import time

EMAIL = "togetherplay951@gmail.com"
PASSWORD = "peib rskk kcyu dwsz"
BOT_TOKEN = "8952288898:AAHgxb6nVT7kZk-M526hgxE0sa4rzBNEeV0"
CHAT_ID = "8056034836"
last_code = ""

while True:
    try:
        server = IMAPClient('imap.gmail.com', ssl=True)
        server.login(EMAIL, PASSWORD)

        server.select_folder('INBOX')

        messages = server.search(
            ['FROM', 'noreply@rockstargames.com']
        )

        if messages:
            latest = messages[-1]

            raw_message = server.fetch(
                [latest],
                ['BODY[]']
            )

            message = pyzmail.PyzMessage.factory(
                raw_message[latest][b'BODY[]']
            )

            body = ""

            if message.text_part:
                body = message.text_part.get_payload().decode(
                    message.text_part.charset
                )

            elif message.html_part:
                body = message.html_part.get_payload().decode(
                    message.html_part.charset
                )

            code = re.search(r'\b\d{6}\b', body)

            if code:
                otp = code.group()

                if otp != last_code:
                    last_code = otp

                    requests.get(
                        f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage",
                        params={
                            "chat_id": CHAT_ID,
                            "text": f"Rockstar Code: {otp}"
                        }
                    )

                    print("Code sent:", otp)

        server.logout()

    except Exception as e:
        print(e)

    time.sleep(15)
