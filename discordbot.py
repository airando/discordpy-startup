from discord.ext import commands
import os
import traceback

bot = commands.Bot(command_prefix='k!')
token = os.environ['DISCORD_BOT_TOKEN']


@bot.event
async def on_command_error(ctx, error):
    await ctx.send(str(error))


@bot.command()
async def ping(ctx):
    await ctx.send('pong')


if __name__ == '__main__':
    bot.run(token)
