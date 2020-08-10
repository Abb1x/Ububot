import discord
from discord.ext import commands
import random
from googletrans import Translator
import wikipedia
import urbandictionary as ud
import requests #used to send get request
import json
import psycopg2
import os
from decouple import config
#api key for weather
api_key = config("WEATHER_KEY")
base_url = "http://api.openweathermap.org/data/2.5/weather?"
#Cog for misc commands
class MiscCog(commands.Cog):
    def __init__(self, client):
        self.client = client
    @commands.command()
    async def github(self, ctx):
        await ctx.send("https://github.com/Abb1x/Tux")
    @commands.command()
    async def echo(self, ctx, *, arg):
        await ctx.send(f"{arg}")

    @commands.command()
    async def ping(self,ctx):
        await ctx.send(f':ping_pong: Pong **{round(self.client.latency * 1000)}ms**')

    @commands.command()
    async def skin(self,ctx,arg):
        embed=discord.Embed(title=f"{arg}'s minecraft skin")
        embed.set_image(url=f"https://mc-heads.net/avatar/{arg}/500/")
        await ctx.send(embed=embed)

    @commands.command(aliases=["8ball","ball"])
    async def _8ball(self,ctx,arg):
        responses = ["It is certain.",

                    "It is decidedly so.",

                    "Without a doubt.",

                    "Yes - definitely.",

                    "You may rely on it.",

                    "As I see it, yes.",

                    "Most likely.",

                    "Outlook good.",

                    "Yes.",

                    "Signs point to yes.",

                    "Reply hazy, try again.",

                    "Ask again later.",

                    "Better not tell you now.",

                    "Cannot predict now.",

                    "Concentrate and ask again.",

                    "Don't count on it.",

                    "My reply is no.",

                    "My sources say no.",

                    "Outlook not so good.",

                    "Very doubtful."
    ]

        await ctx.send(random.choice(responses))

    @commands.command()
    async def avatar(self,ctx,member: discord.Member):
        embed=discord.Embed(title=f"{member.name}'s avatar")
        embed.set_image(url=f"{member.avatar_url}")
        await ctx.send(embed=embed)

    @commands.command()
    async def trans(self,ctx,arg,arg2):
        translator = Translator()
        translation = translator.translate(f'{arg}',dest=f"{arg2}")
        embed=discord.Embed(title="Translator", color=0x4f8bed)
        embed.add_field(name="Original Word:", value=f"`{translation.origin}`", inline=False)
        embed.add_field(name="Translated Word:", value=f"`{translation.text}`", inline=True)
        await ctx.send(embed=embed)
    @commands.command(aliases=['wikipedia','pedia'])
    async def wiki(self,ctx,*,arg):

        search = wikipedia.search(f"{arg}")
        result = search[0]
        id = result.replace('4', '')
        page = wikipedia.page(f"{id}")
        wiki = wikipedia.summary(f"{id}",sentences=1)
        images = page.images
        rand = random.randint(1,20)
        embed=discord.Embed(title="Wikipedia", colour=0xf4eded)
        embed.add_field(name="Search", value=f"`{arg}`", inline=False)
        embed.add_field(name="Result", value=f"`{wiki}`", inline=True)
        embed.set_thumbnail(url=f"{images[rand]}")
        if "svg" in images[rand]:
                embed.set_thumbnail(url=f"{images[random.randint(1,20)]}")
        if "webm" in images[rand]:
                embed.set_thumbnail(url=f"{images[random.randint(1,20)]}")
        if "webp" in images[rand]:
                embed.set_thumbnail(url=f"{images[random.randint(1,20)]}")
        await ctx.send(embed=embed)
    @commands.command()
    async def weather(self,ctx,*,arg):
        complete_url = base_url + "appid=" + api_key + "&q=" + arg
        response = requests.get(complete_url)
        x = response.json()
        if x["cod"] != "404":
            y = x["main"]
            z = x["sys"]
            current_temperature = y["temp"]

            w = x["weather"]

            basic = w[0]

            sky = basic["description"]

            country = z["country"]

            current_pressure = y["pressure"]

            current_humidiy = y["humidity"]

            z = x["weather"]

            lower_country = country.lower()
            weather_description = z[0]["description"]
            celsius = round(current_temperature-273.15,3)
            embed=discord.Embed(title="Weather",color=discord.Colour.from_rgb(255, 255, 8))
            embed.add_field(name=f":cityscape: City: {arg}", value="\u200b", inline=False)
            embed.add_field(name=f":flag_{lower_country}: Country: {country}", value="\u200b", inline=True)
            embed.add_field(name=f":thermometer: Temperature: {celsius} °C", value="\u200b", inline=False)
            embed.add_field(name=f":droplet: Humidity: {current_humidiy}%", value="\u200b", inline=True)
            embed.add_field(name=f":white_sun_cloud: Sky: {sky}", value="\u200b", inline=False)

            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=f":x: │ **City not found**",colour=discord.Colour.red())
            await ctx.send(embed=embed)
    @commands.command()
    async def urban(self,ctx,*,arg):
        defs = ud.define(f'{arg}')
        d = defs[0]
        def_final = d.definition.translate({ord(i): None for i in '[]'})
        embed=discord.Embed(color=0xdf3908)
        embed.set_author(name="Urban Dictionary",icon_url="https://i.pinimg.com/originals/37/46/41/374641157f9fa2ae904664d6c89b984b.jpg")
        embed.add_field(name="Search", value=f"`{arg}`", inline=False)
        embed.set_thumbnail(url="https://i.pinimg.com/originals/37/46/41/374641157f9fa2ae904664d6c89b984b.jpg")
        embed.add_field(name="Result", value=f"`{def_final}`", inline=True)
        await ctx.send(embed=embed)
    @commands.command()
    async def joke(self,ctx):
        data = requests.get("https://official-joke-api.appspot.com/random_joke")
        rand_joke = data.json()
        str = rand_joke
        embed=discord.Embed(title="Random joke",color=random.randint(0,0xffffff))
        embed.add_field(name=f"Category: {str['type']}", value="\u200b", inline=False)
        embed.add_field(name=f"Joke: {str['setup']}", value=f"{str['punchline']}", inline=True)
        await ctx.send(embed=embed)
    @commands.command()
    async def choose(self,ctx,*,choices):
        choices = choices.split(" ")
        choice = random.choice(choices).strip()
        embed=discord.Embed(title="Choose command", color=random.randint(0, 0xffffff))
        embed.add_field(name="Choices:", value=f"`{choices}`", inline=False)
        embed.add_field(name="Choice:", value=f"`{choice}`", inline=True)
        await ctx.send(embed=embed)
    @commands.command()
    async def twans(self,ctx,*,arg):
        def replaceMultiple(mainString, toBeReplaces, newString):
            for elem in toBeReplaces :
                if elem in mainString :
                    # Replace the string
                    mainString = mainString.replace(elem, newString)

            return mainString
        trans = replaceMultiple(arg, ['l', 'r'] , "w")
        await ctx.send(trans)
    @commands.command()
    async def ngskin(self,ctx,arg):
            embed=discord.Embed(title=f"{arg}'s nationsglory skin")
            embed.set_image(url=f"https://skins.nationsglory.fr/face/{arg}/64")
            await ctx.send(embed=embed)
    @commands.command()
    async def info(self,ctx):
        embed=discord.Embed(colour=discord.Colour.blue())
        embed.set_author(name="Tux v0.5",icon_url="https://images-ext-1.discordapp.net/external/o0qmGA7HWp5CLR0_qdh4ISSemzj4JIQivBJxVbFChwM/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/725734772479098880/b266fa6609aab9d47d65a6f9687f09ba.webp?width=549&height=549")
        embed.add_field(name=f"Ping: {round(self.client.latency * 1000)}ms", value="\u200b", inline=False)
        embed.add_field(name=f"Library: Discord.py 1.3.4 ", value="\u200b", inline=False)
        embed.add_field(name=f"Servers: {len(self.client.guilds)} ", value="\u200b", inline=False)
        embed.add_field(name=f"Created by: <:abbix:738920766451482714> Abbix#4319", value="\u200b", inline=False)
        await ctx.send(embed=embed)
    @commands.command()
    async def testdb(self,ctx):
            conn = psycopg2.connect("postgres://lfhtzuomwrfrlb:c8a897770748d7802579b93b44004582399992cee9684793f84bab71676c9fba@ec2-35-173-94-156.compute-1.amazonaws.com:5432/d3232lt1k8u332")
            cur = conn.cursor()
            cur.execute("""CREATE TABLE  "AGENTS"
                (
            "AGENT_CODE" CHAR(6) NOT NULL PRIMARY KEY,
        	"AGENT_NAME" CHAR(40),
        	"WORKING_AREA" CHAR(35),
        	"COMMISSION" INT(10,2),
        	"PHONE_NO" CHAR(15),
        	"COUNTRY" VARCHAR2(25)
        	 );""")
            cur.execute("""INSERT INTO AGENTS VALUES ('A007', 'Ramasundar', 'Bangalore', '0.15', '077-25814763', '');""")
            conn.commit()
            cur.close()
            conn.close()
        #connect to the database
            await ctx.send("data sent!")

def setup(client):
    client.add_cog(MiscCog(client))