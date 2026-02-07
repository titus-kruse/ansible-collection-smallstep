#!/usr/bin/python

# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

DOCUMENTATION = r"""
---
module: step_ssh_certificate
author: Titus Kruse <mail@tituskruse.de>
short_description: Sign a SSH certificate using the SSH CA
version_added: '0.25.0'
description: >
    Creates, updates, revokes or deletes a SSH key pair and creates a certificate. on the target system.
    This module exposes mostly the same parameters as the upstream
    L(step ssh certificate,https://smallstep.com/docs/step-cli/reference/ssh/certificate)
    and L(step ssh revoke,https://smallstep.com/docs/step-cli/reference/ssh/revoke/) commands, depending on the selected
    certificate I(state).
notes:
  - Check mode is supported.
  - This module currently not supports all options provided by step-cli command.
  - Revoke and delete of certtificates not tested yet.
options:
  ca_url:
    description: URI of the targeted Step Certificate Authority
    type: str
  comment:
    description: The comment used when adding the certificate to an agent. Defaults to the subject if not provided.
    type: str
  console:
    description: Complete the flow while remaining inside the terminal
    type: bool
  crt_file:
    description: File to write the certificate (PEM format).
    type: path
  curve:
    aliases:
      - crv
    description: >
      The elliptic curve to use for EC and OKP key types. Corresponds to the "crv" JWK parameter.
      Valid curves are defined in JWA RFC7518. If unset, default is P-256 for EC keys and Ed25519 for OKP keys.
    type: str
    choices:
      - P-256
      - P-384
      - P-521
      - Ed25519
  force:
    description: >
        If I(true) and I(state=present), a new certificate will be generated each time this module is executed,
        regardless of existing certificates.
    type: bool
  host:
    description: Create a host certificate instead of a user certificate.
    type: bool
  host_id:
    description: Specify a UUID to identify the host rather than using an auto-generated UUID. If "machine" is passed, derive a UUID from "/etc/machine-id."
    type: uuid
  insecure:
    description: >
        Option no_password requires this insecure flag.
    type: bool
  k8ssa_token_path:
    description: Configure the file from which to read the kubernetes service account token.
    type: path
  key_file:
    description: The private key name when generating a new key pair, or the public key path when we are just signing it.
    type: path
  key_id:
    description: The certificate identity. If no principals are passed we will use the key-id as a principal, if it has the format abc@def then the principal will be abc.
    type: list
  kms:
    description: The uri to configure a Cloud KMS or an HSM.
    type: str
  kty:
    description: >
      The kty to build the certificate upon. If unset, default is EC. I(kty) is a case-sensitive string.
    type: str
    choices:
      - EC
      - OKP
      - RSA
  nebula_cert:
    description: Certificate file in PEM format to store in the 'nebula' header of a JWT.
    type: path
  nebula_key:
    description: >
      Private key file, used to sign a JWT,
      corresponding to the certificate that will be stored in the 'nebula' header.
    type: path
  no_password:
    description: >
        Encrypt a private key without passwird. Sensitive key material will be written to disk unencrypted. This is not recommended.
    type: bool
  not_after:
    description: >
      The time/duration when the certificate validity period ends. If a time is used it is expected to be in RFC 3339 format.
      If a duration is used, it is a sequence of decimal numbers, each with optional fraction and a unit suffix,
      such as "300ms", "-1.5h" or "2h45m". Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".
    type: str
  not_before:
    description: >
      The time/duration when the certificate validity period starts. If a time is used it is expected to be in RFC 3339 format.
      If a duration is used, it is a sequence of decimal numbers, each with optional fraction and a unit suffix,
      such as "300ms", "-1.5h" or "2h45m". Valid time units are "ns", "us" (or "µs"), "ms", "s", "m", "h".
    type: str
  principal:
    description: Add the specified principals (user or host names) to the certificate request.
    type: list
    elements: str
  private_key:
    description: When signing an existing public key, use this flag to specify the corresponding private key so that the pair can be added to an SSH Agent.
    type: path
  password_file:
    description: >
        The path to the file containing the password to encrypt the private key.
    type: path
  provisioner:
    aliases:
      - issuer
    description: The provisioner name to use. Required if I(state=present).
    type: str
  provisioner_password:
    description: >
      The password to decrypt the one-time token generating key.
      Will be passed to step-cli through a temporary file.
      Mutually exclusive with I(provisioner_password_file)
    type: str
  provisioner_password_file:
    description: >
        The path to the file containing the password to decrypt the one-time token generating key.
        Mutually exclusive with I(provisioner_password)
    type: path
  revoke_on_delete:
    description: If I(state=absent), attempt to revoke the certificate before deleting it
    type: bool
    default: true
  revoke_reason:
    description: >
        The string representing the reason for which the cert is being revoked.
        Only has an effect if I(state=revoked) or I(state=absent) and I(revoke_on_delete=True)
    type: str
  revoke_reason_code:
    description: >
        The reasonCode specifies the reason for revocation - chose from a list of common revocation reasons.
        If unset, the default is Unspecified.
        See U(https://smallstep.com/docs/step-cli/reference/ca/revoke) for a list of codes
    type: str
  serial:
    description: The serial number of the SSH certificate to revoke.
    type: str
  set:
    description: The key=value pair with template data variables to send to the CA. Must be a list.
    type: list
    elements: str
  set_file:
    description: The path of a JSON file with the template data to send to the CA.
    type: path
  sign:
    description: Sign the public key passed as an argument instead of creating one.
    type: bool
  size:
    description: >
      The size (in bits) of the key for RSA and oct key types. RSA keys require a minimum key size of 2048 bits.
      If unset, default is 2048 bits for RSA keys and 128 bits for oct keys.
    type: int
  state:
    description: >
        State that the certificate should be in.
        If I(state=present), the certificate will be (re-)issued if it doesn't exist, is invalid/expired or if its SAN/private key parameters change.
        If I(state=revoked), the certificate will be revoked with the CA
        If I(state=absent), the certificate will be removed from the host (and optionally revoked with the CA beforehand, see I(revoke_on_delete).
    type: str
    choices:
      - present
      - revoked
      - absent
    default: present
  token:
    description: The one-time token used to authenticate with the CA in order to create the certificate.
    type: str
  x5c_cert:
    description: Certificate (chain) in PEM format to store in the 'x5c' header of a JWT.
    type: str
  x5c_key:
    description: Private key path, used to sign a JWT, corresponding to the certificate that will be stored in the 'x5c' header.
    type: path

extends_documentation_fragment:
  - maxhoesel.smallstep.cli_executable
  - maxhoesel.smallstep.ca_connection
"""

