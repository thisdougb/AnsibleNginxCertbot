Role Name
=========

Setup Dovecot with some users, and server imaps/pop3s using Certbot certs.

Requirements
------------

The centos_certbot_easydns role should have run and put certs in the right place.

Role Variables
--------------
The *mail_server* variable is used for the certificate path, aligning with the centos_certbot_easydns role.
```
mail_server_domainname: mydomain.com
```
Then we have a list of mailboxes.
The passwords are stored encrypted on the mail host.
As coded, the role expects logins to be email addresses.
```
dovecot_mailboxes:
  - login: first.last@mydomain.com
    password: e3dhvFGHE_48sndow
```

Dependencies
------------

None.

Example Playbook
----------------

```
- hosts: smtp

  roles:
    - { role: centos_dovecot_tls,
        vars: {
            dovecot_tls_server_domainname: "{{ mail_server_domainname }}"
        },
        tags: dovecot }
```

License
-------

MIT / BSD

Author Information
------------------

[@thisdougb](https://twitter.com/thisdougb "Twitter")
