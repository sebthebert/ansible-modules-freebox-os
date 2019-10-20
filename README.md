# Ansible modules for Freebox OS

## Before using Freebox OS Ansible modules

You need to configure your Freebox to accept API requests.

Launch the ['ìnitialize.yml' playbook](initialize.yml) and accept the request on your Freebox LCD Screen.

Then, go to `Parametres de la Freebox > Divers / Gestion des Acces > Applications`

and check `Modification des reglages de la Freebox`.

![test](freebox_gestion_acces_applications.png "Check 'Modification des reglages de la Freebox'")

## Modules

### Module 'freebox_os_switch_port'

Usage:

```yaml
# Configure Freebox Router port '2' with 'full' duplex and speed '1000'
- name: Configure port '2' with 'full' duplex and speed '1000'
  freebox_os_switch_port:
    id: 2
    duplex: 'full'
    speed: 1000
```
