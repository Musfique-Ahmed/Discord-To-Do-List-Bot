# 🚀 Deployment Guide for Discord To-Do List Bot

## Prerequisites
- Python 3.11+ installed
- Discord Bot Token (already in `.env`)
- Git installed

## 📋 Quick Start (Local Testing)

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the bot:**
   ```bash
   python todo_bot.py
   ```

---

## ☁️ Cloud Deployment Options

### Option 1: Railway (Recommended - Free Tier Available)

1. **Sign up:** https://railway.app/
2. **Create New Project** → **Deploy from GitHub repo**
3. **Connect your repository**
4. **Add Environment Variables:**
   - Go to Variables tab
   - Add: `DISCORD_TOKEN` = (your token from .env file)
5. **Deploy** - Railway will auto-detect Python and use `railway.json`

**Pros:** Easy, free tier ($5 credit/month), auto-deploys on git push  
**Cons:** Requires credit card after trial

---

### Option 2: Render (Paid - $7/month)

1. **Sign up:** https://render.com/
2. **New** → **Background Worker**
3. **Connect GitHub repository**
4. **Configure:**
   - Name: `discord-todo-bot`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python todo_bot.py`
5. **Environment Variables:**
   - Add `DISCORD_TOKEN` with your token
6. **Select plan:** Starter ($7/month minimum)
7. **Create Service**

**Pros:** Reliable, easy to use, good documentation  
**Cons:** No free tier, starts at $7/month

---

### Option 3: Heroku

1. **Install Heroku CLI:** https://devcenter.heroku.com/articles/heroku-cli
2. **Login and create app:**
   ```bash
   heroku login
   heroku create your-bot-name
   ```
3. **Set environment variable:**
   ```bash
   heroku config:set DISCORD_TOKEN=your_token_here
   ```
4. **Deploy:**
   ```bash
   git push heroku main
   ```
5. **Scale worker:**
   ```bash
   heroku ps:scale worker=1
   ```

**Pros:** Reliable, well-documented  
**Cons:** No free tier anymore (starts at $5/month)

---

### Option 4: VPS (DigitalOcean, Linode, AWS EC2)

1. **Create Ubuntu 22.04 server**
2. **SSH into server:**
   ```bash
   ssh root@your-server-ip
   ```
3. **Install Python:**
   ```bash
   apt update
   apt install python3 python3-pip git -y
   ```
4. **Clone repository:**
   ```bash
   git clone https://github.com/yourusername/Discord-To-Do-List-Bot.git
   cd Discord-To-Do-List-Bot
   ```
5. **Create `.env` file:**
   ```bash
   nano .env
   ```
   Add: `DISCORD_TOKEN=your_token_here`
   
6. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```
7. **Run with systemd (keeps bot running):**
   ```bash
   nano /etc/systemd/system/discord-bot.service
   ```
   
   Add:
   ```ini
   [Unit]
   Description=Discord To-Do Bot
   After=network.target

   [Service]
   Type=simple
   User=root
   WorkingDirectory=/root/Discord-To-Do-List-Bot
   ExecStart=/usr/bin/python3 /root/Discord-To-Do-List-Bot/todo_bot.py
   Restart=on-failure

   [Install]
   WantedBy=multi-user.target
   ```

8. **Start service:**
   ```bash
   systemctl daemon-reload
   systemctl enable discord-bot
   systemctl start discord-bot
   systemctl status discord-bot
   ```

**Pros:** Full control, best performance  
**Cons:** More setup, need to manage server

---

### Option 5: PythonAnywhere (Free Tier)

1. **Sign up:** https://www.pythonanywhere.com/
2. **Upload files** via Files tab
3. **Open Bash console**
4. **Install dependencies:**
   ```bash
   pip install --user -r requirements.txt
   ```
5. **Create `.env` file** with your token
6. **Run bot** (Note: free tier has limitations)

**Pros:** Free tier, easy to use  
**Cons:** Free tier is limited, may not support always-on bots

---

## 🔐 Security Checklist

- ✅ Bot token is in `.env` file (not hardcoded)
- ✅ `.env` is in `.gitignore` (not committed to git)
- ✅ Never share your bot token publicly
- ✅ Regenerate token if accidentally exposed

---

## 🐛 Troubleshooting

**Bot won't start:**
- Check `.env` file exists and has correct token
- Verify `python-dotenv` is installed: `pip install python-dotenv`

**Commands not showing:**
- Wait 1 hour for Discord to sync globally
- Or use guild-specific commands (faster)

**Data not persisting:**
- Ensure `todo_data.json` has write permissions
- On cloud platforms, use persistent storage/volumes

---

## 📝 Post-Deployment

1. **Invite bot to server:**
   - Go to Discord Developer Portal
   - OAuth2 → URL Generator
   - Select: `bot`, `applications.commands`
   - Bot Permissions: `Send Messages`, `Use Slash Commands`
   - Copy and visit the URL

2. **Test commands:**
   - `/todo_add task: Test task`
   - `/todo_list`

3. **Monitor logs** on your hosting platform

---

## 🎉 You're Done!

Your Discord bot should now be running 24/7. Choose the deployment option that best fits your needs and budget.

**Need help?** Check the logs on your hosting platform for any error messages.
