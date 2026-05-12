"""
Utilities module for TaskFlow Pro
Provides color formatting and helper functions
"""

import os
import sys
from typing import Optional


class Colors:
    """ANSI color codes for terminal output"""
    # Reset
    RESET = '\033[0m'

    # Foreground Colors
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

    # Bright Colors
    BRIGHT_RED = '\033[91m'
    BRIGHT_GREEN = '\033[92m'
    BRIGHT_YELLOW = '\033[93m'
    BRIGHT_BLUE = '\033[94m'
    BRIGHT_MAGENTA = '\033[95m'
    BRIGHT_CYAN = '\033[96m'

    # Background Colors
    BG_RED = '\033[41m'
    BG_GREEN = '\033[42m'
    BG_YELLOW = '\033[43m'
    BG_BLUE = '\033[44m'

    # Styles
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    ITALIC = '\033[3m'

    @staticmethod
    def disable():
        """Disable colors on Windows if needed"""
        if sys.platform == 'win32':
            os.system('color')


class Formatter:
    """Output formatting utilities"""

    @staticmethod
    def clear_screen() -> None:
        """Clear the terminal screen"""
        os.system('clear' if os.name == 'posix' else 'cls')

    @staticmethod
    def print_header(text: str, color: str = Colors.BRIGHT_CYAN) -> None:
        """Print formatted header"""
        print(f"\n{color}{Colors.BOLD}{'=' * 60}{Colors.RESET}")
        print(f"{color}{Colors.BOLD}{text.center(60)}{Colors.RESET}")
        print(f"{color}{Colors.BOLD}{'=' * 60}{Colors.RESET}\n")

    @staticmethod
    def print_subheader(text: str, color: str = Colors.BRIGHT_BLUE) -> None:
        """Print formatted subheader"""
        print(f"\n{color}{Colors.BOLD}{text}{Colors.RESET}")
        print(f"{color}{'-' * len(text)}{Colors.RESET}")

    @staticmethod
    def print_success(text: str) -> None:
        """Print success message"""
        print(f"{Colors.BRIGHT_GREEN}✓ {text}{Colors.RESET}")

    @staticmethod
    def print_error(text: str) -> None:
        """Print error message"""
        print(f"{Colors.BRIGHT_RED}✗ {text}{Colors.RESET}")

    @staticmethod
    def print_warning(text: str) -> None:
        """Print warning message"""
        print(f"{Colors.BRIGHT_YELLOW}⚠ {text}{Colors.RESET}")

    @staticmethod
    def print_info(text: str) -> None:
        """Print info message"""
        print(f"{Colors.BRIGHT_BLUE}ℹ {text}{Colors.RESET}")

    @staticmethod
    def print_task(task_obj, index: int = None) -> None:
        """Print formatted task"""
        priority_color = {
            "HIGH": Colors.BRIGHT_RED,
            "MEDIUM": Colors.BRIGHT_YELLOW,
            "LOW": Colors.BRIGHT_GREEN
        }.get(task_obj.priority.name, Colors.WHITE)

        status_icon = "✓" if task_obj.completed else "○"
        status_color = Colors.BRIGHT_GREEN if task_obj.completed else Colors.WHITE

        index_str = f"[{index}] " if index is not None else ""
        print(f"{status_color}{status_icon}{Colors.RESET} {index_str}", end="")
        print(f"{Colors.BOLD}{task_obj.title}{Colors.RESET}", end="")
        print(f" | {priority_color}{task_obj.priority.name}{Colors.RESET}", end="")
        print(f" | {Colors.CYAN}{task_obj.category}{Colors.RESET}", end="")
        if task_obj.due_date:
            print(f" | 📅 {Colors.YELLOW}{task_obj.due_date}{Colors.RESET}", end="")
        print()
        if task_obj.description:
            print(f"  {Colors.WHITE}{task_obj.description}{Colors.RESET}")

    @staticmethod
    def print_table(headers: list, rows: list, colors: Optional[list] = None) -> None:
        """Print formatted table"""
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                col_widths[i] = max(col_widths[i], len(str(cell)))

        # Print header
        header_line = " | ".join(
            f"{Colors.BOLD}{Colors.BRIGHT_CYAN}{h:<{col_widths[i]}}{Colors.RESET}"
            for i, h in enumerate(headers)
        )
        print(header_line)
        print("-" * (len(header_line) - 20))  # Adjust for color codes

        # Print rows
        for row_idx, row in enumerate(rows):
            color = colors[row_idx] if colors and row_idx < len(colors) else Colors.WHITE
            row_line = " | ".join(
                f"{color}{str(cell):<{col_widths[i]}}{Colors.RESET}"
                for i, cell in enumerate(row)
            )
            print(row_line)

    @staticmethod
    def format_priority_bar(completed: int, total: int) -> str:
        """Create a progress bar"""
        if total == 0:
            return "N/A"
        percentage = (completed / total) * 100
        bar_length = 20
        filled = int(bar_length * completed / total)
        bar = "█" * filled + "░" * (bar_length - filled)

        if percentage >= 80:
            color = Colors.BRIGHT_GREEN
        elif percentage >= 50:
            color = Colors.BRIGHT_YELLOW
        else:
            color = Colors.BRIGHT_RED

        return f"{color}{bar} {percentage:.0f}%{Colors.RESET}"

    @staticmethod
    def get_input(prompt: str, color: str = Colors.BRIGHT_CYAN) -> str:
        """Get user input with colored prompt"""
        return input(f"{color}{Colors.BOLD}{prompt}{Colors.RESET} ")

    @staticmethod
    def get_yes_no(prompt: str) -> bool:
        """Get yes/no input from user"""
        while True:
            response = Formatter.get_input(f"{prompt} (y/n): ").lower().strip()
            if response in ('y', 'yes'):
                return True
            elif response in ('n', 'no'):
                return False
            else:
                Formatter.print_error("Please enter 'y' or 'n'")


class Validator:
    """Input validation utilities"""

    @staticmethod
    def validate_title(title: str) -> tuple[bool, str]:
        """Validate task title"""
        title = title.strip()
        if not title:
            return False, "Title cannot be empty"
        if len(title) > 200:
            return False, "Title is too long (max 200 characters)"
        return True, title

    @staticmethod
    def validate_date(date_str: str) -> tuple[bool, str]:
        """Validate date format (YYYY-MM-DD)"""
        from datetime import datetime
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True, date_str
        except ValueError:
            return False, "Invalid date format. Use YYYY-MM-DD"

    @staticmethod
    def validate_priority(priority_str: str) -> tuple[bool, str]:
        """Validate priority level"""
        valid_priorities = ['HIGH', 'MEDIUM', 'LOW']
        priority = priority_str.upper().strip()
        if priority in valid_priorities:
            return True, priority
        return False, f"Priority must be one of: {', '.join(valid_priorities)}"

    @staticmethod
    def validate_description(description: str) -> tuple[bool, str]:
        """Validate task description"""
        description = description.strip()
        if len(description) > 1000:
            return False, "Description is too long (max 1000 characters)"
        return True, description

    @staticmethod
    def validate_category(category: str) -> tuple[bool, str]:
        """Validate category"""
        category = category.strip()
        if not category:
            category = "General"
        if len(category) > 50:
            return False, "Category is too long (max 50 characters)"
        return True, category
