# AI Interview Agent

A free, private mock interview coach that runs entirely on your own computer. Upload your CV, tell it what job you're applying for, and have a realistic interview with detailed feedback — no account needed, no internet required, nothing sent anywhere.

---

## What it does

1. You upload your CV as a PDF and enter the role you're applying for.
2. An AI interviewer reads your CV and asks you tailored questions — one at a time.
3. You type your answers as if you were in a real interview.
4. When the interview ends, you get a detailed feedback report with scores, strengths, areas to improve, and specific tips.
5. You can download the full report as a PDF and ask follow-up questions to your feedback coach.

You can also choose the **interview style** (e.g. a friendly phone screen or a tough final round) and the **difficulty level** before you start.

---

## What you need to install

You need two free programs. Neither requires an account.

| Program | What it does | Where to get it |
|---|---|---|
| **Docker Desktop** | Runs the app in the background | https://www.docker.com/products/docker-desktop |
| **Ollama** | Runs the AI on your computer | https://ollama.com |

---

## Setup — step by step

### Step 1 — Install Docker Desktop

**Windows**

1. Go to https://www.docker.com/products/docker-desktop and click **Download for Windows**
2. Run the downloaded `.exe` file and follow the on-screen steps
3. If asked about "WSL 2", click **Yes** or **OK** — this is normal
4. Once installed, open **Docker Desktop** from the Start menu
5. Wait for the startup animation to finish — the whale icon in the taskbar (bottom right) should stop moving

**Mac**

1. Go to https://www.docker.com/products/docker-desktop and download the version for your chip (Apple Silicon or Intel — check Apple menu → About This Mac → Chip)
2. Open the downloaded `.dmg` file, drag Docker into your Applications folder, then launch it
3. Wait for the whale icon in the top menu bar to go solid before continuing

---

### Step 2 — Install Ollama and download the AI model

**Windows**

1. Go to https://ollama.com/download/windows and download the installer
2. Run it and follow the steps — Ollama will start automatically
3. Open a terminal by pressing **Windows key + R**, typing `cmd`, and pressing Enter
4. Paste in this command and press Enter — it downloads the AI model (about 2 GB, takes a few minutes):

```
ollama pull llama3.2
```

5. Wait for it to finish, then you can close the terminal window

**Mac**

1. Go to https://ollama.com/download/mac and download the app
2. Open the `.dmg` and drag Ollama to your Applications folder, then launch it
3. Once the icon appears in the top menu bar, open Terminal (press **Command + Space**, type `Terminal`, press Enter) and run:

```
ollama pull llama3.2
```

4. Wait for the download to complete, then close the Terminal window

> Leave Ollama running in the background — it starts automatically when your computer starts after installation.

---

### Step 3 — Download this project

**Option A — Download as a ZIP (easiest)**

1. On this GitHub page, click the green **Code** button near the top right
2. Click **Download ZIP**
3. Find the downloaded ZIP in your Downloads folder and extract it (right-click → Extract All on Windows, or double-click on Mac)
4. Remember where you extracted it — you'll need this folder in the next step

**Option B — Using Git**

If you have Git installed, open a terminal and run:

```
git clone https://github.com/KJH91/agentic_interviewer.git
```

---

### Step 4 — Start the app

**Windows**

1. Open **File Explorer** and navigate to the folder you extracted in Step 3
2. Click on the address bar at the top of the window (it shows the folder path), type `cmd`, and press Enter — a terminal opens in the right place
3. Paste this command and press Enter:

```
docker compose up --build
```

**Mac**

1. Open **Terminal** (Command + Space, type Terminal, press Enter)
2. Type `cd ` (with a space after), then drag the project folder from Finder into the Terminal window — it fills in the path automatically. Press Enter.
3. Run:

```
docker compose up --build
```

**The first time you run this it will take 3–5 minutes** while it sets up. You'll see a lot of text scrolling — that's normal. When you see a line containing `You can now view your Streamlit app in your browser`, it's ready.

---

### Step 5 — Open the app

Open your web browser and go to:

**[http://localhost:8501](http://localhost:8501)**

The app will load and you're ready to go.

---

## How to use it

### Starting an interview

1. **Upload your CV** — click the upload area and select your CV as a PDF. It must be a normal PDF (not a scanned image). If your CV is in Word format, open it and use File → Save As → PDF first.
2. **Target job role** — type the role you're applying for, e.g. `Marketing Manager` or `Software Developer`
3. **Industry** (optional) — helps the interviewer adopt the right persona, e.g. `Healthcare` or `Finance`
4. **Difficulty** — choose how tough you want the interviewer to be:
   - *Easy* — warm and encouraging, good for first-time practice
   - *Medium* — professional and balanced (recommended)
   - *Hard* — direct and demanding, pushes for detail on every answer
5. **Interview format** — choose the type of interview:
   - *Mixed* — a broad mix of question types (good default)
   - *Phone Screen* — conversational, focused on background and fit
   - *Technical Deep-Dive* — focused on skills and hands-on experience
   - *Behavioural Panel* — STAR-format questions ("Tell me about a time when…")
   - *Final Round* — strategic and values-focused
6. **Job description** (optional) — paste the full job advert for much more targeted questions
7. **Number of questions** — between 5 and 20 (10 is a good starting point)
8. Click **Start Interview**

### During the interview

Type your answers in the text box and click **Submit Answer**. Take your time — there's no clock. If you want to stop early, click **End Interview Early**.

### After the interview

- Read your **feedback report** — you'll get an overall score, a breakdown across five competency areas, and specific comments on each question
- Click **Download Report (PDF)** to save it
- Use the **feedback coach** chat at the bottom to ask follow-up questions like *"What would a stronger answer to question 3 have looked like?"*

### Demo mode

If you just want to see how the app works without uploading a CV, scroll down on the setup screen and click **Load Demo** — it loads a complete pre-written interview and generates live feedback.

---

## Stopping and restarting

To stop the app, go back to the terminal and press **Ctrl + C**.

To start it again later (faster, no rebuild needed):

```
docker compose up
```

---

## Troubleshooting

### The app won't start / Docker errors

Make sure Docker Desktop is open and fully loaded (whale icon is still). If you just installed it, try restarting your computer.

### "Cannot connect to Ollama" error in the app

Ollama needs to be running. On Windows, check the system tray (bottom right of the taskbar) for the Ollama icon. On Mac, check the menu bar. If it's not there, open Ollama from your Applications.

### The AI responses are very slow

This is normal if your computer doesn't have a dedicated graphics card — the AI runs on your CPU. `llama3.2` (the default) is the fastest option. Responses typically take 10–30 seconds on an average laptop.

### My CV won't upload

The app only accepts **text-based PDFs**. If your CV was created in Word or Google Docs, export it as a PDF using File → Save As / Download As → PDF. Scanned CVs (photos of a physical document) are not supported.

### I need to update the app after downloading a new version

Stop the app (Ctrl + C), then run:

```
docker compose up --build
```

The `--build` flag picks up any changes.

---

## System requirements

- Windows 10/11 or macOS 12+
- 8 GB RAM minimum (16 GB recommended for smooth performance)
- ~3 GB free disk space (for the AI model)
- No internet connection required after setup
