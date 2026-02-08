# Orbix

**Orbix** is a fully offline, terminal-native AI assistant that understands natural language, executes Linux commands safely, remembers user context, and runs reproducibly inside Docker.

It is designed as a **privacy-first alternative to cloud AI copilots**, bringing intelligent system interaction directly to the local shell.

---

## ✨ Features

### Natural-Language Linux Control
- Converts plain English into real Linux commands
- Executes common system tasks such as:
  - disk usage inspection
  - process monitoring
  - file discovery
- Provides optional AI explanations of command output

### Fully Offline Operation
- Powered by a **local LLM via Ollama**
- **No internet required**
- All data remains **on the user’s device**

### Secure Command Execution
- Blocks destructive or unsafe commands
- Prevents shell injection risks
- Applies validation before execution

### Persistent Memory
- Stores conversation history in **SQLite**
- Remembers user preferences across sessions
- Enables **stateful assistant behavior**

### Streaming AI Responses
- Token-by-token output for responsive UX
- Reduces perceived latency similar to modern AI copilots

### Reproducible Deployment
- One-command setup via installer script
- Containerized runtime using **Docker**
- Consistent execution across machines and environments

---

## 🏗 Architecture Overview
-User Prompt
↓
-Local LLM (Ollama)
↓
-Command Generation + Safety Filter
↓
-Secure Shell Execution
↓
-Streaming Explanation + SQLite Memory

---

## 🚀 Installation (Local)

```bash
git clone <https://github.com/ShravanSaysHi/orbix>
cd orbix
./install.sh
./run.sh

