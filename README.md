# Ansible, Nginx, Certbot, and EasyDNS, on DigitalOcean
Orchestration is feels like the undervalued sibling of automation.
Building automation that performs solos is really useful, but when you coordinate in concert the real power of automation comes through.

So here's a demo...

I want to setup a web server, to serve pages over https.
I'll run the web server on an existing instance in DigitalOcean, so we can focus on the higher layers.


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
    - { role: centos_nginx_webserver, tags: nginx }
    - { role: centos_nginx_certbot_easydns, tags: certbot }
```
Here we are setting up nginx, and then updating its certificates with Certbot.
So we're doing some on-instance ssh'ing, and then reaching over to the EasyDNS API to create validation records for Certbot.
Once Certbot has done its thing, we go back to EasyDNS and delete the validation record.
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
Turning on SSH access only during playbook execution is strangely something the security-wonks haven't woken up to yet.

This is orchestration, we're pulling together actions from two different vendor APIs and on-instance changes to get to our desired state.
Small and re-usable components, the simpler things are the more powerful they turn out to be.