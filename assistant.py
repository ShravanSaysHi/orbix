import ollama
import subprocess
from memory import Memory
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()
memory = Memory()

# ---------- Models ----------
CMD_MODEL = "phi3"
EXPLAIN_MODEL = "phi3"


# ---------- Safety Filter ----------
def is_safe(command: str) -> bool:
    blocked = [
        "rm ", "reboot", "shutdown", "mkfs", "dd ",
        "kill ", "killall", "poweroff", "init",
        ":(){", "chmod 777", "chown", ">/", ">>/"
    ]
    cmd = command.lower()
    return not any(b in cmd for b in blocked)


# ---------- Run Shell Command ----------
def run_command(command: str) -> str:
    try:
        result = subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=10,
            executable="/bin/bash"
        )
        return result.stdout or result.stderr or "No output."
    except Exception as e:
        return f"Execution error: {e}"


# ---------- Streaming Command Generation ----------
def get_linux_command_stream(prompt: str) -> str:
    stream = ollama.chat(
        model=CMD_MODEL,
        stream=True,
        options={"num_predict": 32},
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a Linux expert. "
                    "Return ONLY one short safe Linux command. "
                    "No explanation, no backticks, max 20 tokens."
                ),
            },
            {"role": "user", "content": prompt},
        ],
    )

    console.print("\n[bold yellow]Command:[/bold yellow] ", end="")

    full_cmd = ""

    for chunk in stream:
        text = chunk["message"]["content"]
        full_cmd += text
        console.print(text, end="", soft_wrap=True)

    console.print()

    # cleanup formatting artifacts
    cmd = full_cmd.strip().strip("`").replace("```", "").splitlines()[0]
    return cmd


# ---------- Streaming Explanation ----------
def stream_explanation(prompt: str, command: str, output: str):
    stream = ollama.chat(
        model=EXPLAIN_MODEL,
        stream=True,
        options={"num_predict": 128},
        messages=[
            {"role": "system", "content": "Explain the result briefly in simple terms."},
            {
                "role": "user",
                "content": f"Request: {prompt}\nCommand: {command}\nOutput:\n{output}",
            },
        ],
    )

    console.print("\n[bold cyan]Explanation:[/bold cyan] ", end="")
    for chunk in stream:
        console.print(chunk["message"]["content"], end="", soft_wrap=True)
    console.print("\n")


# ---------- Help Menu ----------
def show_help():
    text = """
[bold]Orbix Commands[/bold]

[cyan]General[/cyan]
  help            Show this help menu
  exit / quit     Exit Orbix

[cyan]Memory[/cyan]
  history         Show recent conversations
  showprefs       List saved preferences
  setpref k v     Save preference
  getpref k       Retrieve preference

[cyan]AI Usage[/cyan]
  Type any natural-language Linux request:
    • show disk usage
    • list large files
    • check memory usage
"""
    console.print(Panel(text, title="Orbix Help", border_style="cyan"))


# ---------- Startup Banner ----------
def show_banner():
    banner = Text("Orbix — Offline Terminal AI Assistant", style="bold green")
    console.print(Panel(banner, expand=False))
    console.print("Fast • Private • Offline\n", style="dim")


# ---------- Main Loop ----------
def main():
    show_banner()

    while True:
        try:
            prompt = console.input("[bold magenta]orbix ❯ [/bold magenta]").strip()

            if prompt.lower() in ["exit", "quit"]:
                console.print("\nGoodbye from Orbix.\n", style="bold green")
                break

            # ---------- Help ----------
            if prompt == "help":
                show_help()
                continue

            # ---------- History ----------
            if prompt == "history":
                items = memory.get_recent_conversations()
                console.print("\n[bold cyan]Recent Conversations[/bold cyan]")
                for p, c, o, t in items:
                    console.print(f"[dim]{t}[/dim]  [yellow]{p}[/yellow] → [green]{c}[/green]")
                console.print()
                continue

            # ---------- Preferences ----------
            if prompt == "showprefs":
                prefs = memory.get_all_prefs()
                console.print("\n[bold cyan]Preferences[/bold cyan]")
                for k, v in prefs:
                    console.print(f"{k} = {v}")
                console.print()
                continue

            if prompt.startswith("setpref "):
                try:
                    key, value = prompt.replace("setpref ", "").split(" ", 1)
                    memory.set_pref(key, value)
                    console.print("Preference saved.\n", style="green")
                except:
                    console.print("Usage: setpref <key> <value>\n", style="red")
                continue

            if prompt.startswith("getpref "):
                key = prompt.replace("getpref ", "").strip()
                val = memory.get_pref(key, "Not set")
                console.print(f"{key} = {val}\n", style="cyan")
                continue

            # ---------- AI Command (STREAMING) ----------
            command = get_linux_command_stream(prompt)

            if not is_safe(command):
                console.print("⚠️ Blocked unsafe command.\n", style="bold red")
                continue

            output = run_command(command)

            console.print("\n[bold green]Output:[/bold green]")
            console.print(output)

            memory.save_conversation(prompt, command, output)

            # ---------- Optional Explanation ----------
            choice = console.input("[dim]Explain output? (y/n): [/dim]").lower()
            if choice == "y":
                stream_explanation(prompt, command, output)

        except KeyboardInterrupt:
            console.print("\nInterrupted. Type 'exit' to quit.\n", style="red")


if __name__ == "__main__":
    main()
