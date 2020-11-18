import sys
import argparse
import utils as fl

parser = argparse.ArgumentParser(description="Create Connected AI Testbed")
parser.add_argument(
            "-c",
            "--core",
            type=str,
            help="Import core configuration file (.yaml)",
)
parser.add_argument(
            "-f",
            "--flexran",
            type=str,
            help="Import core configuration file (.yaml)",
)
parser.add_argument(
            "-r",
            "--ran",
            type=str,
            help="Import ran configuration file (.yaml)",
)
    
args = parser.parse_args()

if args.core:
    fl.core(args.core)

if args.flexran:
    fl.flexran(args.flexran)

if args.ran:
    fl.ran(args.ran)

