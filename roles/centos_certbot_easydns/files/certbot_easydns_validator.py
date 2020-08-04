#!/usr/bin/env python3
"""Certbot DNS Validation With EasyDNS.

This is a validation hook for EasyDNS, used by Certbot during certification creation.

$ certbot certonly --manual
                   --preferred-challenges=dns
                   --manual-auth-hook certbot_easydns_validator.py
                   --manual-cleanup-hook certbot_easydns_cleanup.py
                   -d <domain.name>
                   --dry-run
                   --test-cert
"""

import json
import logging
import time
import os
import requests


logging.basicConfig(filename='/tmp/certbot_easydns.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

logging.info("certbot_easydns_validator(): Running Certbot DNS validation through EasyDNS.")

try:
    CERTBOT_DOMAIN = os.environ['CERTBOT_DOMAIN']
    CERTBOT_VALIDATION_STRING = os.environ['CERTBOT_VALIDATION']

    EASYDNS_API = os.environ['EASYDNS_API']
    EASYDNS_TOKEN = os.environ['EASYDNS_TOKEN']
    EASYDNS_KEY = os.environ['EASYDNS_KEY']

except KeyError as error:
    logging.error("certbot_easydns_validator(): %s is not defined as an environment var, exiting.",
                  error)
    exit(1)

# add the TXT record
URL = "{0}/zones/records/add/{1}/txt?format=json".format(EASYDNS_API, CERTBOT_DOMAIN)
DATA = {
    "rdata": CERTBOT_VALIDATION_STRING,
    "host": "_acme-challenge"
}
logging.info("certbot_easydns_validator(): API request %s", URL)
API_RESPONSE = requests.put(URL, auth=(EASYDNS_TOKEN, EASYDNS_KEY), data=DATA)
logging.info(json.dumps(API_RESPONSE.json(), indent=2))

if API_RESPONSE.status_code == 201:
    RESPONSE_CONTENT = API_RESPONSE.json()

    TMP_FILE = "/tmp/{0}.certbot".format(CERTBOT_DOMAIN)
    with open(TMP_FILE, 'w') as tmp_fh:
        tmp_fh.write(RESPONSE_CONTENT['data']['id'])

    logging.info("certbot_easydns_validator(): Finished writing validation record to EasyDNS, sleeping 10s then exit.")
    time.sleep(10)  # sleep because this is part of a Certbot script chain, so let DNS update
    exit(0)

else:
    logging.error("certbot_easydns_validator(): [ERROR] API_RESPONSE was %s, exiting.",
                  API_RESPONSE.status_code)
    exit(1)
