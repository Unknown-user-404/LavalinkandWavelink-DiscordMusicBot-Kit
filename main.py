import discord
import os
import json
import sqlite3
from discord.ext import commands
from discord.ext.menus import MenuPages, ListPageSource

bot = commands.Bot(command_prefix="rr?", intents=discord.Intents.all())

current_path = os.getcwd()

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f'cogs.{filename[:-3]}')

os.chdir(current_path)

@bot.event
async def on_ready():
    db = sqlite3.connect('main.sqlite')
    cursor = db.cursor()
    cursor.execute('''
      CREATE TABLE IF NOT EXISTS main(
        user_id TEXT,
        song_list TEXT
      )
    ''')
    db.commit()
    cursor.close()
    db.close()
    db1 = sqlite3.connect('co.sqlite')
    cursor1 = db1.cursor()
    cursor1.execute('''
      CREATE TABLE IF NOT EXISTS co(
        user_id TEXT,
        song_url TEXT
      )
    ''')
    db1.commit()
    cursor1.close()
    db1.close()
    await bot.change_presence(activity=discord.Game(name="rr?help"))
    print("Bot ready!")

@bot.command()
@commands.is_owner()
async def reload(ctx, cog_name: str):
  if cog_name.lower() == "all":
    for filename in os.listdir('./cogs'):
      if filename.endswith('.py'):
        bot.reload_extension(f'cogs.{filename[:-3]}')
    await ctx.send("Sucessfuly reloaded all cogs")
  else:
    if os.path.exists(f'./cogs/{cog_name}.py'):
      if ".py" in cog_name:
        bot.reload_extension(f'cogs.{cog_name[:-3]}')
      else:
        bot.reload_extension(f'cogs.{cog_name}')
      await ctx.send(f"Sucessfuly reloaded {cog_name}")
    else:
      return await ctx.send(f"There is no cog called {cog_name}")

@bot.command(description="blacklist a member(Give limitation)")
@commands.has_permissions(manage_messages=True)
async def blacklist(ctx, member: discord.Member):
  if not member.id == ctx.author.id:
    with open("blacklist.json", 'r') as f:
      blacklist_data = json.load(f)
    if str(ctx.guild.id) in blacklist_data:
      if not str(member.id) in blacklist_data[str(ctx.guild.id)]:
        if not member.guild_permissions.manage_messages:
          blacklist_data[str(ctx.guild.id)][str(member.id)] = {}
          await ctx.send("Member blacklisted!")
        else:
          return await ctx.send("That member is a mod!")
      else:
        return await ctx.send("That member is already blacklisted!")
    else:
      if not member.guild_permissions.manage_messages:
        blacklist_data[str(ctx.guild.id)] = {}
        blacklist_data[str(ctx.guild.id)][str(member.id)] = {}
        await ctx.send("Member blacklisted!")
      else:
        return await ctx.send("That member is a mod!")
  else:
    return await ctx.send("You can't blacklist yourself!")
  with open('blacklist.json', 'w') as f:
    json.dump(blacklist_data, f)

@bot.command(description="Whitelist a member(unblacklist)")
@commands.has_permissions(manage_messages=True)
async def whitelist(ctx, member: discord.Member):
  if not member.id == ctx.author.id:
    with open("blacklist.json", 'r') as f:
      blacklist_data = json.load(f)
    if str(ctx.guild.id) in blacklist_data:
      if str(member.id) in blacklist_data[str(ctx.guild.id)]:
        del blacklist_data[str(ctx.guild.id)][str(member.id)]
        await ctx.send("Member whitelisted!")
      else:
        return await ctx.send("That member is not blacklisted!")
    else:
      return await ctx.send("No one is blacklisted in your server!")
  else:
    return await ctx.send("You can't whitelist yourself!")
  with open('blacklist.json', 'w') as f:
    json.dump(blacklist_data, f)

bot.run("YOUR_TOKEN_HERE")