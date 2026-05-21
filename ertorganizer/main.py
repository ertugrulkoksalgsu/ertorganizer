import os
import shlex
import time
from collections import defaultdict

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.styles import Style
from rich.align import Align
from rich.console import Console
from rich.live import Live
from rich.panel import Panel
from rich.prompt import Confirm
from rich.table import Table
from rich.text import Text

from . import __version__
from . import system as ertsystem
from .converters import convert_file, supported_pairs
from .organizer import organize_folder

console = Console()
NL = chr(10)


SKILLS = [
    ('/organize', 'Mevcut klasördeki dosyaları türüne göre ayırır (Resimler, Belgeler vs.)'),
    ('/convert', 'Belirtilen dosyanın formatını dönüştürür (Örn: /convert a.png a.jpg)'),
    ('/formats', 'Desteklenen tüm dönüşüm formatlarını tablo halinde gösterir'),
    ('/doctor', 'Sistem ve Python bağımlılıklarını tarar, eksikleri raporlar'),
    ('/install', 'Eksik bağımlılığı otomatik kurar (örn: /install libreoffice ya da /install all)'),
    ('/cd', 'Çalışma dizinini başka bir klasöre değiştirir'),
    ('/pwd', 'Şu an işlem yapılan klasörün tam yolunu gösterir'),
    ('/help', 'Tüm komutların detaylı listesini görüntüler'),
    ('/version', 'ErtOrganizer sürümünü gösterir'),
    ('/exit', 'ErtOrganizer sisteminden çıkış yapar'),
    ('/quit', 'ErtOrganizer sisteminden çıkış yapar'),
]


class SkillCompleter(Completer):
    def get_completions(self, document, complete_event):
        word = document.get_word_before_cursor(WORD=True)
        if not document.text.startswith('/'):
            return
        for skill, description in SKILLS:
            if skill.startswith(word):
                yield Completion(
                    skill,
                    start_position=-len(word),
                    display=skill,
                    display_meta=description,
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
        "                             |___/                            ",
    ]

    welcome_text = Text(justify="left")
    title = f"[bold blue]ErtOrganizer v{__version__}[/bold blue]"
    panel = Panel(Align.center(welcome_text), title=title, border_style="blue", expand=False)

    with Live(panel, refresh_per_second=20) as live:
        for line in ascii_art:
            welcome_text.append(line, style="bold cyan")
            welcome_text.append(NL)
            live.update(Panel(Align.center(welcome_text), title=title, border_style="blue", expand=False), refresh=True)
            time.sleep(0.04)

        time.sleep(0.15)
        welcome_text.append(f"{NL}🚀 Sistem Başlatıldı ve Kullanıma Hazır.{NL}{NL}", style="bold yellow")
        live.update(Panel(Align.center(welcome_text), title=title, border_style="blue", expand=False), refresh=True)
        time.sleep(0.2)

        welcome_text.append(f"Dosya organizasyonu, toplu taşıma ve format dönüşümleri parmaklarınızın ucunda.{NL}", style="italic white")
        live.update(Panel(Align.center(welcome_text), title=title, border_style="blue", expand=False), refresh=True)
        time.sleep(0.2)

        welcome_text.append("Komutları görmek için ", style="dim white")
        welcome_text.append("/", style="bold magenta")
        welcome_text.append(" yazın · Format listesi için ", style="dim white")
        welcome_text.append("/formats", style="bold magenta")
        welcome_text.append(f"{NL}{NL}", style="dim white")
        live.update(Panel(Align.center(welcome_text), title=title, border_style="blue", expand=False), refresh=True)
        time.sleep(0.2)

        welcome_text.append(f"📍 Hedef Konum: {os.getcwd()}{NL}", style="green")
        live.update(Panel(Align.center(welcome_text), title=title, border_style="blue", expand=False), refresh=True)


