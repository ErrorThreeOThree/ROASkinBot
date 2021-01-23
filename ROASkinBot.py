#!/bin/python
import os, sys
import discord
from discord.ext import commands
import random
from roaskins import *
import cv2
import numpy as np

prefix = "!skin "

with open('token.secret', 'r') as tokenfile:
    TOKEN = tokenfile.read()

bot = commands.Bot(command_prefix=prefix)

def find_rival(string : str):
    lower = string.lower()
    for rival in rivals().values():
        if lower == rival.name.lower() or lower in [x.lower() for x in rival.aliases]:
            return rival
    return None

def do_command_rival_multiple_skins(rival: Rival, i: int):
    padding = 5
    skin_num = min(4, max(1, int(i)))
    answer = ""
    image = None
    skins = []
    for i in range(skin_num):
        skins.append(rival.create_random_skin())
    #stitch 'em up
    rows,cols,dims = skins[0].get_preview().shape
    skin_rows = rows
    skin_cols = cols
    if skin_num > 1:
        cols = cols * 2 + padding
    if skin_num > 2:
        rows = rows * 2 + padding
    skin = np.zeros((rows, cols, dims))
    skin[0:skin_rows, 0:skin_cols, 0:dims] = skins[0].get_preview()
    if skin_num >= 2:
        skin[0:skin_rows, skin_cols + padding:skin_cols * 2 + padding, 0:dims] = skins[1].get_preview()
    if skin_num >= 3:
        skin[skin_rows + padding:skin_rows * 2 + padding, 0:skin_cols, 0:dims] = skins[2].get_preview()
    if skin_num >= 4:
        skin[skin_rows + padding:skin_rows * 2 + padding, skin_cols + padding:skin_cols * 2 + padding, 0:dims] = skins[3].get_preview()
    path = "skins/" + rival.name.lower() + "/" + "-".join(map(str, skins)) + ".png"
    cv2.imwrite(path, skin)
    answer = rival.name + "\n`" + "`\n`".join(map(str, skins)) + "`"
    return answer, discord.File(path)


def do_command_rival(rival : Rival, args : list):
    answer = ""
    image = None
    skin = None
    if (len(args) > 0):
        # check if multiple random skins:
        return do_command_rival_multiple_skins(rival, int(args[0]))
    if skin is None:
        skin = rival.create_random_skin()
    
    path = "skins/" + rival.name.lower() + "/" + str(skin) + ".png"
    skin.save_preview(path)
    image = discord.File(path)
    answer += "{}\n`{}`".format(rival.name, skin)
    return (answer, image)

def is_command_random(command : str):
    cmds_random = ["random", "rand"]
    cmd_lower = command.lower()
    return cmd_lower in cmds_random



@bot.event
async def on_message(message):
    # force command part to be lower letters
    # hack to allow capitalized commands
    split_message = message.content.split(" ")

    # 2 because prefix is "!skin "
    if len(split_message) >= 2:
        split_message[1] = split_message[1].lower()
    
    message.content = " ".join(split_message)

    if (message.content == "!skin"):
        message.content = "!skin random"
    await bot.process_commands(message)

for rival in rivals().values():
    @bot.command(rival.name.lower(), aliases=[x.lower() for x in rival.aliases],\
        description="Name:        {}\n".format(rival.name)
                  + "Aliases:     {}\n".format(", ".join(rival.aliases))
                  + "Description: Generate random {} skin\n".format(rival.name)
                  + "Arguments:   [Number of skins (1-4)]\n".format(" ".join(prefix), rival.name),)
    async def function(ctx, *args):
        # first word is !skin
        rival_name = ctx.command.name
        answer,image = do_command_rival(find_rival(rival_name), args)
        if image is None:
            await ctx.send(answer)
        else:
            await ctx.send(answer, file=image)

@bot.command("1", aliases=["2", "3", "4"],\
        description="Name:        {}\n".format("1")
                  + "Aliases:     {}\n".format(", ".join(["2", "3", "4"]))
                  + "Description: Generate a number of random skins\n".format("random")
                  + "Arguments:   [Number of skins (1-4)]\n".format(" ".join(prefix), "random"))
async def do_command_numer(ctx, *args):
    answer,image = do_command_rival(random.choice(list(rivals().values())), ctx.message.content.split(" ")[1])
    if image is None:
       await ctx.send(answer)
    else:
        await ctx.send(answer, file=image)

@bot.command("random", aliases=["rand"],\
        description="Name:        {}\n".format("random")
                  + "Aliases:     {}\n".format(", ".join(["rand"]))
                  + "Description: Generate random skin\n".format("random")
                  + "Arguments:   [Number of skins (1-4)]\n".format(" ".join(prefix), "random"))
async def do_command_random(ctx, *args):
    answer,image = do_command_rival(random.choice(list(rivals().values())), args)
    if image is None:
       await ctx.send(answer)
    else:
        await ctx.send(answer, file=image)

@bot.command("present",\
        description="Name:        {}\n".format("present")
                  + "Aliases:     {}\n".format(", ".join([]))
                  + "Description: Present a skin to others. You may give it a name and credit the author!\n"
                  + "Example:     !skin present kragg 9FD7-7F3C-C52E-F898-11BD-6A87-0201 lime by Zerfallskonstante\n"
                  + "Arguments:   [rival] [color code] [Name of the skin]\n\n".format(" ".join(prefix), "random")
                  + "Example:\n!skin present kragg 9FD7-7F3C-C52E-F898-11BD-6A87-0201 lime by Zerfallskonstante\n")
async def do_command_present(ctx, *args):
    answer = ""
    image = None
    if (len(args) < 2):
        answer += "Wrong usage! Specify rival and color code!\n"
    else:
        rival = find_rival(args[0])
        if rival is None:
            answer += "Rival does not exist!\n"
        else:
            skin = rival.create_skin_from_code(args[1])
            if skin is None:
                answer += "Invalid color code `{}` for {}!".format(args[1], rival.name)
            else:
                # TODO: Error on skin present, tuple does not have 'r'
                author = ctx.author.mention
                skin_name = rival.name
                # check for custom name
                if len(args) >= 3:
                    if args[-2] == "by":
                        author = args[-1]
                        skin_name = " ".join(args[2:-2]) + " " + rival.name
                    else:
                        skin_name = " ".join(args[2:]) + " " + rival.name
                path = "skins/" + rival.name.lower() + "/" + str(skin) + ".png"
                skin.save_preview(path)
                image = discord.File(path)
                answer += "**{}** by *{}*\n`{}`".format(skin_name, author, skin)
    

    await ctx.send(answer, file=image)

    

bot.run(TOKEN)