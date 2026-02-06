# display.py

import os
import sys
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from datetime import datetime, timezone, timedelta

from config import APP_TITLE

console = Console()


class Display:
    def __init__(self):
        self.cursor_hidden = False

    def clear(self):
        os.system("cls" if os.name == "nt" else "clear")

    def hide_cursor(self):
        if not self.cursor_hidden:
            sys.stdout.write("\033[?25l")
            sys.stdout.flush()
            self.cursor_hidden = True

    def show_cursor(self):
        if self.cursor_hidden:
            sys.stdout.write("\033[?25h")
            sys.stdout.flush()
            self.cursor_hidden = False

    @staticmethod
    def format_probability(p: float) -> str:
        return f"{round(p * 100)}%"
    
    @staticmethod
    def now_brazil():
        return datetime.now(timezone.utc) - timedelta(hours=3)

    @staticmethod
    def color_probability(p_up: float, p_down: float) -> tuple[str, str]:
        if p_up > p_down:
            return "green", "red"
        elif p_down > p_up:
            return "red", "green"
        else:
            return "white", "white"

    @staticmethod
    def color_volatility(label: str) -> str:
        if label == "LOW":
            return "green"
        elif label == "MEDIUM":
            return "yellow"
        return "red"

    @staticmethod
    def color_trend(trend: str) -> str:
        if trend == "UP":
            return "green"
        elif trend == "DOWN":
            return "red"
        return "yellow"
    
    def color_tech_change(self, change: float | None) -> str:
        if change is None:
            return "white"
        if change > 1.0:
            return "green"
        if change < -1.0:
            return "red"
        return "yellow"
    
    def renderLoadingInfo(self):
        self.clear()
        print("📡 Getting Bitcoin market info...")

    def render(self, current_price: float, window_data: dict):
        self.clear()

        header = Panel(
            Text(APP_TITLE, justify="center", style="bold cyan"),
            expand=False
        )
        console.print(header)
        
        last_update = self.now_brazil().strftime("%H:%M:%S (UTC-3)")

        console.print(
            f"[bold]Current Price:[/bold] ${current_price:,.2f}    "
            f"[bold]Last Update:[/bold] {last_update}\n"
        )

        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Period")
        table.add_column("Period Change")
        table.add_column("S&P Tech Δ")
        table.add_column("Trend")
        table.add_column("P(UP)")
        table.add_column("P(DOWN)")
        table.add_column("Volatility")

        for days in sorted(window_data.keys(), reverse=True):
            data = window_data[days]

            p_up = data["p_up"]
            p_down = data["p_down"]
            vol_label = data["volatility_label"]
            
            trend = data["trend"]
            trend_color = self.color_trend(trend)
            
            tech_change = data.get("tech_change_pct")
            tech_color = self.color_tech_change(
                tech_change * 100 if tech_change is not None else None
            )

            tech_text = (
                f"{tech_change:+.2%}"
                if tech_change is not None
                else "N/A"
            )

            up_color, down_color = self.color_probability(p_up, p_down)
            vol_color = self.color_volatility(vol_label)

            change_pct = data["change_pct"]
            price_color = "green" if change_pct >= 0 else "red"

            table.add_row(
                f"{days}d",
                f"[{price_color}]{change_pct:+.2%}[/{price_color}]",
                f"[{tech_color}]{tech_text}[/{tech_color}]",
                f"[{trend_color}]{trend}[/{trend_color}]",
                f"[{up_color}]{self.format_probability(p_up)}[/{up_color}]",
                f"[{down_color}]{self.format_probability(p_down)}[/{down_color}]",
                f"[{vol_color}]{vol_label}[/{vol_color}]"
            )

        console.print(table)
        console.print("\nNext update in: 10 minutes")