EXAMPLES = r"""
# See https://smallstep.com/docs/step-cli/reference/ssh/certificate/ for more examples
- name: Generate a new SSH key pair and user certificate
  maxhoesel.smallstep.step_ssh_certificate:
    key_id: "mariano@work"
    key_file: "id_ecdsa"
"""
import os

from pathlib import Path
from typing import cast, Dict, Any

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.validation import check_required_if, check_mutually_exclusive

from ..module_utils.params.ca_connection import CaConnectionParams
from ..module_utils.cli_wrapper import CliCommand, CliCommandArgs, StepCliExecutable
from ..module_utils import helpers
from ..module_utils.constants import DEFAULT_STEP_CLI_EXECUTABLE

# maps the kty cli parameter to inspect outputs subject_key_info.key_algorithm.name
CERTINFO_KEY_TYPES = {
    "RSA": "RSA",
    "EC": "ECDSA",
    "OKP": "Ed25519"
}
CERTINFO_KEYINFO_KEY = {
    "RSA": "rsa_public_key",
    "ECDSA": "ecdsa_public_key"
}


def create_certificate(executable: StepCliExecutable, module: AnsibleModule) -> Dict[str, Any]:
    module_params = cast(Dict, module.params)
    result = {}
    # step ca certificate arguments
    cert_cliargs = ["comment", "console", "curve", "force", "host", "host_id", "insecure",
                    "k8ssa_token_path", "kms", "kty", "nebula_cert", "nebula_key", "no_password", "not_after",
                    "not_before", "password_file", "principal", "private_key", "provisioner", "provisioner_password_file", "set",
                    "set_file", "sign", "size","token", "x5c_cert", "x5c_key"]
    # All parameters can be converted to a mapping by just appending -- and replacing the underscores
    cert_cliarg_map = {arg: f"--{arg.replace('_', '-')}" for arg in cert_cliargs}

    args = ["ssh", "certificate", module_params["key_id"], module_params["key_file"]]
    # Never add key to ssh agent with Ansible
    args.append("--no-agent")

    create_args = CaConnectionParams.cli_args().join(CliCommandArgs(
        args, cert_cliarg_map, {"provisioner_password": "--provisioner-password-file"}))
    create_cmd = CliCommand(executable, create_args)
    create_cmd.run(module)
    return {"changed": True}


