#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: step_ssh_config
author: Titus Kruse <mail@tituskruse.de>
short_description: Configures ssh to be used with certificates
version_added: '0.25.0'
description: >
  Configures SSH to be used with certificates.
notes:
  - Check mode is supported.
  - This module currently not supports all options provided by step-cli command.
options:
  host:
    desscription: Configures a SSH server instead of a client.
    type: bool
  roots:
    desscription: Prints the public keys used to verify user or host certificates.
    type: bool
  ca_url:
    description: URI of the targeted Step Certificate Authority
    type: str

extends_documentation_fragment: maxhoesel.smallstep.step_cli
"""

EXAMPLES = r"""
- name: Download CA public keys
  maxhoesel.smallstep.step_ssh_config:
    roots: true
    ca_url: https://ca.example.org
"""

import json
import os

from typing import Dict, cast, Any

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.common.validation import check_mutually_exclusive

from ..module_utils.cli_wrapper import CliCommand, CliCommandArgs, StepCliExecutable
from ..module_utils.params.ca_connection import CaConnectionParams
from ..module_utils.constants import DEFAULT_STEP_CLI_EXECUTABLE

DEFAULTS_FILE = "{steppath}/config/defaults.json".format(
    steppath=os.environ.get("STEPPATH", os.environ["HOME"] + "/.step"))


def run_module():
    argument_spec = dict(
        step_cli_executable=dict(type="path", default="step-cli"),
        host=dict(type="bool"),
        roots=dict(type="bool"),
        ca_url=dict(type="str"),
    )
    result: Dict[str, Any] = dict(changed=False)
    module = AnsibleModule(argument_spec={
        **CaConnectionParams.argument_spec,
        **argument_spec
    }, supports_check_mode=True)
    module_params = cast(Dict, module.params)

    try:
        CaConnectionParams(module).check()
    except TypeError as e:
        module.fail_json(f"Parameter validation failed: {e}")

    executable = StepCliExecutable(module, module_params["step_cli_executable"])

    # Regular args
    ssh_config_cliargs = ["host", "roots", "ca_url"]
    # All parameters can be converted to a mapping by just appending -- and replacing the underscores
    ssh_config_cliarg_map = {arg: f"--{arg.replace('_', '-')}" for arg in ssh_config_cliargs}

    ssh_config_args = CaConnectionParams.cli_args().join(CliCommandArgs(
        ["ssh", "config"],
        ssh_config_cliarg_map
    ))
    ssh_config_cmd = CliCommand(executable, ssh_config_args)
    ssh_config_res = ssh_config_cmd.run(module)

    result["changed"] = True
    if module_params["roots"]:
        result["roots"] = ssh_config_res.stdout
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
