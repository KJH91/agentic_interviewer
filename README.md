# AI Interview Agent

A locally hosted AI-powered mock interview coach. Upload your CV, pick a target role, and have a realistic adaptive interview conducted by a local LLM — no cloud, no data leaving your machine.

## How it works

1. You upload a PDF CV and enter a target job role.
2. The app parses your CV and feeds it to a local Llama model via Ollama.
3. A LangChain-powered interview agent asks you tailored questions one at a time, mixing technical, behavioural, and situational styles.
4. After all questions are answered, the agent provides structured feedback with a score out of 10.
5. You can download the full transcript as a PDF.

---

## Prerequisites

| Tool | Purpose | Download |
|---|---|---|
| Docker Desktop | Runs the app in a container | https://www.docker.com/products/docker-desktop |
| Ollama | Serves the LLM locally on your host machine | https://ollama.com |

---

## Setup

### 1. Install Docker Desktop

**Windows**

1. Download the installer from https://www.docker.com/products/docker-desktop
2. Run the `.exe` and follow the prompts (WSL 2 backend is recommended — accept it if prompted)
3. Launch Docker Desktop from the Start menu
4. Wait for it to finish starting — the whale icon in the system tray should go solid white
5. Close and reopen PowerShell so the `docker` command is on your PATH

**macOS**

1. Download Docker Desktop from https://www.docker.com/products/docker-desktop
2. Open the `.dmg`, drag Docker to Applications, and launch it
3. Wait for the menu-bar whale icon to go solid before continuing

**Linux**

Follow the official guide for your distro: https://docs.docker.com/engine/install/

### 2. Install Ollama and pull the model

**Windows**

1. Download the installer from https://ollama.com/download/windows
2. Run the `.exe` and follow the prompts — Ollama will be added to your PATH automatically
3. Close and reopen PowerShell, then run:

```powershell
ollama pull llama3.2
```

**macOS**

1. Download the app from https://ollama.com/download/mac
2. Open the `.dmg`, drag Ollama to Applications, and launch it
3. Once the menu-bar icon appears, run:

```bash
ollama pull llama3.2
```

**Linux**

```bash
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2
```

Leave Ollama running in the background (it starts automatically after installation on all platforms).

### 3. Clone or download this project

```bash
git clone <repo-url>
cd interviewer-app
```

### 4. Build and run with Docker Compose

```powershell
docker compose up --build
```

The first build will take a few minutes while Python dependencies are installed inside the container.

### 5. Open the app

Navigate to [http://localhost:8501](http://localhost:8501) in your browser.

---

## Usage

1. **Upload your CV** — PDF format only (text-based, not scanned).
2. **Enter the target role** — e.g. `Senior React Developer` or `Data Scientist`.
3. **Choose a model** — defaults to `llama3.2`; any model you have pulled in Ollama appears in the dropdown.
4. **Set the number of questions** — between 5 and 20 (default 10).
5. Click **Start Interview** and follow the interviewer's prompts.
6. When the interview ends, read your feedback and optionally **Download Transcript (PDF)**.

---

## Troubleshooting

### Ollama not reachable from Docker

The container reaches Ollama via `host.docker.internal:11434`. Make sure:

- Ollama is running on your host machine (`ollama serve` or the Ollama app is open).
- Your firewall is not blocking port `11434`.
- On Linux, Docker Compose is configured with `extra_hosts: host-gateway` (already set in `docker-compose.yml`).

Test connectivity from inside the container:

```bash
docker exec -it <container-name> curl http://host.docker.internal:11434/api/tags
```

### Model not found

If the selected model isn't pulled yet, pull it on your host:

```bash
ollama pull llama3.2
```

Any model visible in `ollama list` will appear in the app's model dropdown.

### PDF parsing errors

The app uses PyMuPDF to extract text. Scanned / image-only PDFs will fail with a friendly error message. Use a digitally created PDF (exported from Word, Google Docs, etc.).

### Slow responses

Larger models produce better interviews but are slower. On CPU-only machines, `llama3.2` (3B) is the recommended model. If you have a GPU, `llama3.2:8b` or `mistral` will give richer answers.

---

## Project structure

```
interviewer-app/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── README.md
└── app/
    ├── main.py        # Streamlit UI
    ├── agent.py       # LangChain interview agent
    └── cv_parser.py   # PyMuPDF CV text extraction
```

---

## Development

The `app/` directory is mounted as a volume, so you can edit `main.py`, `agent.py`, or `cv_parser.py` and the Streamlit hot-reload will pick up changes without rebuilding the container.

To restart cleanly:

```powershell
docker compose down
docker compose up
```
