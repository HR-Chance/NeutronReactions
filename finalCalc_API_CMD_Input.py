import os
import sys
import endf
import urllib.request
import io
import csv
import re
import matplotlib.pyplot as plt
from isotopes_data import isotopes_data
import numpy as np
from mendeleev import element
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="endf.material")

def get_isotope_half_life(symbol, A):
    # Convert symbol to lowercase as required by API
    symbol_lower = symbol.lower()
    nuclide = f"{A}{symbol_lower}"
    
    url = f"https://nds.iaea.org/relnsd/v1/data?fields=ground_states&nuclides={nuclide}"
    
    # Add user-agent to avoid potential 403 error
    req = urllib.request.Request(url)
    req.add_header('User-Agent', 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0')
    
    try:
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            # Parse CSV
            csv_reader = csv.DictReader(io.StringIO(content))
            data = next(csv_reader, None)
            
            if data is None:
                return None
            
            # Extract half-life and unit
            half_life = data.get('half_life', 'N/A')
            unit_hl = data.get('unit_hl', '')
            
            if half_life == 'STABLE':
                return 'Stable'
            
            # Convert half-life to seconds
            try:
                half_life_value = float(half_life)
                # Conversion factors to seconds
                unit_conversions = {
                    'Y': 31557600,  # Years (based on 365.25 days)
                    'D': 86400,     # Days
                    'H': 3600,      # Hours
                    'M': 60,        # Minutes
                    'S': 1,         # Seconds
                    'MS': 0.001,    # Milliseconds
                    'US': 0.000001  # Microseconds
                }
                # Get conversion factor (case-insensitive)
                conversion_factor = unit_conversions.get(unit_hl.upper(), 1)
                return half_life_value * conversion_factor
            except ValueError:
                return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def getENDF(A, Z, elem):
    curDir = os.getcwd()
    endf_file = curDir + "/ENDF/neutrons-version.VIII.1/n-" + str(Z) + "_" + elem + "_" + str(A) + ".endf"
    return endf_file

def main():
    # Check for command-line argument
    if len(sys.argv) > 2 and len(sys.argv) > 0:
        print("Usage: python3 finalCalc_API.py <element_symbol>")
        sys.exit(1)
    
    # Get element symbol from command-line argument and convert to string
    elem = str(sys.argv[1])
    
    try:
        tmpElem = element(elem)
        dat = isotopes_data[elem]
    except (KeyError, ValueError):
        print(f"Error: Invalid element symbol '{elem}' or not found in isotopes_data")
        sys.exit(1)
    
    barnsConv = 1e-24  # Barns to cm^2
    Nenergy = 14.1e6   # Neutron Energy
    Natoms = 1e23      # Number of Initial Atoms
    Nflux = 1e13       # Neutron Flux    
    iradTime = 60*60   # Irradiated for 60 minutes
    Ntransmuted = 0
    Activity = 0

    for isotope in dat['isotopes']:
        a = f"{isotope['mass_number']:03d}"
        z = f"{tmpElem.atomic_number:03d}"
        if isotope.get('abundance', 'N/A') == 'N/A':
            # print(f"Warning: Abundance data for {elem}-{a} not available, skipping isotope")
            continue
        abund = float(re.sub(r'\s*\([^)]+\)$', '', isotope.get('abundance', 'N/A')).strip())
        endfFilePath = getENDF(a, z, elem)  # Get file name for isotope ENDF file 
        try:
            mat = endf.Material(endfFilePath)
            xsAb = mat.section_data[3, 102]['sigma']  # Neutron Cross Section Grep
        except FileNotFoundError:
            print(f"Warning: ENDF file for {elem}-{a} not found, skipping isotope")
            continue
        
        nIso = Natoms * abund
        tmp = nIso * (1 - np.exp(-xsAb(Nenergy) * barnsConv * Nflux * iradTime))
        Ntransmuted = Ntransmuted + tmp

        daughter = isotope['mass_number'] + 1
        halfLife = get_isotope_half_life(elem, daughter)
        if halfLife != 'Stable' and halfLife is not None:
            decay_constant = np.log(2) / halfLife
            tmpActivity = tmp * decay_constant
            Activity = Activity + tmpActivity
        
    print('Percentage Transmuted', f"{(Ntransmuted/Natoms)*100:.3e}", '%')
    print('Product Activity', f"{Activity:.3e}", 'Bq')

    # return (Ntransmuted/Natoms)*100, Activity

if __name__ == "__main__":
    main()