#!/usr/bin/env python3
"""
AutoClean EEG Pipeline - Command Line Interface

This module provides a flexible CLI for AutoClean that works both as a
standalone tool (via uv tool) and within development environments.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional

from autoclean.utils.logging import message
from autoclean.utils.user_config import user_config


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser for AutoClean CLI."""
    from autoclean.utils.branding import AutoCleanBranding
    
    parser = argparse.ArgumentParser(
        description=f"{AutoCleanBranding.PRODUCT_NAME}\n{AutoCleanBranding.TAGLINE}\n\nGitHub: https://github.com/cincibrainlab/autoclean_pipeline",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Simple usage (recommended)
  autoclean process RestingEyesOpen data.raw
  autoclean process RestingEyesOpen data_directory/
  
  # Advanced usage with options
  autoclean process --task RestingEyesOpen --file data.raw --output results/
  autoclean process --task RestingEyesOpen --dir data/ --output results/
  
  # Use Python task file
  autoclean process --task-file my_task.py --file data.raw
  
  # List available tasks
  autoclean list-tasks --include-custom
  
  # Start review GUI
  autoclean review --output results/
  
  # Add a custom task (saves to user config)
  autoclean task add my_task.py --name MyCustomTask
  
  # List custom tasks
  autoclean task list
  
  # Remove a custom task
  autoclean task remove MyCustomTask
  
  # Run setup wizard
  autoclean setup
  
  # Show user config location
  autoclean config show
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Process command
    process_parser = subparsers.add_parser("process", help="Process EEG data")

    # Positional arguments for simple usage: autoclean process TaskName FilePath
    process_parser.add_argument(
        "task_name", nargs="?", type=str, help="Task name (e.g., RestingEyesOpen)"
    )
    process_parser.add_argument(
        "input_path", nargs="?", type=Path, help="EEG file or directory to process"
    )

    # Optional named arguments (for advanced usage)
    process_parser.add_argument(
        "--task", type=str, help="Task name (alternative to positional)"
    )
    process_parser.add_argument(
        "--task-file", type=Path, help="Python task file to use"
    )

    # Input options (for advanced usage)
    process_parser.add_argument(
        "--file",
        type=Path,
        help="Single EEG file to process (alternative to positional)",
    )
    process_parser.add_argument(
        "--dir",
        "--directory",
        type=Path,
        dest="directory",
        help="Directory containing EEG files to process (alternative to positional)",
    )

    process_parser.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Output directory (default: workspace/output)",
    )
    process_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be processed without running",
    )

    # List tasks command
    subparsers.add_parser("list-tasks", help="List available tasks")

    # Review command
    review_parser = subparsers.add_parser("review", help="Start review GUI")
    review_parser.add_argument(
        "--output",
        type=Path,
        required=True,
        help="AutoClean output directory to review",
    )

    # Task management commands
    task_parser = subparsers.add_parser("task", help="Manage custom tasks")
    task_subparsers = task_parser.add_subparsers(
        dest="task_action", help="Task actions"
    )

    # Add task
    add_task_parser = task_subparsers.add_parser("add", help="Add a custom task")
    add_task_parser.add_argument("task_file", type=Path, help="Python task file to add")
    add_task_parser.add_argument(
        "--name", type=str, help="Custom name for the task (default: filename)"
    )
    add_task_parser.add_argument(
        "--force", action="store_true", help="Overwrite existing task with same name"
    )

    # Remove task
    remove_task_parser = task_subparsers.add_parser(
        "remove", help="Remove a custom task"
    )
    remove_task_parser.add_argument(
        "task_name", type=str, help="Name of the task to remove"
    )

    # List custom tasks
    list_custom_parser = task_subparsers.add_parser("list", help="List custom tasks")
    list_custom_parser.add_argument(
        "--verbose", "-v", action="store_true", help="Show detailed information"
    )

    # Show config location
    config_parser = subparsers.add_parser("config", help="Manage user configuration")
    config_subparsers = config_parser.add_subparsers(
        dest="config_action", help="Config actions"
    )

    # Show config location
    config_subparsers.add_parser("show", help="Show configuration directory location")

    # Setup/reconfigure workspace
    config_subparsers.add_parser("setup", help="Reconfigure workspace location")

    # Reset config
    reset_parser = config_subparsers.add_parser(
        "reset", help="Reset configuration to defaults"
    )
    reset_parser.add_argument(
        "--confirm", action="store_true", help="Confirm the reset action"
    )

    # Export/import config
    export_parser = config_subparsers.add_parser("export", help="Export configuration")
    export_parser.add_argument(
        "export_path", type=Path, help="Directory to export configuration to"
    )

    import_parser = config_subparsers.add_parser("import", help="Import configuration")
    import_parser.add_argument(
        "import_path", type=Path, help="Directory to import configuration from"
    )

    # Setup command (same as config setup for simplicity)
    subparsers.add_parser("setup", help="Setup or reconfigure workspace")

    # Version command
    subparsers.add_parser("version", help="Show version information")
    
    # Help command (for consistency)
    subparsers.add_parser("help", help="Show detailed help information")

    # Tutorial command
    subparsers.add_parser("tutorial", help="Show a helpful tutorial for first-time users")

    return parser


