import logging
from pprint import pprint

from q_sdk.main import QApi


def main():
    q = QApi(username="omikron", password="Hallo-123", uri="http://127.0.0.1:8000/api/v1", verify=False)
    q.authenticate()
    pprint(q.time_period_get())


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    main()
