"""
Intended entry point of the application's CLI.

Please use the following command to run the CLI: `python3 -m cli`
"""

from . import __main__
from cli.app import main

if __name__ == "__main__":
    main()