def validate_args(args) -> bool:
    """Validate command line arguments."""
    if args.command == "process":
        # Normalize positional vs named arguments
        task_name = args.task_name or args.task
        input_path = args.input_path or args.file or args.directory

        # Check that either task or task-file is provided
        if not task_name and not args.task_file:
            message("error", "Either task name or --task-file must be specified")
            return False

        if task_name and args.task_file:
            message("error", "Cannot specify both task name and --task-file")
            return False

        # Check input exists
        if input_path and not input_path.exists():
            message("error", f"Input path does not exist: {input_path}")
            return False
        elif not input_path:
            message("error", "Input file or directory must be specified")
            return False

        # Store normalized values back to args
        args.final_task = task_name
        args.final_input = input_path

        # Check task file exists if provided
        if args.task_file and not args.task_file.exists():
            message("error", f"Task file does not exist: {args.task_file}")
            return False

    elif args.command == "review":
        if not args.output.exists():
            message("error", f"Output directory does not exist: {args.output}")
            return False

    return True


def cmd_process(args) -> int:
    """Execute the process command."""
    try:
        # Lazy import Pipeline only when needed
        from autoclean.core.pipeline import Pipeline

        # Initialize pipeline
        pipeline_kwargs = {"output_dir": args.output}

        pipeline = Pipeline(**pipeline_kwargs)

        # Add Python task file if provided
        if args.task_file:
            task_name = pipeline.add_task(args.task_file)
            message("info", f"Loaded Python task: {task_name}")
        else:
            task_name = args.final_task

            # Check if this is a custom task using the new discovery system
            from autoclean.utils.task_discovery import get_task_by_name
            
            task_class = get_task_by_name(task_name)
            if task_class:
                # Task found via discovery system
                message("info", f"Loaded task: {task_name}")
            else:
                # Fall back to old method for compatibility
                custom_task_path = user_config.get_custom_task_path(task_name)
                if custom_task_path:
                    task_name = pipeline.add_task(custom_task_path)
                    message(
                        "info",
                        f"Loaded custom task '{args.final_task}' from user configuration",
                    )

        if args.dry_run:
            message("info", "DRY RUN - No processing will be performed")
            message("info", f"Would process: {args.final_input}")
            message("info", f"Task: {task_name}")
            message("info", f"Output: {args.output}")
            return 0

        # Process files
        if args.final_input.is_file():
            message("info", f"Processing single file: {args.final_input}")
            pipeline.process_file(file_path=args.final_input, task=task_name)
        else:
            message("info", f"Processing directory: {args.final_input}")
            pipeline.process_directory(directory=args.final_input, task=task_name)

        message("info", "Processing completed successfully!")
        return 0

    except Exception as e:
        message("error", f"Processing failed: {str(e)}")
        return 1


