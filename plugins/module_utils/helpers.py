from dataclasses import dataclass
import json
from pathlib import Path
from typing import Dict, Any

from ansible.module_utils.basic import AnsibleModule
from ..module_utils.cli_wrapper import CliCommand, StepCliExecutable, CliCommandArgs


@dataclass
class CertificateInfo:
    data: Dict[str, Any]
    valid: bool
    invalid_reason: str = ""


def get_certificate_info(
    executable: StepCliExecutable, module: AnsibleModule, path: Path,
    bundle: bool = False, insecure: bool = False, server_name: str = "", roots: str = ""
) -> CertificateInfo:
    """Retrieve information about a certificate and return step-cli json-formatted information

    Args:
        executable (StepCliExecutable): The executable to run this command with
        module (AnsibleModule): The Ansible module
        path (Path): Path to the certificate
        bundle (bool, optional): See step-cli docs. Defaults to False.
        insecure (bool, optional): See step-cli docs. Defaults to False.
        server_name (str, optional): See step-cli docs. Defaults to "".
        roots (str, optional): See step-cli docs. Defaults to "".

    Returns:
        CertificateInfo: The JSON information as output by step-cli as well as validity information
    """
    inspect_args = ["certificate", "inspect", path, "--format", "json"]
    if bundle:
        inspect_args.append("--bundle")
    if insecure:
        inspect_args.append("--insecure")
    if server_name:
        inspect_args.extend(["--server-name", server_name])
    if roots:
        inspect_args.extend(["--roots", roots])

    inspect_cmd = CliCommand(executable, CliCommandArgs(inspect_args), run_in_check_mode=True)
    inspect_res = inspect_cmd.run(module)
    # The docs say inspect outputs to stderr, but my shell says otherwise:
    # https://github.com/smallstep/cli/issues/1032
    try:
        data = json.loads(inspect_res.stdout)
    except json.JSONDecodeError as e:
        module.fail_json(f"Unable to decode returned certificate information. Error: {e}")

    verify_args = ["certificate", "verify", path]
    if server_name:
        verify_args.extend(["--server-name", server_name])
    if roots:
        verify_args.extend(["--roots", roots])
    verify_cmd = CliCommand(executable, CliCommandArgs(verify_args), run_in_check_mode=True, fail_on_error=False)
    verify_res = verify_cmd.run(module)
    valid = verify_res.rc == 0
    invalid_reason = "" if valid else verify_res.stderr

    return CertificateInfo(data, valid, invalid_reason)

def get_ssh_renewal_info(
    executable: StepCliExecutable, module: AnsibleModule, path: Path, expires_in: str = ""
) -> CertificateInfo:
    """Retrieve information about a certificate and return step-cli exit code

    Args:
        executable (StepCliExecutable): The executable to run this command with
        module (AnsibleModule): The Ansible module
        path (Path): Path to the certificate
        expires_in (str, optional): See step-cli docs. Defaults to "".

    Returns:
        CertificateInfo: Returns '0' if the SSH certificate needs renewal, '1' if the SSH certificate does not need renewal,
          '2' if the SSH certificate file does not exist, and '255' for any other error.
    """
    verify_args = ["ssh", "needs-renewal", path]
    if expires_in:
        verify_args.extend(["--expires-in", expires_in])
    verify_cmd = CliCommand(executable, CliCommandArgs(verify_args), run_in_check_mode=True, fail_on_error=False)
    verify_res = verify_cmd.run(module)
    verify_res_rc = verify_res.rc
    valid = verify_res_rc == 0
    invalid_reason = "" if valid else verify_res.stderr

    return CertificateInfo(verify_res_rc, valid, invalid_reason)
