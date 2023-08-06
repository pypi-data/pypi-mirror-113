"""
This is a skeleton file that can serve as a starting point for a Python
console script. To run this script uncomment the following lines in the
``[options.entry_points]`` section in ``setup.cfg``::

    console_scripts =
         clisycp = clisy.skeleton:run

Then run ``pip install .`` (or ``pip install -e .`` for editable mode)
which will install the command ``clisycp`` inside your current environment.

Besides console scripts, the header (i.e. until ``_logger``...) of this file can
also be used as template for Python modules.

Note:
    This skeleton file can be safely removed if not needed!

References:
    - https://setuptools.readthedocs.io/en/latest/userguide/entry_point.html
    - https://pip.pypa.io/en/stable/reference/pip_install
"""

import argparse
import logging
import sys

__author__ = "Nilesh Kumar"
__copyright__ = "Nilesh Kumar"
__license__ = "MIT"

from clisy.searcher.clisyfactory import ClisyFactory
from clisy.searcher.searchoptions import SearchOptions

_logger = logging.getLogger(__name__)


# ---- CLI ----
# The functions defined in this section are wrappers around the main Python
# API allowing them to be called directly from the terminal as a CLI
# executable/script.


def parse_args(args):
    """Parse command line parameters

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--help"]``).

    Returns:
      :obj:`argparse.Namespace`: command line parameters namespace
    """
    return get_parser().parse_args(args)


def get_parser():
    parser = argparse.ArgumentParser(
        description="A command line utility to open browser for when you want to search something across various "
                    "search options")
    add_mutually_exclusive_group(parser)
    add_optional_arg_v(parser)
    add_optional_arg_vv(parser)
    return parser


def add_optional_arg_vv(parser):
    parser.add_argument(
        "-vv",
        "--very-verbose",
        dest="loglevel",
        help="set loglevel to DEBUG",
        action="store_const",
        const=logging.DEBUG,
    )


def add_optional_arg_v(parser):
    parser.add_argument(
        "-v",
        "--verbose",
        dest="loglevel",
        help="set loglevel to INFO",
        action="store_const",
        const=logging.INFO,
    )


def add_mutually_exclusive_group(parser):
    mutually_exclusive_group = parser.add_mutually_exclusive_group()
    mutually_exclusive_group.add_argument(
        "--ddg",
        "--duck-duck-go",
        dest="ddg",
        type=str,
        required=False,
        metavar="<query_string>",
        help="Search in DuckDuckGo"
    )
    mutually_exclusive_group.add_argument(
        "-g",
        "--google",
        dest="g",
        type=str,
        required=False,
        metavar="<query_string>",
        help="Search in Google"
    )
    mutually_exclusive_group.add_argument(
        "-w",
        "--wikipedia",
        dest="w",
        type=str,
        required=False,
        metavar="<query_string>",
        help="Search in Wikipedia"
    )
    mutually_exclusive_group.add_argument(
        "--wc",
        "--wirecutter",
        dest="wc",
        type=str,
        required=False,
        metavar="<query_string>",
        help="Search in Wirecutter"
    )
    mutually_exclusive_group.add_argument(
        "-a",
        "--amazon",
        dest="a",
        type=str,
        required=False,
        metavar="<query_string>",
        help="Search in Amazon"
    )
    mutually_exclusive_group.add_argument(
        "--cci",
        "--creative-commons-image",
        dest="cci",
        type=str,
        required=False,
        metavar="<query_string>",
        help="Image Search in Creative Commons"
    )
    mutually_exclusive_group.add_argument(
        "--imdb",
        dest="imdb",
        type=str,
        required=False,
        metavar="<query_string>",
        help="Search in IMDb"
    )
    mutually_exclusive_group.add_argument(
        "--sw",
        "--swiggy",
        dest="sw",
        type=str,
        required=False,
        metavar="<query_string>",
        help="Search in Swiggy"
    )


def setup_logging(loglevel):
    """Setup basic logging

    Args:
      loglevel (int): minimum loglevel for emitting messages
    """
    logformat = "[%(asctime)s] %(levelname)s:%(name)s:%(message)s"
    logging.basicConfig(
        level=loglevel, stream=sys.stdout, format=logformat, datefmt="%Y-%m-%d %H:%M:%S"
    )


def main(args):
    """Wrapper allowing to be called with string arguments in a CLI fashion

    Instead of returning the value from, it prints the result to the
    ``stdout`` in a nicely formatted message.

    Args:
      args (List[str]): command line parameters as list of strings
          (for example  ``["--verbose", "test"]``).
    """
    args = parse_args(args)
    setup_logging(args.loglevel)

    _logger.debug("Starting crazy search...")
    try:
        if args.ddg:
            ClisyFactory(SearchOptions.DUCKDUCKGO).get_searcher().open(query_string=args.ddg)
        elif args.g:
            ClisyFactory(SearchOptions.GOOGLE).get_searcher().open(query_string=args.g)
        elif args.w:
            ClisyFactory(SearchOptions.WIKIPEDIA).get_searcher().open(query_string=args.w)
        elif args.wc:
            ClisyFactory(SearchOptions.WIRECUTTER).get_searcher().open(query_string=args.wc)
        elif args.a:
            ClisyFactory(SearchOptions.AMAZON).get_searcher().open(query_string=args.a)
        elif args.cci:
            ClisyFactory(SearchOptions.CREATIVE_COMMONS_IMAGE).get_searcher().open(query_string=args.cci)
        elif args.imdb:
            ClisyFactory(SearchOptions.IMDB).get_searcher().open(query_string=args.imdb)
        elif args.sw:
            ClisyFactory(SearchOptions.SWIGGY).get_searcher().open(query_string=args.sw)
        else:
            ClisyFactory(SearchOptions.DUCKDUCKGO).get_searcher().open(query_string=args.query_string)
    except Exception as ex:
        _logger.error("You provided an incorrect option to search. Here is the error message : %r", ex)
        raise

    _logger.info("Script ends here")


def run():
    """Calls :func:`main` passing the CLI arguments extracted from :obj:`sys.argv`

    This function can be used as entry point to create console scripts with setuptools.
    """
    main(sys.argv[1:])


if __name__ == "__main__":
    # ^  This is a guard statement that will prevent the following code from
    #    being executed in the case someone imports this file instead of
    #    executing it as a script.
    #    https://docs.python.org/3/library/__main__.html

    # After installing your project with pip, users can also run your Python
    # modules as scripts via the ``-m`` flag, as defined in PEP 338::
    #
    #     python -m clisy.skeleton
    #
    run()