def cmd_list_tasks(_args) -> int:
    """Execute the list-tasks command."""
    try:
        from autoclean.utils.task_discovery import safe_discover_tasks
        from rich.console import Console
        from rich.panel import Panel
        from rich.table import Table
        from pathlib import Path
        
        console = Console()

        valid_tasks, invalid_files = safe_discover_tasks()

        console.print("\n[bold]Available Processing Tasks[/bold]\n")

        # --- Built-in Tasks ---
        built_in_tasks = [task for task in valid_tasks if "autoclean/tasks" in task.source]
        if built_in_tasks:
            built_in_table = Table(show_header=True, header_style="bold blue", box=None, padding=(0, 1))
            built_in_table.add_column("Task Name", style="cyan", no_wrap=True)
            built_in_table.add_column("Module", style="dim")
            built_in_table.add_column("Description", style="dim", max_width=50)
            
            for task in sorted(built_in_tasks, key=lambda x: x.name):
                # Extract just the module name from the full path
                module_name = Path(task.source).stem
                built_in_table.add_row(
                    task.name, 
                    module_name + ".py",
                    task.description or "No description"
                )
            
            built_in_panel = Panel(
                built_in_table,
                title="[bold]Built-in Tasks[/bold]",
                border_style="blue",
                padding=(1, 1)
            )
            console.print(built_in_panel)
        else:
            console.print(Panel(
                "[dim]No built-in tasks found[/dim]",
                title="[bold]Built-in Tasks[/bold]",
                border_style="blue",
                padding=(1, 1)
            ))

        # --- Custom Tasks ---
        custom_tasks = [task for task in valid_tasks if "autoclean/tasks" not in task.source]
        if custom_tasks:
            custom_table = Table(show_header=True, header_style="bold magenta", box=None, padding=(0, 1))
            custom_table.add_column("Task Name", style="magenta", no_wrap=True)
            custom_table.add_column("File", style="dim")
            custom_table.add_column("Description", style="dim", max_width=50)
            
            for task in sorted(custom_tasks, key=lambda x: x.name):
                # Show just the filename for custom tasks
                file_name = Path(task.source).name
                custom_table.add_row(
                    task.name,
                    file_name,
                    task.description or "No description"
                )
            
            custom_panel = Panel(
                custom_table,
                title="[bold]Custom Tasks[/bold]",
                border_style="magenta",
                padding=(1, 1)
            )
            console.print(custom_panel)
        else:
            console.print(Panel(
                "[dim]No custom tasks found.\n"
                "Use [yellow]autoclean-eeg task add <file.py>[/yellow] to add one.[/dim]",
                title="[bold]Custom Tasks[/bold]",
                border_style="magenta",
                padding=(1, 1)
            ))

        # --- Invalid Task Files ---
        if invalid_files:
            invalid_table = Table(show_header=True, header_style="bold red", box=None, padding=(0, 1))
            invalid_table.add_column("File", style="red", no_wrap=True)
            invalid_table.add_column("Error", style="yellow", max_width=70)
            
            for file in invalid_files:
                # Show relative path if in workspace, otherwise just filename
                file_path = Path(file.source)
                if file_path.is_absolute():
                    display_name = file_path.name
                else:
                    display_name = file.source
                    
                invalid_table.add_row(display_name, file.error)
            
            invalid_panel = Panel(
                invalid_table,
                title="[bold]Invalid Task Files[/bold]",
                border_style="red",
                padding=(1, 1)
            )
            console.print(invalid_panel)

        # Summary statistics
        console.print(f"\n[dim]Found {len(valid_tasks)} valid tasks "
                     f"({len(built_in_tasks)} built-in, {len(custom_tasks)} custom) "
                     f"and {len(invalid_files)} invalid files[/dim]")

        return 0

    except Exception as e:
        message("error", f"Failed to list tasks: {str(e)}")
        return 1


