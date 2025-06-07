from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.align import Align
from rich.live import Live
from datetime import datetime
import os
import time

console = Console()
TARGET_ID = None

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_to_file(content):
    with open("reports.txt", "a", encoding="utf-8") as f:
        f.write(content + "\n")

def ask_target_id():
    global TARGET_ID
    clear()
    panel = Panel(
        Align.center("[bold yellow]Welcome to PORY_CYB Gozaresh System\n\n[/bold yellow]"
                     "Lotfan [bold green]ID ya GUID[/bold green] target ra vared konid:", vertical="middle"),
        title="[bold cyan]Target ID Input[/bold cyan]",
        border_style="bold green",
        padding=(1, 4),
        width=60
    )
    console.print(panel, justify="center")
    TARGET_ID = Prompt.ask("[bold green]➤ Target ID/GUID")

def show_header():
    header = Panel(
        Align.center(
            f"[bold green]:sparkles: PORY REPORT SYSTEM SOROSH :sparkles:[/bold green]\n[cyan]🎯 Target: [bold white]{TARGET_ID}[/bold white][/cyan]",
            vertical="middle"),
        title="[cyan bold]Security & Gozaresh[/cyan bold]",
        subtitle="by PORY_CYB",
        padding=(1, 4),
        border_style="bold green",
        width=60
    )
    console.print(header, justify="center")

def main_menu():
    menu = Panel(
        """[bold yellow]Lotfan Yeki Az Gozineha Ra Entekhab Konid:[/bold yellow]

[bold cyan]1[/bold cyan]. 📝 Gozaresh Khali
[bold cyan]2[/bold cyan]. 💬 Gozaresh Ba Matn
[bold red]0[/bold red]. ❌ Khorooj
""",
        title="[blue]Menu Asli[/blue]",
        border_style="bold blue",
        width=50
    )
    console.print(menu, justify="center")
    return Prompt.ask("Shomare ra Vared Konid", choices=["1", "2", "0"])

def report_empty():
    clear()
    show_header()

    table = Table(title="🗂️ Anvae Gozaresh Khali", show_lines=True, box=None)
    table.add_column("Shomare", justify="center", style="cyan")
    table.add_column("Noe Gozaresh", style="magenta")

    options = ["Harzname", "Hesabe Jaali", "Khoshoonat", "Koodak Azari", "Mostahjan", "Copy Right"]
    for i, opt in enumerate(options, 1):
        table.add_row(str(i), f"🛑 {opt}")

    console.print(table)

    index = IntPrompt.ask("\nShomare mored nazar ra vared konid", choices=[str(i) for i in range(1, 7)])
    count = IntPrompt.ask("Chand bar ersal shavad?")

    with Live(console=console, refresh_per_second=10) as live:
        for i in range(1, count + 1):
            timestamp = now()
            msg = f"{i}. Gozaresh ersal shod ({timestamp})"
            live.update(Panel(f"[green]{msg} ✅", width=60))
            save_to_file(f"[{timestamp}] Target: {TARGET_ID} | Gozaresh Khali ({options[index-1]}) | Shomare {i}")
            time.sleep(0.3)

def report_with_text():
    clear()
    show_header()

    text = Prompt.ask("📝 Lotfan matne gozaresh ra vared konid")
    count = IntPrompt.ask("Chand bar ersal shavad?")

    with Live(console=console, refresh_per_second=10) as live:
        for i in range(1, count + 1):
            timestamp = now()
            msg = f"{i}. {text} - Gozaresh ersal shod ({timestamp})"
            live.update(Panel(f"[yellow]{msg} 📨", width=60))
            save_to_file(f"[{timestamp}] Target: {TARGET_ID} | Gozaresh Ba Matn: {text} | Shomare {i}")
            time.sleep(0.3)

def run():
    ask_target_id()
    while True:
        clear()
        show_header()
        choice = main_menu()

        if choice == "1":
            report_empty()
            console.input("\n[bold cyan]Baraye bazgasht be menu Enter bezan...[/bold cyan]")
        elif choice == "2":
            report_with_text()
            console.input("\n[bold cyan]Baraye bazgasht be menu Enter bezan...[/bold cyan]")
        elif choice == "0":
            console.print("\n[bold red]Khorooj az barname...[/bold red] ❌")
            break

if __name__ == "__main__":
    run()
