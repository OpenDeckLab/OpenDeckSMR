# -*- coding: utf-8 -*-
# =================================================================================
# File        : wrapping.py
# Description : [This file contains the python wrapping of the exe OpenDeckSMR]
# Author      : [Safran SA / Safran Tech / DST]
# Created     : [2025-06-02]
# Updated     : [2025-10-20]
# Version     : [v1.0]
#
# ================================================================================
import re
import subprocess
import pandas as pd

from odsmr.predefined_flight_conditions import Climb1_DeckSMR, Climb2_DeckSMR


def get_key_value(dictionary, key_name, default_value=0):
    if key_name in dictionary.keys():
        return dictionary[key_name]
    else:
        return default_value


def call_value_from_keys(RAWKDATA, phase, segment, ALT=None, DTAMB=None, MACH=None):
    if phase == "MCL":
        min_k = float(RAWKDATA.loc['MCL1', segment])
        max_k = float(RAWKDATA.loc['MCL2', segment])
        # In a future version the code could provide more predefined climb points
        ALT1 = Climb1_DeckSMR.flight_condition.ALT
        ALT2 = Climb2_DeckSMR.flight_condition.ALT
        MACH1 = Climb1_DeckSMR.flight_condition.MACH
        MACH2 = Climb2_DeckSMR.flight_condition.MACH
        ratio_ALT   = (ALT - ALT1) / (ALT2 - ALT1)
        ratio_MACH  = (MACH - MACH1) / (MACH2 - MACH1)

        weight = (ratio_ALT + ratio_MACH) / 2.0

        return min_k + weight * (max_k-min_k)
    else:
        return float(RAWKDATA.loc[phase, segment])


