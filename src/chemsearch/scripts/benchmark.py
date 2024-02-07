import argparse
import asyncio
from datetime import datetime
from pathlib import Path
from random import seed, shuffle

from pyprojroot import here
from tqdm import tqdm

from chemsearch import io, utils
from chemsearch.constants import Events, Queries
from chemsearch.logging import get_logger
from chemsearch.query import query_cluster
from chemsearch.urls import construct_substructure_search_url


def parse_args() -> argparse.Namespace:
    """Parse arguments from command line.

    Returns:
        argparse.Namespace: Parsed arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-q",
        "--queries",
        help="SMI file to read query molecules from.",
        required=True,
        type=Path,
    )
    parser.add_argument(
        "-l",
        "--log-file",
        help="Filepath to write logs to.",
        default=here()
        / "logs"
        / f"app_{datetime.now().strftime('%Y_%m_%d_%H_%M_%S.log')}",
        type=Path,
    )
    parser.add_argument(
        "-n",
        "--dns-name",
        help="DNS name of service for cluster.",
        required=True,
        type=str,
    )
    parser.add_argument(
        "-p",
        "--port",
        help="Port that containers are listening on.",
        type=int,
        default=5000,
    )
    parser.add_argument(
        "-f",
        "--format",
        help="Format of query strings.",
        default=Queries.SMILES,
        type=Queries,
    )
    parser.add_argument(
        "--seed",
        help="Seed for shuffling queries.",
        default=None,
        type=int,
    )

    args = parser.parse_args()

    return args


def main():
    """Entry point for script."""
    args = parse_args()

    if args.seed is not None:
        seed(args.seed)

    queries = io.read_smi_file(args.queries)
    shuffle(queries)

    # Start with dummy query to load app dependencies
    queries.insert(0, "C")

    logger = get_logger(args.log_file)

    print("Getting IP addresses to query.")
    ip_addresses = utils.get_ip_addresses(args.dns_name, args.port)

    for address in ip_addresses:
        print(address)

    print("\nQuerying cluster:")
    for query in tqdm(queries):
        urls = [
            construct_substructure_search_url(
                address, args.port, query, args.format, persist=True
            )
            for address in ip_addresses
        ]

        duration, hits = utils.time_func(asyncio.run)(query_cluster(urls))

        logger.info(
            event=Events.completed_get,
            query=query,
            duration=duration,
            hits=sum(i["count"] for i in hits),
        )


if __name__ == "__main__":
    main()
