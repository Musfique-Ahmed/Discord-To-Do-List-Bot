# 📝 Discord To-Do List Bot

A simple and powerful Discord bot that manages personal and shared to-do lists inside any server.  
Supports bulk item addition, multiple lists per server, and slash commands.

---

## 🚀 Features

### ✅ Core To-Do Commands
| Command | Description |
|--------|-------------|
| `/todo list` | View all to-do lists or items in a list |
| `/todo add "Task name"` | Add a single task |
| `/todo add-bulk "Task 1; Task 2; Task 3"` | Add multiple tasks (separated by `;`) |
| `/todo check <task_number>` | Mark a task as completed |
| `/todo uncheck <task_number>` | Mark a completed task as uncompleted |
| `/todo clear` | Delete all tasks in the current list |
| `/todo create-list <name>` | Create a new to-do list |
| `/todo switch <name>` | Switch to another list |
| `/todo delete-list <name>` | Delete a to-do list |

### 👥 Shared Lists
- Anyone in the server can view and update lists.
- (Optional) List-level permissions.

### 💾 Persistent Storage
- **SQLite** (default)
- MongoDB/Postgres optional

### ⚙️ Slash Commands
- Built using Discord's Interactions API.
- Fast and modern.

---

## 🏗️ Tech Stack

| Component | Technology |
|-----------|------------|
| **Bot** | Node.js + discord.js |
| **Database** | SQLite (Prisma / better-sqlite3) |
| **Commands** | Discord Slash Commands |
| **Hosting** | Railway / Render / VPS / Replit |

---

## 📦 Installation

### 1️⃣ Clone the Repo
```bash
git clone https://github.com/yourname/discord-todo-bot.git
cd discord-todo-bot
