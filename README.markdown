# LLM Hackathon: Radioactive Activity Calculator

This repository contains Python scripts for calculating the percentage of atoms transmuted and the resulting radioactive activity (in becquerels) for a given element or alloy under neutron irradiation. The calculations use nuclear data from ENDF files and half-life data from the IAEA LiveChart API. The project was developed as part of the LLM Hackathon.

**Important**: Users should use either `finalCalc_API_CMD_input.py` (provide the element symbol via command-line) for single-element calculations or `alloyCalc.py` for alloy activation calculations. The scripts in the `LocalENSDF` directory and the 'Legacy' branch are not intended for general use.

## Features

- Calculates the percentage of atoms transmuted due to neutron capture for single elements or alloys.
- Computes the total activity (in becquerels) of radioactive daughter isotopes.
- Fetches half-life data dynamically from the IAEA LiveChart API.
- Processes neutron cross-section data from ENDF nuclear data files.
- Supports two scripts:
  - Command-line input: Pass the element symbol as an argument in `finalCalc_API_CMD_input.py`.
  - Alloy activation: Calculate activation for an alloy used in fusion reactor cladding with `alloyCalc.py`.

## Prerequisites

To run the scripts, you need:

- **Python 3.6 or higher**
- **Python packages**:
  - **Required (install via pip)**:
    - `mendeleev`: For accessing element properties.
    - `numpy`: For numerical computations.
    - `matplotlib`: Included but not currently used.
    - `endf`: For parsing ENDF nuclear data files.
  - **Standard Library (built-in)**:
    - `urllib.request`: For making HTTP requests to the IAEA API.
    - `csv`: For parsing API responses.
    - `re`: For regular expression operations.
    - `warnings`: For handling warnings.
- **ENDF nuclear data files** (version VIII.1), stored in the `./ENDF/neutrons-version.VIII.1/` directory.
- **isotopes_data.py**: A user-provided module containing isotope abundance data (included in the repository as `isotopes_data.py`).
- **Internet connection**: Required for fetching half-life data from the IAEA LiveChart API.

## Installation

