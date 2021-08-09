#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#  Copyright (c) 2021. Vignesh M
#  This file parser.py, part of the attractors package is licensed under the MIT license.
#  See LICENSE.md in the project root for license information.
# ------------------------------------------------------------------------------
from __future__ import unicode_literals

import random
import re

from prompt_toolkit import prompt
from prompt_toolkit.application import Application
from prompt_toolkit.completion import FuzzyWordCompleter
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.key_binding.key_bindings import KeyBindings, merge_key_bindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.shortcuts import confirm
from prompt_toolkit.styles import Style
from prompt_toolkit.validation import Validator
from prompt_toolkit.widgets import Label, RadioList

from attractors import Attractor as Attr

_rgbstring = re.compile(r"#[a-fA-F0-9]{6}$")

_param_style = Style.from_dict(
    {
        "param": "#62f5eb",
    }
)


def radiolist_dialog(title="", values=None, style=None):
    bindings = KeyBindings()

    @bindings.add("n")
    def exit_(event):
        event.app.exit()

    @bindings.add("y")
    def exit_with_value(event):
        event.app.exit(result=radio_list.current_value)

    radio_list = RadioList(values)
    application = Application(
        layout=Layout(HSplit([Label(title), radio_list])),
        key_bindings=merge_key_bindings([load_key_bindings(), bindings]),
        mouse_support=True,
        style=style,
        full_screen=False,
    )
    return application.run()


des_completer = FuzzyWordCompleter(Attr.list_des())
attractors_completer = FuzzyWordCompleter(Attr.list_attractors())
themes_completer = FuzzyWordCompleter(list(Attr.list_themes().keys()))


def is_valid_float(num):
    try:
        float(num)
        return True
    except ValueError:
        return False


def is_valid_num(num):
    return num.isdigit() and int(num) > 0


def is_valid_attractor(attractor):
    return attractor in Attr.list_attractors()


def is_valid_des(des):
    return des in Attr.list_des()


def is_valid_theme(theme):
    return theme in Attr.list_themes()


def is_valid_hex(hexstring):
    return bool(_rgbstring.match(hexstring))


def is_valid_palette(palette):
    return all(bool(_rgbstring.match(i)) for i in palette.split(" "))


attractors_validator = Validator.from_callable(
    is_valid_attractor,
    error_message="Not a valid attractor",
    move_cursor_to_end=False,
)

des_validator = Validator.from_callable(
    is_valid_des,
    error_message="Not a valid ODE solver",
    move_cursor_to_end=False,
)

theme_validator = Validator.from_callable(
    is_valid_theme,
    error_message="Not a valid theme",
    move_cursor_to_end=False,
)

num_validator = Validator.from_callable(
    is_valid_num,
    error_message="Input must be a valid positive int",
    move_cursor_to_end=False,
)

float_validator = Validator.from_callable(
    is_valid_float,
    error_message="Input must be a valid floating point",
    move_cursor_to_end=False,
)

bg_validator = Validator.from_callable(
    is_valid_hex,
    error_message="Background must be a valid 6 character hex string",
    move_cursor_to_end=False,
)

palette_validator = Validator.from_callable(
    is_valid_palette,
    error_message=(
        "Palette must be list of space seperated valid 6 character hex strings"
    ),
    move_cursor_to_end=False,
)


def main():
    try:
        attractor_name = prompt(
            "> Attractor to simulate: ",
            completer=attractors_completer,
            complete_while_typing=True,
            validator=attractors_validator,
            validate_while_typing=False,
        )

        param_dict = Attr.list_params(attractor_name)
        for p, d in param_dict.items():
            prompt_message = [
                ("class:normal", "  > Enter value for "),
                ("class:param", p),
                ("class:param", ": "),
            ]

            param = float(
                prompt(
                    prompt_message,
                    validator=float_validator,
                    validate_while_typing=False,
                    default=f"{d}",
                    style=_param_style,
                )
            )
            param_dict[p] = param

        des_name = prompt(
            "> ODE Solver: ",
            completer=des_completer,
            complete_while_typing=True,
            default="rk4",
            validator=des_validator,
            validate_while_typing=False,
        )
        sim_time = int(
            prompt(
                "> Simulation Time: ",
                validator=num_validator,
                validate_while_typing=False,
            )
        )
        sim_points = int(
            prompt(
                "> Number of points for simulation: ",
                validator=num_validator,
                validate_while_typing=False,
            )
        )
        plot_type = radiolist_dialog(
            title="> Choose visualization type :",
            values=[
                ("Multipoint", "Multipoint"),
                ("Gradient", "Gradient"),
            ],
        )

        # if plot_type == "Multipoint":
        #     n = int(
        #         prompt(
        #             "> Number of starting points: ",
        #             validator=num_validator,
        #             validate_while_typing=False,
        #             default="3",
        #         )
        #     )
        # else:
        #     n = random.randint(1, 10)

        output_type = radiolist_dialog(
            title="> Choose output type :",
            values=[
                ("Animation", "Animation"),
                ("Plot", "Plot"),
            ],
        )

        # Figure stuff
        figure_stuff = confirm("> Do you want to change figure values:")
        if figure_stuff:
            width = float(
                prompt(
                    "> Figure width (in inches): ",
                    validator=float_validator,
                    validate_while_typing=False,
                    default="16",
                )
            )
            height = float(
                prompt(
                    "> Figure height (in inches): ",
                    validator=float_validator,
                    validate_while_typing=False,
                    default="9",
                )
            )
            dpi = int(
                prompt(
                    "> Figure dpi: ",
                    validator=num_validator,
                    validate_while_typing=False,
                    default="120",
                )
            )
        else:
            width = 16
            height = 9
            dpi = 120

        # theme_select = confirm("> Do you want to choose a theme:")
        # if theme_select:
        #     theme = prompt(
        #         "> Theme: ",
        #         validator=theme_validator,
        #         validate_while_typing=False,
        #     )
        #     bgcolor = None
        #     palette = None
        # else:
        #     theme = None
        #     bgcolor = prompt(
        #         "> Background color: ",
        #         validator=bg_validator,
        #         validate_while_typing=False,
        #         default="#000000",
        #     )
        #     palette = prompt(
        #         "> Palette: ",
        #         validator=palette_validator,
        #         validate_while_typing=False,
        #         default=" ".join(
        #             ["#" + "%06X" % random.randint(0, 0xFFFFFF) for _ in range(n)]
        #         ),
        #     )

        # if output_type == "Animation":
        #     fps = int(
        #         prompt(
        #             "> Animation FPS: ",
        #             validator=num_validator,
        #             validate_while_typing=False,
        #             default="60",
        #         )
        #     )
        #
        #     live_type = radiolist_dialog(
        #         title="> Animation type :",
        #         values=[
        #             ("Live", "Live plot"),
        #             ("Video", "Video"),
        #         ],
        #     )
        #
        #     if live_type == "Video":
        #         outf = prompt(
        #             "> Output file name: ",
        #             default="output.mp4",
        #         )

    except KeyboardInterrupt:
        print("Exiting...")
        return 1

    print(
        f"Attractor: {attractor_name}\nODE Solver: {des_name}"
        f"\nSimulation Time: {sim_time}\nNumber of points: {sim_points}\n"
        f"Plot Type: {plot_type}\nOutput Type: {output_type}\n"
        f"\nFigure: {width * dpi:.0f} x {height * dpi:.0f}"
    )


if __name__ == "__main__":
    main()
