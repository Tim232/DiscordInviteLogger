import discord
from discord.ext import commands
import hPickle as pic

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix='l!', intents=intents)

# db = {
#     34209482323423 : {
#         "channel" : 4238092384234234,
#         "invites" : {
#             # code : uses
#         }
#     }
# }

db = pic.load("db.pickle")


async def fetch(member: discord.Member):
    await bot.wait_until_ready()

    db = pic.load("db.pickle")
    
    if member.guild.id not in db:
        return
    
    channel = member.guild.get_channel(db[member.guild.id]["channel"])
    
    if not channel:
        return
    
    afterInvites = await member.guild.invites()
    
    for afterInvite in afterInvites:
        if afterInvite.code in db[member.guild.id]["invites"]:
            if afterInvite.uses == db[member.guild.id]["invites"][afterInvite.code]:
                continue
            # log
            pass
        else:
            # log
            pass
        
        db[member.guild.id]["invites"][afterInvite.code] = afterInvite.uses
        
        eme = discord.Embed(title=f"{member} just joined the server", color=0x03d692, description=f"Inviter: {afterInvite.inviter.mention} (`{str(afterInvite.inviter)}` | `{afterInvite.inviter.id}`)\nCode: `{afterInvite.code}`\nUses: `{afterInvite.inviter.uses}`")
        eme.set_author(name=str(member), icon_url=member.avatar_url)
        eme.set_footer(text=f"ID: {member.id}")
        eme.timestamp = member.joined_at
        await channel.send(embed=eme)
        
    pic.save("db.pickle", db)


@bot.event
async def on_ready():
    print("ready!")


@bot.event
async def on_member_join(member):
    await fetch(member)
    
@bot.command()
@commands.guild_only()
@commands.has_permissions(administrator=True)
async def register(ctx, channel: discord.TextChannel = None):
    if not channel:
        channel = ctx.channel
        
    try:
        await channel.send("This channel is registered as my invite log channel!")
    except:
        try:
            await ctx.send(f"I don't have the permission to send messages at {channel.mention}!")
        except:
            await ctx.author.send(f"I don't have the permission to send messages at {channel.mention}!")
        return
    
    db = pic.load("db.pickle")
    
    db[ctx.guild.id]["channel"] = channel.id
    
    pic.save("db.pickle", db)
    
    await channel.send(f"{channel.mention} is registered as my invite log channel!")
    

bot.run("token")
