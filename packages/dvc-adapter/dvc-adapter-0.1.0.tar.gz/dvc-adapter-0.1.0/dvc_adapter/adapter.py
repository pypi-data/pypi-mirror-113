import time
import argparse
import sys
import os

from watchdog.observers import Observer

from .handler import Handler
from .logger import logger
from .oddrn import Generator

CLOUD = {
    "type": "aws",
    "region": "REGION1",
    "account": "ACC2"
}

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pipeline-path', type=str, required=True, dest="pipeline_path", help="defines the base value")
    parser.add_argument('--catalog-url', type=str, required=True, default="INFO", dest="catalog_url")
    parser.add_argument('--oddrn-prefix', type=str, required=True, default="INFO", dest="oddrn_prefix")
    # Optional
    parser.add_argument('--log-level', type=str, default="INFO", dest="log_level", help="defines log level of adapter")
    parser.add_argument('--log-file', type=str, default="None", dest="log_file", help="defines log level of adapter")
    # LOG_FILE

    # TODO:
    #  2) Logs to file,
    #  3) Logger constructor pass to Handler

    args = parser.parse_args()

    oddrn_generator = Generator(source="dvc", prefix=args.oddrn_prefix)

    if not os.path.isdir(args.pipeline_path):
        logger.error(f"No such directory exists: {args.pipeline_path}")
        sys.exit()

    handler = Handler(oddrn_generator, args.catalog_url)
    observer = Observer()

    observer.schedule(handler, path=args.pipeline_path, recursive=True)
    observer.start()

    try:
        while True:
            time.sleep(5)
    except KeyboardInterrupt:
        observer.stop()
        observer.join()