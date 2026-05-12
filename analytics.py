"""
Analytics module for TaskFlow Pro
Provides productivity insights and statistics
"""

from datetime import datetime, timedelta
from typing import List, Dict, Any
from task import Task, TaskStatus, Priority


class ProductivityAnalytics:
    """Analyzes task completion and productivity metrics"""

    def __init__(self, tasks: List[Task]):
        self.tasks = tasks

    def get_completed_count(self) -> int:
        """Get total number of completed tasks"""
        return len([t for t in self.tasks if t.completed])

    def get_pending_count(self) -> int:
        """Get total number of pending tasks"""
        return len([t for t in self.tasks if not t.completed and t.get_status() == TaskStatus.PENDING])

    def get_overdue_count(self) -> int:
        """Get total number of overdue tasks"""
        return len([t for t in self.tasks if t.get_status() == TaskStatus.OVERDUE])

    def get_total_tasks(self) -> int:
        """Get total number of tasks"""
        return len(self.tasks)

    def get_productivity_percentage(self) -> float:
        """Calculate productivity percentage"""
        total = self.get_total_tasks()
        if total == 0:
            return 0.0
        completed = self.get_completed_count()
        return round((completed / total) * 100, 2)

    def get_tasks_by_priority(self) -> Dict[str, int]:
        """Count tasks by priority level"""
        result = {"HIGH": 0, "MEDIUM": 0, "LOW": 0}
        for task in self.tasks:
            if not task.completed:
                result[task.priority.name] += 1
        return result

    def get_tasks_by_category(self) -> Dict[str, int]:
        """Count tasks by category"""
        result = {}
        for task in self.tasks:
            if not task.completed:
                category = task.category
                result[category] = result.get(category, 0) + 1
        return result

    def get_daily_summary(self) -> Dict[str, Any]:
        """Get summary for today's tasks"""
        today = datetime.now().strftime("%Y-%m-%d")
        today_tasks = [t for t in self.tasks if t.created_date.startswith(today)]
        
        return {
            "date": today,
            "total_created": len(today_tasks),
            "completed_today": len([t for t in today_tasks if t.completed]),
            "pending_today": len([t for t in today_tasks if not t.completed]),
            "due_today": len([t for t in self.tasks if t.due_date == today and not t.completed])
        }

    def get_weekly_summary(self) -> Dict[str, Any]:
        """Get summary for the current week"""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_start_str = week_start.strftime("%Y-%m-%d")

        week_tasks = [
            t for t in self.tasks
            if t.created_date >= week_start_str
        ]

        return {
            "week_start": week_start_str,
            "total_created": len(week_tasks),
            "completed": len([t for t in week_tasks if t.completed]),
            "pending": len([t for t in week_tasks if not t.completed]),
            "average_daily_completion": round(
                len([t for t in week_tasks if t.completed]) / 7, 2
            ) if week_tasks else 0,
            "productivity_percentage": round(
                (len([t for t in week_tasks if t.completed]) / len(week_tasks) * 100)
                if week_tasks else 0, 2
            )
        }

    def get_overdue_tasks(self) -> List[Task]:
        """Get all overdue tasks"""
        return [t for t in self.tasks if t.get_status() == TaskStatus.OVERDUE]

    def get_upcoming_tasks(self, days: int = 7) -> List[Task]:
        """Get tasks due within specified days"""
        today = datetime.now()
        end_date = today + timedelta(days=days)

        return [
            t for t in self.tasks
            if t.due_date and not t.completed and
            today <= datetime.strptime(t.due_date, "%Y-%m-%d") <= end_date
        ]

    def get_completion_rate_by_priority(self) -> Dict[str, float]:
        """Calculate completion rate for each priority level"""
        result = {}
        for priority in Priority:
            priority_tasks = [t for t in self.tasks if t.priority == priority]
            if priority_tasks:
                completed = len([t for t in priority_tasks if t.completed])
                result[priority.name] = round((completed / len(priority_tasks)) * 100, 2)
            else:
                result[priority.name] = 0.0
        return result

    def generate_analytics_report(self) -> str:
        """Generate comprehensive analytics report"""
        report = "\n" + "=" * 50 + "\n"
        report += "📊 PRODUCTIVITY ANALYTICS REPORT\n"
        report += "=" * 50 + "\n\n"

        # Overall Statistics
        report += "📈 OVERALL STATISTICS:\n"
        report += f"  Total Tasks: {self.get_total_tasks()}\n"
        report += f"  Completed: {self.get_completed_count()}\n"
        report += f"  Pending: {self.get_pending_count()}\n"
        report += f"  Overdue: {self.get_overdue_count()}\n"
        report += f"  Productivity: {self.get_productivity_percentage()}%\n\n"

        # Priority Breakdown
        report += "🎯 PENDING TASKS BY PRIORITY:\n"
        priority_counts = self.get_tasks_by_priority()
        for priority, count in priority_counts.items():
            report += f"  {priority}: {count}\n"
        report += "\n"

        # Completion Rate by Priority
        report += "✓ COMPLETION RATE BY PRIORITY:\n"
        completion_rates = self.get_completion_rate_by_priority()
        for priority, rate in completion_rates.items():
            report += f"  {priority}: {rate}%\n"
        report += "\n"

        # Category Breakdown
        report += "📁 TASKS BY CATEGORY:\n"
        category_counts = self.get_tasks_by_category()
        if category_counts:
            for category, count in category_counts.items():
                report += f"  {category}: {count}\n"
        else:
            report += "  No pending tasks in any category\n"
        report += "\n"

        # Daily Summary
        daily = self.get_daily_summary()
        report += "📅 TODAY'S SUMMARY:\n"
        report += f"  Tasks Created: {daily['total_created']}\n"
        report += f"  Completed: {daily['completed_today']}\n"
        report += f"  Pending: {daily['pending_today']}\n"
        report += f"  Due Today: {daily['due_today']}\n\n"

        # Weekly Summary
        weekly = self.get_weekly_summary()
        report += "📊 WEEKLY SUMMARY:\n"
        report += f"  Week Starting: {weekly['week_start']}\n"
        report += f"  Total Created: {weekly['total_created']}\n"
        report += f"  Completed: {weekly['completed']}\n"
        report += f"  Pending: {weekly['pending']}\n"
        report += f"  Avg Daily Completion: {weekly['average_daily_completion']}\n"
        report += f"  Weekly Productivity: {weekly['productivity_percentage']}%\n\n"

        # Overdue Tasks
        report += "⚠️  OVERDUE TASKS:\n"
        overdue = self.get_overdue_tasks()
        if overdue:
            for task in overdue:
                report += f"  • {task.title} (Due: {task.due_date})\n"
        else:
            report += "  No overdue tasks!\n"
        report += "\n"

        # Upcoming Tasks
        report += "📌 UPCOMING TASKS (Next 7 Days):\n"
        upcoming = self.get_upcoming_tasks()
        if upcoming:
            for task in upcoming:
                report += f"  • {task.title} (Due: {task.due_date})\n"
        else:
            report += "  No upcoming tasks\n"

        report += "\n" + "=" * 50 + "\n"
        return report
