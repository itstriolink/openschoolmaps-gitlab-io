#!/usr/bin/env python3

import subprocess
from pathlib import Path
from types import MappingProxyType as frozen


materials = Path('lehrmittel')
SOLUTION_SIGNATURE = 'def::show_solutions['


def main():
    adoc_file_paths = list(materials.glob('**/*.adoc'))
    for p in adoc_file_paths:
        sanity_check(p)
        make_pdfs(p)


def sanity_check(path):
    for p in path.parts:
        if p != p.strip():
            raise Exception(
                f'Part "{p}" of path "{path}"'
                ' has leading or trailing whitespace.'
            )


def make_pdfs(adoc_file_path):
    make_pdf_without_solutions(adoc_file_path)
    if has_solution(adoc_file_path):
        make_pdf_with_solutions(adoc_file_path)


def make_pdf_without_solutions(adoc_file_path):
    call_asciidoctor(
        infile=adoc_file_path,
    )


def make_pdf_with_solutions(adoc_file_path):
    outfile_name = f"{adoc_file_path.stem}_solutions.pdf"
    outfile_path = adoc_file_path.parent / outfile_name
    call_asciidoctor(
        infile=adoc_file_path,
        outfile=outfile_path,
        extra_attributes=dict(show_solutions=True),
    )


def has_solution(adoc_file_path):
    with open(adoc_file_path) as f:
        return any(SOLUTION_SIGNATURE in line for line in f)


def call_asciidoctor(infile, outfile=None, extra_attributes=frozen({})):
    default_attributes = frozen({
        'icons': 'font',
        'source-highlighter': 'coderay',
    })
    attributes = {**default_attributes, **extra_attributes}
    outfile_args = ('-o', outfile) if outfile else ()
    command = (
        'asciidoctor-pdf',
        *attributes_iterable(attributes),
        infile,
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
    main()
