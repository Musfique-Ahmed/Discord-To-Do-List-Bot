import discord
from discord import app_commands
from discord.ext import commands
import json
import os

DATA_FILE = "todo_data.json"

# -------------------- DATA LOADING --------------------

def load_data():
    if not os.path.exists(DATA_FILE):
        return {}
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

data = load_data()

# -------------------- DISCORD BOT --------------------

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Create per-server todo list structure
def ensure_server(guild_id):
    guild_id = str(guild_id)
    if guild_id not in data:
        data[guild_id] = {
            "current_list": "default",
            "lists": {"default": []}
        }
        save_data(data)
    return data[guild_id]


@bot.event
async def on_ready():
    print(f"Bot logged in as {bot.user}")
    await bot.tree.sync()
    print("Commands synced.")

# -------------------- COMMANDS --------------------

# /todo add
@bot.tree.command(name="todo_add", description="Add a task to the current list.")
async def todo_add(interaction: discord.Interaction, task: str):
    server = ensure_server(interaction.guild_id)
    lst = server["current_list"]
    server["lists"][lst].append({"task": task, "done": False})
    save_data(data)

    await interaction.response.send_message(f"✅ Added task: **{task}** to list **{lst}**")


# /todo add_bulk
@bot.tree.command(name="todo_add_bulk", description="Add multiple tasks separated by semicolons.")
async def todo_add_bulk(interaction: discord.Interaction, tasks: str):
    server = ensure_server(interaction.guild_id)
    lst = server["current_list"]

    task_list = [t.strip() for t in tasks.split(";") if t.strip()]

    for t in task_list:
        server["lists"][lst].append({"task": t, "done": False})

    save_data(data)

    await interaction.response.send_message(
        f"✅ Added **{len(task_list)}** tasks to list **{lst}**"
    )


# /todo list
@bot.tree.command(name="todo_list", description="Show the current todo list.")
async def todo_list(interaction: discord.Interaction):
    server = ensure_server(interaction.guild_id)
    lst = server["current_list"]
    items = server["lists"][lst]

    if not items:
        await interaction.response.send_message(f"📭 **List '{lst}' is empty.**")
        return

    msg = f"📋 **TODO LIST: {lst}**\n\n"
    for i, item in enumerate(items, start=1):
        status = "✔️" if item["done"] else "❌"
        msg += f"{i}. {status} {item['task']}\n"

    await interaction.response.send_message(msg)


# /todo check
@bot.tree.command(name="todo_check", description="Mark a task as done.")
async def todo_check(interaction: discord.Interaction, index: int):
    server = ensure_server(interaction.guild_id)
    lst = server["current_list"]

    items = server["lists"][lst]
    if 1 <= index <= len(items):
        items[index - 1]["done"] = True
        save_data(data)
        await interaction.response.send_message(f"✔️ Marked task **#{index}** as complete.")
    else:
        await interaction.response.send_message("❌ Invalid task number.")


# /todo uncheck
@bot.tree.command(name="todo_uncheck", description="Mark a task as not done.")
async def todo_uncheck(interaction: discord.Interaction, index: int):
    server = ensure_server(interaction.guild_id)
    lst = server["current_list"]

    items = server["lists"][lst]
    if 1 <= index <= len(items):
        items[index - 1]["done"] = False
        save_data(data)
        await interaction.response.send_message(f"❌ Unchecked task **#{index}**.")
    else:
        await interaction.response.send_message("❌ Invalid task number.")


# /todo clear
@bot.tree.command(name="todo_clear", description="Clear the current list.")
async def todo_clear(interaction: discord.Interaction):
    server = ensure_server(interaction.guild_id)
    lst = server["current_list"]

    server["lists"][lst] = []
    save_data(data)

    await interaction.response.send_message(f"🗑 Cleared list **{lst}**")


# /todo list_create
@bot.tree.command(name="todo_list_create", description="Create a new todo list.")
async def todo_list_create(interaction: discord.Interaction, list_name: str):
    server = ensure_server(interaction.guild_id)

    if list_name in server["lists"]:
        await interaction.response.send_message("⚠️ List already exists.")
        return

    server["lists"][list_name] = []
    save_data(data)

    await interaction.response.send_message(f"📁 Created new list: **{list_name}**")


# /todo list_switch
@bot.tree.command(name="todo_list_switch", description="Switch to a different list.")
async def todo_list_switch(interaction: discord.Interaction, list_name: str):
    server = ensure_server(interaction.guild_id)

    if list_name not in server["lists"]:
        await interaction.response.send_message("❌ List does not exist.")
        return

    server["current_list"] = list_name
    save_data(data)

    await interaction.response.send_message(f"🔄 Switched to list: **{list_name}**")


bot.run("YOUR_BOT_TOKEN")
