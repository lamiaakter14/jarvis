import os
import subprocess

class Executor:
    def __init__(self, memory_manager):
        """
        Initialize the Executor Agent.
        Args:
            memory_manager: Instance of the MemoryManager to interact with system memory.
        """
        self.memory_manager = memory_manager

    def execute_task(self, task):
        """
        Execute a task based on the details provided in the task dictionary.
        Args:
            task (dict): A task dictionary containing information about what needs to be executed.

        Returns:
            dict: Execution log containing status, errors (if any), and metadata.
        """
        task_name = task.get("task")
        task_type = task.get("type")  # Example: "script", "automation", "manual"
        task_details = task.get("details", {})

        print(f"Executing task: {task_name} (Type: {task_type})")
        execution_log = {"task": task_name, "status": "pending", "output": "", "errors": []}

        try:
            if task_type == "script":
                # Execute a script from the task details
                script_path = task_details.get("script_path")
                if not os.path.isfile(script_path):
                    raise FileNotFoundError(f"Script not found: {script_path}")

                result = subprocess.run(
                    ["python", script_path], capture_output=True, text=True, check=True
                )
                execution_log["status"] = "success"
                execution_log["output"] = result.stdout.strip()
            
            elif task_type == "manual":
                # Log that manual action is required
                execution_log["status"] = "manual_pending"
                execution_log["output"] = "Task requires manual intervention. See task details."

            else:
                # Default to unrecognized task type
                execution_log["status"] = "failed"
                execution_log["errors"].append(f"Unrecognized task type: {task_type}")

        except subprocess.CalledProcessError as e:
            # Handle errors during script execution
            execution_log["status"] = "failed"
            execution_log["errors"].append(f"Script execution failed: {str(e)}")
            execution_log["output"] = e.stderr.strip()

        except Exception as e:
            # Handle other types of exceptions
            execution_log["status"] = "failed"
            execution_log["errors"].append(str(e))

        return execution_log

    def run_tasks(self):
        """
        Execute all tasks in the daily plan and log results to execution logs.

        Returns:
            None
        """
        # Load daily plan
        daily_plan = self.memory_manager.get_working_memory("daily_plan.json")
        execution_logs = {}

        for task in daily_plan.get("tasks", []):
            # Execute each task and log the results
            task_execution_log = self.execute_task(task)
            execution_logs[task["task"]] = task_execution_log

            # Print the log to the console for review
            print(f"Task Execution Log: {task_execution_log}")

        # Save all execution logs
        self.save_execution_logs(execution_logs)

    def save_execution_logs(self, execution_logs):
        """
        Save the execution logs to the respective file in the working memory.

        Args:
            execution_logs (dict): All task execution logs.

        Returns:
            None
        """
        logs_path = "execution_logs/logs.json"
        self.memory_manager.save_working_memory(logs_path, execution_logs)

        print(f"Execution logs saved to {logs_path}.")
