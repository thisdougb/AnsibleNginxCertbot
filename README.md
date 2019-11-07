# Ansible, Nginx, Certbot, and EasyDNS, on DigitalOcean
Orchestration is feels like the undervalued sibling of automation.
Building automation that performs solo tasks is really useful.
But when you coordinate in concert, the real power of automation comes through.

So here's an example...

I want to setup a web server, to serve pages over https with real certificates.
Certbot can give us real certs, and I'm hosting DNS records with EasyDNS.
So I'll need to build some code to make the Cerbot DNS authentication play well with EasyDNS.

I'll setup the web server on an existing instance in DigitalOcean, so we can focus on the higher layers.


```
- hosts: web_servers
```
We want this playbook to run on our web_servers group, for now this is a single instance.
```
  roles:
    - { role: digitalocean_firewall,
        vars: {
            digitalocean_firewall_name: fw-web-servers,
            digitalocean_firewall_rule: ssh-inbound,
            digitalocean_firewall_rule_status: enable
        },
        tags: [ ssh_on ]
      }
```
The *digitalocean_firewall* role allows me to switch on and off SSH access to the hosts.
This is done through calls to DigitalOcean's management API.
It means SSH access is only made public during the playbook run, as I switch it off again at the end of the playbook.
```
    - { role: centos_certbot_easydns,
        vars: {
            centos_certbot_easydns_api: "{{ easydns_api }}",
            centos_certbot_easydns_token: "{{ easydns_token }}",
            centos_certbot_easydns_key: "{{ easydns_key }}",
            centos_certbot_easydns_domain: "{{ website_domain }}",
            centos_certbot_easydns_email: "{{ website_domain_email }}"
        },
        tags: certbot }

    - { role: centos_nginx_webserver, tags: nginx }
```
Here we are getting our certs first, and then setting up Nginx.
This keeps things nice and simple, one thing at a time.
So in the certbot role we reach over to the EasyDNS API to create validation TXT records for Certbot.

Once Certbot has done its thing, we go back to EasyDNS and delete the validation record to keep things clean.
Once the certs are in place on the filesystem, we go ahead a install/config Nginx with those certs.
```
    - { role: digitalocean_firewall,
        vars: {
            digitalocean_firewall_name: fw-web-servers,
            digitalocean_firewall_rule: ssh-inbound,
            digitalocean_firewall_rule_status: disable
        },
        tags: [ ssh_off ]
      }
```
Finally, once we're done working on the instance we switch off SSH access via the DigitalOcean API.
You can save a lot of false-alerting by preventing SSH brute-force attempts in this way.

This is orchestration, we're pulling together actions from different vendor APIs plus on-instance changes to get to our desired state.
Small and re-usable components, the simpler things are the more powerful they turn out to be.

#### Neat Things

The neat thing with all of this, is that when we want to renew our web certs we already have the code!
Just re-run this on a schedule and it'll re-run Certbot with EasyDNS API credentials (which are stored in Vault).
Code once, re-use often.

Neat thing number two is the *digitalocean_firewall* role.
Not only is it re-usable and simple, it's also very easy to extend with additional rulesets.
For example, you may want to automate some sort of data load process.
So open up access just for that process to complete, then close it off again to avoid mistakes.

I added another playbook to deploy the cert to smtp servers.
This meant upgrading the cert to include a wildcard for subdomains.
#### Author Information

[@thisdougb](https://twitter.com/thisdougb "Twitter")
