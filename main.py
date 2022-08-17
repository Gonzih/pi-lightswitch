import discord
import os
from gpiozero import LED


class BotClient(discord.Client):

    def set_led(self, n):
        self.led = LED(n)

    def set_admin_id(self, admin_id):
        self.admin_id = admin_id

    async def on_ready(self):
        print(f"Logged on as {self.user}")

    async def on_message(self, message):
        print(f"Message from {message.author}: {message.content}")

        if message.author == self.user:
            return

        if str(message.author) != self.admin_id:
            return

        if message.content.startswith("!ping"):
            await message.channel.send("pong")

        if message.content.startswith("!switch"):
            state = ""

            if "on" in message.content:
                self.led.on()
                state = "on"
            if "off" in message.content:
                self.led.off()
                state = "off"

            await message.channel.send(f"Lights are {state}")


def start():
    client = BotClient()
    client.set_led(18)
    client.set_admin_id(os.environ['DISCORD_ADMIN'])
    client.run(os.environ['DISCORD_TOKEN'])


start()