1. Install Python 3.x from [python.org](https://www.python.org/downloads/).
2. Clone this repository:
   ```bash
   git clone https://github.com/HR-Chance/LLM_Hackathon.git
   cd LLM_Hackathon
   ```
3. Install the required Python packages:
   ```bash
   pip install mendeleev numpy matplotlib
   ```
4. **ENDF module**: The `endf` package may not be available via pip. If you have a custom `endf` module, ensure it is installed or accessible in your Python environment. Contact the repository owner for guidance if needed.
5. **ENDF files**: Download ENDF nuclear data files (version VIII.1) from a reliable source (e.g., [IAEA](https://www-nds.iaea.org/) or [NNDC](https://www.nndc.bnl.gov/)) and place them in the `./ENDF/neutrons-version.VIII.1/` directory. File names should follow the format `n-<Z>_<Element>_<A>.endf` (e.g., `n-030_Zn_064.endf`).
6. **isotopes_data.py**: This file is included in the repository and contains isotope abundance data for supported elements.

## Usage

The repository provides two primary scripts for calculating transmutation and activity:

### 1. Command-Line Input (`finalCalc_API_CMD_input.py`)

- **Description**: Accepts the element symbol as a command-line argument for single-element activation calculations.
- **How to Use**:
  Run the script with an element symbol as an argument:
  ```bash
  python3 finalCalc_API_CMD_input.py Zn
  ```
  Replace `Zn` with the desired element symbol (e.g., `Cu`, `Fe`).

### 2. Alloy Activation (`alloyCalc.py`)

- **Description**: Calculates the activation of an alloy used for cladding in a fusion reactor, accounting for the contributions of multiple elements based on their composition.
- **How to Use**:
  1. Open `alloyCalc.py` in a text editor.
  2. In the `main()` function, specify the alloy composition using the format `alloy = "Fe74C4Mn8Co4Zn10"` (example alloy formula, representing percentages of Fe, C, Mn, Co, and Zn).
  3. Run the script:
     ```bash
     python3 alloyCalc.py
     ```

### Input Parameters

- **Element Symbol** (for `finalCalc_API_CMD_input.py`): A valid chemical symbol (e.g., `Zn` for Zinc, `Cu` for Copper).
- **Alloy Composition** (for `alloyCalc.py`): Specify the alloy's elemental composition in the `main()` function (e.g., `alloy = "Fe74C4Mn8Co4Zn10"` for an alloy with 74% Fe, 4% C, 8% Mn, 4% Co, and 10% Zn).
- **Hardcoded Parameters** (defined in both scripts):
  - Neutron Energy: 14.1 MeV
  - Number of Initial Atoms: 1e23
  - Neutron Flux: 1e13 neutrons/cm²/s
  - Irradiation Time: 3600 seconds (60 minutes)

### Output

Both scripts output:

- **Percentage Transmuted**: The percentage of atoms transmuted due to neutron capture (for single elements or aggregated for alloys).
- **Product Activity**: The total activity of radioactive daughter isotopes in becquerels (Bq).

Example output for `finalCalc_API_CMD_input.py`:

```plaintext
Percentage Transmuted 1.234e-02 %
Product Activity 5.678e+10 Bq
```

## File Structure

- `finalCalc_API_CMD_input.py`: Script for command-line element symbol input.
- `alloyCalc.py`: Script for calculating activation of alloys used in fusion reactor cladding.
- `isotopes_data.py`: Module containing isotope abundance data for supported elements.
- `ENDF/neutrons-version.VIII.1/`: Directory for ENDF nuclear data files (not included; must be provided by the user).
- `LocalENSDF/`: Directory containing alternative scripts (not recommended for general use).

## Notes

- **Supported Elements**: The scripts rely on `isotopes_data.py` for isotope abundance data. Ensure the element symbol is supported in this file (e.g., `Zn`, `Cu`, `Fe`).
- **ENDF Files**: The scripts expect ENDF files in the format `n-<Z>_<Element>_<A>.endf`. If a file is missing, the script will skip the corresponding isotope and print a warning.
- **IAEA API**: The scripts fetch half-life data from the IAEA LiveChart API. A stable internet connection is required.
- **Error Handling**: The scripts handle invalid element symbols, missing ENDF files, and API errors gracefully, with appropriate warnings or error messages.
- **Stable Isotopes**: Stable daughter isotopes are excluded from activity calculations.
- **Legacy Branch**: The 'Legacy' branch contains outdated scripts and is not intended for use.

## Dependencies

- **Python Libraries**:
  - **Installed**: `mendeleev`, `numpy`, `matplotlib`, `endf` (custom or non-standard).
  - **Standard Library**: `urllib.request`, `csv`, `re`, `warnings`.
- **External Data**: ENDF nuclear data files (version VIII.1).
- **Network Access**: For IAEA LiveChart API queries.

## Limitations

- The `isotopes_data.py` file supports a limited set of elements. Users must verify their element is included.
- Hardcoded irradiation parameters (e.g., neutron energy, flux) may need manual adjustment for different scenarios.
- The `LocalENSDF` scripts are not recommended for use and may require additional setup not covered here.
- The `alloyCalc.py` script requires the alloy composition to be specified in the `main()` function in the correct format.

## Future Improvements

- Add command-line arguments for irradiation parameters (e.g., neutron energy, flux, time).
- Expand `isotopes_data.py` to include more elements or fetch abundances dynamically.
- Implement plotting with `matplotlib` to visualize transmutation or activity results.
- Improve error handling for network issues with the IAEA API.
- Enhance `alloyCalc.py` to support flexible input formats for alloy compositions.

## Contributing

Contributions are welcome! Please fork the repository, make changes, and submit a pull request. Ensure any changes are tested with both `finalCalc_API_CMD_input.py` and `alloyCalc.py`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for details (if included).

## Contact

For issues, questions, or suggestions, please email hchance@utexas.edu