# TaskFlow Pro - Smart Productivity Manager 🚀

A comprehensive command-line task and productivity management application built with Python. Organize your tasks, track your productivity, and achieve your goals efficiently!

## Features

### 📋 Task Management
- ✅ Add new tasks with title, description, priority, and due dates
- ✏️ Edit/update existing tasks
- ❌ Delete tasks
- ✔️ Mark tasks as completed or incomplete
- 🏷️ Organize tasks by categories

### 🎯 Priority & Deadline System
- **Priority Levels**: HIGH, MEDIUM, LOW
- **Due Dates**: Set and track task deadlines
- **Status Tracking**: Monitor PENDING and OVERDUE tasks automatically
- **Reminders**: Placeholder for task reminders (extensible feature)

### 📊 Productivity Analytics
- **Statistics Dashboard**:
  - Total tasks count
  - Completed vs. Pending tasks
  - Overdue tasks tracking
  - Real-time productivity percentage
  
- **Detailed Reports**:
  - Daily performance summary
  - Weekly productivity analysis
  - Priority-based completion rates
  - Category-wise task breakdown
  - Upcoming tasks (next 7 days)

### 💾 Data Storage
- **JSON-based Storage**: Automatic persistence to `tasks.json`
- **Auto-save**: Tasks saved automatically after each operation
- **Auto-load**: Retrieve all tasks on application restart
- **Import/Export**: Backup and restore tasks from JSON files

### 🎨 User Experience
- **Menu-driven Interface**: Intuitive terminal navigation
- **Colorful Output**: ANSI color codes for better readability
- **Clean Formatting**: Well-organized, easy-to-read display
- **Error Handling**: Comprehensive input validation
- **Keyboard Interrupts**: Graceful exit handling

### 🌟 Bonus Features
- 🎨 **Colorful CLI**: Vibrant terminal interface with color-coded priority levels
- 🔍 **Search & Filter**: Find tasks by keyword, priority, category, or status
- 📁 **Category Organization**: Group tasks by custom categories
- 📈 **Visual Progress**: Progress bars and status indicators
- ♻️ **Data Management**: Import/Export capabilities for backup and migration

## Installation

### Requirements
- Python 3.8 or higher
- No external dependencies (uses Python standard library)

### Setup
1. Clone or download the project:
```bash
git clone https://github.com/yourusername/taskflow-pro.git
cd taskflow-pro
```

2. Ensure all Python files are in the same directory:
- `main.py` (entry point)
- `task.py` (task model)
- `task_manager.py` (business logic)
- `data_storage.py` (JSON persistence)
- `analytics.py` (productivity analytics)
- `utils.py` (utilities and formatting)

## Usage

### Starting the Application
```bash
python main.py
```

### Main Menu Options

#### Task Management
1. **Add New Task** - Create a new task with details
2. **View All Tasks** - Display all tasks
3. **View Active Tasks** - Show incomplete tasks
4. **View Completed Tasks** - Show finished tasks
5. **Search/Filter Tasks** - Find tasks by keyword, priority, category, or status
6. **Edit Task** - Modify task details
7. **Mark Task Complete** - Check off a task
8. **Mark Task Incomplete** - Reopen a completed task
9. **Delete Task** - Remove a task permanently

#### Analytics & Reports
- **A**: Comprehensive analytics report
- **B**: Daily performance summary
- **C**: Weekly performance summary
- **D**: View all overdue tasks
- **E**: View tasks due in next 7 days

#### Data Management
- **I**: Import tasks from JSON file
- **E**: Export tasks to JSON file
- **C**: Clear all tasks (with confirmation)

#### Exit
- **EXIT** or **X**: Close the application

## Examples

### Add a Task
```
1. Select "Add New Task"
2. Enter title: "Complete project report"
3. Enter description: "Finish Q1 performance report"
4. Set priority: HIGH
5. Set due date: 2024-03-15
6. Set category: Work
```

