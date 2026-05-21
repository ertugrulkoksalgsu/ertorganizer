import os
import sys
import shlex
import time
from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from rich.align import Align
from rich import print as rprint
from organizer import organize_folder
from converter import convert_file

console = Console()
NL = chr(10)

class SkillCompleter(Completer):
    def __init__(self):
        self.skills = [
            ('/organize', 'Mevcut klasördeki dosyaları türüne göre ayırır (Resimler, Belgeler vs.)'),
            ('/convert', 'Belirtilen dosyanın formatını dönüştürür (Örn: /convert a.png a.jpg)'),
            ('/cd', 'Çalışma dizinini başka bir klasöre değiştirir'),
            ('/pwd', 'Şu an işlem yapılan klasörün tam yolunu gösterir'),
            ('/help', 'Tüm komutların detaylı listesini görüntüler'),
            ('/exit', 'ErtOrganizer sisteminden çıkış yapar'),
            ('/quit', 'ErtOrganizer sisteminden çıkış yapar')
        ]

    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor(WORD=True)
        if document.text.startswith('/'):
            for skill, description in self.skills:
                if skill.startswith(word):
                    yield Completion(
                        skill,
                        start_position=-len(word),
                        display=skill,
                        display_meta=description
                    )

def print_welcome():
    ascii_art = [
        "  ______      _    ____                        _              ",
        " |  ____|    | |  / __ \\                      (_)             ",
        " | |__   _ __| |_| |  | |_ __ __ _  __ _ _ __  _ _______ _ __ ",
        " |  __| | '__| __| |  | | '__/ _` |/ _` | '_ \\| |_  / _ \\ '__|",
        " | |____| |  | |_| |__| | | | (_| | (_| | | | | |/ /  __/ |   ",
        " |______|_|   \\__|\\____/|_|  \\__, |\\__,_|_| |_|_/___\\___|_|   ",
        "                              __/ |                           ",
        "                             |___/                            "
    ]
    
    welcome_text = Text(justify="left")
    panel = Panel(Align.center(welcome_text), title="[bold blue]ErtOrganizer Sistemi[/bold blue]", border_style="blue", expand=False)
    
    with Live(panel, refresh_per_second=20) as live:
        for line in ascii_art:
            welcome_text.append(line, style="bold cyan")
            welcome_text.append(NL)
            live.update(Panel(Align.center(welcome_text), title="[bold blue]ErtOrganizer Sistemi[/bold blue]", border_style="blue", expand=False), refresh=True)
            time.sleep(0.05)
            
        time.sleep(0.2)
        
        welcome_text.append(f"{NL}🚀 Sistem Başlatıldı ve Kullanıma Hazır.{NL}{NL}", style="bold yellow")
        live.update(Panel(Align.center(welcome_text), title="[bold blue]ErtOrganizer Sistemi[/bold blue]", border_style="blue", expand=False), refresh=True)
        time.sleep(0.3)
        
        welcome_text.append(f"Dosya organizasyonu, toplu taşıma ve format dönüşümleri artık parmaklarınızın ucunda.{NL}", style="italic white")
        live.update(Panel(Align.center(welcome_text), title="[bold blue]ErtOrganizer Sistemi[/bold blue]", border_style="blue", expand=False), refresh=True)
        time.sleep(0.3)
        
        welcome_text.append("Akıllı menüyü açmak ve komutları görüntülemek için klavyeden ", style="dim white")
        welcome_text.append("/", style="bold magenta")
        welcome_text.append(f" yazın.{NL}{NL}", style="dim white")
        live.update(Panel(Align.center(welcome_text), title="[bold blue]ErtOrganizer Sistemi[/bold blue]", border_style="blue", expand=False), refresh=True)
        time.sleep(0.3)
        
        welcome_text.append(f"📍 Hedef Konum: {os.getcwd()}{NL}", style="green")
        live.update(Panel(Align.center(welcome_text), title="[bold blue]ErtOrganizer Sistemi[/bold blue]", border_style="blue", expand=False), refresh=True)

