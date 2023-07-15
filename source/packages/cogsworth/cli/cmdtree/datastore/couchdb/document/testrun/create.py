
__author__ = "Myron Walker"
__copyright__ = "Copyright 2023, Myron W Walker"
__credits__ = []
__version__ = "1.0.0"
__maintainer__ = "Myron Walker"
__email__ = "myron.walker@gmail.com"
__status__ = "Development" # Prototype, Development or Production
__license__ = "MIT"

import json
import os

import click

HELP_RESULTS = "A folder containing test results to publish"
HELP_EXPIRY = "A number of days to persist the up uploaded results."

@click.command("create")
@click.option("--results", required=True, type=str, help=HELP_RESULTS)
@click.argument('filename')
def command_datastore_couchdb_publish_testrun(results: str, filename: str):
    
    if not os.path.exists(results):
        errmsg = "The specified result folder does not exist. folder={}".format(results)
        click.BadParameter(errmsg)

    # Make sure the summary document and the tests document exists
    summary_file = os.path.join(results, "testrun_summary.json")
    testresults_file = os.path.join(results, "testrun_results.jsos")

    from mojo.xmods.jsos import load_jsos_stream_from_file

    summary = None
    with open(summary_file, 'r') as sf:
        summary = json.load(sf)

    trstream = load_jsos_stream_from_file(testresults_file)

    document = {
        "summary": summary,
        "version": "1.0",
        "dtype": "testrun",
        "testresults": trstream
    }

    with open(filename, 'w') as of:
        json.dump(document, of)

    return