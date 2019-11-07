Role Name
=========

Installs Certbot, and drops EasyDNS hook scripts into /tmp and attempts to get certificates with EasyDNS validation.

Note, the certificate will include the domain and a wildcard for subdomains.

Requirements
------------

You will need EasyDNS API tokens, as env vars like this:

Role Variables
--------------

Name | Default | Required | Description
--- | --- | --- | ---
centos_certbot_easydns_api | undefined | yes | The EasyDNS API URL.
centos_certbot_easydns_token | undefined | yes | Your EasyDNS API Token.
centos_certbot_easydns_key | undefined | yes | Your EasyDNS API Key.
centos_certbot_easydns_domain | undefined | yes | The domain you want certificates for.
centos_certbot_easydns_email | undefined | yes | The email address for LetEncrypt notifications.

Dependencies
------------

None.

Example Playbook
----------------

```
- hosts: web_servers

  roles:
    - { role: centos_certbot_easydns, tags: certbot }
```

Logs are recorded by Certbot and by the web-hook scripts:

```
/var/log/letsencrypt/letsencrypt.log
/tmp/certbot_easydns.log
```

License
-------

MIT / BSD

Author Information
------------------

[@thisdougb](https://twitter.com/thisdougb "Twitter")
