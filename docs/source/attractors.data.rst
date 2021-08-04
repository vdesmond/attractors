`data` package
=======================

The data folder consists of 2 JSON files.

`themes.json`
---------------

This JSON file contains various themes listed with their color palette.
This file is imported inside the module :mod:`attractors.attractor`

`params.json`
---------------

This JSON file contains the following parameters for each attractor

    - `params` (List[str]): Names of parameters
    - `default_params` (List[float]): Default values of parameters
    - `init_coord` (List[float]): Default initial coordinates
    - `xlim` (List[float]): Default X-axis limits
    - `ylim` (List[float]): Default Y-axis limits
    - `zlim` (List[float]): Default Z-axis limits

This file is imported inside the module :mod:`attractors.utils.base`