def main():
    print_welcome()

    skill_completer = SkillCompleter()

    style = Style.from_dict({
        'prompt': '#00dddd bold',
        'completion-menu.completion': 'bg:#008888 #ffffff',
        'completion-menu.completion.current': 'bg:#00dddd #000000 bold',
        'scrollbar.background': 'bg:#88aaaa',
        'scrollbar.button': 'bg:#222222',
    })

    session = PromptSession(completer=skill_completer, style=style)

    while True:
        try:
            cwd_name = os.path.basename(os.getcwd())
            if not cwd_name:
                cwd_name = "/"
                
            prompt_text = f"{NL}[{cwd_name}] ❯ "
            user_input = session.prompt(prompt_text).strip()
            
            if not user_input:
                continue

            try:
                args = shlex.split(user_input)
            except ValueError as e:
                console.print(f"[red]Hata: Geçersiz komut formatı ({e})[/red]")
                continue

            command = args[0].lower()

            if command in ('/exit', '/quit', 'exit', 'quit'):
                console.print("[yellow]ErtOrganizer kapatılıyor. İyi çalışmalar dileriz![/yellow]")
                break
                
            elif command == '/help':
                console.print(f"{NL}[bold cyan]Kullanılabilir Skiller:[/bold cyan]")
                console.print("  [magenta]/organize[/magenta] [klasör_yolu]   - Dosyaları uzantılarına göre ayırır.")
                console.print("  [magenta]/convert[/magenta] <girdi> <hedef>  - Dosya formatını dönüştürür (Örn: resim.png resim.jpg).")
                console.print("  [magenta]/pwd[/magenta]                      - Mevcut çalışma dizinini gösterir.")
                console.print("  [magenta]/cd[/magenta] <klasör_yolu>         - Çalışma dizinini değiştirir.")
                console.print("  [magenta]/help[/magenta]                     - Bu yardım menüsünü gösterir.")
                console.print(f"  [magenta]/exit, /quit[/magenta]              - Çıkış yapar.{NL}")
                
            elif command == '/pwd':
                console.print(f"[green]Mevcut konum:[/green] {os.getcwd()}")
                
            elif command == '/cd':
                if len(args) > 1:
                    target_dir = os.path.expanduser(args[1])
                    try:
                        os.chdir(target_dir)
                        console.print(f"[green]Konum değiştirildi:[/green] {os.getcwd()}")
                    except FileNotFoundError:
                        console.print(f"[red]Hata: Klasör bulunamadı '{target_dir}'[/red]")
                    except Exception as e:
                        console.print(f"[red]Hata: {e}[/red]")
                else:
                    console.print("[yellow]Kullanım: /cd <klasör_yolu>[/yellow]")
                    
            elif command == '/organize':
                target_path = os.getcwd()
                if len(args) > 1:
                    target_path = os.path.expanduser(args[1])
                console.print(f"[cyan]✨ Organizasyon işlemi başlatıldı: {target_path}[/cyan]")
                organize_folder(target_path)
                
            elif command == '/convert':
                if len(args) >= 3:
                    input_file = os.path.expanduser(args[1])
                    output_file = os.path.expanduser(args[2])
                    
                    if not os.path.isabs(input_file):
                        input_file = os.path.join(os.getcwd(), input_file)
                    if not os.path.isabs(output_file):
                        output_file = os.path.join(os.getcwd(), output_file)
                        
                    console.print("[cyan]🔄 Dönüştürülüyor...[/cyan]")
                    convert_file(input_file, output_file)
                else:
                    console.print("[yellow]Kullanım: /convert <girdi_dosyası> <hedef_dosya>[/yellow]")
                    
            else:
                if command.startswith('/'):
                    console.print(f"[red]Bilinmeyen yetenek '{command}'. Yetenekleri listelemek için klavyeden '/' tuşuna basın.[/red]")
                else:
                    console.print(f"[red]ErtOrganizer'da tüm komutlar '/' ile başlar (Örn: /organize).[/red]")

        except KeyboardInterrupt:
            continue
        except EOFError:
            console.print(f"{NL}[yellow]ErtOrganizer kapatılıyor...[/yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]Beklenmeyen bir hata oluştu: {e}[/bold red]")

if __name__ == "__main__":
    main()
