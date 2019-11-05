Role Name
=========

Add and delete firewall rulesets from DigitalOcean firewalls, via API calls.

Requirements
------------

None

Role Variables
--------------

None of these variables are set for you, so pass them in as you see fit.

Name | Default | Required | Description
--- | --- | --- | ---
digitalocean_api_token | undefined | yes | Generate an API token in the DigitalOcean console. At the very least use Ansible Vault to encrypt the variable.
digitalocean_firewall_name | undefined | yes | Name of the firewall to change rules for.
digitalocean_firewall_rule | undefined | yes | Example shows ssh-inbound, use this var to refer to the imported .json file containing the rulset. You must supply the ruleset with matching name in the files directory, eg: ./files/ssh-inbound-rule.json.
digitalocean_firewall_rule_status | undefined | no | The default action, when undefined, is to run the DELETE rules task.

Dependencies
------------

None

Example Playbook
----------------

Here is an example of enabling ssh access, doing some work, and then disabling ssh access:

```
- hosts: web_servers

  roles:
    - { role: digitalocean_firewall,
        vars: {
            digitalocean_firewall_name: fw-web-servers,
            digitalocean_firewall_rule: ssh-inbound,
            digitalocean_firewall_rule_status: enable
        }
      }

    - { role: certbot_update }

    - { role: digitalocean_firewall,
        vars: {
            digitalocean_firewall_name: fw-web-servers,
            digitalocean_firewall_rule: ssh-inbound,
            digitalocean_firewall_rule_status: disable
        }
      }
```

License
-------

MIT / BSD

Author Information
------------------

@thisdougb