def print_help():
    console.print(f"{NL}[bold cyan]Kullanılabilir Komutlar:[/bold cyan]")
    console.print("  [magenta]/organize[/magenta] [klasör_yolu]   - Dosyaları uzantılarına göre ayırır.")
    console.print("  [magenta]/convert[/magenta] <girdi> <hedef>  - Dosya formatını dönüştürür (Örn: rapor.docx rapor.pdf).")
    console.print("  [magenta]/formats[/magenta]                  - Desteklenen tüm dönüşüm formatlarını listeler.")
    console.print("  [magenta]/doctor[/magenta]                   - Sistem ve Python bağımlılıklarını tarar.")
    console.print("  [magenta]/install[/magenta] <ad|all>         - Eksik bağımlılığı otomatik kurar.")
    console.print("  [magenta]/pwd[/magenta]                      - Mevcut çalışma dizinini gösterir.")
    console.print("  [magenta]/cd[/magenta] <klasör_yolu>         - Çalışma dizinini değiştirir.")
    console.print("  [magenta]/version[/magenta]                  - ErtOrganizer sürümünü gösterir.")
    console.print("  [magenta]/help[/magenta]                     - Bu yardım menüsünü gösterir.")
    console.print(f"  [magenta]/exit, /quit[/magenta]              - Çıkış yapar.{NL}")


def print_doctor():
    table = Table(
        title="[bold]🩺 Sistem Sağlık Kontrolü[/bold]",
        header_style="bold blue",
        show_lines=False,
    )
    table.add_column("Bağımlılık", style="bold")
    table.add_column("Tip", justify="center")
    table.add_column("Durum", justify="center")
    table.add_column("İşlev")
    table.add_column("Kurulum", style="dim")

    for req, ok in ertsystem.status():
        kind_label = "🐍 Python" if req.kind == 'python' else "🔧 Sistem"
        status_label = "[green]✓ Var[/green]" if ok else "[red]✗ Yok[/red]"
        install_hint = "—" if ok else f"/install {req.key}"
        table.add_row(req.display, kind_label, status_label, req.purpose, install_hint)

    console.print(table)
    missing_count = sum(1 for _, ok in ertsystem.status() if not ok)
    if missing_count:
        console.print(
            f"[yellow]{missing_count} bağımlılık eksik.[/yellow] "
            "Hepsini kurmak için: [magenta]/install all[/magenta]"
        )
    else:
        console.print("[green]🎉 Tüm bağımlılıklar hazır![/green]")
    console.print()


def _do_install_one(req):
    console.print(f"[cyan]➤ {req.display} kuruluyor...[/cyan]")
    if req.notes:
        console.print(f"  [dim]Not: {req.notes}[/dim]")
    ok, msg = ertsystem.install_requirement(req)
    if ok:
        console.print(f"  [green]✓[/green] {msg}")
    else:
        console.print(f"  [red]✗[/red] {msg}")
    return ok


def run_install(args):
    if len(args) < 2:
        console.print("[yellow]Kullanım: /install <ad>  veya  /install all[/yellow]")
        console.print("[dim]Mevcut adlar için: [magenta]/doctor[/magenta][/dim]")
        return

    target = args[1].lower()

    if target == 'all':
        missing = [r for r, ok in ertsystem.status() if not ok]
        if not missing:
            console.print("[green]🎉 Zaten tüm bağımlılıklar kurulu.[/green]")
            return
        console.print(f"[yellow]{len(missing)} eksik bağımlılık tespit edildi:[/yellow]")
        for r in missing:
            note = f" — [dim]{r.notes}[/dim]" if r.notes else ""
            console.print(f"  • {r.display} ({r.purpose}){note}")
        if not Confirm.ask("\nHepsini şimdi kurmak istiyor musun?", default=True):
            return
        success = 0
        for r in missing:
            if _do_install_one(r):
                success += 1
        console.print(f"\n[bold]{success}/{len(missing)}[/bold] bağımlılık kuruldu.")
        return

    req = ertsystem.find(target)
    if req is None:
        console.print(f"[red]Bilinmeyen bağımlılık: '{target}'[/red]")
        console.print("[dim]Mevcut adlar için: [magenta]/doctor[/magenta][/dim]")
        return

    if req.detect():
        console.print(f"[green]{req.display} zaten kurulu.[/green]")
        return

    console.print(f"[cyan]{req.display}[/cyan] — {req.purpose}")
    if req.kind == 'system':
        cmd = req.install_cmd.get(ertsystem.os_kind(), '(bu platform için tanımlı değil)')
        console.print(f"[dim]Çalıştırılacak komut: {cmd}[/dim]")
    if req.notes:
        console.print(f"[dim]Not: {req.notes}[/dim]")
    if not Confirm.ask("Devam edelim mi?", default=True):
        return
    _do_install_one(req)


