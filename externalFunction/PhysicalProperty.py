# PEFPROF查找氢气物性模块的封装
from ctREFPROP.ctREFPROP import REFPROPFunctionLibrary

RP = REFPROPFunctionLibrary('F:\\1_Refprop\\REFPRP64.DLL', 'dll')
RP.SETPATHdll('F:\\1_Refprop\\REFPROP\\fluids')
r = RP.SETUPdll(1, 'HYDROGEN.FLD', 'HMX.BNC', 'DEF')
assert (r.ierr == 0)
info = RP.INFOdll(1)


def searchHByPD(P, D):
    # P: kPa, D: kg/m^3, h: kJ/kg
    sig1 = RP.PDFL1dll(P, D / info.wmm, [1.0])
    return RP.ENTHALdll(sig1.T, D, [1.0]) / info.wmm


def searchTByDH(D, h):
    # D: kg/m^3, h: kJ/kg, T: K
    sig = RP.DHFL1dll(D / info.wmm, h * info.wmm, [1.0])
    return sig.T


def searchPByDH(D, h):
    # D: kg/m^3, h: J/mol, p: kPa
    sig1 = RP.DHFL1dll(D / info.wmm, h * info.wmm, [1.0])
    return RP.PRESSdll(sig1.T, D / info.wmm, [1.0])
