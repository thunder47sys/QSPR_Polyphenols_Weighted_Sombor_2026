import pandas as pd
import numpy as np
import os
import sys
import math

# --- INSTALL RDKIT ---
try:
    from rdkit import Chem
except ImportError:
    import subprocess
    print("📦 Installing RDKit...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "rdkit-pypi"])
    from rdkit import Chem
    from rdkit.Chem import PeriodicTable

# --- 1. LOAD FILE ---
print(f"📂 Current Folder: {os.getcwd()}")
files = [f for f in os.listdir() if f.endswith('.xlsx') or f.endswith('.csv')]

if not files:
    print("❌ ERROR: Please upload your data file!")
else:
    target_file = files[0]
    print(f"✅ Found file: '{target_file}'")
    if target_file.endswith('.xlsx'):
        df = pd.read_excel(target_file)
    else:
        df = pd.read_csv(target_file)

    # --- 2. DEFINE WEIGHTS ---
    pt = Chem.GetPeriodicTable()

    # Atomic Properties Lookup
    atom_props = {
        6: {'en': 2.55, 'ie': 11.26}, # Carbon
        1: {'en': 2.20, 'ie': 13.60}, # Hydrogen
        8: {'en': 3.44, 'ie': 13.61}, # Oxygen
        7: {'en': 3.04, 'ie': 14.53}, # Nitrogen
        16: {'en': 2.58, 'ie': 10.36}, # Sulfur
        9: {'en': 3.98, 'ie': 17.42}, # Fluorine
        17: {'en': 3.16, 'ie': 12.97}, # Chlorine
        15: {'en': 2.19, 'ie': 10.49}, # Phosphorus
    }

    def get_prop(atom, prop_name):
        idx = atom.GetAtomicNum()
        if prop_name == 'mass': return pt.GetAtomicWeight(idx)
        if prop_name == 'radius': return pt.GetRcovalent(idx)
        if prop_name == 'en': return atom_props.get(idx, {}).get('en', 1.0)
        if prop_name == 'ie': return atom_props.get(idx, {}).get('ie', 1.0)
        return 1.0

    # --- 3. THE FORMULAS (FROM cal.py) ---
    def calculate_indices_from_cal_py(smiles, prop_name):
        try:
            mol = Chem.MolFromSmiles(str(smiles))
            if not mol: return [None]*7

            # A. Calculate Weighted Degrees
            w_c = get_prop(Chem.Atom(6), prop_name) # Carbon Reference
            degrees = {}
            for atom in mol.GetAtoms():
                d_w = 0
                idx = atom.GetIdx()
                w_i = get_prop(atom, prop_name)
                for neighbor in atom.GetNeighbors():
                    bond = mol.GetBondBetweenAtoms(idx, neighbor.GetIdx())
                    bo = bond.GetBondTypeAsDouble()
                    w_j = get_prop(neighbor, prop_name)
                    # Weight Formula
                    d_w += (w_c * w_c) / (bo * w_i * w_j)
                degrees[idx] = d_w

            # B. Apply Logic from cal.py
            SO = 0
            SO3 = 0
            SO4 = 0
            SO5 = 0
            SO6 = 0
            ESO = 0
            MESO = 0

            for bond in mol.GetBonds():
                du = degrees[bond.GetBeginAtomIdx()]
                dv = degrees[bond.GetEndAtomIdx()]

                # Logic from cal.py
                term = math.sqrt(du**2 + dv**2)

                # (1) Standard Sombor
                SO += term

                # (2) SO3 (Geometric/Pi definition)
                if (du + dv) != 0:
                    SO3 += (math.sqrt(2) * math.pi * ((du**2 + dv**2) / (du + dv)))

                # (3) SO4 (Geometric/Pi definition)
                if (du + dv) != 0:
                    SO4 += ((math.pi / 2) * (((du**2 + dv**2) / (du + dv)) ** 2))

                # (4) SO5 (Absolute value definition)
                denom_so5 = (math.sqrt(2) + 2 * term)
                if denom_so5 != 0:
                    SO5 += (2 * math.pi * (abs(du**2 - dv**2) / denom_so5))

                # (5) SO6 (Similar structure to SO5)
                if denom_so5 != 0:
                    SO6 += (math.pi * ((abs(du**2 - dv**2) / denom_so5) ** 2))

                # (6) ESO (Linear-product definition from cal.py)
                ESO += ((du + dv) * term)

            # (7) MESO (Inverse of ESO)
            if ESO != 0:
                MESO = 1 / ESO
            else:
                MESO = 0

            return [SO, SO3, SO4, SO5, SO6, ESO, MESO]
        except Exception as e:
            return [None]*7

    # --- 4. RUN CALCULATIONS ---
    print("🚀 Calculating Indices (Rounding to 4 decimal places)...")

    properties = ['mass', 'radius', 'en', 'ie']
    variations = ['SO', 'SO3', 'SO4', 'SO5', 'SO6', 'ESO', 'MESO']

    # Find SMILES column
    smiles_col = [c for c in df.columns if 'smi' in c.lower()][0]

    for p in properties:
        print(f"   ... processing {p} weighting")
        results = df[smiles_col].apply(lambda x: calculate_indices_from_cal_py(x, p))

        # Create column names
        new_cols = [f"{v}_{p}" for v in variations]

        # Create DataFrame and ROUND results instantly
        result_df = pd.DataFrame(results.tolist(), index=df.index)
        df[new_cols] = result_df.round(4)

    # --- 5. SAVE ---
    output_name = "Polyphenols_Weighted_Rounded.csv"
    df.to_csv(output_name, index=False)
    print(f"🎉 DONE! Cleaned file saved to: {output_name}")

    try:
        from google.colab import files
        files.download(output_name)
    except:
        print("   (Download manually from folder)")
