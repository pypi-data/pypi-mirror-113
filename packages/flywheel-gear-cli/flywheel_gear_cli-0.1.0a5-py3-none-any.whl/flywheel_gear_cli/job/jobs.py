"""Add job commands to parser."""
from . import job_pull


def add_commands(subparsers, parsers, parents):  # pragma: no cover
    """Add job commands to parser."""
    job_parser = subparsers.add_parser("job", help="job commands")
    parsers["job"] = job_parser

    job_subparsers = job_parser.add_subparsers(title="Available job commands")

    job_pull_p = job_pull.add_command(job_subparsers, parents)
    parsers["job pull"] = job_pull_p

    return job_parser, job_subparsers
