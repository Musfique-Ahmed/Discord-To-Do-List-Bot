import discord
from discord import app_commands
from discord.ext import commands
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

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

# Create command group for /todo
todo_group = app_commands.Group(name="todo", description="Manage your to-do lists")

# /todo add
@todo_group.command(name="add", description="Add a task to the current list.")
async def todo_add(interaction: discord.Interaction, task: str):
    server = ensure_server(interaction.guild_id)
    lst = server["current_list"]
    server["lists"][lst].append({"task": task, "done": False})
    save_data(data)

    await interaction.response.send_message(f"✅ Added task: **{task}** to list **{lst}**")


# /todo add-bulk
@todo_group.command(name="add-bulk", description="Add multiple tasks separated by semicolons.")
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
@todo_group.command(name="list", description="Show the current todo list.")
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
@todo_group.command(name="check", description="Mark a task as done.")
async def todo_check(interaction: discord.Interaction, task_number: int):
    server = ensure_server(interaction.guild_id)
    lst = server["current_list"]

    items = server["lists"][lst]
    if 1 <= task_number <= len(items):
        items[task_number - 1]["done"] = True
        save_data(data)
        await interaction.response.send_message(f"✔️ Marked task **#{task_number}** as complete.")
    else:
        await interaction.response.send_message("❌ Invalid task number.")


# /todo uncheck
@todo_group.command(name="uncheck", description="Mark a task as not done.")
async def todo_uncheck(interaction: discord.Interaction, task_number: int):
    server = ensure_server(interaction.guild_id)
    lst = server["current_list"]

    items = server["lists"][lst]
    if 1 <= task_number <= len(items):
        items[task_number - 1]["done"] = False
        save_data(data)
        await interaction.response.send_message(f"❌ Unchecked task **#{task_number}**.")
    else:
        await interaction.response.send_message("❌ Invalid task number.")


# /todo clear
@todo_group.command(name="clear", description="Clear the current list.")
async def todo_clear(interaction: discord.Interaction):
    server = ensure_server(interaction.guild_id)
    lst = server["current_list"]

    server["lists"][lst] = []
    save_data(data)

    await interaction.response.send_message(f"🗑 Cleared list **{lst}**")


# /todo create-list
@todo_group.command(name="create-list", description="Create a new todo list.")
async def todo_list_create(interaction: discord.Interaction, name: str):
    server = ensure_server(interaction.guild_id)

    if name in server["lists"]:
        await interaction.response.send_message("⚠️ List already exists.")
        return

    server["lists"][name] = []
    save_data(data)

    await interaction.response.send_message(f"📁 Created new list: **{name}**")


# /todo switch
@todo_group.command(name="switch", description="Switch to a different list.")
async def todo_list_switch(interaction: discord.Interaction, name: str):
    server = ensure_server(interaction.guild_id)

    if name not in server["lists"]:
        await interaction.response.send_message("❌ List does not exist.")
        return

    server["current_list"] = name
    save_data(data)

    await interaction.response.send_message(f"🔄 Switched to list: **{name}**")


# /todo delete-list
@todo_group.command(name="delete-list", description="Delete a to-do list.")
async def todo_delete_list(interaction: discord.Interaction, name: str):
    server = ensure_server(interaction.guild_id)

    if name == "default":
        await interaction.response.send_message("❌ Cannot delete the default list.")
        return

    if name not in server["lists"]:
        await interaction.response.send_message("❌ List does not exist.")
        return

    del server["lists"][name]
    
    # Switch to default if we deleted the current list
    if server["current_list"] == name:
        server["current_list"] = "default"
    
    save_data(data)
    await interaction.response.send_message(f"🗑 Deleted list: **{name}**")


# Add the group to the bot
bot.tree.add_command(todo_group)


# Get token from environment variable
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise ValueError("DISCORD_TOKEN not found in environment variables. Check your .env file.")

bot.run(TOKEN)
