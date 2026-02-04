
import json
import os
from pathlib import Path
import markdown
import yaml
from typing import Any, Dict


class MemoryManager:
    def __init__(self, memory_dir: str = "memory"):
        """
        Initialize the Memory Manager to handle working, knowledge, and strategic memory.
        Args:
            memory_dir (str): The root directory for memory storage.
        """
        self.memory_dir = Path(memory_dir)
        self.working_memory_path = self.memory_dir / "working"
        self.knowledge_memory_path = self.memory_dir / "knowledge"
        self.strategic_memory_path = self.memory_dir / "strategic"

        # Ensure directories exist
        self.working_memory_path.mkdir(parents=True, exist_ok=True)
        self.knowledge_memory_path.mkdir(parents=True, exist_ok=True)
        self.strategic_memory_path.mkdir(parents=True, exist_ok=True)
        (self.working_memory_path / "execution_logs").mkdir(parents=True, exist_ok=True)
        (self.strategic_memory_path / "architecture_decision_records").mkdir(parents=True, exist_ok=True)

    # ---------------- Working Memory Operations ------------------

    def get_working_memory(self, file_name: str) -> Dict:
        """
        Retrieve data from the working memory (JSON files).

        Args:
            file_name (str): Filename within the working memory directory (e.g., 'daily_context.json').

        Returns:
            dict: JSON data from the requested working memory file.
        """
        file_path = self.working_memory_path / file_name
        if file_path.exists():
            with open(file_path, "r") as file:
                return json.load(file)
        return {}  # Return empty dict if file does not exist

    def save_working_memory(self, file_name: str, data: Dict) -> None:
        """
        Save data to a working memory file in JSON format.

        Args:
            file_name (str): Target filename (e.g., 'daily_context.json').
            data (dict): JSON serializable data.
        """
        file_path = self.working_memory_path / file_name
        with open(file_path, "w") as file:
            json.dump(data, file, indent=4)

    def add_execution_log(self, task_id: str, log_data: Dict) -> None:
        """
        Append a new execution log for a specific task.

        Args:
            task_id (str): Unique identifier for the task.
            log_data (dict): Log details to save.
        """
        log_file_path = self.working_memory_path / "execution_logs" / f"{task_id}.json"
        with open(log_file_path, "w") as file:
            json.dump(log_data, file, indent=4)

    # ---------------- Knowledge Memory Operations ------------------

    def get_knowledge(self, file_name: str) -> Dict:
        """
        Retrieve structured data from a knowledge file (Markdown with YAML frontmatter).

        Args:
            file_name (str): Filename within the knowledge memory directory (e.g., 'roadmap.md').

        Returns:
            dict: Parsed knowledge structure.
        """
        file_path = self.knowledge_memory_path / file_name
        if file_path.exists():
            with open(file_path, "r") as file:
                content = file.read()
                md = markdown.Markdown(extensions=["yaml_metadata"])
                return md.convert(content)
        return {}  # Return empty dict if file does not exist

    def save_knowledge(self, file_name: str, data: Dict) -> None:
        """
        Save structured data to a knowledge file (Markdown with YAML-embedded content).

        Args:
            file_name: Target filename (e.g., 'reflections.md').
            data: Data to serialize as YAML frontmatter + Markdown body.
        """
        file_path = self.knowledge_memory_path / file_name

        # Serialize YAML frontmatter and append the content
        yaml_metadata = yaml.dump(data, default_flow_style=False)
        body = data.get("body", "")  # Markdown content for the file
        with open(file_path, "w") as file:
            file.write(f"---\n{yaml_metadata}---\n{body}")

    def append_to_knowledge(self, file_name: str, new_data: Dict) -> None:
        """
        Append data to an existing knowledge file in an append-only format.

        Args:
            file_name (str): Filename to append data into.
            new_data (dict): Additional data to append.
        """
        existing_data = self.get_knowledge(file_name)
        body = existing_data.get("body", "")
        yaml_metadata = existing_data.get("unresolved_gaps", [])

        # Append new data into YAML or body
        yaml_metadata.extend(new_data.get("unresolved_gaps", []))
        body += f"\n\n{new_data.get('body', '')}"

        # Save updated file
        self.save_knowledge(file_name, {"unresolved_gaps": yaml_metadata, "body": body})

    # ---------------- Strategic Memory Operations ------------------

    def get_strategic_file(self, file_name: str) -> str:
        """
        Retrieve content from a strategic memory file (Markdown).

        Args:
            file_name (str): Filename within the strategic memory directory 
                           (e.g., 'long_term_goal.md', 'milestones.md').

        Returns:
            str: Content of the strategic file.
        """
        file_path = self.strategic_memory_path / file_name
        if file_path.exists():
            with open(file_path, "r") as file:
                return file.read()
        return ""  # Return empty string if file does not exist

    def get_adr(self, adr_number: str) -> str:
        """
        Retrieve an Architecture Decision Record.

        Args:
            adr_number (str): ADR number (e.g., '001', '002').

        Returns:
            str: Content of the ADR file.
        """
        # ADR files follow naming pattern: {number}-{title}.md
        adr_dir = self.strategic_memory_path / "architecture_decision_records"
        for adr_file in adr_dir.glob(f"{adr_number}-*.md"):
            with open(adr_file, "r") as file:
                return file.read()
        return ""  # Return empty string if ADR not found

    def list_adrs(self) -> list:
        """
        List all Architecture Decision Records.

        Returns:
            list: List of ADR filenames.
        """
        adr_dir = self.strategic_memory_path / "architecture_decision_records"
        if adr_dir.exists():
            return sorted([f.name for f in adr_dir.glob("*.md")])
        return []
