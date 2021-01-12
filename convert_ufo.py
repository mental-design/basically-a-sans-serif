# Copyright 2020 Mental Design. All Rights Reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
# this list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
# this list of conditions and the following disclaimer in the documentation
# and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Convert UFO files to OTF/TTF/WOFF2.
"""

import argparse
import os

import defcon
import ufo2ft


def get_font_name(font):
    """Parse the font name from the Font object.

    :param font: A defcon Font object
    :type font: defcon.Font
    :returns: The font name
    :rtype: {[str]}
    """
    info = font.info
    familyName = info.familyName.replace(" ", "")
    styleName = info.styleName
    return f"{familyName}-{styleName}"


def convert_font(input_path, output_path, convert):
    """Convert a Font object.

    Render down all glyph in a font object and save it.
    :param input_path: The path to the UFO file
    :type input_path: str
    :param output_path: The output path (optional)
    :type output_path: str
    :param convert_otf: Flag to convert to OTF
    :type convert_otf: boolean
    :param convert_woff: Flag to convert to WOFF2
    :type convert_woff: boolean
    """
    # Load font
    font = defcon.Font(input_path)
    font_name = get_font_name(font)

    if output_path is None:
        output_path = os.path.dirname(input_path)
    out_folder = output_path

    # Convert to OTF
    if convert["otf"] or convert["woff2"]:
        print("Converting rendered UFO to OTF")
        otf = ufo2ft.compileOTF(font)

        # OTF
        if convert["otf"]:
            otf_file = font_name + ".otf"
            otf_folder = os.path.join(out_folder, 'otf')
            otf_path = os.path.join(otf_folder, otf_file)
            if not os.path.exists(otf_folder):
                os.makedirs(otf_folder)
            print(f"Saving OTF to {otf_path}")
            otf.save(otf_path)

        # WOFF2
        if convert["woff2"]:
            otf.flavor = "woff2"
            woff2_file = font_name + "." + otf.flavor
            woff2_folder = os.path.join(out_folder, 'woff2')
            woff2_path = os.path.join(woff2_folder, woff2_file)
            if not os.path.exists(woff2_folder):
                os.makedirs(woff2_folder)
            print(f"Saving WOFF2 to {woff2_path}")
            otf.save(woff2_path)

    # Convert to TTF
    if convert["ttf"]:
        print("Converting rendered UFO to TTF")
        ttf = ufo2ft.compileTTF(font)

        # OTF
        if convert["otf"]:
            ttf_file = font_name + ".ttf"
            ttf_folder = os.path.join(out_folder, 'ttf')
            ttf_path = os.path.join(ttf_folder, ttf_file)
            if not os.path.exists(ttf_folder):
                os.makedirs(ttf_folder)
            print(f"Saving TTF to {ttf_path}")
            ttf.save(ttf_path)


def main(input_path, output_path, convert):
    """
    The main function
    """
    if input_path.endswith(".ufo"):
        convert_font(input_path, output_path, convert)
    elif os.path.isdir(input_path):
        ufo_files = [f for f in os.listdir(input_path)
                     if os.path.splitext(f)[-1] == ".ufo"]

        if len(ufo_files) < 1:
            print(f"Could not find any .ufo files in {input_path}")
            return

        for file in ufo_files:
            file_path = os.path.join(input_path, file)
            convert_font(file_path, output_path, convert)
    else:
        print(f"Could not find any .ufo files in {input_path}")


def create_argparser():
    """Create the argparse

    :returns: an argparser
    :rtype: argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="the input .ufo file or folder containing .ufo files")
    parser.add_argument("-o", "--output", help="the output .ufo file")
    parser.add_argument("-c", "--convert", action='store_true',
                        help="convert .ufo to .otf")
    parser.add_argument("-w", "--woff", action='store_true',
                        help="convert .ufo to .woff2")
    parser.add_argument("-t", "--ttf", action='store_true',
                        help="convert .ufo to .ttf")
    parser.add_argument("-a", "--all", action='store_true',
                        help="convert .ufo to all formats")
    return parser


if __name__ == '__main__':
    parser = create_argparser()
    args = parser.parse_args()

    input_path = args.input
    output_path = args.output
    convert_otf = args.convert
    convert_woff = args.woff
    convert_ttf = args.ttf
    convert_all = args.all

    convert = {
        "otf": convert_otf or convert_all,
        "ttf": convert_ttf or convert_all,
        "woff2": convert_woff or convert_all
    }

    main(input_path, output_path, convert)
