Role Name
=========

Switch the SELinux state and policy, rebooting when changed.

Requirements
------------

None.

Role Variables
--------------

Name | Default | Required | Description
--- | --- | --- | ---
centos_selinux_state | disabled | no | disabled, permissive, enforcing
centos_selinux_policy | undefined | when state!=disabled | targeted, minimum, mls
Dependencies
------------

Example Playbook
----------------

```
- hosts: smtp

  roles:
    - { role: centos_selinux,
        vars: {
            centos_selinux_state: disabled  # for demo only
        },
        tags: selinux }
```

License
-------

MIT / BSD

Author Information
------------------

[@thisdougb](https://twitter.com/thisdougb "Twitter")