def cmd_review(args) -> int:
    """Execute the review command."""
    try:
        # Lazy import Pipeline only when needed
        from autoclean.core.pipeline import Pipeline

        pipeline = Pipeline(output_dir=args.output)

        message("info", f"Starting review GUI for: {args.output}")
        pipeline.start_autoclean_review()

        return 0

    except Exception as e:
        message("error", f"Failed to start review GUI: {str(e)}")
        return 1


def cmd_setup(_args) -> int:
    """Run the setup wizard."""
    try:
        user_config.setup_workspace()
        return 0
    except Exception as e:
        message("error", f"Setup failed: {str(e)}")
        return 1


def cmd_version(_args) -> int:
    """Show version information."""
    try:
        from autoclean import __version__
        from autoclean.utils.branding import AutoCleanBranding
        from autoclean.utils.user_config import UserConfigManager
        from rich.console import Console

        console = Console()
        
        # Professional header consistent with setup
        AutoCleanBranding.get_professional_header(console)
        console.print(f"\n{AutoCleanBranding.get_simple_divider()}")
        
        console.print("\n[bold]Version Information:[/bold]")
        console.print(f"  🏷️  [bold]{__version__}[/bold]")
        
        # Include system information for troubleshooting
        console.print("\n[bold]System Information:[/bold]")
        temp_config = UserConfigManager()
        temp_config._display_system_info(console)
        
        console.print(f"\n[dim]{AutoCleanBranding.TAGLINE}[/dim]")
        
        # GitHub and support info
        console.print("\n[bold]GitHub Repository:[/bold]")
        console.print("  [blue]https://github.com/cincibrainlab/autoclean_pipeline[/blue]")
        console.print("  [dim]Report issues, contribute, or get help[/dim]")
        
        return 0
    except ImportError:
        print("AutoClean EEG (version unknown)")
        return 0


def cmd_task(args) -> int:
    """Execute task management commands."""
    if args.task_action == "add":
        return cmd_task_add(args)
    elif args.task_action == "remove":
        return cmd_task_remove(args)
    elif args.task_action == "list":
        return cmd_task_list(args)
    else:
        message("error", "No task action specified")
        return 1


def cmd_task_add(args) -> int:
    """Add a custom task by copying to workspace tasks folder."""
    try:
        if not args.task_file.exists():
            message("error", f"Task file not found: {args.task_file}")
            return 1

        # Ensure workspace exists
        if not user_config.tasks_dir.exists():
            user_config.tasks_dir.mkdir(parents=True, exist_ok=True)

        # Determine destination name
        if args.name:
            dest_name = f"{args.name}.py"
        else:
            dest_name = args.task_file.name

        dest_file = user_config.tasks_dir / dest_name

        # Check if task already exists
        if dest_file.exists() and not args.force:
            message(
                "error", f"Task '{dest_name}' already exists. Use --force to overwrite."
            )
            return 1

        # Copy the task file
        import shutil

        shutil.copy2(args.task_file, dest_file)

        # Extract class name for usage message
        try:
            class_name, _ = user_config._extract_task_info(dest_file)
            task_name = class_name
        except Exception:
            task_name = dest_file.stem

        message("info", f"Task '{task_name}' added to workspace!")
        print(f"📁 Copied to: {dest_file}")
        print("\nUse your custom task with:")
        print(f"  autoclean process {task_name} <data_file>")

        return 0

    except Exception as e:
        message("error", f"Failed to add custom task: {str(e)}")
        return 1


