import discord
from redmail import gmail
import pandas as pd

discord_token = "MTA5NjIxNDY4OTI0NTA1NzA5Ng.GbaOfg.RNRmFcDAYmwf-x10XXJnvbZE5h3vbfiyTzrY8I"
gmail_user_name = "astracode7@gmail.com"
gmail_password = "crvbbmmtvwctlogp"

def send_alert(img_path):
    message = "Animal intruder found!!"
    
    # Send message in Discord channel
    client = discord.Client(intents=discord.Intents.default())

    # @client.event
    # async def on_ready():  #  Called when internal cache is loaded
    #     channel = client.get_channel(int("1096215456651690076")) #  Gets channel from internal cache
    #     with open(img_path, 'rb') as f:
    #         picture = discord.File(f)
    #         await channel.send(content=message,file=picture) #  Sends message to channel
    #     await client.close()

    # client.run(discord_token)  # Starts up the bot

    # Send an email
    gmail.user_name = gmail_user_name
    gmail.password = gmail_password

    gmail.send(
        subject="Intruder Alert",
        sender=gmail_user_name,
        receivers=["akhileshwar333@gmail.com", "rockingnaveen12@gmail.com"],
        html="""
            <h1>Unauthorized Person found!</h1>
            {{ myimg }}
        """,
        body_images={"myimg": img_path}
    )

