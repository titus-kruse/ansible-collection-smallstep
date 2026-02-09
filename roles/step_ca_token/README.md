# maxhoesel.smallstep.step_ca_token

Generate an OTT granting access to the CA.

This role uses `step-cli` to generate tokens by configured CA.

## Requirements

- The following distributions are currently supported:
  - Ubuntu 18.04 LTS or newer
  - Debian 10 or newer
  - CentOS 8 or newer
- This role requires root access. Make sure to run this role with `become: yes` or equivalent
- The host should be bootstrapped with `step_bootstrap_host` and the root user must be able to access the CA.

## Role Variables

### General

##### `step_cli_executable`
- Path or name of the step-cli executable to use for executing commands in this role
- Can be an absolute path or a command (make sure the executable is in $PATH) for all users
- Default: `step-cli`

##### `step_cli_steppath`
- Optionally set a custom `$STEPPATH` from which to read the step config
- Example: `/etc/step-cli`
- Default: `/root/.step/`

### CA

(To Do)

### Token

(To Do)

## Example Playbooks

```yaml
- hosts: clients
  tasks:
    # This will generate an OTT granting access to the CA
    # See the step_ca_token README for more options
    - role: maxhoesel.smallstep.step_ca_token
      vars:
        step_ca_token_subject: "{{ ansible_fqdn }}"
        step_ca_token_provisioner: jwk
        step_ca_token_provisioner_password: "secret"
      debug:
        var: step_ca_token_result
```