def cmd_task_remove(args) -> int:
    """Remove a custom task by deleting from workspace tasks folder."""
    try:
        # Find task file by class name or filename
        custom_tasks = user_config.list_custom_tasks()

        task_file = None
        if args.task_name in custom_tasks:
            # Found by class name
            task_file = Path(custom_tasks[args.task_name]["file_path"])
        else:
            # Try by filename
            potential_file = user_config.tasks_dir / f"{args.task_name}.py"
            if potential_file.exists():
                task_file = potential_file

        if not task_file or not task_file.exists():
            message("error", f"Task '{args.task_name}' not found")
            return 1

        # Remove the file
        task_file.unlink()
        message("info", f"Task '{args.task_name}' removed from workspace!")
        return 0

    except Exception as e:
        message("error", f"Failed to remove custom task: {str(e)}")
        return 1


def cmd_task_list(args) -> int:
    """List custom tasks."""
    try:
        custom_tasks = user_config.list_custom_tasks()

        if not custom_tasks:
            message("info", "No custom tasks found")
            print("  Add custom tasks with: autoclean task add <file>")
            return 0

        message("info", f"Custom tasks ({len(custom_tasks)} found):")

        for task_name, task_info in custom_tasks.items():
            print(f"\n  📝 {task_name}")
            print(f"     Description: {task_info.get('description', 'No description')}")

            if args.verbose:
                print(f"     File: {task_info['file_path']}")
                print(f"     Added: {task_info.get('added_date', 'Unknown')}")
                if task_info.get("original_path"):
                    print(f"     Original: {task_info['original_path']}")

        print(
            f"\nUse any task with: autoclean process {list(custom_tasks.keys())[0]} <data_file>"
        )
        return 0

    except Exception as e:
        message("error", f"Failed to list custom tasks: {str(e)}")
        return 1


def cmd_config(args) -> int:
    """Execute configuration management commands."""
    if args.config_action == "show":
        return cmd_config_show(args)
    elif args.config_action == "setup":
        return cmd_config_setup(args)
    elif args.config_action == "reset":
        return cmd_config_reset(args)
    elif args.config_action == "export":
        return cmd_config_export(args)
    elif args.config_action == "import":
        return cmd_config_import(args)
    else:
        message("error", "No config action specified")
        return 1


def cmd_config_show(_args) -> int:
    """Show user configuration directory."""
    config_dir = user_config.config_dir
    message("info", f"User configuration directory: {config_dir}")

    custom_tasks = user_config.list_custom_tasks()
    print(f"  • Custom tasks: {len(custom_tasks)}")
    print(f"  • Tasks directory: {config_dir / 'tasks'}")
    print(f"  • Config file: {config_dir / 'user_config.json'}")

    return 0


def cmd_config_setup(_args) -> int:
    """Reconfigure workspace location."""
    try:
        user_config.setup_workspace()
        return 0
    except Exception as e:
        message("error", f"Failed to reconfigure workspace: {str(e)}")
        return 1


def cmd_config_reset(args) -> int:
    """Reset user configuration to defaults."""
    if not args.confirm:
        message("error", "This will delete all custom tasks and reset configuration.")
        print("Use --confirm to proceed with reset.")
        return 1

    try:
        user_config.reset_config()
        message("info", "User configuration reset to defaults")
        return 0
    except Exception as e:
        message("error", f"Failed to reset configuration: {str(e)}")
        return 1


def cmd_config_export(args) -> int:
    """Export user configuration."""
    try:
        if user_config.export_config(args.export_path):
            return 0
        else:
            return 1
    except Exception as e:
        message("error", f"Failed to export configuration: {str(e)}")
        return 1


def cmd_config_import(args) -> int:
    """Import user configuration."""
    try:
        if user_config.import_config(args.import_path):
            return 0
        else:
            return 1
    except Exception as e:
        message("error", f"Failed to import configuration: {str(e)}")
        return 1


