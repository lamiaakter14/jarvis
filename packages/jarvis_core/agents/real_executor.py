"""Real Executor Agent - Phase 9: Real-world execution engine."""

import os
import json
import subprocess
from datetime import datetime
from typing import Dict, List, Optional

EXECUTION_LOG = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'memory', 'execution_log.json')

class RealExecutor:
    def __init__(self):
        self.name = "RealExecutor"
        self.version = "9.0.0"
        self.safe_actions = ["read", "status", "list", "generate_pdf"]
        self.risky_actions = ["create", "edit", "commit"]
        self.dangerous_actions = ["delete", "push", "publish"]
        self.action_queue = []
        self._init_log()
    
    def _init_log(self):
        os.makedirs(os.path.dirname(EXECUTION_LOG), exist_ok=True)
        if not os.path.exists(EXECUTION_LOG):
            with open(EXECUTION_LOG, 'w') as f:
                json.dump([], f)
    
    def _log(self, action: str, status: str, details: str = ""):
        with open(EXECUTION_LOG, 'r') as f:
            log = json.load(f)
        log.append({
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "status": status,
            "details": details
        })
        with open(EXECUTION_LOG, 'w') as f:
            json.dump(log[-50:], f, indent=2)
    
    def check_permission(self, action: str) -> Dict:
        if action in self.safe_actions:
            return {"level": "auto", "message": "Safe action - auto allowed"}
        elif action in self.risky_actions:
            return {"level": "confirm", "message": "Low risk - one click approval needed"}
        elif action in self.dangerous_actions:
            return {"level": "double", "message": "High risk - type CONFIRM to proceed"}
        return {"level": "blocked", "message": "This action is not allowed"}
    
    def read_file(self, path: str) -> Dict:
        try:
            # Safety: only allow reading within project directory
            base = os.path.expanduser("~/jarvis")
            full_path = os.path.join(base, path)
            if not full_path.startswith(base):
                return {"status": "blocked", "message": "Cannot read outside project"}
            if not os.path.exists(full_path):
                return {"status": "error", "message": "File not found"}
            with open(full_path, 'r') as f:
                content = f.read()[:5000]  # Limit size
            self._log("read_file", "success", path)
            return {"status": "success", "content": content, "path": path, "size": len(content)}
        except Exception as e:
            self._log("read_file", "error", str(e))
            return {"status": "error", "message": str(e)}
    
    def create_file(self, path: str, content: str) -> Dict:
        try:
            base = os.path.expanduser("~/jarvis")
            full_path = os.path.join(base, path)
            if not full_path.startswith(base):
                return {"status": "blocked", "message": "Cannot write outside project"}
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            with open(full_path, 'w') as f:
                f.write(content)
            self._log("create_file", "success", path)
            return {"status": "success", "path": path, "size": len(content)}
        except Exception as e:
            self._log("create_file", "error", str(e))
            return {"status": "error", "message": str(e)}
    
    def delete_file(self, path: str, confirmation: str = "") -> Dict:
        if confirmation != "CONFIRM":
            return {"status": "blocked", "message": "Type CONFIRM to delete. This cannot be undone."}
        try:
            base = os.path.expanduser("~/jarvis")
            full_path = os.path.join(base, path)
            if not full_path.startswith(base):
                return {"status": "blocked", "message": "Cannot delete outside project"}
            if not os.path.exists(full_path):
                return {"status": "error", "message": "File not found"}
            os.remove(full_path)
            self._log("delete_file", "success", path)
            return {"status": "success", "message": f"Deleted: {path}"}
        except Exception as e:
            self._log("delete_file", "error", str(e))
            return {"status": "error", "message": str(e)}
    
    def git_status(self) -> Dict:
        try:
            result = subprocess.run(["git", "-C", os.path.expanduser("~/jarvis"), "status", "--short"], 
                                    capture_output=True, text=True, timeout=10)
            self._log("git_status", "success")
            return {"status": "success", "output": result.stdout[:1000] or "Clean working tree"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def git_commit(self, message: str) -> Dict:
        try:
            subprocess.run(["git", "-C", os.path.expanduser("~/jarvis"), "add", "-A"], 
                          capture_output=True, timeout=10)
            result = subprocess.run(["git", "-C", os.path.expanduser("~/jarvis"), "commit", "-m", message], 
                                    capture_output=True, text=True, timeout=10)
            self._log("git_commit", "success", message)
            return {"status": "success", "output": result.stdout[:500]}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def git_push(self, confirmation: str = "") -> Dict:
        if confirmation != "CONFIRM":
            return {"status": "blocked", "message": "Type CONFIRM to push to GitHub."}
        try:
            result = subprocess.run(["git", "-C", os.path.expanduser("~/jarvis"), "push", "origin", "main"], 
                                    capture_output=True, text=True, timeout=30)
            self._log("git_push", "success")
            return {"status": "success", "output": result.stdout[:500] or "Pushed successfully"}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def generate_pdf(self, template: str, data: Dict) -> Dict:
        # Simple PDF generation (text-based for now)
        try:
            content = f"""
            {'='*50}
            {template.upper()}
            {'='*50}
            Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}
            
            """
            for key, value in data.items():
                content += f"{key}: {value}\n"
            
            content += f"\n{'='*50}\nGenerated by JARVIS OS v9.0\n"
            
            filename = f"{template.lower().replace(' ', '_')}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            filepath = os.path.join(os.path.expanduser("~/jarvis/memory/exports"), filename)
            os.makedirs(os.path.dirname(filepath), exist_ok=True)
            
            with open(filepath, 'w') as f:
                f.write(content)
            
            self._log("generate_pdf", "success", filename)
            return {"status": "success", "filename": filename, "path": f"memory/exports/{filename}", "content": content[:1000]}
        except Exception as e:
            return {"status": "error", "message": str(e)}
    
    def get_queue(self) -> List[Dict]:
        return self.action_queue
    
    def get_log(self) -> List[Dict]:
        try:
            with open(EXECUTION_LOG, 'r') as f:
                return json.load(f)[-20:]
        except:
            return []
