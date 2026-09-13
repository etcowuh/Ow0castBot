from .task1.main import Task1

def run_tasks(site):
    tasks = [Task1()]
    
    for task in tasks:
        task.run(site)