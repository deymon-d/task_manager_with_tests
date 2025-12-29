from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt, Confirm
from rich.panel import Panel
from datetime import datetime
import sys
from database import Database

console = Console()

class TaskManager:
    def __init__(self):
        self.db = Database()
        console.print(Panel.fit("[bold green]📝 Менеджер задач[/bold green]", 
                              subtitle="Простой консольный менеджер"))
    
    def display_menu(self):
        console.print("\n[bold cyan]МЕНЮ:[/bold cyan]")
        console.print("1. 📋 Показать все задачи")
        console.print("2. 📥 Добавить новую задачу")
        console.print("3. ✅ Отметить задачу как выполненную")
        console.print("4. ❌ Удалить задачу")
        console.print("5. ⏳ Показать невыполненные задачи")
        console.print("6. 📊 Статистика")
        console.print("7. 🚪 Выход")
    
    def show_all_tasks(self):
        tasks = self.db.get_all_tasks()
        if not tasks:
            console.print("[yellow]Нет задач[/yellow]")
            return
        
        table = Table(title="Все задачи", show_lines=True)
        table.add_column("ID", style="cyan", width=5)
        table.add_column("Заголовок", style="bold", width=30)
        table.add_column("Описание", width=40)
        table.add_column("Статус", width=15)
        table.add_column("Создана", width=20)
        
        for task in tasks:
            status = "✅ Выполнена" if task.completed else "⏳ В процессе"
            created = task.created_at.strftime("%d.%m.%Y %H:%M")
            table.add_row(
                str(task.id),
                task.title,
                task.description or "-",
                status,
                created
            )
        
        console.print(table)
    
    def add_task(self):
        console.print("\n[bold green]Добавление новой задачи[/bold green]")
        
        title = Prompt.ask("Введите заголовок задачи")
        while not title.strip():
            console.print("[red]Заголовок не может быть пустым![/red]")
            title = Prompt.ask("Введите заголовок задачи")
        
        description = Prompt.ask("Введите описание (необязательно)", default="")
        
        due_date_str = Prompt.ask(
            "Введите срок выполнения (ДД.ММ.ГГГГ) или оставьте пустым",
            default=""
        )
        
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, "%d.%m.%Y")
            except ValueError:
                console.print("[red]Неверный формат даты![/red]")
        
        task = self.db.add_task(title, description, due_date)
        console.print(f"[green]✅ Задача '{task.title}' добавлена с ID: {task.id}[/green]")
    
    def complete_task(self):
        task_id = Prompt.ask("Введите ID задачи для отметки как выполненной")
        
        try:
            task_id = int(task_id)
            task = self.db.complete_task(task_id)
            
            if task:
                console.print(f"[green]✅ Задача '{task.title}' отмечена как выполненная[/green]")
            else:
                console.print(f"[red]Задача с ID {task_id} не найдена[/red]")
        except ValueError:
            console.print("[red]ID должен быть числом![/red]")
    
    def delete_task(self):
        task_id = Prompt.ask("Введите ID задачи для удаления")
        
        try:
            task_id = int(task_id)
            if Confirm.ask(f"Вы уверены, что хотите удалить задачу {task_id}?"):
                task = self.db.delete_task(task_id)
                
                if task:
                    console.print(f"[green]✅ Задача '{task.title}' удалена[/green]")
                else:
                    console.print(f"[red]Задача с ID {task_id} не найдена[/red]")
        except ValueError:
            console.print("[red]ID должен быть числом![/red]")
    
    def show_pending_tasks(self):
        tasks = self.db.get_pending_tasks()
        if not tasks:
            console.print("[yellow]Нет невыполненных задач[/yellow]")
            return
        
        table = Table(title="Невыполненные задачи", style="blue")
        table.add_column("ID", style="cyan")
        table.add_column("Заголовок", style="bold")
        table.add_column("Описание")
        table.add_column("Создана")
        
        for task in tasks:
            created = task.created_at.strftime("%d.%m.%Y")
            table.add_row(
                str(task.id),
                task.title,
                task.description or "-",
                created
            )
        
        console.print(table)
    
    def show_statistics(self):
        all_tasks = self.db.get_all_tasks()
        pending_tasks = self.db.get_pending_tasks()
        
        total = len(all_tasks)
        completed = total - len(pending_tasks)
        
        stats_table = Table(title="Статистика", style="magenta")
        stats_table.add_column("Метрика", style="bold")
        stats_table.add_column("Значение", style="green")
        
        stats_table.add_row("Всего задач", str(total))
        stats_table.add_row("Выполнено", str(completed))
        stats_table.add_row("В процессе", str(len(pending_tasks)))
        
        if total > 0:
            percentage = (completed / total) * 100
            stats_table.add_row("Процент выполнения", f"{percentage:.1f}%")
        
        console.print(stats_table)
    
    def run(self):
        while True:
            self.display_menu()
            
            choice = Prompt.ask(
                "\nВыберите действие (1-7)",
                choices=["1", "2", "3", "4", "5", "6", "7"],
                show_choices=False
            )
            
            if choice == "1":
                self.show_all_tasks()
            elif choice == "2":
                self.add_task()
            elif choice == "3":
                self.complete_task()
            elif choice == "4":
                self.delete_task()
            elif choice == "5":
                self.show_pending_tasks()
            elif choice == "6":
                self.show_statistics()
            elif choice == "7":
                console.print("[bold blue]До свидания![/bold blue]")
                self.db.close()
                sys.exit(0)

def main():
    try:
        manager = TaskManager()
        manager.run()
    except KeyboardInterrupt:
        console.print("\n[yellow]Программа завершена пользователем[/yellow]")
    except Exception as e:
        console.print(f"[red]Ошибка: {e}[/red]")

if __name__ == "__main__":
    main()
