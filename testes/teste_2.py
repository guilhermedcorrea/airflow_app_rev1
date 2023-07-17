
from __future__ import print_function

import sys
from random import random
from operator import add

from livy.client import HttpClient

if __name__ == "__main__":
    """
        Usage: pi_app [livy url] [slices]

        To run this Python script you need to install livy-python-api-*version*.tar.gz with
        easy_install first.

        python /pathTo/pi_app.py http://<livy-server>:8998 2
    """

    if len(sys.argv) != 3:
        print("Usage: pi_app <livy url> <slices>", file=sys.stderr)
        exit(-1)

    slices = int(sys.argv[2])
    samples = 100000 * slices

    client = HttpClient(sys.argv[1])

    def f(_):
        x = random() * 2 - 1
        y = random() * 2 - 1
        return 1 if x ** 2 + y ** 2 <= 1 else 0

    def pi_job(context):
        count = context.sc.parallelize(range(1, samples + 1), slices).map(f).reduce(add)
        return 4.0 * count / samples

    pi = client.submit(pi_job).result()

    print("Pi is roughly %f" % pi)
    client.stop(True)