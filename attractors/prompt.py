#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ------------------------------------------------------------------------------
#  Copyright (c) 2021. Vignesh M
#  This file parser.py, part of the attractors package is licensed under the MIT license.
#  See LICENSE.md in the project root for license information.
# ------------------------------------------------------------------------------

from prompt_toolkit import prompt
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.shortcuts import CompleteStyle
from prompt_toolkit.validation import Validator

from attractors import Attractor as Attr

des_completer = WordCompleter(Attr.list_des(), ignore_case=True)
attractors_completer = WordCompleter(Attr.list_attractors(), ignore_case=True)
themes_completer = WordCompleter(list(Attr.list_themes().keys()), ignore_case=True)


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
    error_message="Points must be a valid positive int",
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
        sim_points = prompt(
            "> Number of points for simulation: ",
            completer=des_completer,
            complete_while_typing=True,
            validator=num_validator,
            validate_while_typing=False,
        )

    except KeyboardInterrupt:
        print("Exiting...")
        return 1

    print(
        f"Attractor: {attractor_name}\nODE Solver: {des_name}\nNumber of points:{sim_points}"
    )


if __name__ == "__main__":
    main()
