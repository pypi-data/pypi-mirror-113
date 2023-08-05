import logging
import re
import string

from nipype.interfaces.base import (
    CommandLine,
    CommandLineInputSpec,
    File,
    TraitedSpec,
    traits,
)

log = logging.getLogger(__name__)


class FSLHDInputSpec(CommandLineInputSpec):
    in_file = File(
        exists=True,
        mandatory=True,
        argstr="%s > ",
        position=1,
        desc="the input NIFTI file",
    )
    x_param = traits.Bool(mandatory=False, argstr="-x", position=0, desc="fsl x param")
    out_file = traits.Str(mandatory=False, argstr="%s", position=2, desc="out file")


class FSLHDOutputSpec(TraitedSpec):
    out_file = File(desc="xml file")


class FSLHD(CommandLine):
    _cmd = "fslhd"
    input_spec = FSLHDInputSpec
    output_spec = FSLHDOutputSpec

    def _list_outputs(self):
        return {"out_file": self.inputs.out_file}


def assign_type(s):
    """
    Sets the type of a given input.
    """
    if type(s) == list:
        try:
            return [int(x) for x in s]
        except ValueError:
            try:
                return [float(x) for x in s]
            except ValueError:
                return [format_string(x) for x in s]
    else:
        s = str(s)
        try:
            return int(s)
        except ValueError:
            try:
                return float(s)
            except ValueError:
                return s


def format_string(in_string):
    """
    Remove non-ascii characters.
    """
    in_string = str(in_string)
    formatted = re.sub(r"[^\x00-\x7f]", r"", in_string)  #
    formatted = "".join(filter(lambda x: x in string.printable, formatted))
    return formatted


def _extract_nifti_xml_header(fslhd_xml):
    """
    Extract nifti header from xml
    """

    with open(fslhd_xml, "r") as f:
        lines = f.readlines()

    nifti_header = {}
    for l in lines[1:-2]:  # todo : fix when l is empty
        # print(l)
        string = l.replace("\n", "")
        k, v = string.split(" = ")
        key = k.strip()
        value = v.replace("'", "").strip()
        nifti_header[key] = assign_type(value)

    return nifti_header


def _extract_nifti_text_header(fslhd_txt):
    """
    Extract nifti header from xml
    """

    with open(fslhd_txt, "r") as f:
        lines = f.readlines()

    nifti_header = {}
    for line in lines:
        content = line.split()
        if len(content) == 2:
            key, value = content[0], content[1]
            nifti_header[key] = assign_type(value)

    return nifti_header


def get_nifti_header(fslhd_xml, fslhd_txt):
    # Grab the nifti_header from the xml
    nifti_xml_header = _extract_nifti_xml_header(fslhd_xml)
    nifti_txt_header = _extract_nifti_text_header(fslhd_txt)

    # Combine the header dictionaries
    nifti_header = nifti_xml_header.copy()
    nifti_header.update(nifti_txt_header)

    return nifti_header


def _get_descrip_fields(fslhd):
    """
    Parse descrip field from nifti header to extract individual values
    """
    descrip = {}

    if "descrip" in fslhd:
        fslhd_descrip = fslhd["descrip"]
        log.info("Parsing descrip field...")
        log.info("  " + fslhd_descrip)
        try:
            descrip_list = fslhd_descrip.split(";")
            if descrip_list:
                for d in descrip_list:
                    try:
                        k, v = d.split("=")
                        descrip[k] = assign_type(v)
                    except:
                        descrip = descrip_list
        except:
            log.info("Failed to parse descrip!")
            return None

    return descrip
