import sys
import json
from datetime import datetime

JSON_FILE = "tasks.json"
VALID_STATUSES = ["todo", "in-progress", "done"]

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.load_task()
        
    def load_task(self):
        try:
            with open(JSON_FILE, "r") as file:
                self.tasks = json.load(file)
        except FileNotFoundError:
            self.tasks = []
        except json.JSONDecodeError:
            print("错误：无效的json文件")
            sys.exit(1)
    
    def save_task(self):
        try:
            with open(JSON_FILE, "w",) as file:
                json.dump(self.tasks, file, indent = 2)
        except IOError as e:
            print(f"保存文件时出错：{e}")
            sys.exit(1)
    
    def generate_unique_id(self):
        return max([t["id"] for t in self.tasks], default= 0) + 1
        
    def add_task(self, description):
        id = self.generate_unique_id()
        now = datetime.now().isoformat()
        task = {
            "id" : id,
            "description" : description,
            "status" : "todo",
            "createAt" : now,
            "updateAt" : now
        }
        self.tasks.append(task)
        self.save_task()
        print("任务添加成功！")
        
    def update_task(self, task_id, description):
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if not task:
            print("错误：任务id不存在")
            return
        task["description"] = description
        task["updateAt"] = datetime.now().isoformat()
        self.save_task()
        print("任务更新成功！")
        
    def delete_task(self, task_id):
        original_count = len(self.tasks)
        self.tasks = [t for t in self.tasks if t["id"] != task_id]
        if len(self.tasks) <= original_count:
            self.save_task()
            print("任务删除成功！")
        else:
            print("错误：任务ID不存在")
        
    def mark_status(self, task_id, new_status):
        if new_status not in VALID_STATUSES:
            print("错误：任务状态无效")
            return
        
        task = next((t for t in self.tasks if t["id"] == task_id), None)
        if not task:
            print("错误：任务ID不存在")
            return
        
        task["status"] = new_status
        task["updateAt"] = datetime.now().isoformat()
        self.save_task()
        print(f"任务状态已更新为{new_status}")
        
    def list_task(self, status = None):
        if status:
            if status not in VALID_STATUSES:
                print("错误：状态值不存在")
                return
            else:
                filtered = [t for t in self.tasks if t["status"] == status]
        else:
            filtered = self.tasks
        
        print(f"{"id":<5}{"状态":<10}{"任务":<30}{"创建时间":<25}{"更新时间"}")
        print("-" * 90)
        for t in filtered:
            print(f"{t["id"]:<5}{t["status"]:<10}{t["description"]:<30}{t["createAt"]:<25}{t["updateAt"]:<20}")
             
def main():
    if len(sys.argv) < 2:
        print("使用方法：python taskcli.py add/delete/update/list (in-progress/done)/mark-in-progress/mark-done")
        sys.exit(1)
    
    Manager = TaskManager()
    command = sys.argv[1]

    if command == "add":
        if len(sys.argv) < 3:
            print("用法：taskcli.py add 任务描述")
            return
        Manager.add_task(sys.argv[2])
        
    elif command == "update":
        if len(sys.argv) < 4:
            print("用法：tackcli.py update 任务id 任务描述")
            return
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("任务id为整数")
            return
        Manager.update_task(task_id, sys.argv[3])
        
    elif command == "delete":
        if len(sys.argv) < 3:
            print("用法：taskcli.py delete 任务id")
            return
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("任务id为整数")
            return
        Manager.delete_task(task_id)
        
    elif command == "list":
        if len(sys.argv) > 2:
            status = sys.argv[2]
        else:
            status = None
        Manager.list_task(status)
    
    elif command == "mark-in-progress":
        if len(sys.argv) < 3:
            print("用法：taskcli mark-in-progress 任务id")
            return
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("任务id需为整数")
            return
        Manager.mark_status(task_id, "in-progress")
    
    elif command == "mark-done":
        if len(sys.argv) < 3:
            print("用法：taskcli mark-done 任务id")
            return
        try:
            task_id = int(sys.argv[2])
        except ValueError:
            print("任务id需为整数")
            return
        Manager.mark_status(task_id, "done")
        
    else:
        print("无效命令")
        sys.exit(1)
        
if __name__ == "__main__":
    main()