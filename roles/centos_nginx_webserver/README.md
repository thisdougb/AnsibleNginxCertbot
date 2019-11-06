Role Name
=========

Install Nginx and a holding page, on Centos in particular.

* with HTTP redirecting to HTTPS
* expects certificate files to be available

Requirements
------------

None.

Role Variables
--------------

Name | Default | Required | Description
--- | --- | --- | ---
centos_nginx_webserver_name | mywebsite.com | yes | The name of the website to server traffic for.
centos_nginx_webserver_root | /var/www | yes | Where the website exists on the filesystem, in a subdir here.
centos_nginx_webserver_cert_path | undefined | yes | Path to the cert files (eg, /etc/letsencrypt/live/).

Dependencies
------------

None.

Example Playbook
----------------

```
- hosts: web_servers

  roles:
    - { role: centos_nginx_webserver, tags: nginx }
```

License
-------

MIT / BSD

Author Information
------------------

[@thisdougb](https://twitter.com/thisdougb "Twitter")
