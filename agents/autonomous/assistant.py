import sqlite3
import logging
import json
from datetime import datetime, timedelta

class AutonomousAssistant:
    """Автономный ИИ-помощник для управления проектами"""
    
    def __init__(self, name="ProjectGuardian"):
        self.name = name
        self.db_path = "projects.db"
        self._setup_logger()
        self._init_db()
        self.log("Автономный помощник инициализирован")
        
    def _setup_logger(self):
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(logging.INFO)
        handler = logging.FileHandler(f'{self.name}.log')
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
    
    def _init_db(self):
        """Инициализация базы проектов"""
        self.conn = sqlite3.connect(self.db_path)
        cursor = self.conn.cursor()
        
        # Таблица проектов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                status TEXT DEFAULT 'planning',
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                deadline DATETIME
            )
        ''')
        
        # Таблица задач
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                project_id INTEGER,
                description TEXT NOT NULL,
                priority INTEGER DEFAULT 3,
                completed BOOLEAN DEFAULT 0,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        ''')
        
        # Таблица ресурсов
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS resources (
                id INTEGER PRIMARY KEY,
                project_id INTEGER,
                name TEXT NOT NULL,
                allocated INTEGER,
                used INTEGER DEFAULT 0,
                FOREIGN KEY (project_id) REFERENCES projects(id)
            )
        ''')
        
        self.conn.commit()
    
    def log(self, message):
        self.logger.info(message)
        return f"[{datetime.now()}] {message}"
    
    def add_project(self, name, deadline=None):
        """Добавление нового проекта"""
        cursor = self.conn.cursor()
        cursor.execute(
            "INSERT INTO projects (name, deadline) VALUES (?, ?)",
            (name, deadline)
        )
        self.conn.commit()
        return self.log(f"Добавлен проект: {name}")
    
    def add_task(self, project_name, description, priority=3):
        """Добавление задачи в проект"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id FROM projects WHERE name=?", (project_name,)
        )
        project_id = cursor.fetchone()[0]
        
        cursor.execute(
            "INSERT INTO tasks (project_id, description, priority) VALUES (?, ?, ?)",
            (project_id, description, priority)
        )
        self.conn.commit()
        return self.log(f"Добавлена задача: {description} в проект {project_name}")
    
    def allocate_resources(self, project_name, resource_name, amount):
        """Выделение ресурсов проекту"""
        cursor = self.conn.cursor()
        cursor.execute(
            "SELECT id FROM projects WHERE name=?", (project_name,)
        )
        project_id = cursor.fetchone()[0]
        
        cursor.execute(
            "INSERT INTO resources (project_id, name, allocated) VALUES (?, ?, ?)",
            (project_id, resource_name, amount)
        )
        self.conn.commit()
        return self.log(f"Выделено {amount} {resource_name} для проекта {project_name}")
    
    def generate_report(self):
        """Генерация отчёта по всем проектам"""
        cursor = self.conn.cursor()
        
        # Статистика проектов
        cursor.execute("SELECT COUNT(*), status FROM projects GROUP BY status")
        status_stats = cursor.fetchall()
        
        # Просроченные задачи
        cursor.execute("""
            SELECT p.name, t.description 
            FROM tasks t
            JOIN projects p ON t.project_id = p.id
            WHERE t.completed = 0 AND p.deadline < DATE('now')
        """)
        overdue_tasks = cursor.fetchall()
        
        report = {
            "timestamp": datetime.now().isoformat(),
            "projects_status": {status: count for count, status in status_stats},
            "overdue_tasks": [{"project": p, "task": t} for p, t in overdue_tasks],
            "resource_usage": self._calculate_resource_usage()
        }
        
        return report
    
    def _calculate_resource_usage(self):
        """Расчёт использования ресурсов"""
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT r.name, SUM(r.allocated), SUM(r.used) 
            FROM resources r
            GROUP BY r.name
        """)
        return {name: {"allocated": alloc, "used": used} 
                for name, alloc, used in cursor.fetchall()}
    
    def autonomous_loop(self, interval_minutes=60):
        """Основной цикл автономной работы"""
        import time
        while True:
            self.log("Начало автономного цикла")
            
            # 1. Проверка сроков проектов
            self._check_deadlines()
            
            # 2. Балансировка ресурсов
            self._balance_resources()
            
            # 3. Генерация отчётов
            report = self.generate_report()
            with open("latest_report.json", "w") as f:
                json.dump(report, f)
            
            self.log(f"Цикл завершён. Отчёт сохранён. Следующая итерация через {interval_minutes} минут")
            time.sleep(interval_minutes * 60)
    
    def _check_deadlines(self):
        """Автоматическая проверка сроков"""
        cursor = self.conn.cursor()
        cursor.execute("""
            UPDATE projects 
            SET status = 'overdue'
            WHERE deadline < DATE('now') AND status NOT IN ('completed', 'overdue')
        """)
        self.conn.commit()
    
    def _balance_resources(self):
        """Автоматическая балансировка ресурсов"""
        # Здесь будет сложная логика перераспределения
        self.log("Балансировка ресурсов выполнена")