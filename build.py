#!/usr/bin/env python3

import subprocess
import sys
from abc import ABC
from pathlib import Path
from types import MappingProxyType as frozen
from typing import Collection


materials = Path('lehrmittel')
SOLUTION_SIGNATURE = 'def::show_solutions['


def main(output_type):
    supported_file_types: dict = {'pdf': AsciiDoctorPDF, 'html': AsciiDoctorHTML}
    adoc_file_paths = list(materials.glob('**/*.adoc'))
    for path in adoc_file_paths:
        sanity_check(path)
    supported_file_types[output_type.lower()]().make_files(adoc_file_paths)


def sanity_check(path: Path):
    for p in path.parts:
        if p != p.strip():
            raise Exception(
                f'Part "{p}" of path "{path}"'
                ' has leading or trailing whitespace.'
            )


class AsciiDoctor(ABC):
    def make_files(self, adoc_file_paths: Collection[Path]):
        for p in adoc_file_paths:
            self.make_file_pair(p)

    def make_file_pair(self, adoc_file_path):
        self.make_file_without_solutions(adoc_file_path)
        if self.has_solution(adoc_file_path):
            self.make_file_with_solutions(adoc_file_path)

    def make_file_without_solutions(self, adoc_file_path):
        self.call_asciidoctor(
            infile=adoc_file_path,
        )

    def make_file_with_solutions(self, adoc_file_path):
        outfile_name = f"{adoc_file_path.stem}_solutions.{self.file_ending}"  # pylint: disable=no-member
        outfile_path = adoc_file_path.parent / outfile_name
        self.call_asciidoctor(
            infile=adoc_file_path,
            outfile=outfile_path,
            extra_attributes=dict(show_solutions=True),
        )

    def has_solution(self, adoc_file_path):
        with open(adoc_file_path) as f:
            return any(SOLUTION_SIGNATURE in line for line in f)

    def call_asciidoctor(self, infile, outfile=None, extra_attributes=frozen({})):
        default_attributes = frozen({
            'icons': 'font',
            'source-highlighter': 'coderay',
        })
        attributes = {**default_attributes, **extra_attributes}
        file_type = ('-b', self.file_ending)  # pylint: disable=no-member
        outfile_args = ('-o', outfile) if outfile else ()
        command = (
            self.asciidoctor_cmd,  # pylint: disable=no-member
            *self.attributes_iterable(attributes),
            infile,
            *file_type,
            *outfile_args,
        )
        subprocess.run(
            command,
            check=True,
        )

    def attributes_iterable(self, attributes_dict):
        for key, value in attributes_dict.items():
            yield '--attribute'
            yield key if value is True else f"{key}={value}"


class AsciiDoctorPDF(AsciiDoctor):
    file_ending: str = 'pdf'
    asciidoctor_cmd: str = 'asciidoctor-pdf'


class AsciiDoctorHTML(AsciiDoctor):
    file_ending: str = 'html'
    asciidoctor_cmd: str = 'asciidoctor'


if __name__ == '__main__':
    main(output_type=sys.argv[1])
