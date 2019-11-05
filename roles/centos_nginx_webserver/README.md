Role Name
=========

Install Nginx with a basic non-TLS config and a holding page, on Centos in particular.

Requirements
------------

None.

Role Variables
--------------

Name | Default | Required | Description
--- | --- | --- | ---
centos_nginx_webserver_name | mywebsite.com | yes | The name of the website to server traffic for.
centos_nginx_webserver_root | /var/www | yes | Where the website exists on the filesystem, in a subdir here.

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
