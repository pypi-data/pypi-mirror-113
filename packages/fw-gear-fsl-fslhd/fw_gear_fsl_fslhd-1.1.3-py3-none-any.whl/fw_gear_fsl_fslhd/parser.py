"""Parser module to parse gear config.json."""
from typing import Tuple

from flywheel_gear_toolkit import GearToolkitContext


def parse_config(
    gear_context: GearToolkitContext,
) -> Tuple[str, str, str, bool, bool, dict]:
    """Parses gear config file and returns relevant inputs and config.

    Args:
        gear_context (GearToolkitContext): Context

    Returns:
            - path to nifti file
            - nifti file name
            - output_json
            - parse_descrip
            - exsting_info
    """

    nifti_file_path = gear_context.get_input("nifti").get("location").get("path")
    nifti_file_name = gear_context.get_input("nifti").get("location").get("name")

    output_json = gear_context.config.get("output_json")
    parse_descrip = gear_context.config.get("parse_descrip")
    existing_info = gear_context.get_input("nifti").get("object").get("info")

    return (
        nifti_file_path,
        nifti_file_name,
        output_json,
        parse_descrip,
        existing_info,
    )
