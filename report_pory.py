from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt, IntPrompt
from rich.table import Table
from rich.align import Align
from rich.live import Live
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import os
import time
from deep_translator import GoogleTranslator
from pyfiglet import Figlet

console = Console()
TARGET_ID = None
TARGET_INFO = {}

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def print_logo():
    f = Figlet(font='doom')
    logo = f.renderText('PORY')
    console.print(f"[bold bright_green]{logo}[/bold bright_green]")

def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def save_to_file(content):
    with open("reports.txt", "a", encoding="utf-8") as f:
        f.write(content + "\n")

def fetch_user_info(username):
    global TARGET_INFO
    if not username.startswith("@"):
        username = "@" + username

    url = f"https://splus.ir/{username[1:]}"
    try:
        res = requests.get(url)
        if res.status_code != 200:
            TARGET_INFO = {"name": "نام پیدا نشد", "bio": "بیوگرافی پیدا نشد", "photo": "عکسی پیدا نشد", "url": url}
            return TARGET_INFO

        soup = BeautifulSoup(res.text, "html.parser")

        name_tag = soup.find("meta", attrs={"property": "og:title"})
        bio_tag = soup.find("meta", attrs={"property": "og:description"})
        img_tag = soup.find("meta", attrs={"property": "og:image"})

        name = name_tag["content"] if name_tag else "نام پیدا نشد"
        bio = bio_tag["content"] if bio_tag else "بیوگرافی پیدا نشد"
        photo = img_tag["content"] if img_tag else "عکسی پیدا نشد"

        TARGET_INFO = {"name": name, "bio": bio, "photo": photo, "url": url}
        return TARGET_INFO
    except:
        TARGET_INFO = {"name": "نام پیدا نشد", "bio": "بیوگرافی پیدا نشد", "photo": "عکسی پیدا نشد", "url": url}
        return TARGET_INFO

def ask_target_id():
    global TARGET_ID
    clear()
    print_logo()
    panel = Panel(
        Align.center(
            "[bold bright_yellow]Welcome to PORY_CYB Gozaresh System[/bold bright_yellow]\n\n"
            "Lotfan [bold bright_green]ID ya GUID[/bold bright_green] target ra vared konid:",
            vertical="middle",
        ),
        title="[bold bright_green]Target ID Input[/bold bright_green]",
        border_style="bright_green",
        padding=(1, 4),
        width=65,
    )
    console.print(panel, justify="center")
    TARGET_ID = Prompt.ask("[bold bright_green]➤ Target ID/GUID[/bold bright_green]")
    fetch_user_info(TARGET_ID)
    clear()
    print_logo()
    show_header()
    console.input("\n[bold bright_cyan]Baraye edame Enter bezanid...[/bold bright_cyan]")

def show_header():
    info_panel = Panel(
        Align.left(
            f"[bold bright_green]👤 Name:[/bold bright_green] {TARGET_INFO.get('name')}\n"
            f"[bold bright_green]📝 Bio:[/bold bright_green] {TARGET_INFO.get('bio')}\n"
            f"[bold bright_green]🖼 Photo:[/bold bright_green] {TARGET_INFO.get('photo')}\n"
            f"[bold bright_green]🔗 Link:[/bold bright_green] {TARGET_INFO.get('url')}\n",
            vertical="top",
        ),
        title=f"[bright_green]📄 Etela'at Karbar: {TARGET_ID}[/bright_green]",
        border_style="bright_green",
        width=80,
    )
    console.print(info_panel)

def main_menu():
    clear()
    print_logo()
    menu_text = """
[bold bright_green]===============================================[/bold bright_green]
[bold bright_yellow]>>> Choose your operation:[/bold bright_yellow]

[bold bright_green]1[/bold bright_green]. 📝 Gozaresh Khali
[bold bright_green]2[/bold bright_green]. 💬 Gozaresh Ba Matn
[bold bright_green]3[/bold bright_green]. 🌐 Motarjem (Translator)
[bold bright_red]0[/bold bright_red]. ❌ Exit
[bold bright_green]===============================================[/bold bright_green]
"""
    panel = Panel(menu_text, border_style="bright_green", width=65)
    console.print(panel, justify="center")
    return Prompt.ask("[bold bright_green]Enter your choice[/bold bright_green]", choices=["1","2","3","0"])

def report_empty():
    clear()
    print_logo()
    show_header()

    table = Table(title="🗂️ Anvae Gozaresh Khali", show_lines=True, box=None)
    table.add_column("Shomare", justify="center", style="bright_green")
    table.add_column("Noe Gozaresh", style="bright_green")

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
            live.update(Panel(f"[bright_green]{msg} ✅", width=60))
            save_to_file(f"[{timestamp}] Target: {TARGET_ID} | Gozaresh Khali ({options[index-1]}) | Shomare {i}")
            time.sleep(0.3)

def report_with_text():
    clear()
    print_logo()
    show_header()

    text = Prompt.ask("📝 Lotfan matne gozaresh ra vared konid")
    count = IntPrompt.ask("Chand bar ersal shavad?")

    with Live(console=console, refresh_per_second=10) as live:
        for i in range(1, count + 1):
            timestamp = now()
            msg = f"{i}. {text} - Gozaresh ersal shod ({timestamp})"
            live.update(Panel(f"[bright_yellow]{msg} 📨", width=60))
            save_to_file(f"[{timestamp}] Target: {TARGET_ID} | Gozaresh Ba Matn: {text} | Shomare {i}")
            time.sleep(0.3)

def translator_menu():
    clear()
    print_logo()
    show_header()
    panel = Panel(
        """[bold bright_yellow]Lotfan Yeki Az Zabanha Ra Entekhab Konid:[/bold bright_yellow]

[bold bright_green]1[/bold bright_green]. Arabic (عربی)
[bold bright_green]2[/bold bright_green]. English (انگلیسی)
[bold bright_green]3[/bold bright_green]. Russian (روسی)
[bold bright_green]4[/bold bright_green]. German (آلمانی)
""",
        title="[bright_green]Translator Menu[/bright_green]",
        border_style="bright_green",
        width=60,
    )
    console.print(panel, justify="center")

    lang_choice = Prompt.ask("[bold bright_green]Shomare Zaban Ra Vared Konid[/bold bright_green]", choices=["1", "2", "3", "4"])

    languages = {
        "1": "ar",
        "2": "en",
        "3": "ru",
        "4": "de"
    }

    target_lang = languages[lang_choice]
    text = Prompt.ask("Matn ra vared konid")

    try:
        translated_text = GoogleTranslator(source='auto', target=target_lang).translate(text)
        console.print(Panel(f"[bold bright_green]Matn tarjomeye shode:[/bold bright_green]\n\n{translated_text}", title="Natije Tarjome", border_style="bright_green"))
    except Exception as e:
        console.print(f"[bold bright_red]Error dar tarjome matn: {e}[/bold bright_red]")

    console.input("\n[bold bright_cyan]Baraye bazgasht be menu Enter bezan...[/bold bright_cyan]")

def run():
    ask_target_id()
    while True:
        choice = main_menu()

        if choice == "1":
            report_empty()
            console.input("\n[bold bright_cyan]Baraye bazgasht be menu Enter bezan...[/bold bright_cyan]")
        elif choice == "2":
            report_with_text()
            console.input("\n[bold bright_cyan]Baraye bazgasht be menu Enter bezan...[/bold bright_cyan]")
        elif choice == "3":
            translator_menu()
        elif choice == "0":
            console.print("\n[bold bright_red]Khorooj az barname...[/bold bright_red] ❌")
            break

if __name__ == "__main__":
    run()