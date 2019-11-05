#!/usr/bin/env python
"""Certbot DNS Cleanup With EasyDNS.

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
import os
import requests


logging.basicConfig(filename='/tmp/certbot_easydns.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)

logging.info("certbot_easydns_cleanup(): Running Certbot DNS cleanup through EasyDNS.")

try:
    CERTBOT_DOMAIN = os.environ['CERTBOT_DOMAIN']
    CERTBOT_VALIDATION_STRING = os.environ['CERTBOT_VALIDATION']

    EASYDNS_API = os.environ['EASYDNS_API']
    EASYDNS_TOKEN = os.environ['EASYDNS_TOKEN']
    EASYDNS_KEY = os.environ['EASYDNS_KEY']

except KeyError as error:
    logging.error("certbot_easydns_cleanup(): %s is not defined as an environment var, exiting.",
                  error)
    exit(1)

TMP_FILE = "/tmp/{0}.certbot".format(CERTBOT_DOMAIN)
with open(TMP_FILE) as tmp_fh:
    FILE_CONTENT = tmp_fh.readlines()

if len(FILE_CONTENT) == 1:
    RECORD_ID = FILE_CONTENT[0].strip()
    logging.info("certbot_easydns_cleanup(): deleting record %s", RECORD_ID)

    URL = "{0}/zones/records/{1}/{2}?format=json".format(EASYDNS_API, CERTBOT_DOMAIN, RECORD_ID)

    API_RESPONSE = requests.delete(URL, auth=(EASYDNS_TOKEN, EASYDNS_KEY))
    logging.info(json.dumps(API_RESPONSE.json(), indent=2))

    if API_RESPONSE.status_code != 200:
        logging.error("certbot_easydns_cleanup(): DNS record failed to delete correctly, exiting.")
        exit(1)

logging.info("certbot_easydns_cleanup(): Finished running Certbot DNS cleanup through EasyDNS.")
