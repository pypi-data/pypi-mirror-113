import os
import re
import subprocess
import sys
import json

from io import BufferedIOBase
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict, Union

from .Error import Error
from .Payload import Payload

def as_bytes(data) -> str:
    """Converts the input into bytes. Input data should be a string, bytes, or a file-like object.

    Args:
        data: input data

    Returns:
        bytes: bytes representation of the input data
    """

    str_data = None

    #
    if isinstance(data, str):
        str_data = data.encode("utf-8")

    elif isinstance(data, bytes):
        str_data = data

    else:
        read_f = getattr(data, "read", None)
        if callable(read_f):
            str_data = read_f()

    return str_data

def run(payload: Dict[str, Payload], script: Union[str, bytes, BufferedIOBase], timeout=30) -> bytes:
    """Executes DataWeave with the specified payloads and script.

    Args:
        payload (Dict[str, DataWeavePayload]): Dictionary of payloads to pass
            to the DataWeave script. Payloads will be written to temporary
            files and then removed after execution.
        script (Union[str, bytes, BufferedIOBase]): DataWeave script. Will be
            written to a temporary file and removed after execution.
        timeout (int, optional): Timeout in seconds for script execution.
            Defaults to 30.

    Returns:
        bytes: Output from the DataWeave script.
    """

    args = [ str((Path(__file__) / ".." / "bin" / "dw").resolve()) ]

    # convert payloads to temp files
    for p in iter(payload):
        with NamedTemporaryFile("wb", suffix=f"-.{payload[p].payloadType}", delete=False) as tempFile:
            tempFile.write(as_bytes(payload[p].data))
            payload[p].data = tempFile.name
        args.append("-i")
        args.append(p)
        args.append(payload[p].data)

    # convert script file to temp file
    with NamedTemporaryFile("wb", suffix="-script.dwl", delete=False) as tempFile:
        tempFile.write(as_bytes(script))
        script = tempFile.name
    args.append("-f")
    args.append(script)

    try:

        # execute dataweave
        result = subprocess.run(
            args,
            shell=False,
            capture_output=True,
            timeout=timeout
        )

        # catch any dataweave-reported errors
        out_str = result.stdout.decode("utf-8")
        if len(out_str.strip()) == 0:
            raise Error(
                "DataWeave execution failed.",
                executable=args[0],
                parameters=args[1:],
                stdout=out_str,
                stderr=result.stderr.decode("utf-8")
            )

        # process and return captured output
        else:
            without_warnings = ""
            out_lines = out_str.splitlines()
            for l in range(len(out_lines)):
                if re.match(r'^(\u001b\[33m)?\[warning\]', out_lines[l]):
                    pass # skip warning lines
                else:
                    without_warnings = "\n".join(out_lines[l:])
                    break

            out_bytes = without_warnings.encode("utf-8")

    # catch any system-level errors
    except Exception as e:
        raise Error(
            "DataWeave execution failed: " + str(e),
            executable=args[0],
            parameters=args[1:],
            stdout="",
            stderr=e.args
        )

    # clean up temporary files
    finally:
        
        # remove temporary files
        for p in iter(payload):
            os.remove(payload[p].data)
        os.remove(script)

    return out_bytes

    