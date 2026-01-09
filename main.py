"""Main entry point for Convertify video converter."""

from pathlib import Path
from typing import Annotated

import typer
from rich.console import Console
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeElapsedColumn,
)
from rich.table import Table

from src.config import load_settings
from src.container import Container

app = typer.Typer(
    name="convertify",
    help="Convert AVI videos to MP4 format automatically",
    add_completion=False,
)
console = Console()


def show_results_table(results):
    """Display conversion results in a table."""
    table = Table(title="Conversion Results", show_header=True, header_style="bold magenta")
    table.add_column("File", style="cyan", no_wrap=False)
    table.add_column("Status", justify="center")
    table.add_column("Original Size", justify="right")
    table.add_column("New Size", justify="right")
    table.add_column("Reduction", justify="right")
    table.add_column("Time", justify="right")

    for result in results:
        status = "✓ Success" if result.success else "✗ Failed"
        status_style = "green" if result.success else "red"

        original_size = f"{result.original_size_mb:.2f} MB" if result.original_size_mb > 0 else "-"
        new_size = f"{result.converted_size_mb:.2f} MB" if result.converted_size_mb > 0 else "-"
        reduction = (
            f"{result.size_reduction_percent:.1f}%" if result.size_reduction_percent > 0 else "-"
        )
        duration = f"{result.duration_seconds:.1f}s" if result.duration_seconds > 0 else "-"

        table.add_row(
            result.video_file.filename,
            f"[{status_style}]{status}[/{status_style}]",
            original_size,
            new_size,
            reduction,
            duration,
        )

    console.print(table)


@app.command()
def convert(
    directories: Annotated[
        list[str] | None,
        typer.Option(
            "--dir",
            "-d",
            help="Directories to scan for AVI files (can be specified multiple times)",
        ),
    ] = None,
    lab: Annotated[
        bool,
        typer.Option(
            "--lab",
            help="Use predefined lab directories (network paths)",
        ),
    ] = False,
    remove_source: Annotated[
        bool | None,
        typer.Option(
            "--remove-source/--keep-source",
            help="Remove source AVI files after conversion",
        ),
    ] = None,
    skip_existing: Annotated[
        bool | None,
        typer.Option(
            "--skip-existing/--overwrite",
            help="Skip conversion if MP4 already exists",
        ),
    ] = None,
):
    """Convert AVI videos to MP4 format."""
    try:
        # Load settings
        settings = load_settings()

        # Override settings with CLI arguments if provided
        if lab:
            # Use predefined lab directories (UNC network paths)
            settings.conversion_directories = [
                r"\\TNAS-Click\Team-design\4. PREPARAR RESUMEN",
                r"\\TNAS-Click\Team-design\8. Base Datos Unica"
            ]
            console.print("[cyan]Using lab directories:[/cyan]")
            console.print(r"  - \\TNAS-Click\Team-design\4. PREPARAR RESUMEN")
            console.print(r"  - \\TNAS-Click\Team-design\8. Base Datos Unica")
            console.print(f"[yellow]Total directories configured: {len(settings.conversion_directories)}[/yellow]")
            import sys
            sys.stdout.flush()  # Force output when running from VBS
        elif directories:
            settings.conversion_directories = directories
        
        if remove_source is not None:
            settings.remove_source = remove_source
        if skip_existing is not None:
            settings.skip_if_exists = skip_existing

        # Validate directories - use current directory if none specified
        dirs = settings.get_conversion_directories()
        console.print(f"[yellow]Directories to process: {len(dirs)}[/yellow]")
        for idx, d in enumerate(dirs, 1):
            console.print(f"[yellow]  {idx}. {d}[/yellow]")
        
        if not dirs:
            # Use current directory as default
            dirs = [Path(".")]
            console.print(
                "[yellow]No directories specified. Using current directory.[/yellow]"
            )

        # Initialize container
        container = Container(settings)
        config = container.get_conversion_config()

        # Display configuration
        console.print("\n[bold cyan]Convertify - AVI to MP4 Converter[/bold cyan]\n")
        console.print(f"[yellow]Directories:[/yellow] {', '.join(str(d) for d in dirs)}")
        console.print(f"[yellow]Codec:[/yellow] {config.codec} (CRF: {config.crf})")
        console.print(f"[yellow]Remove source:[/yellow] {config.remove_source}")
        console.print(f"[yellow]Skip existing:[/yellow] {config.skip_if_exists}\n")

        # Execute conversion with progress bar
        use_case = container.convert_videos_use_case

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TextColumn("({task.completed}/{task.total})"),
            TimeElapsedColumn(),
            console=console,
        ) as progress:
            task = progress.add_task("[cyan]Converting videos...", total=100)

            def update_progress(current: int, total: int):
                progress.update(task, completed=current, total=total)

            results = use_case.execute(dirs, config, progress_callback=update_progress)

        # Display results
        if results:
            console.print()
            show_results_table(results)

            # Summary
            successful = sum(1 for r in results if r.success)
            failed = sum(1 for r in results if not r.success)
            total_time = sum(r.duration_seconds for r in results)

            console.print(
                f"\n[bold green]✓ Completed:[/bold green] {successful} successful, "
                f"[bold red]{failed} failed[/bold red], "
                f"[bold yellow]Total time: {total_time:.1f}s[/bold yellow]"
            )
        else:
            console.print("[yellow]No AVI files found to convert.[/yellow]")

    except KeyboardInterrupt:
        console.print("\n[yellow]Conversion cancelled by user.[/yellow]")
        raise typer.Exit(130) from None
    except Exception as e:
        console.print(f"\n[red]Error:[/red] {str(e)}")
        raise typer.Exit(1) from e


@app.command()
def version():
    """Show version information."""
    console.print("[bold cyan]Convertify[/bold cyan] version [green]2.0.0[/green]")
    console.print("Modern AVI to MP4 video converter")


if __name__ == "__main__":
    import sys

    # If no arguments provided (just running the exe), execute convert by default
    if len(sys.argv) == 1:
        sys.argv.append("convert")

    app()
