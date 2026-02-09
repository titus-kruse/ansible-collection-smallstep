# maxhoesel.smallstep.step_ssh_principal

Configures ssh host principals.

This role is more a SSHd configuration helper role instead of a wrapper for step-ca commands.

## Requirements

- The following distributions are currently supported:
  - Ubuntu 18.04 LTS or newer
  - Debian 10 or newer
  - CentOS 8 or newer

## Role Variables

### General

##### `step_ssh_principal_users`
- List of dicts for users. See documentation below.
- Default: `[]`

##### `step_ssh_principal_directory`
- Optionally set a custom path for a directory to store the users principal configuration files.
- Default: `/etc/ssh/auth_principals`

### User entry

##### `user`
- Username of local user
- Required: yes

##### `principals`
- List of principals for the user
- Default: `user:bob`


## Example Playbooks

```yaml
tasks:
- name: Configure principals on host
  ansible.builtin.include_role:
    name: maxhoesel.smallstep.step_ssh_principal
  vars:
    step_ssh_principal_users:
      - user: alice
      - principals: ['user:bob']
```
