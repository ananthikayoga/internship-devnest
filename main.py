"""
Command-line interface for TaskFlow Pro
Main user-facing application
"""

import sys
from typing import Optional
from datetime import datetime
from task_manager import TaskManager
from utils import Formatter, Colors, Validator


class TaskFlowCLI:
    """CLI interface for TaskFlow Pro"""

    def __init__(self):
        self.manager = TaskManager("tasks.json")
        self.running = True

    def display_welcome(self) -> None:
        """Display welcome screen"""
        Formatter.clear_screen()
        Formatter.print_header("🚀 TASKFLOW PRO - Smart Productivity Manager", Colors.BRIGHT_CYAN)
        print(f"{Colors.BRIGHT_CYAN}Welcome to TaskFlow Pro!{Colors.RESET}")
        print(f"Organize your tasks, boost your productivity!\n")

    def display_main_menu(self) -> None:
        """Display main menu"""
        stats = self.manager.get_statistics_summary()
        
        print(f"\n{Colors.BRIGHT_GREEN}📊 QUICK STATS:{Colors.RESET}")
        print(f"  Total: {stats['total']} | "
              f"Completed: {stats['completed']} | "
              f"Pending: {stats['pending']} | "
              f"Overdue: {stats['overdue']} | "
              f"Productivity: {stats['productivity']}%")
        
        Formatter.print_subheader("MAIN MENU", Colors.BRIGHT_BLUE)
        print("""
  1️⃣  Add New Task
  2️⃣  View All Tasks
  3️⃣  View Active Tasks
  4️⃣  View Completed Tasks
  5️⃣  Search/Filter Tasks
  6️⃣  Edit Task
  7️⃣  Mark Task Complete
  8️⃣  Mark Task Incomplete
  9️⃣  Delete Task
  
  📊 Analytics & Reports
  A️⃣  View Analytics Report
  B️⃣  View Daily Summary
  C️⃣  View Weekly Summary
  D️⃣  View Overdue Tasks
  E️⃣  View Due Soon Tasks
  
  ❌ Exit
        """)

    def add_task(self) -> None:
        """Add new task"""
        Formatter.print_subheader("ADD NEW TASK", Colors.BRIGHT_GREEN)

        # Get title
        while True:
            title = Formatter.get_input("Task Title: ")
            is_valid, result = Validator.validate_title(title)
            if is_valid:
                title = result
                break
            Formatter.print_error(result)

        # Get description
        description = Formatter.get_input("Description (optional): ")
        is_valid, description = Validator.validate_description(description)

        # Get priority
        while True:
            priority = Formatter.get_input("Priority (HIGH/MEDIUM/LOW) [MEDIUM]: ").upper().strip()
            if not priority:
                priority = "MEDIUM"
            is_valid, priority = Validator.validate_priority(priority)
            if is_valid:
                break
            Formatter.print_error(priority)

        # Get due date
        due_date = None
        if Formatter.get_yes_no("Set due date?"):
            while True:
                due_date = Formatter.get_input("Due Date (YYYY-MM-DD): ")
                is_valid, result = Validator.validate_date(due_date)
                if is_valid:
                    due_date = result
                    break
                Formatter.print_error(result)

        # Get category
        category = Formatter.get_input("Category (optional) [General]: ").strip()
        if not category:
            category = "General"
        is_valid, result = Validator.validate_category(category)
        if is_valid:
            category = result
        else:
            Formatter.print_error(result)
            category = "General"

        # Add task
        task = self.manager.add_task(title, description, priority, due_date, category)
        Formatter.print_success(f"Task added successfully! ID: {task.id}")

    def view_tasks(self, filter_type: str = "all") -> None:
        """View tasks"""
        if filter_type == "all":
            tasks = self.manager.get_all_tasks()
            Formatter.print_subheader("ALL TASKS", Colors.BRIGHT_BLUE)
        elif filter_type == "active":
            tasks = self.manager.get_active_tasks()
            Formatter.print_subheader("ACTIVE TASKS", Colors.BRIGHT_YELLOW)
        elif filter_type == "completed":
            tasks = self.manager.get_completed_tasks()
            Formatter.print_subheader("COMPLETED TASKS", Colors.BRIGHT_GREEN)
        else:
            tasks = self.manager.get_all_tasks()

        if not tasks:
            Formatter.print_info("No tasks found.")
            return

        for index, task in enumerate(tasks, 1):
            Formatter.print_task(task, index)

    def search_filter_tasks(self) -> None:
        """Search and filter tasks"""
        Formatter.print_subheader("SEARCH/FILTER TASKS", Colors.BRIGHT_BLUE)
        
        print("\n1. Search by keyword")
        print("2. Filter by priority")
        print("3. Filter by category")
        print("4. Filter by status")
        
        choice = Formatter.get_input("Select option (1-4): ").strip()

        if choice == "1":
            query = Formatter.get_input("Search query: ")
            tasks = self.manager.search_tasks(query)
            if tasks:
                print(f"\n{Colors.BRIGHT_GREEN}Found {len(tasks)} task(s):{Colors.RESET}")
                for index, task in enumerate(tasks, 1):
                    Formatter.print_task(task, index)
            else:
                Formatter.print_info("No tasks matching your search.")

        elif choice == "2":
            priority = Formatter.get_input("Priority (HIGH/MEDIUM/LOW): ").upper()
            is_valid, priority = Validator.validate_priority(priority)
            if is_valid:
                tasks = self.manager.get_tasks_by_priority(priority)
                print(f"\n{Colors.BRIGHT_GREEN}{priority} Priority Tasks:{Colors.RESET}")
                for index, task in enumerate(tasks, 1):
                    Formatter.print_task(task, index)
            else:
                Formatter.print_error(priority)

        elif choice == "3":
            category = Formatter.get_input("Category: ")
            tasks = self.manager.get_tasks_by_category(category)
            if tasks:
                print(f"\n{Colors.BRIGHT_GREEN}Tasks in {category}:{Colors.RESET}")
                for index, task in enumerate(tasks, 1):
                    Formatter.print_task(task, index)
            else:
                Formatter.print_info(f"No tasks in category '{category}'.")

        elif choice == "4":
            print("1. Completed tasks")
            print("2. Pending tasks")
            status_choice = Formatter.get_input("Select (1-2): ")
            if status_choice == "1":
                tasks = self.manager.get_completed_tasks()
                print(f"\n{Colors.BRIGHT_GREEN}Completed Tasks:{Colors.RESET}")
            else:
                tasks = self.manager.get_active_tasks()
                print(f"\n{Colors.BRIGHT_YELLOW}Pending Tasks:{Colors.RESET}")
            
            for index, task in enumerate(tasks, 1):
                Formatter.print_task(task, index)

    def edit_task(self) -> None:
        """Edit task"""
        Formatter.print_subheader("EDIT TASK", Colors.BRIGHT_BLUE)
        
        tasks = self.manager.get_all_tasks()
        if not tasks:
            Formatter.print_info("No tasks available to edit.")
            return
        
        for index, task in enumerate(tasks, 1):
            Formatter.print_task(task, index)
        
        try:
            selection = Formatter.get_input("\nSelect task number to edit: ").strip()
            index = int(selection)
            
            if not (1 <= index <= len(tasks)):
                Formatter.print_error(f"Please enter a number between 1 and {len(tasks)}")
                return
            
            task = tasks[index - 1]
            task_id = task.id
        except ValueError:
            Formatter.print_error("Invalid input. Please enter a task number.")
            return

        print(f"\n{Colors.BRIGHT_GREEN}Current Task:{Colors.RESET}")
        Formatter.print_task(task)

        print("\n1. Edit title")
        print("2. Edit description")
        print("3. Edit priority")
        print("4. Edit due date")
        print("5. Edit category")

        choice = Formatter.get_input("Select field to edit (1-5): ").strip()

        if choice == "1":
            new_title = Formatter.get_input("New title: ")
            is_valid, new_title = Validator.validate_title(new_title)
            if is_valid:
                self.manager.update_task(task_id, title=new_title)
                Formatter.print_success("Task updated!")
            else:
                Formatter.print_error(new_title)

        elif choice == "2":
            new_desc = Formatter.get_input("New description: ")
            is_valid, new_desc = Validator.validate_description(new_desc)
            if is_valid:
                self.manager.update_task(task_id, description=new_desc)
                Formatter.print_success("Task updated!")
            else:
                Formatter.print_error(new_desc)

        elif choice == "3":
            priority = Formatter.get_input("New priority (HIGH/MEDIUM/LOW): ").upper()
            is_valid, priority = Validator.validate_priority(priority)
            if is_valid:
                self.manager.update_task(task_id, priority=priority)
                Formatter.print_success("Task updated!")
            else:
                Formatter.print_error(priority)

        elif choice == "4":
            due_date = Formatter.get_input("New due date (YYYY-MM-DD or leave empty): ").strip()
            if due_date:
                is_valid, due_date = Validator.validate_date(due_date)
                if is_valid:
                    self.manager.update_task(task_id, due_date=due_date)
                    Formatter.print_success("Task updated!")
                else:
                    Formatter.print_error(due_date)
            else:
                self.manager.update_task(task_id, due_date=None)
                Formatter.print_success("Due date removed!")

        elif choice == "5":
            category = Formatter.get_input("New category: ")
            is_valid, category = Validator.validate_category(category)
            if is_valid:
                self.manager.update_task(task_id, category=category)
                Formatter.print_success("Task updated!")
            else:
                Formatter.print_error(category)

    def mark_completed(self) -> None:
        """Mark task as completed"""
        Formatter.print_subheader("MARK TASK COMPLETE", Colors.BRIGHT_GREEN)
        
        tasks = self.manager.get_active_tasks()
        if not tasks:
            Formatter.print_info("No active tasks to complete.")
            return
        
        for index, task in enumerate(tasks, 1):
            Formatter.print_task(task, index)
        
        try:
            selection = Formatter.get_input("\nSelect task number to mark complete: ").strip()
            index = int(selection)
            
            if 1 <= index <= len(tasks):
                task_id = tasks[index - 1].id
                if self.manager.mark_completed(task_id):
                    Formatter.print_success("Task marked as completed!")
                else:
                    Formatter.print_error("Task not found.")
            else:
                Formatter.print_error(f"Please enter a number between 1 and {len(tasks)}")
        except ValueError:
            Formatter.print_error("Invalid input. Please enter a task number.")

    def mark_incomplete(self) -> None:
        """Mark task as incomplete"""
        Formatter.print_subheader("MARK TASK INCOMPLETE", Colors.BRIGHT_YELLOW)
        
        tasks = self.manager.get_completed_tasks()
        if not tasks:
            Formatter.print_info("No completed tasks to reopen.")
            return
        
        for index, task in enumerate(tasks, 1):
            Formatter.print_task(task, index)
        
        try:
            selection = Formatter.get_input("\nSelect task number to mark incomplete: ").strip()
            index = int(selection)
            
            if 1 <= index <= len(tasks):
                task_id = tasks[index - 1].id
                if self.manager.mark_incomplete(task_id):
                    Formatter.print_success("Task marked as incomplete!")
                else:
                    Formatter.print_error("Task not found.")
            else:
                Formatter.print_error(f"Please enter a number between 1 and {len(tasks)}")
        except ValueError:
            Formatter.print_error("Invalid input. Please enter a task number.")

    def delete_task(self) -> None:
        """Delete task"""
        Formatter.print_subheader("DELETE TASK", Colors.BRIGHT_RED)
        
        tasks = self.manager.get_all_tasks()
        if not tasks:
            Formatter.print_info("No tasks available to delete.")
            return
        
        for index, task in enumerate(tasks, 1):
            Formatter.print_task(task, index)
        
        try:
            selection = Formatter.get_input("\nSelect task number to delete: ").strip()
            index = int(selection)
            
            if not (1 <= index <= len(tasks)):
                Formatter.print_error(f"Please enter a number between 1 and {len(tasks)}")
                return
            
            task_id = tasks[index - 1].id
        except ValueError:
            Formatter.print_error("Invalid input. Please enter a task number.")
            return

        if Formatter.get_yes_no("Are you sure you want to delete this task?"):
            if self.manager.delete_task(task_id):
                Formatter.print_success("Task deleted!")
            else:
                Formatter.print_error("Task not found.")
        else:
            Formatter.print_info("Deletion cancelled.")

    def view_analytics(self) -> None:
        """View analytics report"""
        analytics = self.manager.get_analytics()
        print(analytics.generate_analytics_report())

    def view_overdue_tasks(self) -> None:
        """View overdue tasks"""
        Formatter.print_subheader("OVERDUE TASKS", Colors.BRIGHT_RED)
        
        overdue = self.manager.get_overdue_tasks()
        if overdue:
            for index, task in enumerate(overdue, 1):
                Formatter.print_task(task, index)
        else:
            Formatter.print_success("No overdue tasks!")

    def view_due_soon(self) -> None:
        """View due soon tasks"""
        Formatter.print_subheader("TASKS DUE SOON (Next 7 Days)", Colors.BRIGHT_YELLOW)
        
        upcoming = self.manager.get_due_soon_tasks()
        if upcoming:
            for index, task in enumerate(upcoming, 1):
                Formatter.print_task(task, index)
        else:
            Formatter.print_info("No upcoming tasks.")

    def run(self) -> None:
        """Run the CLI application"""
        self.display_welcome()

        while self.running:
            try:
                self.display_main_menu()
                choice = Formatter.get_input("Select an option: ").strip().upper()

                if choice == "1":
                    self.add_task()
                elif choice == "2":
                    self.view_tasks("all")
                elif choice == "3":
                    self.view_tasks("active")
                elif choice == "4":
                    self.view_tasks("completed")
                elif choice == "5":
                    self.search_filter_tasks()
                elif choice == "6":
                    self.edit_task()
                elif choice == "7":
                    self.mark_completed()
                elif choice == "8":
                    self.mark_incomplete()
                elif choice == "9":
                    self.delete_task()
                elif choice == "A":
                    self.view_analytics()
                elif choice == "B":
                    analytics = self.manager.get_analytics()
                    daily = analytics.get_daily_summary()
                    Formatter.print_subheader("TODAY'S SUMMARY", Colors.BRIGHT_CYAN)
                    print(f"Date: {daily['date']}")
                    print(f"Tasks Created: {daily['total_created']}")
                    print(f"Completed: {daily['completed_today']}")
                    print(f"Pending: {daily['pending_today']}")
                    print(f"Due Today: {daily['due_today']}")
                elif choice == "C":
                    analytics = self.manager.get_analytics()
                    weekly = analytics.get_weekly_summary()
                    Formatter.print_subheader("WEEKLY SUMMARY", Colors.BRIGHT_CYAN)
                    print(f"Week Starting: {weekly['week_start']}")
                    print(f"Total Created: {weekly['total_created']}")
                    print(f"Completed: {weekly['completed']}")
                    print(f"Pending: {weekly['pending']}")
                    print(f"Avg Daily Completion: {weekly['average_daily_completion']}")
                    print(f"Weekly Productivity: {weekly['productivity_percentage']}%")
                elif choice == "D":
                    self.view_overdue_tasks()
                elif choice == "E":
                    self.view_due_soon()
                elif choice == "EXIT" or choice == "X":
                    Formatter.print_success("Thank you for using TaskFlow Pro! Goodbye!")
                    self.running = False
                else:
                    Formatter.print_error("Invalid option. Please try again.")

                if self.running:
                    input(f"\n{Colors.CYAN}Press Enter to continue...{Colors.RESET}")

            except KeyboardInterrupt:
                print(f"\n{Colors.BRIGHT_YELLOW}Interrupted by user.{Colors.RESET}")
                if Formatter.get_yes_no("Exit TaskFlow Pro?"):
                    Formatter.print_success("Thank you for using TaskFlow Pro! Goodbye!")
                    self.running = False
            except Exception as e:
                Formatter.print_error(f"An error occurred: {e}")


def main():
    """Main entry point"""
    try:
        app = TaskFlowCLI()
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
