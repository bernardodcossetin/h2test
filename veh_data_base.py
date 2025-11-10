import numpy as np
import pandas as pd

index = ['Vehicle Cost [BRL]', 
         'Gasoline Fuel Economy [km/L]'   , 
         'Ethanol Fuel Economy [km/L]'    , 
         'Electric Fuel Economy [kWh/km]' ,
         'Hydrogen Fuel Economy [km/kg H₂]',
         'Vehicle Mass [kg]',
         'Battery Capacity [kWh]', 
         'Vehicle Type',
         'Vehicle Category'
         ]
df = pd.DataFrame(index = index)

df['Compact'] = [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,'Compact']
df['Sub-Compact'] = [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,'Sub-Compact']
df['Medium'] = [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,'Medium']
df['Large'] = [np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,np.nan,'Large']

df['RENAULT - KWID']         = [ 70144,  15.3, 10.8,      0, np.nan, 818,    0, 'ICEV', 'Sub-Compact']
df['FIAT - MOBI']            = [ 73114,  13.5,  9.6,      0, np.nan, 933,    0, 'ICEV', 'Sub-Compact']
df['FIAT - ARGO']            = [ 85700,  13.3,  9.4,      0, np.nan, 1105,    0, 'ICEV', 'Compact']
df['HYUNDAI - HB20']         = [ 87453,  13.5,  9.6,      0, np.nan, 990,    0, 'ICEV', 'Compact']
df['CHEVROLET - ONIX']       = [ 99682,  13.3,  9.3,      0, np.nan, 1030,    0, 'ICEV', 'Medium']
df['VW - POLO']              = [102314,  12.5,  8.5,      0, np.nan, 1113,    0, 'ICEV', 'Medium']
df['TOYOTA - COROLLA']       = [156913,  12.3,  8.6,      0, np.nan, 1375,    0, 'ICEV', 'Large']
df['HONDA - CITY']           = [146025,  13.1,  9.2,      0, np.nan, 1165,    0, 'ICEV', 'Large']
df['CHEVROLET - TRACKER']    = [148819,  11.9,  8.2,      0, np.nan, 1228,    0, 'ICEV', 'Large']
df['VW - NIVUS']             = [140526,  10.7,  7.3,      0, np.nan, 1206,    0, 'ICEV', 'Large']
df['JEEP - RENEGADE']        = [137548,  11.0,  7.7,      0, np.nan, 1206,    0, 'ICEV', 'Large']


df['KIA - STONIC*']           = [154110,  13.7, np.nan,    0, np.nan, 1256,    0,  'HEV', 'Medium' ]
df['HYUNDAI - IONIQ']          = [130032,  18.9, np.nan,    0, np.nan, 1422,  1.3,  'HEV', 'Medium']
df['TOYOTA - PRIUS (2021)']    = [182100,  18.9, np.nan,    0, np.nan, 1400,  1.3,  'HEV', 'Medium']
df['TOYOTA - COROLLA ALTIS']   = [189012,  18.5,   12.6,    0, np.nan, 1405,  1.6,  'HEV', 'Large']
df['GWM - HAVAL H6']           = [219034,  13.8, np.nan,    0, np.nan, 1699,  1.6,  'HEV', 'Large']
df['TOYOTA - COROLLA CROSS']   = [206788,  17.8,   11.8,    0, np.nan, 1400,  1.3,  'HEV', 'Large']
df['CAOA CHERY - ARRIZO 6*']  = [140487,  12.5,    8.9,    0, np.nan, 1378,    0,  'HEV', 'Large']
df['FIAT - FASTBACK AUDACE*'] = [149417,  12.6,    8.9,    0, np.nan, 1253,    0,  'HEV', 'Large']
df['FIAT - PULSE AUDACE*']    = [129520,  13.4,    9.3,    0, np.nan, 1234,    0,  'HEV', 'Large']


df['BYD - SONG PLUS']        = [229965,  15.1, np.nan, 0.1806, np.nan, 1790, 18.3,  'PHEV', 'Large']
df['BYD - SONG PRO']         = [181425,  15.2, np.nan, 0.1556, np.nan, 1700, 12.9,  'PHEV', 'Large']
df['BYD - KING']             = [164580,  16.8, np.nan, 0.1389, np.nan, 1515,  8.3,  'PHEV', 'Large']
df['JEEP - COMPASS']         = [279516,  11.5, np.nan, 0.2222, np.nan, 1908, 11.4,  'PHEV', 'Large']


df['RENAULT - KWID E-TECH']  = [101000,     0,    0, 0.1233, np.nan,  977, 26.8,  'BEV', 'Sub-Compact']
df['BYD - DOLPHIN MINI']     = [120800,     0,    0, 0.1139, np.nan, 1239,   38,  'BEV', 'Sub-Compact']
df['JAC - E-J61']            = [134566,     0,    0, 0.1389, np.nan, 1180,   30,  'BEV', 'Sub-Compact']
df['BYD - DOLPHIN']          = [159777,     0,    0, 0.1167, np.nan, 1412, 44.9,  'BEV', 'Medium']
df['VOLVO - EX30']           = [219020,     0,    0, 0.1528, np.nan, 1840,   51,  'BEV', 'Medium']
df['BYD - YUAN PRO']         = [178020,     0,    0, 0.1417, np.nan, 1550, 45.1,  'BEV', 'Medium']
df['GWM - ORA 03']           = [159000,     0,    0, 0.1444, np.nan, 1570,   48,  'BEV', 'Medium']
df['BYD - YUAN PLUS']        = [235801,     0,    0, 0.1556, np.nan, 1700, 60.5,  'BEV', 'Large']

df['TOYOTA - MIRAI']        = [np.nan, 0,     0,    0, 122, 1900, 0,  'FCEV', 'Large']

def veh_data_base(cat_fuel):
    for cat in df.loc['Vehicle Category'].unique():
        df[cat] = df.loc[:,df.loc['Vehicle Category']==cat].apply(pd.to_numeric, errors="coerce").mean(axis=1)
        df.loc['Vehicle Category',cat]=cat
        df.loc['Vehicle Type',cat]=cat_fuel
    veh_data_base = df.loc[:,df.loc['Vehicle Type']==cat_fuel]
    return veh_data_base

