#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#  Copyright (c) 2021. Vignesh M
#  This file parser.py, part of the attractors package is licensed under the MIT license.
#  See LICENSE.md in the project root for license information.
# ------------------------------------------------------------------------------
from __future__ import unicode_literals

from prompt_toolkit import prompt
from prompt_toolkit.application import Application
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.key_binding.defaults import load_key_bindings
from prompt_toolkit.key_binding.key_bindings import KeyBindings, merge_key_bindings
from prompt_toolkit.layout import Layout
from prompt_toolkit.layout.containers import HSplit
from prompt_toolkit.shortcuts import confirm
from prompt_toolkit.validation import Validator
from prompt_toolkit.widgets import Label, RadioList

from attractors import Attractor as Attr


def radiolist_dialog(title="", values=None, style=None):
    # Add exit key binding.
    bindings = KeyBindings()

    @bindings.add("n")
    def exit_(event):
        """
        Pressing Ctrl-d will exit the user interface.
        """
        event.app.exit()

    @bindings.add("y")
    def exit_with_value(event):
        """
        Pressing Ctrl-a will exit the user interface returning the selected value.
        """
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


des_completer = WordCompleter(Attr.list_des(), ignore_case=True)
attractors_completer = WordCompleter(Attr.list_attractors(), ignore_case=True)
themes_completer = WordCompleter(list(Attr.list_themes().keys()), ignore_case=True)


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


def main():
    try:
        attractor_name = prompt(
            "> Attractor to simulate: ",
            completer=attractors_completer,
            complete_while_typing=True,
            validator=attractors_validator,
            validate_while_typing=False,
        )
        des_name = prompt(
            "> ODE Solver: ",
            completer=des_completer,
            complete_while_typing=True,
            default="rk4",
            validator=des_validator,
            validate_while_typing=False,
        )
        sim_time = prompt(
            "> Simulation Time: ",
            validator=num_validator,
            validate_while_typing=False,
        )
        sim_points = prompt(
            "> Number of points for simulation: ",
            validator=num_validator,
            validate_while_typing=False,
        )
        plot_type = radiolist_dialog(
            title="> Choose visualization type :",
            values=[
                ("Multipoint", "Multipoint"),
                ("Gradient", "Gradient"),
            ],
        )
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