def cmd_help(_args) -> int:
    """Show elegant, user-friendly help information."""
    from autoclean.utils.branding import AutoCleanBranding
    from rich.console import Console
    from rich.panel import Panel
    from rich.columns import Columns
    from rich.table import Table
    
    console = Console()
    
    # Professional header with branding
    AutoCleanBranding.get_professional_header(console)
    console.print(f"\n{AutoCleanBranding.get_simple_divider()}")
    
    # Main help sections organized for new users
    console.print("\n[bold bright_green]🚀 Getting Started[/bold bright_green]")
    console.print("  [bright_yellow]autoclean-eeg setup[/bright_yellow]     [dim]→[/dim] Configure your workspace (run this first!)")
    console.print("  [bright_yellow]autoclean-eeg version[/bright_yellow]   [dim]→[/dim] Check system information")
    
    # Core workflow - Processing
    console.print("\n[bold bright_blue]⚡ Process EEG Data[/bold bright_blue]")
    
    # Simple usage examples
    simple_panel = Panel(
        "[green]autoclean-eeg process RestingEyesOpen data.raw[/green]\n"
        "[green]autoclean-eeg process MMN data_folder/[/green]\n"
        "[green]autoclean-eeg process ASSR experiment.edf[/green]\n\n"
        "[dim]Built-in tasks: RestingEyesOpen, RestingEyesClosed, MMN, ASSR, Chirp[/dim]",
        title="[bold]Simple Processing[/bold]",
        border_style="green",
        padding=(0, 1)
    )
    
    # Advanced usage examples
    advanced_panel = Panel(
        "[yellow]autoclean-eeg process --task RestingEyesOpen \\[/yellow]\n"
        "[yellow]  --file data.raw --output results/[/yellow]\n\n"
        "[yellow]autoclean-eeg process --task-file my_task.py \\[/yellow]\n"
        "[yellow]  --file data.raw[/yellow]\n\n"
        "[dim]Specify custom output locations and task files[/dim]",
        title="[bold]Advanced Options[/bold]",
        border_style="yellow",
        padding=(0, 1)
    )
    
    console.print(Columns([simple_panel, advanced_panel], equal=True, expand=True))
    
    # Task management workflow
    console.print("\n[bold bright_magenta]📋 Task Management[/bold bright_magenta]")
    
    task_info_panel = Panel(
        "[cyan]list-tasks[/cyan]          [dim]View all available tasks[/dim]\n"
        "[cyan]list-tasks --include-custom[/cyan]  [dim]Include your custom tasks[/dim]\n"
        "[cyan]task list[/cyan]           [dim]Show your custom tasks only[/dim]",
        title="[bold]Discover Tasks[/bold]",
        border_style="cyan",
        padding=(0, 1)
    )
    
    task_manage_panel = Panel(
        "[cyan]task add my_task.py[/cyan]  [dim]Add custom task[/dim]\n"
        "[cyan]task add my_task.py --name Custom[/cyan]  [dim]Add with custom name[/dim]\n"
        "[cyan]task remove MyTask[/cyan]   [dim]Remove custom task[/dim]",
        title="[bold]Manage Tasks[/bold]",
        border_style="cyan", 
        padding=(0, 1)
    )
    
    console.print(Columns([task_info_panel, task_manage_panel], equal=True, expand=True))
    
    # Results and configuration
    console.print("\n[bold bright_cyan]🔍 Review & Configure[/bold bright_cyan]")
    
    review_panel = Panel(
        "[cyan]review --output results/[/cyan]  [dim]Launch GUI to review results[/dim]\n"
        "[cyan]config show[/cyan]             [dim]Show configuration location[/dim]\n"
        "[cyan]config setup[/cyan]            [dim]Reconfigure workspace[/dim]",
        title="[bold]Results & Settings[/bold]",
        border_style="cyan",
        padding=(0, 1)
    )
    
    console.print(review_panel)
    
    # Quick reference table
    console.print("\n[bold]📖 Quick Reference[/bold]")
    
    ref_table = Table(show_header=True, header_style="bold blue", box=None, padding=(0, 1))
    ref_table.add_column("Command", style="cyan", no_wrap=True)
    ref_table.add_column("Purpose", style="dim")
    ref_table.add_column("Example", style="green")
    
    ref_table.add_row("process", "Process EEG data", "process RestingEyesOpen data.raw")
    ref_table.add_row("setup", "Configure workspace", "setup")
    ref_table.add_row("list-tasks", "Show available tasks", "list-tasks --include-custom")
    ref_table.add_row("review", "Review results", "review --output results/")
    ref_table.add_row("task", "Manage custom tasks", "task add my_task.py")
    ref_table.add_row("config", "Manage settings", "config show")
    ref_table.add_row("version", "System information", "version")
    
    console.print(ref_table)
    
    # Help tips
    console.print("\n[bold]💡 Pro Tips[/bold]")
    console.print("  • Get command-specific help: [bright_white]autoclean-eeg <command> --help[/bright_white]")
    console.print("  • Process entire directories: [bright_white]autoclean-eeg process TaskName folder/[/bright_white]") 
    console.print("  • Use tab completion if available in your shell")
    
    # Support section
    console.print("\n[bold]🤝 Support & Community[/bold]")
    console.print("  [blue]https://github.com/cincibrainlab/autoclean_pipeline[/blue]")
    console.print("  [dim]Report issues • Documentation • Contribute • Get help[/dim]")
    
    return 0


