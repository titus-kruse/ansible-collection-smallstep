# maxhoesel.smallstep.step_ca_root

Download the root certificate from a CA.

This role uses `step-cli` to download the certificate from the configured CA.

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

##### `step_bootstrap_ca_url`
- URL of the `step-ca` CA
- Example: https://myca.localdomain

##### `step_bootstrap_fingerprint`
- Fingerprint of the CA root cert
- This is used to verify the authenticity of the remote CA

### Certificate

##### `step_ca_root_certfile`
- Details about the cert file on disk
- Is a dict with the following elements:
  - `path`: Absolute path to the cert file. Defaults to `/etc/ssl/root.crt`. The directory must already exist.
  - `mode`: File mode for the cert file. Defaults to `644` for the cert.
  - `owner`/`group`: Owner and group of the file. Defaults to root.

## Example Playbooks

```yaml
- hosts: clients
  tasks:
    # This will download the certificate to /etc/step/root.crt that you can then use in other applications.
    # See the step_ca_root README for more options
    - role: maxhoesel.smallstep.step_ca_root
      vars:
        step_bootstrap_ca_url: https://myca.localdomain
        step_bootstrap_fingerprint: your CAs fingerprint
        step_ca_root_certfile:
          path: /etc/step/root.crt
      become: yes
```
