# maxhoesel.smallstep.step_ssh_cert

Sign a SSH certificate using the SSH CA.

This role uses `step-cli` to generate tokens by configured CA.

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

##### `step_ssh_cert_user`
- Username of the user the SSH certificate will be sign. Should be `root` for host or any other existing user for user certificates.
- Default: `root`

##### `step_ssh_cert_steppath`
- Optionally set a custom `$STEPPATH` from which to read the step config
- Example: `/root/.step/`
- Default: `$HOME/.step`

### Required arguments

##### `step_ssh_cert_keyid`
- The certificate identity. If no principals are passed key-id will be used as a principal, if it has the format abc@def then the principal will be abc.
- Example: `bob`

##### `step_ssh_cert_keyfile`
- The private key name when generating a new key pair, or the public key path when we are just signing it.
- Example: `id_ecdsa`

##### `step_ssh_cert_ca_provisioner`
- Name of the provisioner on the CA that will issue the certificate
- Example: `jwk`

### Optional arguments

(To Do)

## Example Playbooks

```yaml
# This will issue a SSH host certificate to sign an existing host key
- hosts: server
  tasks:
    ansible.builtin.include_role:
      name: maxhoesel.smallstep.step_ssh_cert
    vars:
      step_ssh_cert_host: yes
      step_ssh_cert_ca_provisioner: "jwk"
      step_ssh_cert_ca_provisioner_password: "secret"
      step_ssh_cert_keyid: "server.example.com"
      step_ssh_cert_keyfile: "/etc/ssh/ssh_host_ecdsa_key.pub"
      step_ssh_cert_sign: yes
```

```yaml
# This will generate a key pair and issue a SSH user certificate
- hosts: client
  tasks:
    ansible.builtin.include_role:
      name: maxhoesel.smallstep.step_ssh_cert
    vars:
      step_ssh_cert_host: no
      step_ssh_cert_ca_provisioner: "jwk"
      step_ssh_cert_ca_provisioner_password: "secret"
      step_ssh_cert_keyid: "bob@client.example.com"
      step_ssh_cert_keyfile: "id_ecdsa"
      step_ssh_cert_sign: no
      step_ssh_cert_no_password: yes
      step_ssh_cert_insecure: yes
      step_ssh_cert_user: "bob"
```