def revoke_certificate(executable: StepCliExecutable, module: AnsibleModule) -> Dict[str, Any]:  # pylint: disable=unused-argument
    module_params = cast(Dict, module.params)
    revoke_cliarg_map = {
        "revoke_reason": "--reason",
        "revoke_reason_code": "--reasonCode",
        "token": "--token"
    }
    args = ["ssh", "revoke", module_params["serial"]]
    revoke_args = CaConnectionParams.cli_args().join(CliCommandArgs(args, revoke_cliarg_map))
    revoke_cmd = CliCommand(executable, revoke_args, fail_on_error=False)
    res = revoke_cmd.run(module)

    if res.rc != 0 and "is already revoked" in res.stderr:
        return {}
    elif res.rc != 0:
        module.fail_json(f"Error revoking certificate: {res.stderr}")
        return {"changed": True}  # only here to satisfy the type checker, fail_json never returns
    else:
        # ran successfully => revoked
        return {"changed": True}


def delete_certificate(executable: StepCliExecutable, module: AnsibleModule, revoke: bool) -> Dict[str, Any]:
    module_params = cast(Dict, module.params)
    result = {}
    if revoke:
        result = revoke_certificate(executable, module)

    param_key_file = Path(module_params["key_file"])

    if not param_key_file.suffix == ".pub":
        key_file = param_key_file
        pub_file = key_file + ".pub"
        cert_file = key_file + "-cert.pub"
    else:
        key_file = os.path.splitext(param_key_file)[0]
        pub_file = key_file + ".pub"
        cert_file = key_file + "-cert.pub"

    for file in [key_file, pub_file, cert_file]:
        if file.exists():
            try:
                file.unlink()
            except FileNotFoundError:
                pass
            except OSError as e:
                module.fail_json(f"Could not delete file: {e}")
            result["changed"] = True
    return result


def run_module():
    argument_spec = dict(
        comment=dict(type="str"),
        console=dict(type="bool"),
        crt_file=dict(type="path"),
        curve=dict(type="str", choices=[
                   "P-256", "P-384", "P-521", "Ed25519"], aliases=["crv"]),
        force=dict(type="bool"),
        host=dict(type="bool"),
        host_id=dict(type="uuid"),
        insecure=dict(type="bool"),
        k8ssa_token_path=dict(type="path"),
        key_file=dict(type="path"),
        key_id=dict(type="str"),
        kms=dict(type="str"),
        kty=dict(type="str", choices=["EC", "OKP", "RSA"]),
        nebula_cert=dict(type="path"),
        nebula_key=dict(type="path"),
        no_password=dict(type="bool"),
        not_after=dict(type="str"),
        not_before=dict(type="str"),
        password_file=dict(type="path", no_log=False),
        principal=dict(type="list", elements="str"),
        private_key=dict(type="path"),
        provisioner=dict(type="str", aliases=["issuer"]),
        provisioner_password=dict(type="str", no_log=True),
        provisioner_password_file=dict(type="path", no_log=False),
        revoke_on_delete=dict(type="bool", default=True),
        revoke_reason=dict(type="str"),
        revoke_reason_code=dict(type="str"),
        serial=dict(type="str"),
        set=dict(type="list", elements="str"),
        set_file=dict(type="path"),
        sign=dict(type="bool"),
        size=dict(type="int"),
        state=dict(type="str", choices=["present", "revoked", "absent"], default="present"),
        token=dict(type="str", no_log=True),
        verify_roots=dict(type="str"),
        x5c_cert=dict(type="str"),
        x5c_key=dict(type="path"),
        step_cli_executable=dict(type="path", default=DEFAULT_STEP_CLI_EXECUTABLE)
    )
    result: Dict[str, Any] = dict(changed=False)
    module = AnsibleModule(argument_spec={
        **CaConnectionParams.argument_spec,
        **argument_spec,
    }, supports_check_mode=True)
    module_params = cast(Dict, module.params)

    try:
        CaConnectionParams(module).check()
        check_required_if([
            ["state", "present", ["key_file", "key_id", "provisioner"], True],
        ], module_params)
        check_mutually_exclusive(["provisioner_password", "provisioner_password_file"], module_params)
    except TypeError as e:
        module.fail_json(f"Parameter validation failed: {e}")

    executable = StepCliExecutable(module, module_params["step_cli_executable"])

    # TODO: Handle already existing files as in module 'step_ca_certificate.py'
    if module_params["state"] == "present":
        result.update(create_certificate(executable, module))
    elif module_params["state"] == "revoked":
        result.update(revoke_certificate(executable, module))
    elif module_params["state"] == "absent":
        result.update(delete_certificate(executable, module, module_params["revoke_on_delete"]))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