### Search Tasks
```
1. Select "Search/Filter Tasks"
2. Choose search by keyword
3. Enter query: "report"
4. View matching tasks
```

### View Analytics
```
1. Select "View Analytics Report"
2. Review comprehensive productivity metrics
3. Check daily/weekly performance
4. Identify overdue tasks
```

## File Structure

```
taskflow-pro/
├── main.py              # CLI application entry point
├── task.py              # Task class and data models
├── task_manager.py      # Core business logic
├── data_storage.py      # JSON data persistence
├── analytics.py         # Productivity analytics engine
├── utils.py             # Utilities and formatting helpers
├── tasks.json           # Auto-generated tasks database
└── README.md            # This file
```

## Data Storage

### tasks.json Format
```json
[
  {
    "id": "a1b2c3d4",
    "title": "Complete project",
    "description": "Finish the main project",
    "priority": "HIGH",
    "due_date": "2024-03-15",
    "category": "Work",
    "completed": false,
    "created_date": "2024-03-10 10:30:00",
    "completed_date": null,
    "reminders_set": false
  }
]
```

## Key Features Explained

### Priority System
- **HIGH** (🔴): Urgent, critical tasks
- **MEDIUM** (🟡): Important, regular tasks
- **LOW** (🟢): Optional, can be deferred

### Status Types
- **PENDING**: Active, not yet completed
- **COMPLETED**: Finished successfully
- **OVERDUE**: Not completed and past due date

### Productivity Metrics
- **Productivity %**: (Completed Tasks / Total Tasks) × 100
- **Daily Summary**: Tasks created and completed today
- **Weekly Summary**: Aggregated performance over the week
- **Completion Rate by Priority**: How efficiently you complete each priority level

## Color Codes

The application uses these colors:
- 🔵 **Cyan**: Headers and important info
- 🟢 **Green**: Success messages and completed items
- 🟠 **Yellow**: Warnings and medium priority
- 🔴 **Red**: Errors and high priority
- ⚪ **White**: Regular text and low priority

## Keyboard Shortcuts

- **Ctrl+C**: Interrupt and exit (with confirmation)
- **Enter**: Confirm input or continue

## Tips & Tricks

1. **Bulk Operations**: Use export to create backups before clearing tasks
2. **Task Templates**: Export completed workflows and reimport them later
3. **Weekly Reviews**: Check weekly summaries every Friday
4. **Category Management**: Organize by department/project/context
5. **Priority Filtering**: Focus on HIGH priority tasks first
6. **Overdue Tracking**: Check overdue tasks daily to stay on top

## Limitations & Future Enhancements

### Current Limitations
- Single-user application (no multi-user support)
- No task dependencies or subtasks
- Reminders are placeholder functionality
- No recurring/recurring tasks yet

### Planned Features
- 📱 Web interface
- 👥 Multi-user support with authentication
- 📧 Email reminders and notifications
- 🔄 Recurring task templates
- 📊 Advanced reporting and charts
- 🤖 AI-powered task suggestions
- ⏱️ Time tracking integration

## Troubleshooting

### Issue: "Task not found"
- Ensure you're using the correct task ID
- Task IDs are displayed next to each task

### Issue: "No tasks found"
- Check filters or search parameters
- Use "View All Tasks" to see everything

### Issue: Colors not displaying properly
- On Windows, colors should auto-enable
- Try running with: `python main.py`

### Issue: Cannot save tasks
- Ensure write permissions in the application directory
- Check if `tasks.json` file is locked

## Performance

- Handles 1000+ tasks efficiently
- JSON parsing optimized for speed
- Memory-efficient task filtering
- Fast search with keyword indexing

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Improve documentation

## Support

For issues, questions, or suggestions:
1. Check the documentation above
2. Review the troubleshooting section
3. Open an issue on the project repository

---

**TaskFlow Pro v1.0** - Making productivity management simple and effective! 🎯

Happy task managing! 🚀