class DeckSMR:

    def __init__(self, ROOT=None):
        if ROOT is None:
            raise ValueError('You should have set a root name')
        else:
            self.ROOT = ROOT
        
        self.RAWKDATA = {
                "Segment": ["MTO", "MCL1", "MCL2", "CR"],
                "Fan_sec": [2.133, 3.209, 3.206, 3.283],
                "Bst": [0.977, 1.105, 1.407, 1.215],
                "HPC": [1.393, 1.439, 2.377, 1.932]
            }
        self.RAWKDATA = pd.DataFrame(self.RAWKDATA)
        self.RAWKDATA.set_index("Segment", inplace=True)
        
    def run_simulation_multi_parameters(
        self, inputs, list_parameters, sim_type=None, sim_options=None
    ):
        complete_df = []
        if len(inputs) != len(list_parameters):
            print("len inputs:", len(inputs), "len parameters", len(list_parameters))
            print(inputs)
            print(list_parameters)
            raise ValueError("len of inputs & parameters not matching")
        for input, param in zip(inputs, list_parameters):
            PHASE_TYPE = input["PHASE_TYPE"]
            FN_CR = input["COMMAND"]
            ALT = input["ALT"]
            DTAMB = input["DTAMB"]
            MACH = input["MACH"]

            # Compute coefficients k, no need to interpolate (but maybe if we change FN_CR? Check with Panos again in doubt)
            dico_k = {}
            for key_seg in ["Fan_sec", "Bst", "HPC"]:
                dico_k[key_seg] = call_value_from_keys(self.RAWKDATA, PHASE_TYPE, key_seg, ALT=ALT, DTAMB=DTAMB, MACH=MACH )

            deg_CmpBst_s_NcRdes_in = get_key_value(param, "deg_CmpBst_s_NcRdes_in")
            deg_CmpBst_s_mapEff_in = get_key_value(param, "deg_CmpBst_s_mapEff_in")
            deg_CmpBst_s_mapWc_in = get_key_value(param, "deg_CmpBst_s_mapWc_in")
            deduced_by_k = dico_k["Bst"] * deg_CmpBst_s_mapWc_in
            deg_CmpBst_s_mapPR_in = get_key_value(
                param, "deg_CmpBst_s_mapPR_in", deduced_by_k
            )

            deg_CmpFan_s_NcRdes_sec_in = get_key_value(param, "deg_CmpFan_s_NcRdes_in")
            deg_CmpFan_s_mapEff_sec_in = get_key_value(param, "deg_CmpFan_s_mapEff_in")
            deg_CmpFan_s_mapWc_sec_in = get_key_value(param, "deg_CmpFan_s_mapWc_in")
            deduced_by_k = dico_k["Fan_sec"] * deg_CmpFan_s_mapWc_sec_in
            deg_CmpFan_s_mapPR_sec_in = get_key_value(
                param, "deg_CmpFan_s_mapPR_in", deduced_by_k
            )

            deg_CmpH_s_NcRdes_in = get_key_value(param, "deg_CmpH_s_NcRdes_in")
            deg_CmpH_s_mapEff_in = get_key_value(param, "deg_CmpH_s_mapEff_in")
            deg_CmpH_s_mapWc_in = get_key_value(param, "deg_CmpH_s_mapWc_in")
            deduced_by_k = dico_k["HPC"] * deg_CmpH_s_mapWc_in
            deg_CmpH_s_mapPR_in = get_key_value(
                param, "deg_CmpH_s_mapPR_in", deduced_by_k
            )

            deg_TrbH_s_mapEff_in = get_key_value(param, "deg_TrbH_s_mapEff_in")
            deg_TrbH_s_mapNc_in = get_key_value(param, "deg_TrbH_s_mapNc_in")
            deg_TrbH_s_mapPR_in = get_key_value(param, "deg_TrbH_s_mapPR_in")
            deg_TrbH_s_mapWc_in = get_key_value(param, "deg_TrbH_s_mapWc_in")

            deg_TrbL_s_mapEff_in = get_key_value(param, "deg_TrbL_s_mapEff_in")
            deg_TrbL_s_mapNc_in = get_key_value(param, "deg_TrbL_s_mapNc_in")
            deg_TrbL_s_mapPR_in = get_key_value(param, "deg_TrbL_s_mapPR_in")
            deg_TrbL_s_mapWc_in = get_key_value(param, "deg_TrbL_s_mapWc_in")

            if (PHASE_TYPE == "MCL1") or (PHASE_TYPE == "MCL2"):
                CPPPHASE = "MCL"
            else:
                CPPPHASE = PHASE_TYPE

            deg_values = [
                deg_CmpBst_s_NcRdes_in, deg_CmpBst_s_mapEff_in,
                deg_CmpBst_s_mapPR_in, deg_CmpBst_s_mapWc_in,
                deg_CmpFan_s_NcRdes_sec_in, deg_CmpFan_s_mapEff_sec_in,
                deg_CmpFan_s_mapPR_sec_in, deg_CmpFan_s_mapWc_sec_in,
                deg_CmpH_s_NcRdes_in, deg_CmpH_s_mapEff_in,
                deg_CmpH_s_mapPR_in, deg_CmpH_s_mapWc_in,
                deg_TrbH_s_mapEff_in, deg_TrbH_s_mapNc_in,
                deg_TrbH_s_mapPR_in, deg_TrbH_s_mapWc_in,
                deg_TrbL_s_mapEff_in, deg_TrbL_s_mapNc_in,
                deg_TrbL_s_mapPR_in, deg_TrbL_s_mapWc_in
            ]

            command = self.build_command(FN_CR, deg_values, ALT, DTAMB, MACH, CPPPHASE)

            result = subprocess.run(
                command, shell=True, capture_output=True, text=True
            )
            if result.returncode != 0:
                print(result.stdout)
                print("Error when command was launched:")
                print(command)
                print("result commande:", result.returncode)
                return None
            
            pattern_convergence = r"Convergence:(.*)"
            line_convergence = re.search(pattern_convergence, result.stdout)
            patterns  = {
                "Fuel_flow": r"Fuel_flow:(\d+.\d+)",
                "HPC_Pout_st": r"HPC_Pout_st:(\d+.\d+)",
                "HPC_Tin": r"HPC_Tin:(\d+.\d+)",
                "HPC_Tout": r"HPC_Tout:(\d+.\d+)",
                "HP_Nmech": r"HP_Nmech:(\d+.\d+)",
                "LPT_Tin": r"LPT_Tin:(\d+.\d+)",
                "LPT_Tout": r"LPT_Tout:(\d+.\d+)",
                "LP_Nmech": r"LP_Nmech:(\d+.\d+)",
                "TSFC": r"TSFC:(\d+.\d+)",
                "Thrust": r"Thrust:(\d+.\d+)",
                "CmpBst.NcRdesMap": r"CmpBst.NcRdesMap:(\d+.\d+)",
                "CmpBst.SMpct": r"CmpBst.SMpct:(\d+.\d+)",
                "CmpFan.NcRdesMap": r"CmpFan.NcRdesMap:(\d+.\d+)",
                "CmpFan.SMpct": r"CmpFan.SMpct:(\d+.\d+)",
                "CmpFan.NcRdesMap_sec": r"CmpFan.NcRdesMap_sec:(\d+.\d+)",
                "CmpFan.SMpct_sec": r"CmpFan.SMpct_sec:(\d+.\d+)",
                "CmpH.NcRdesMap": r"CmpH.NcRdesMap:(\d+.\d+)",
                "CmpH.SMpct": r"CmpH.SMpct:(\d+.\d+)",
            }

            outputs = {}
            for output, pattern in patterns.items():
                pattern_found = re.search(pattern, result.stdout)
                if pattern_found:
                    outputs[output] = [float(pattern_found.group(1))]

            df = pd.DataFrame(outputs)
            df["Convergence"] = line_convergence.group(0)[len("Convergence:") :]
            complete_df.append(df)

        complete_df = pd.concat(complete_df, ignore_index=True)

        return complete_df

    def build_command(self, FN_CR, deg_values, ALT, DTAMB, MACH, CPPPHASE):

        args_command = [str(FN_CR)] + [str(v) for v in deg_values] + [
                str(ALT),
                str(DTAMB),
                str(MACH),
                str(CPPPHASE)
            ]

        command = f"cd {self.ROOT}\n"
        command += "export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:.\n"
        command += "./main_saearp4868_linux_gcc64v4_8.exe " + " ".join(args_command) + " 0.0 \n"
        command += "cd -\n"

        return command