def print_formats():
    grouped = defaultdict(list)
    for in_ext, out_ext, name in supported_pairs():
        grouped[name].append((in_ext, out_ext))

    console.print(f"{NL}[bold cyan]Desteklenen Dönüşümler:[/bold cyan]")
    for name in sorted(grouped):
        table = Table(title=f"[bold magenta]{name}[/bold magenta]", show_header=True, header_style="bold blue")
        table.add_column("Girdi")
        table.add_column("→", justify="center")
        table.add_column("Hedef")
        for in_ext, out_ext in sorted(set(grouped[name])):
            table.add_row(in_ext, "→", out_ext)
        console.print(table)
    console.print(
        "[dim]Bazı dönüşümler ek bağımlılık gerektirir (pdf2image, openpyxl, pypandoc, LibreOffice vb.). "
        "Eksik olduğunda /convert komutu nasıl kurulacağını söyler.[/dim]" + NL
    )


def _handle_missing_and_retry(input_file, output_file, missing):
    console.print("[yellow]⚠ Bu dönüşüm için eksik bağımlılık var:[/yellow]")
    for spec in missing:
        console.print(f"   • {ertsystem.describe_spec(spec)}")
    if not Confirm.ask("Şimdi kurmak ister misin?", default=True):
        console.print("[dim]Kurulum atlandı. İstediğinde /doctor ile durumu görebilir, /install ile kurabilirsin.[/dim]")
        return None
    installed_all = True
    for spec in missing:
        ok, msg = ertsystem.install_spec(spec, prefer_first=True)
        if ok:
            console.print(f"  [green]✓[/green] {msg}")
        else:
            console.print(f"  [red]✗[/red] {msg}")
            installed_all = False
    if not installed_all:
        console.print("[red]Bazı kurulumlar başarısız oldu, dönüşüm tekrar denenmiyor.[/red]")
        return None
    console.print("[cyan]🔄 Dönüşüm tekrar deneniyor...[/cyan]")
    return convert_file(input_file, output_file)


def run_convert(args):
    if len(args) < 3:
        console.print("[yellow]Kullanım: /convert <girdi_dosyası> <hedef_dosya>[/yellow]")
        return
    input_file = os.path.expanduser(args[1])
    output_file = os.path.expanduser(args[2])
    if not os.path.isabs(input_file):
        input_file = os.path.join(os.getcwd(), input_file)
    if not os.path.isabs(output_file):
        output_file = os.path.join(os.getcwd(), output_file)
    console.print("[cyan]🔄 Dönüştürülüyor...[/cyan]")
    result = convert_file(input_file, output_file)

    if not result.success and result.missing:
        retried = _handle_missing_and_retry(input_file, output_file, result.missing)
        if retried is not None:
            result = retried

    style = "green" if result.success else "red"
    console.print(f"[{style}]{result.message}[/{style}]")


def main():
    print_welcome()

    style = Style.from_dict({
        'prompt': '#00dddd bold',
        'completion-menu.completion': 'bg:#008888 #ffffff',
        'completion-menu.completion.current': 'bg:#00dddd #000000 bold',
        'scrollbar.background': 'bg:#88aaaa',
        'scrollbar.button': 'bg:#222222',
    })

    session = PromptSession(completer=SkillCompleter(), style=style)

    while True:
        try:
            cwd_name = os.path.basename(os.getcwd()) or "/"
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
                print_help()

            elif command == '/formats':
                print_formats()

            elif command == '/doctor':
                print_doctor()

            elif command == '/install':
                run_install(args)

            elif command == '/version':
                console.print(f"[cyan]ErtOrganizer v{__version__}[/cyan]")

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
                run_convert(args)

            else:
                if command.startswith('/'):
                    console.print(f"[red]Bilinmeyen yetenek '{command}'. Yetenekleri listelemek için klavyeden '/' tuşuna basın.[/red]")
                else:
                    console.print("[red]ErtOrganizer'da tüm komutlar '/' ile başlar (Örn: /organize).[/red]")

        except KeyboardInterrupt:
            continue
        except EOFError:
            console.print(f"{NL}[yellow]ErtOrganizer kapatılıyor...[/yellow]")
            break
        except Exception as e:
            console.print(f"[bold red]Beklenmeyen bir hata oluştu: {e}[/bold red]")


if __name__ == "__main__":
    main()
