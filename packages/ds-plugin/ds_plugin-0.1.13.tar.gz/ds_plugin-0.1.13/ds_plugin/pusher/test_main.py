import os
import click
import logging
import json
import main_copy

def main(parameters):
    params = json.loads(parameters) if parameters is not None or parameters != "" else ""
    logging.info("pusher main params: %s", params)
    try:
        main_copy.execute(
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
        logging.error("Execute has error: %s", e)