"""CLI interface for JARVIS cognitive assistant using Typer."""

import typer
from typing import Optional
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import print as rprint
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.bridge.agent_bridge import (
    StrategistBridge,
    MentorBridge,
    ExecutorBridge,
    InnovatorBridge,
    AmplifierBridge
)
from core.memory_manager import MemoryManager

# Create CLI app
app = typer.Typer(
    name="jarvis",
    help="JARVIS Cognitive Assistant CLI",
    add_completion=False
)

console = Console()


@app.command()
def run():
    """Run the complete cognitive loop with all 5 agents."""
    console.print("\n[bold blue]Running JARVIS Cognitive Loop...[/bold blue]\n")
    
    try:
        # Initialize
        memory_manager = MemoryManager()
        
        # Initialize agents
        strategist = StrategistBridge(memory_manager)
        mentor = MentorBridge(memory_manager)
        executor = ExecutorBridge(memory_manager)
        innovator = InnovatorBridge(memory_manager)
        amplifier = AmplifierBridge(memory_manager)
        
        # Execute cognitive loop
        console.print("[cyan]→ Step 1: Planning with Strategist[/cyan]")
        plan = strategist.generate_plan()
        console.print(f"  ✓ Generated plan with {len(plan.get('tasks', []))} tasks\n")
        
        console.print("[cyan]→ Step 2: Analyzing with Mentor[/cyan]")
        gaps = mentor.analyze_execution_logs()
        console.print(f"  ✓ Analyzed execution logs\n")
        
        console.print("[cyan]→ Step 3: Executing with Executor[/cyan]")
        executor.run_tasks()
        console.print("  ✓ Tasks execution completed\n")
        
        console.print("[cyan]→ Step 4: Innovating with Innovator[/cyan]")
        innovations = innovator.create_innovations()
        innovation_count = len(innovations.get('innovations', []))
        console.print(f"  ✓ Generated {innovation_count} innovations\n")
        
        console.print("[cyan]→ Step 5: Optimizing with Amplifier[/cyan]")
        performance = amplifier.amplify()
        console.print(f"  ✓ Productivity score: {performance.get('productivity_score', 0):.2f}\n")
        
        console.print("[bold green]✓ Cognitive loop completed successfully![/bold green]\n")
        
    except Exception as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")
        raise typer.Exit(code=1)


@app.command()
def plan():
    """Generate and display today's daily plan."""
    console.print("\n[bold blue]Generating Daily Plan...[/bold blue]\n")
    
    try:
        memory_manager = MemoryManager()
        strategist = StrategistBridge(memory_manager)
        
        plan = strategist.generate_plan()
        
        # Display plan in a table
        table = Table(title=f"Daily Plan - {plan.get('date', 'Today')}")
        table.add_column("Task", style="cyan", no_wrap=False)
        table.add_column("Priority", style="yellow")
        table.add_column("Cognitive Load", style="magenta")
        table.add_column("ROI", style="green")
        table.add_column("Time", style="blue")
        
        for task in plan.get('tasks', []):
            table.add_row(
                task.get('task', ''),
                task.get('priority', ''),
                task.get('cognitive_load', ''),
                f"{task.get('roi', 0):.2f}",
                task.get('time_allocated', '')
            )
        
        console.print(table)
        console.print()
        
    except Exception as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")
        raise typer.Exit(code=1)


@app.command()
def gaps():
    """Identify and display knowledge gaps."""
    console.print("\n[bold blue]Analyzing Knowledge Gaps...[/bold blue]\n")
    
    try:
        memory_manager = MemoryManager()
        mentor = MentorBridge(memory_manager)
        
        result = mentor.analyze_execution_logs()
        gaps = result.get('updated_gaps', [])
        
        if gaps:
            for i, gap in enumerate(gaps, 1):
                console.print(f"{i}. {gap}")
        else:
            console.print("[green]✓ No significant gaps identified[/green]")
        
        console.print()
        
    except Exception as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")
        raise typer.Exit(code=1)


@app.command()
def innovate():
    """Generate and display innovations."""
    console.print("\n[bold blue]Generating Innovations...[/bold blue]\n")
    
    try:
        memory_manager = MemoryManager()
        innovator = InnovatorBridge(memory_manager)
        
        result = innovator.create_innovations()
        innovations = result.get('innovations', [])
        
        for i, innovation in enumerate(innovations, 1):
            panel = Panel(
                f"[bold]{innovation.get('title', 'Untitled')}[/bold]\n\n"
                f"{innovation.get('description', 'No description')}\n\n"
                f"Impact Score: [green]{innovation.get('impact_score', 0):.2f}[/green]",
                title=f"Innovation {i}",
                border_style="cyan"
            )
            console.print(panel)
        
        console.print()
        
    except Exception as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")
        raise typer.Exit(code=1)


@app.command()
def performance():
    """Display performance metrics and analytics."""
    console.print("\n[bold blue]Performance Analysis...[/bold blue]\n")
    
    try:
        memory_manager = MemoryManager()
        amplifier = AmplifierBridge(memory_manager)
        
        perf = amplifier.amplify()
        
        # Display performance in a panel
        content = (
            f"[cyan]Productivity Score:[/cyan] [bold]{perf.get('productivity_score', 0):.2f}[/bold]\n"
            f"[cyan]Total Tasks:[/cyan] {perf.get('total_tasks', 0)}\n"
            f"[cyan]Completed Tasks:[/cyan] {perf.get('completed_tasks', 0)}\n"
            f"[cyan]Completion Rate:[/cyan] {perf.get('completed_tasks', 0) / max(perf.get('total_tasks', 1), 1) * 100:.1f}%\n"
        )
        
        suggestions = perf.get('optimization_suggestions', [])
        if suggestions:
            content += "\n[yellow]Optimization Suggestions:[/yellow]\n"
            for suggestion in suggestions:
                content += f"  • {suggestion}\n"
        
        panel = Panel(content, title="Performance Metrics", border_style="green")
        console.print(panel)
        console.print()
        
    except Exception as e:
        console.print(f"[bold red]✗ Error: {e}[/bold red]")
        raise typer.Exit(code=1)


@app.command()
def version():
    """Display version information."""
    console.print("\n[bold]JARVIS Cognitive Assistant[/bold]")
    console.print("Version: 1.0.0")
    console.print("Architecture: Clean Architecture")
    console.print("Agents: Strategist, Mentor, Executor, Innovator, Amplifier\n")


if __name__ == "__main__":
    app()
