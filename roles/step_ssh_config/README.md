# maxhoesel.smallstep.step_ssh_config

Configures SSH to be used with certificates.

This role uses `step-cli` to execute step ssh config command.

## Requirements

- The following distributions are currently supported:
  - Ubuntu 18.04 LTS or newer
  - Debian 10 or newer
  - CentOS 8 or newer
- Users or hosts should be bootstrapped with `step_bootstrap_host` and the user must be able to access the CA.

## Role Variables

### General

##### `step_cli_executable`
- Path or name of the step-cli executable to use for executing commands in this role
- Can be an absolute path or a command (make sure the executable is in $PATH) for all users
- Default: `step-cli`

##### `step_ssh_config_user`
- Username of the user the SSH certificate will be sign. Should be `root` for host or any other existing user for user certificates.
- Default: `root`

##### `step_ssh_config_steppath`
- Optionally set a custom `$STEPPATH` from which to read the step config
- Example: `/root/.step/`
- Default: `$HOME/.step`

### Optional arguments

(To Do)

## Example Playbooks

```yaml
# Let host trust our CA
- hosts: server
  tasks:
    ansible.builtin.import_role:
      name: maxhoesel.smallstep.step_ssh_config
    vars:
      step_ssh_config_roots: true
```

```yaml
# Let user trust our host
- hosts: client
  tasks:
    ansible.builtin.import_role:
      name: maxhoesel.smallstep.step_ssh_config
    vars:
      step_ssh_config_roots: true
      step_ssh_config_host: true
      step_ssh_config_user: bob
      step_ssh_config_steppath: /home/bob/.step
```
