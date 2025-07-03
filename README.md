<h1 align="center">📨 MAILSQUEEZE</h1>
<p align="center"><em>Transforming Email Chaos Into Clear, Actionable Insights</em></p>

<p align="center">
  <img src="https://img.shields.io/badge/Status-Active-green" />
  <img src="https://img.shields.io/badge/Jupyter%20Notebook-75%25-blue" />
  <img src="https://img.shields.io/badge/Language-Python-yellow" />
</p>

<p align="center"><strong>Built with the tools and technologies:</strong></p>
<p align="center">
  <img src="https://img.shields.io/badge/Markdown-%23000000.svg?style=flat&logo=markdown&logoColor=white"/>
  <img src="https://img.shields.io/badge/Python-FFD43B?logo=python&logoColor=blue" />
  <img src="https://img.shields.io/badge/Gemini-2.5%20Flash-blueviolet" />
  <img src="https://img.shields.io/badge/Google%20Gmail-red?logo=gmail&logoColor=white" />
  <img src="https://img.shields.io/badge/Pytest-blueviolet" />
</p>

---

## 📚 Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Configuration](#configuration)
- [Usage](#usage)
  - [Running the Bot](#running-the-bot)
  - [Example Output](#example-output)
- [Testing](#testing)
- [Contributing](#contributing)
- [License](#license)

---

## 📖 Overview

**MailSqueeze** is an intelligent developer tool designed to automate the retrieval, summarization, and notification of unread emails. By integrating **Gmail API**, **generative AI (Google Gemini)**, and **Telegram messaging**, it streamlines email management and keeps users (and teams) informed with concise, actionable updates.

### 🤔 Why MailSqueeze?

Managing overwhelming inboxes is a challenge for developers, teams, and productivity enthusiasts. MailSqueeze automates email workflows, extracts the signal from the noise, and improves communication efficiency.

---

## 🚀 Features

- 🔔 **Notification:** Sends real-time AI-generated email summaries directly to Telegram channels or users.
- 🤖 **AI Summarization:** Uses Gemini 2.5 Flash to summarize email content in clear, concise language.
- 🔒 **Secure Access:** Handles OAuth-based Gmail authentication and content extraction securely.
- 🔄 **Workflow Automation:** Supports scheduled tasks for daily or on-demand email digests.
- 🔗 **API Integration:** Seamlessly connects Gmail, Google Gemini, and Telegram APIs.
- 🧪 **Testable:** Built with Jupyter Notebooks for easy prototyping and continuous integration with Pytest.

---

## 🏗️ Architecture

The core architecture is modular, with the following major components:

- **Gmail Integration:** Authenticates and fetches unread emails using Gmail API.
- **Content Extraction:** Decodes email bodies and prepares them for AI processing.
- **AI Summarization:** Sends email content to Gemini 2.5 Flash and retrieves summaries.
- **Notifications:** Delivers summaries to Telegram via bot API.
- **Scheduler:** (Optional) Automates periodic polling and notifications (can be run as a cron job or via notebook).

```
+----------+      +--------------+      +----------------+      +---------------+
|  Gmail   | ---> | Content      | ---> | Gemini AI      | ---> | Telegram Bot  |
|  Inbox   |      | Extraction   |      | Summarization  |      | Notification  |
+----------+      +--------------+      +----------------+      +---------------+
```

---

## 🛠️ Getting Started

### 📦 Prerequisites

- **Programming Language:** Python 3.8+
- **Package Manager:** pip
- **Gmail API access:** Google Cloud project with Gmail API enabled.
- **Telegram Bot:** Telegram account and bot token.

### 💾 Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yugan243/MailSqueeze
   cd MailSqueeze
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   # Or for Windows:
   pip install -r requirements-windows.txt
   ```

### ⚙️ Configuration

1. **Google Credentials:**
   - Create OAuth credentials (`credentials.json`) from [Google Cloud Console](https://console.cloud.google.com/).
   - Place `credentials.json` in the root directory.

2. **Telegram Bot Token:**
   - Create a Telegram bot via [BotFather](https://core.telegram.org/bots#botfather).
   - Note your bot token.

3. **Environment Variables:**
   - Create a `.env` file:
     ```
     GEMINI_API_KEY=your_gemini_key
     TELEGRAM_BOT_TOKEN=your_telegram_bot_token
     TELEGRAM_CHAT_ID=your_telegram_chat_id
     GOOGLE_CLIENT_ID=your_google_client_id
     GOOGLE_CLIENT_SECRET=your_google_client_secret
     ```

---

## ▶️ Usage

### 🏃 Running the Bot

You can run the bot either through the notebook or directly via Python script.

**Python script:**
```bash
python main.py
```

**Jupyter Notebook:**
- Open `MailSqueezeBot.ipynb` and run all cells to test or prototype.

### 💡 Example Output

When a new unread email is detected, the bot will summarize and send a message like:

```
📧 New Email Summary:
This email from FreeBitco.in promotes their **Premium Membership**.

Key benefits include:
• 16 Free Spins on the Wheel of Fortune
• 25% additional interest on BTC deposits
• 1% cashback on Multiply BTC/betting
• 10% APY on FUN Savings
```

---

## 🧪 Testing

- Run Pytest to execute unit tests (if implemented):
  ```bash
  pytest
  ```

- For Jupyter-based development, use notebook cells to test each function interactively.

---



## 📜 License

This project is licensed under the [Apache License 2.0](LICENSE).

---

<p align="center"><strong>MailSqueeze</strong> — Automate your email, focus on what matters.</p>