import os
import discord
from discord.ext import commands
from dotenv import load_dotenv
from wallet import create_account, fund_account, get_balance, send_sol


load_dotenv()
description = ''' A bot that allows you to create and manage a Solana wallet  '''
intents = discord.Intents.default()
bot = commands.Bot(command_prefix='/', description=description, intents=intents)


@bot.event
async def on_ready():
    print('Bot is online')
    print(bot.user.name)
    print(bot.user.id)
    print('------ \n')


@bot.command(description='Create a new solana account')
async def create(ctx):
    sender_username = ctx.message.author
    try:
        public_key = create_account(sender_username)
        if public_key is not None:
            message = "Solana Account created successfully.\n"
            message += "Your account public key is {}".format(public_key)
            await ctx.send(message)
        else:
            message = "Failed to create account.\n"
            await ctx.send(message)
    except Exception as e:
        print('error:',e)
        await ctx.send('Failed to create account')
        return


@bot.command(description='Fund your account')
async def fund(ctx):
    sender_username = ctx.message.author
    incoming_msg = ctx.message.content
    try:
        amount = float(incoming_msg.split(" ")[1])
        if amount <= 2 :
            message = "Requesting {} SOL to your Solana account, please wait !!!".format(amount)
            await ctx.send(message)
            transaction_id = fund_account(sender_username, amount)
            if transaction_id is not None:
                message = "You have successfully requested {} SOL for your Solana account \n".format(
                    amount)
                message += "The transaction id is {}".format(transaction_id)
                await ctx.send(message)
            else:
                message = "Failed to fund your Solana account"
                await ctx.send(message)
        else:
            message = "The maximum amount allowed is 2 SOL"
            await ctx.send(message)
    except Exception as e:
        print('error:',e)
        await ctx.send('Failed to fund account')
        return


@bot.command(description='Check account balance')
async def balance(ctx):
    sender_username = ctx.message.author
    try:
        data = get_balance(sender_username)
        if data is not None:
            public_key = data['publicKey']
            balance = data['balance']
            message = "Your Solana account {} balance is {} SOL".format(
                public_key, balance)
            await ctx.send(message)
        else:
            message = "Failed to retrieve balance"
            await ctx.send(message)
    except Exception as e:
        print('error:',e)
        await ctx.send('Failed to check account balance')
        return


@bot.command(description='Send SOL to another account')
async def send(ctx):
    sender_username = ctx.message.author
    incoming_msg = ctx.message.content
    try:
        split_msg = incoming_msg.split(" ")
        amount = float(split_msg[1])
        receiver = split_msg[2]
        message = "Sending {} SOL to {}, please wait !!!".format(
            amount, receiver)
        await ctx.send(message)
        transaction_id = send_sol(sender_username, amount, receiver)
        if transaction_id is not None:
            message = "You have successfully sent {} SOL to {} \n".format(
                amount, receiver)
            message += "The transaction id is {}".format(transaction_id)
            await ctx.send(message)
        else:
            message = "Failed to send SOL"
            await ctx.send(message)
    except Exception as e:
        print('error:',e)
        await ctx.send('Failed to send SOL')
        return


bot.run(os.environ['BOT_TOKEN'])
