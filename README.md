# 🏛️ IARE Student Council Telegram Bot

A Telegram-based automation bot designed to streamline and standardize club activity coordination at the **Institute of Aeronautical Engineering (IARE)**. This bot enables smooth interaction between **Club Presidents**, **Core Team Members**, and **Student Council Admins** for event-related processes, file submissions, and access control — all through a user-friendly chat interface.

---



### 📌 Club Event Workflow

- **Club & Event Data Collection**  
  Collects key event details like:
  - Club name (dropdown)
  - Event name, duration, date & time, venue
  - Audience size
  - Event type: Tech / Non-Tech

- **Event Overview Submission**  
  Uses a Telegram prompt to collect a short 100-word description of the event.

- **File Upload System**
  Allows clubs to upload required documents with specific time-based conditions:
  - 📄 **Proposal Form** – accepted until 1 day before the event
  - 🗓️ **Flyer & Schedule** – accepted until 1 day before the event
  - 📋 **Participant List** – accepted on the day of the event
  - 📰 **Post-event Report (PDF)** – accepted up to 2 days after the event
  - 📸 **Photos (Drive Link)** – accepted up to 2 days after the event

- **Compendium Coordination**
  - Club can request the presence of a reporter and photographer.
  - Compendium President can enter their contact details directly in the bot.

- **Role-Based Access Control**
  - Bot restricts functionalities based on user roles (e.g., Admins vs Club Presidents)
---

## 👥 User Roles

| Role         | Description                                       |
|--------------|---------------------------------------------------|
| **Club Presidents** | 36 members (18 clubs × 2 reps) – submit event data |
| **Core Team**       | 14 members – involved in coordination         |
| **Admins**          | 6 members (President, VP, Dean, Enforcement) – full access |

---

## ⚙️ Tech Stack

```txt
pyrogram
tgcrypto
asyncpg
pytz
```


---

## 🚀 Getting Started

1. **Clone the repository**
   ```bash
   git clone https://github.com/skullkick/IARE-STUDENT-COUNCIL-BOT.git
   cd IARE-STUDENT-COUNCIL-BOT
    ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
 To run this bot, make sure to configure the following environment variables (either in your `.env` file or via the deployment environment, e.g., Heroku):

    | Variable Name              | Description                               |
    | -------------------------- | ----------------------------------------- |
    | `API_ID`                   | Telegram API ID                           |
    | `API_HASH`                 | Telegram API Hash                         |
    | `ADMIN_AUTHORIZATION_PASS` | Secret passphrase to authorize new admins |
    | `BOT_TOKEN`                | Your Telegram Bot Token                   |
    | `POSTGRES_USER_ID`         | PostgreSQL Username                       |
    | `POSTGRES_PASSWORD`        | PostgreSQL Password                       |
    | `POSTGRES_DATABASE`        | PostgreSQL Database Name                  |
    | `POSTGRES_HOST`            | PostgreSQL Hostname                       |
    | `POSTGRES_PORT`            | PostgreSQL Port                           |


4. **Run the bot**

   ```bash
   python bot.py
   ```
   
---

## 📜 License

This project is licensed under the [BSD-3 Clause License](LICENSE.md).

---


## 🤝 Contributions

- **[@Sricharan Reddy](https://github.com/SricharanReddy129)** - Provided project requirements.
- **[@Skullkick](https://github.com/Skullkick)** - Led development, implemented database, and built core bot logic.
- **[@Varun Reddy](https://github.com/varun240s)** - Enhanced database systems and optimized data handling.
- **[@Meghana Kolanuvada](https://github.com/MeghanaKolanuvada)** - Conducted testing and ensured functionality.

```
