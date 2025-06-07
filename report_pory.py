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

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_to_file(content):
    with open("reports.txt", "a", encoding="utf-8") as f:
        f.write(content + "\n")

def show_header():
    header = Panel(
        Align.center("[bold green]:sparkles: PORY REPORT SYSTEM SOROSH:sparkles:[/bold green]", vertical="middle"),
        title="[cyan bold]امنیت و گزارش[/cyan bold]",
        subtitle="by PORY_CYB",
        padding=(1, 4),
        border_style="bold green",
        width=60
    )
    console.print(header, justify="center")

def main_menu():
    menu = Panel(
        """[bold yellow]لطفا یکی از گزینه‌ها را انتخاب کنید:[/bold yellow]

[bold cyan]1[/bold cyan]. 📝 گزارش خالی
[bold cyan]2[/bold cyan]. 💬 گزارش با متن
[bold red]0[/bold red]. ❌ خروج
""",
        title="[blue]منوی اصلی[/blue]",
        border_style="bold blue",
        width=50
    )
    console.print(menu, justify="center")
    return Prompt.ask("شماره را وارد کنید", choices=["1", "2", "0"])

def report_empty():
    clear()
    show_header()

    table = Table(title="🗂️ انواع گزارش خالی", show_lines=True, box=None)
    table.add_column("شماره", justify="center", style="cyan")
    table.add_column("نوع گزارش", style="magenta")

    options = ["هرزنامه", "حساب کاربر جعلی", "خشونت", "کودک آزاری", "مستهجن", "کپی رایت"]
    for i, opt in enumerate(options, 1):
        table.add_row(str(i), f"🛑 {opt}")

    console.print(table)

    index = IntPrompt.ask("\nشماره مورد نظر را وارد کنید", choices=[str(i) for i in range(1, 7)])
    count = IntPrompt.ask("چند بار ارسال شود؟")

    with Live(console=console, refresh_per_second=10) as live:
        for i in range(1, count + 1):
            timestamp = now()
            msg = f"{i}. گزارش ارسال شد ({timestamp})"
            live.update(Panel(f"[green]{msg} ✅", width=60))
            save_to_file(f"[{timestamp}] گزارش خالی ({options[index-1]}) شماره {i}")
            time.sleep(0.3)

def report_with_text():
    clear()
    show_header()

    text = Prompt.ask("📝 لطفاً متن گزارش را وارد کنید")
    count = IntPrompt.ask("چند بار ارسال شود؟")

    with Live(console=console, refresh_per_second=10) as live:
        for i in range(1, count + 1):
            timestamp = now()
            msg = f"{i}. {text} - گزارش ارسال شد ({timestamp})"
            live.update(Panel(f"[yellow]{msg} 📨", width=60))
            save_to_file(f"[{timestamp}] گزارش با متن: {text} (شماره {i})")
            time.sleep(0.3)

def run():
    while True:
        clear()
        show_header()
        choice = main_menu()

        if choice == "1":
            report_empty()
            console.input("\n[bold cyan]برای بازگشت به منو Enter را بزنید...[/bold cyan]")
        elif choice == "2":
            report_with_text()
            console.input("\n[bold cyan]برای بازگشت به منو Enter را بزنید...[/bold cyan]")
        elif choice == "0":
            console.print("\n[bold red]خروج از برنامه...[/bold red] ❌")
            break

if __name__ == "__main__":
    run()