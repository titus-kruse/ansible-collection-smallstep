#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Max Hösel <ansible@maxhoesel.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function
__metaclass__ = type

DOCUMENTATION = r"""
---
module: step_ca_root
author: Max Hösel (@maxhoesel)
short_description: Download and validate the root certificate
version_added: '0.24.5'
description: >
  Downloads and validates the root certificate from the certificate authority and writes it to a file.
notes:
  - Check mode is supported.
options:
  root_file:
    description: File to write the root certificate file (PEM format)
    type: path
    required: yes
  force:
    description: Force the overwrite of files without asking.
    type: bool
  ca_url:
    description: URI of the targeted Step Certificate Authority
    type: str
  fingerprint:
    description: The fingerprint of the targeted root certificate
    type: str

extends_documentation_fragment: maxhoesel.smallstep.step_cli
"""

EXAMPLES = r"""
- name: Download root certificate and write it to root_file.
  maxhoesel.smallstep.step_ca_root:
    root_file: /path/to/root_ca.crt
    ca_url: https://ca.example.org
    fingerprint: d9d0978692f1c7cc791f5c343ce98771900721405e834cd27b9502cc719f5097
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
        root_file=dict(type="path", required=True),
        force=dict(type="bool"),
        ca_url=dict(type="str"),
        fingerprint=dict(type="str"),
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
    ca_root_cliargs = ["force", "ca_url", "fingerprint"]
    # All parameters can be converted to a mapping by just appending -- and replacing the underscores
    ca_root_cliarg_map = {arg: f"--{arg.replace('_', '-')}" for arg in ca_root_cliargs}

    ca_root_args = CaConnectionParams.cli_args().join(CliCommandArgs(
        ["ca", "root", module_params["root_file"]],
        ca_root_cliarg_map
    ))
    ca_root_cmd = CliCommand(executable, ca_root_args)
    ca_root_res = ca_root_cmd.run(module)
    if "The root certificate has been saved in" in ca_root_res.stderr:
        result["changed"] = True
    module.exit_json(**result)


def main():
    run_module()


if __name__ == "__main__":
    main()
