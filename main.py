import discord
import sqlite3
import random
import asyncio
import requests
from imdb import IMDb
from datetime import datetime, timedelta
from keep_alive import keep_alive
from discord.ext import commands



intents = discord.Intents.default()
intents.members = True
intents.message_content = True
intents.typing = True
intents.presences = True

bad_words = [
    "fuck",
    "shit",
    "asshole",
    "bitch",
    "crap",
    "slut",
    "whore",
    "dick",
    "cock",
    "cunt",
    "bastard",
    "nigger",
    "faggot"]



client = commands.Bot(command_prefix="%", intents=intents)


conn = sqlite3.connect("welcome_channels.db")
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS welcome_channels
            (server_id TEXT PRIMARY KEY, channel_id TEXT)''')
conn.commit()


c.execute('''CREATE TABLE IF NOT EXISTS user_affection
            (user_id TEXT PRIMARY KEY, affection_level INTEGER, last_interaction )''')
conn.commit()


welcome_channel_id = None  # Initialize it globally

last_message_timestamps = {}

  
async def send_random_message(channel):
    random_messages = [
        "Where is everyone?",
        "I'm feeling lonely...",
        "Anybody here?",
        "It's so quiet...",
        "Did everyone take a break?",
        "I wont kill anyone again.. pls comeback"
    ]
    await channel.send(random.choice(random_messages))

async def check_inactivity(server_id, channel):
    while True:
        await asyncio.sleep(28800)  # Check every 10 minutes
        
        last_message_time = last_message_timestamps.get(server_id, None)
        current_time = datetime.utcnow()

        if last_message_time and (current_time - last_message_time).total_seconds() >= 28800:
            await send_random_message(channel)
            last_message_timestamps[server_id] = current_time

@client.event
async def on_ready():
    print(f"Logged in as {client.user.name}")
    
    for guild in client.guilds:
        server_id = str(guild.id)
        print(f"Checking server ID: {server_id}")

        c.execute("SELECT channel_id FROM welcome_channels WHERE server_id = ?", (server_id,))
        result = c.fetchone()

        if result:
            channel_id = int(result[0])
            print(f"Found channel ID: {channel_id}")
            server = client.get_guild(int(server_id))
            channel = server.get_channel(channel_id)

            if channel:
                last_message_timestamps[server_id] = datetime.utcnow()
                asyncio.create_task(check_inactivity(server_id, channel))
            else:
                print("Channel not found.")
        else:
            print(f"Channel not set for server ID: {server_id}")


@client.event
async def on_member_join(member):
    server_id = str(member.guild.id)
    
    c.execute("SELECT channel_id FROM welcome_channels WHERE server_id = ?", (server_id,))
    result = c.fetchone()
    
    if result:
        welcome_channel_id = result[0]
        channel = client.get_channel(int(welcome_channel_id))
        if channel:
            await channel.send(f'Hiiiiii, {member.mention}!')


@client.command()
async def gn(ctx):
  author = ctx.author
  await ctx.send(f"Good Niiight <3 {author.mention}")


@client.command()
@commands.has_permissions(administrator=True)
async def set_welcome_channel(ctx, channel_id):
    await ctx.message.delete()
    server_id = str(ctx.guild.id)
    try:
        channel_id = int(channel_id)
        channel = client.get_channel(channel_id)
        if channel:
            c.execute("INSERT OR REPLACE INTO welcome_channels (server_id, channel_id) VALUES (?, ?)",
                      (server_id, channel_id))
            conn.commit()
            global welcome_channel_id
            welcome_channel_id = channel_id
            await ctx.send(f'Welcome channel set to {channel.mention}')
        else:
            await ctx.send("Channel not found.")
    except ValueError:
        await ctx.send("Invalid channel ID.")



responses = [
    "Don't use bad words, it's not good.",
    "Pretty please, dont be bad person.",
    "Those words makes you evil, so dont say it.",
    "You Under Arrest mister."]

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    content = message.content.lower()

    if contains_bad_words(content):
        response = random.choice(responses)
        await message.channel.send(response)

    update_affection(message.author.id, 1)
  
    await client.process_commands(message)


def contains_bad_words(message):
    return any(bad_word in message for bad_word in bad_words)


uplifting_advices = [
    "You are stronger than you think.",
    "Don't be too hard on yourself. Mistakes happen.",
    "Take a deep breath and remind yourself that you're doing your best.",
    "It's okay to ask for help when you need it.",
    "Focus on the things that bring you joy.",
    "Challenges help you grow. Embrace them.",
    "You have the power to change your perspective.",
    "Believe in yourself, even when things get tough.",
    "Surround yourself with positive people who uplift you.",
    "Every day is a new opportunity to start afresh.",
    "You matter, and your feelings are valid.",
    "Treat yourself with kindness and self-care.",
    "You are not alone in how you feel. Reach out to someone you trust.",
    "Keep moving forward. Progress is progress, no matter how small.",
    "Life's setbacks are temporary. Better days are ahead.",
    "You are worthy of happiness and love.",
    "Take one step at a time. You've got this!",
    "Find joy in the little things that make you smile.",
    "Stay true to yourself and your dreams.",
    "You are resilient. You've overcome challenges before and you can do it again.",
    "It's okay to rest and take care of yourself.",
    "Celebrate your achievements, no matter how small.",
    "You are a work in progress, and that's perfectly okay.",
    "Don't compare yourself to others. Your journey is unique.",
    "Take a moment to appreciate how far you've come.",
    "Remember that setbacks are just stepping stones to success.",
    "Your feelings are valid. Allow yourself to acknowledge and process them.",
    "Surround yourself with positive affirmations and reminders.",
    "Be kind to yourself, like you would to a friend.",
    "Visualize your goals and take steps toward them.",
    "Embrace self-compassion and forgive yourself for past mistakes.",
    "You are enough, exactly as you are.",
    "Focus on what you can control and let go of what you can't.",
    "Practice gratitude for the good things in your life.",
    "Remember that setbacks are temporary and challenges can be overcome.",
    "Take breaks and prioritize self-care to recharge your energy.",
    "Face challenges with a growth mindset and an open heart.",
    "Keep moving forward, even if progress seems slow.",
    "Believe in the power of your dreams and aspirations.",
    "Allow yourself to feel and express your emotions.",
    "You are deserving of happiness and inner peace.",
    "Stay patient with yourself. Healing takes time."]

@client.command()
async def moti(ctx):
    advice = random.choice(uplifting_advices)
    await ctx.send(advice)
    await ctx.message.delete()

@client.command()
async def hi(ctx):
    await ctx.send("Hiiiii, me work. ME WORK")

@client.command()
async def cute(ctx):
    cooldown_duration = timedelta(hours=8)
    user_id = ctx.author.id
    last_interaction = get_last_interaction(user_id)
    current_time = datetime.utcnow()

    if last_interaction is None or (current_time - last_interaction) >= cooldown_duration:
        affection_gain = random.randint(5, 15)
        user_affection = get_user_affection(user_id)
        new_affection = user_affection + affection_gain

        if last_interaction is None:
            initialize_new_user(user_id, new_affection, current_time)
        else:
            update_affection(user_id, new_affection)

        set_last_interaction(user_id)
        await ctx.send(f"{ctx.author.mention}, you've received {affection_gain} affection points for being adorable! Keep spreading the cuteness! ❤️")
    else:
        cooldown_left = cooldown_duration - (current_time - last_interaction)
        cooldown_left_formatted = cooldown_left - timedelta(microseconds=cooldown_left.microseconds)
        cooldown_left_str = str(cooldown_left_formatted).split(".")[0]
        await ctx.send(f"{ctx.author.mention}, you're feeling too cute to be that affectionate! Please wait {cooldown_left_str} before sending more cuteness")

# Function to update user's affection points
def update_affection(user_id, change):
    c.execute("UPDATE user_affection SET affection_level = COALESCE(affection_level, 0) + ? WHERE user_id = ?",
              (change, user_id))
    conn.commit()

def initialize_new_user(user_id, initial_affection, current_time):
    c.execute("INSERT INTO user_affection (user_id, affection_level, last_interaction) VALUES (?, ?, ?)",
              (user_id, initial_affection, current_time))
    conn.commit()
  
# Function to get user's current affection points
def get_user_affection(user_id):
    c.execute("SELECT affection_level FROM user_affection WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    if result:
        return result[0]
    else:
        return 0

# Function to set user's last interaction timestamp
def set_last_interaction(user_id):
    c.execute("UPDATE user_affection SET last_interaction = CURRENT_TIMESTAMP WHERE user_id = ?",
              (user_id,))
    conn.commit()

# Function to get user's last interaction timestamp
def get_last_interaction(user_id):
    c.execute("SELECT last_interaction FROM user_affection WHERE user_id = ?", (user_id,))
    result = c.fetchone()
    if result and result[0]:
        return datetime.strptime(result[0], '%Y-%m-%d %H:%M:%S')
    else:
        return None

# Command to display affection leaderboard
@client.command()
async def alb(ctx):
    c.execute("SELECT user_id, affection_level FROM user_affection ORDER BY affection_level DESC LIMIT 10")
    top_users = c.fetchall()

    leaderboard_message = "Affection Leaderboard:\n"
    for rank, (user_id, affection_level) in enumerate(top_users, start=1):
        user = ctx.guild.get_member(int(user_id))
        leaderboard_message += f"{rank}. {user.display_name if user else 'Unknown User'} - {affection_level} ❤️\n"

    await ctx.send(leaderboard_message)

@client.command()
async def alv(ctx):
    user_id = str(ctx.author.id)
    user_affection = get_user_affection(user_id)
    await ctx.send(f"{ctx.author.mention}, you have {user_affection} affection points ❤️")




@client.command()
async def kill(ctx, user: discord.Member=None):
    # List of GIF URLs
    gif_urls = [
        'https://media.giphy.com/media/0NMF33GNxcfXIj2ctW/giphy.gif',
        'https://media.giphy.com/media/QW9KH3VC6MMJb9iy1y/giphy.gif',
        'https://giphy.com/clips/southpark-season-1-south-park-episode-13-6jTD6KqVNADI746GOC',
        'https://media.giphy.com/media/q4d88C99gfvyOXD9B9/giphy.gif']
    random_gif = random.choice(gif_urls)

    owner_id = 1089138455956693042
  
    if user and not user.bot:  # Check if user exists and is not a bot
        await ctx.send(f'Hey {user.mention}, DIEEEEEEEEE')
        await ctx.send(random_gif)
    elif not user:
        await ctx.send("DIEEEEEEEEEEEEE!")
        await ctx.send(random_gif)
    elif user and user.id == client.user.id:
        await ctx.send(f"DAAAAAD, pls Help meeeee")
        await ctx.send("https://media.giphy.com/media/ukfn7kMzzLqLeyi5Tt/giphy.gif")
    else:
        await ctx.send("Dont try to kill fellow bots")


@client.command()
async def uinfo(ctx, user: discord.Member=None):
    if user is None:
        user = ctx.author
    
    embed = discord.Embed(title="User Information", color=user.color)
    embed.set_thumbnail(url=user.avatar.url if user.avatar else user.default_avatar.url)
    embed.add_field(name="Username", value=user.name, inline=True)
    embed.add_field(name="Discriminator", value=user.discriminator, inline=True)
    embed.add_field(name="ID", value=user.id, inline=False)
    embed.add_field(name="Created At", value=user.created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
    embed.add_field(name="Joined Server At", value=user.joined_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
    embed.add_field(name="Top Role", value=user.top_role.name, inline=False)

    await ctx.send("**Searching the secret Files**")
    await ctx.send(embed=embed)


ia = IMDb()


@client.command()
async def mv(ctx, *, query):

    author = ctx.author.mention

    search_results = ia.search_movie(query)
    if not search_results:
        await ctx.send("Me find no result.")
        return

    first_result = search_results[0]
    movie = ia.get_movie(first_result.getID())

    title = movie.get('title', 'N/A')
    year = movie.get('year', 'N/A')
    rating = movie.get('rating', 'N/A')
    plot = movie.get('plot outline', 'N/A')
    poster_url = movie.get('cover url', None)
    imdb_url = f"https://www.imdb.com/title/{movie.getID()}/"

    cute_messages = [
        f"Aww, {author}, you have a soft spot for {title}! How adorable! 🌼",
        f"Hey there, {author}! {title} is a wonderful choice, don't you think? 💖",
        f"{author}, you've got great taste! {title} is absolutely lovely! 🌟",
        f"Oh my goodness, {title}? You've found a gem, {author}! 🌸",
        f"{author}, {title} is as sweet as can be! Such a heartwarming choice! 🌈",
        f"Guess what, {author}? {title} is a total crowd-pleaser! Great pick! 🌺",
        f"Ah, {author}, {title} is like a warm hug for the soul! Lovely choice! 🍀"]

    embed = discord.Embed(title=title, description=plot, color=discord.Color.blue())
    embed.add_field(name="Year", value=year, inline=True)
    embed.add_field(name="Rating", value=rating, inline=True)

    if poster_url:
        embed.set_thumbnail(url=poster_url)

    embed.add_field(name="IMDb Link", value=f"[IMDb Page]({imdb_url})", inline=False)

    await ctx.send(embed=embed)
    cute_message = random.choice(cute_messages).format(title=title, author=ctx.author.mention)
    await ctx.send(cute_message)

keep_alive()

client.run("BOT TOKEN")
