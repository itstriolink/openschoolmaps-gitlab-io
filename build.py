#!/usr/bin/env python3

import subprocess
import sys
from pathlib import Path
from types import MappingProxyType as frozen


materials = Path('lehrmittel')
SOLUTION_SIGNATURE = 'def::show_solutions['
SUPPORTET_FILE_TYPES = ['pdf', 'html']


def main(output_type):
    adoc_file_paths = list(materials.glob('**/*.adoc'))
    check_for_file_type(output_type)
    print(f'The File Generator is generating {output_type.upper()}s')
    for p in adoc_file_paths:
        sanity_check(p)
    for p in adoc_file_paths:
        make_files(p, output_type)


def sanity_check(path):
    for p in path.parts:
        if p != p.strip():
            raise Exception(
                f'Part "{p}" of path "{path}"'
                ' has leading or trailing whitespace.'
            )


def check_for_file_type(output_type):
    if SUPPORTET_FILE_TYPES.count(output_type.lower()) == 0:
        raise Exception(
            f'The File Type "{output_type}" is not supported by this Build-Script!'
            f'The following types are supported: "{SUPPORTET_FILE_TYPES}"'
        )


def make_files(adoc_file_path, output_type):
    make_files_without_solutions(adoc_file_path, output_type)
    if has_solution(adoc_file_path):
        make_files_with_solutions(adoc_file_path, output_type)


def make_file_without_solutions(adoc_file_path, output_type):
    call_asciidoctor(
        infile=adoc_file_path,
        output_type=output_type,
    )


def make_file_with_solutions(adoc_file_path, output_type):
    outfile_name = f"{adoc_file_path.stem}_solutions.{output_type.lower()}"
    outfile_path = adoc_file_path.parent / outfile_name
    call_asciidoctor(
        infile=adoc_file_path,
        outfile=outfile_path,
        extra_attributes=dict(show_solutions=True),
        output_type=output_type,
    )


def has_solution(adoc_file_path):
    with open(adoc_file_path) as f:
        return any(SOLUTION_SIGNATURE in line for line in f)


def call_asciidoctor(infile, outfile=None, extra_attributes=frozen({}), output_type=None):
    default_attributes = frozen({
        'icons': 'font',
        'source-highlighter': 'coderay',
    })
    attributes = {**default_attributes, **extra_attributes}
    is_pdf = ('-r', 'asciidoctor-pdf') if output_type.lower() == 'pdf' else ()
    file_type = ('-b', output_type.lower()) if output_type else ()
    outfile_args = ('-o', outfile) if outfile else ()
    command = (
        'asciidoctor',
        *attributes_iterable(attributes),
        infile,
        *is_pdf,
        *file_type,
        *outfile_args,
    )
    subprocess.run(
        command,
        check=True,
    )


def attributes_iterable(attributes_dict):
    for key, value in attributes_dict.items():
        yield '--attribute'
        yield key if value is True else f"{key}={value}"


if __name__ == '__main__':
    main(output_type=sys.argv[1])