def cmd_tutorial(_args) -> int:
    """Show a helpful tutorial for first-time users."""
    from autoclean.utils.branding import AutoCleanBranding
    from rich.console import Console
    
    console = Console()
    
    # Use the tutorial header for consistent branding
    AutoCleanBranding.print_tutorial_header(console)
    
    console.print("\n[bold bright_green]🚀 Welcome to the AutoClean EEG Tutorial![/bold bright_green]")
    console.print("This tutorial will walk you through the basics of using AutoClean EEG.")
    console.print("\n[bold bright_yellow]Step 1: Setup your workspace[/bold bright_yellow]")
    console.print("The first step is to set up your workspace. This is where AutoClean EEG will store its configuration and any custom tasks you create.")
    console.print("To do this, run the following command:")
    console.print("\n[green]autoclean-eeg setup[/green]\n")
    
    console.print("\n[bold bright_yellow]Step 2: List available tasks[/bold bright_yellow]")
    console.print("Once your workspace is set up, you can see the built-in processing tasks that are available.")
    console.print("To do this, run the following command:")
    console.print("\n[green]autoclean-eeg list-tasks[/green]\n")

    console.print("\n[bold bright_yellow]Step 3: Process a file[/bold bright_yellow]")
    console.print("Now you are ready to process a file. You will need to specify the task you want to use and the path to the file you want to process.")
    console.print("For example, to process a file called 'data.raw' with the 'RestingEyesOpen' task, you would run the following command:")
    console.print("\n[green]autoclean-eeg process RestingEyesOpen data.raw[/green]\n")

    return 0


def main(argv: Optional[list] = None) -> int:
    """Main entry point for the AutoClean CLI."""
    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.command:
        # Show our custom 80s-style main interface instead of default help
        from autoclean.utils.branding import AutoCleanBranding
        from rich.console import Console
        
        console = Console()
        AutoCleanBranding.print_main_interface(console)
        return 0

    # Validate arguments
    if not validate_args(args):
        return 1

    # Execute command
    if args.command == "process":
        return cmd_process(args)
    elif args.command == "list-tasks":
        return cmd_list_tasks(args)
    elif args.command == "review":
        return cmd_review(args)
    elif args.command == "task":
        return cmd_task(args)
    elif args.command == "config":
        return cmd_config(args)
    elif args.command == "setup":
        return cmd_setup(args)
    elif args.command == "version":
        return cmd_version(args)
    elif args.command == "help":
        return cmd_help(args)
    elif args.command == "tutorial":
        return cmd_tutorial(args)
    else:
        parser.print_help()
        return 1


if __name__ == "__main__":
    sys.exit(main())
