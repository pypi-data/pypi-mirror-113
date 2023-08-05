import os
import click
import logging
import json
from ds_plugin.pusher.main_copy import Pusher

def main(parameters):
    params = json.loads(parameters) if parameters is not None or parameters != "" else ""
    logging.info("pusher main params: %s", params)
    try:
        pusher = Pusher()
        pusher.execute(
            params['converted_model'],
            params['validate_samples'],
            params['output'],
            params['model_name'],
            params['namespace'],
            params['target'],
            params['local_emb'],
            params['validate_accuracy'],
            params['validate_rate'],
            params['cyclone_wait_timeout'],
            params['out_meta'],
        )
    except Exception as e:
        logging.error("Execute has exception: %s", e)
    except OSError as err:
        logging.error("Execute has oserror: %s", err)
    except ValueError as verr:
        logging.error("Execute has valueerror: %s", verr)