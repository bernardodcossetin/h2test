import numpy as np
import pandas as pd

index = ['Vehicle Cost [BRL]', 
         'Gasoline Fuel Economy [km/L]'   , 
         'Ethanol Fuel Economy [km/L]'    , 
         'Electric Fuel Economy [kWh/km]' , 
         'Vehicle Mass [kg]',
         'Battery Capacity [kWh]', 
         'Vehicle Type',
         'Vehicle Category'
         ]
vehicle_Data_Base = pd.DataFrame(index = index)

vehicle_Data_Base['RENAULT - KWID']         = [ 70144,  15.3, 10.8,      0,  818,    0, 'ICEV', 'Sub-Compact']
vehicle_Data_Base['FIAT - MOBI']            = [ 73114,  13.5,  9.6,      0,  933,    0, 'ICEV', 'Sub-Compact']
vehicle_Data_Base['FIAT - ARGO']            = [ 85700,  13.3,  9.4,      0, 1105,    0, 'ICEV', 'Compact']
vehicle_Data_Base['HYUNDAI - HB20']         = [ 87453,  13.5,  9.6,      0,  990,    0, 'ICEV', 'Compact']
vehicle_Data_Base['CHEVROLET - ONIX']       = [ 99682,  13.3,  9.3,      0, 1030,    0, 'ICEV', 'Medium']
vehicle_Data_Base['VW - POLO']              = [102314,  12.5,  8.5,      0, 1113,    0, 'ICEV', 'Medium']
vehicle_Data_Base['TOYOTA - COROLLA']       = [156913,  12.3,  8.6,      0, 1375,    0, 'ICEV', 'Large']
vehicle_Data_Base['HONDA - CITY']           = [146025,  13.1,  9.2,      0, 1165,    0, 'ICEV', 'Large']
vehicle_Data_Base['CHEVROLET - TRACKER']    = [148819,  11.9,  8.2,      0, 1228,    0, 'ICEV', 'Large']
vehicle_Data_Base['VW - NIVUS']             = [140526,  10.7,  7.3,      0, 1206,    0, 'ICEV', 'Large']
vehicle_Data_Base['JEEP - RENEGADE']        = [137548,  11.0,  7.7,      0, 1206,    0, 'ICEV', 'Large']


vehicle_Data_Base['KIA - STONIC*']           = [154110,  13.7, np.nan,    0, 1256,    0,  'HEV', 'Medium' ]
vehicle_Data_Base['HYUNDAI - IONIQ']          = [130032,  18.9, np.nan,    0, 1422,  1.3,  'HEV', 'Medium']
vehicle_Data_Base['TOYOTA - PRIUS (2021)']    = [182100,  18.9, np.nan,    0, 1400,  1.3,  'HEV', 'Medium']
vehicle_Data_Base['TOYOTA - COROLLA ALTIS']   = [189012,  18.5,   12.6,    0, 1405,  1.6,  'HEV', 'Large']
vehicle_Data_Base['GWM - HAVAL H6']           = [219034,  13.8, np.nan,    0, 1699,  1.6,  'HEV', 'Large']
vehicle_Data_Base['TOYOTA - COROLLA CROSS']   = [206788,  17.8,   11.8,    0, 1400,  1.3,  'HEV', 'Large']
vehicle_Data_Base['CAOA CHERY - ARRIZO 6*']  = [140487,  12.5,    8.9,    0, 1378,    0,  'HEV', 'Large']
vehicle_Data_Base['FIAT - FASTBACK AUDACE*'] = [149417,  12.6,    8.9,    0, 1253,    0,  'HEV', 'Large']
vehicle_Data_Base['FIAT - PULSE AUDACE*']    = [129520,  13.4,    9.3,    0, 1234,    0,  'HEV', 'Large']


vehicle_Data_Base['BYD - SONG PLUS']        = [229965,  15.1, np.nan, 0.1806, 1790, 18.3,  'PHEV', 'Large']
vehicle_Data_Base['BYD - SONG PRO']         = [181425,  15.2, np.nan, 0.1556, 1700, 12.9,  'PHEV', 'Large']
vehicle_Data_Base['BYD - KING']             = [164580,  16.8, np.nan, 0.1389, 1515,  8.3,  'PHEV', 'Large']
vehicle_Data_Base['JEEP - COMPASS']         = [279516,  11.5, np.nan, 0.2222, 1908, 11.4,  'PHEV', 'Large']


vehicle_Data_Base['RENAULT - KWID E-TECH']  = [101000,     0,    0, 0.1233,  977, 26.8,  'BEV', 'Sub-Compact']
vehicle_Data_Base['BYD - DOLPHIN MINI']     = [120800,     0,    0, 0.1139, 1239,   38,  'BEV', 'Sub-Compact']
vehicle_Data_Base['JAC - E-J61']            = [134566,     0,    0, 0.1389, 1180,   30,  'BEV', 'Sub-Compact']
vehicle_Data_Base['BYD - DOLPHIN']          = [159777,     0,    0, 0.1167, 1412, 44.9,  'BEV', 'Medium']
vehicle_Data_Base['VOLVO - EX30']           = [219020,     0,    0, 0.1528, 1840,   51,  'BEV', 'Medium']
vehicle_Data_Base['BYD - YUAN PRO']         = [178020,     0,    0, 0.1417, 1550, 45.1,  'BEV', 'Medium']
vehicle_Data_Base['GWM - ORA 03']           = [159000,     0,    0, 0.1444, 1570,   48,  'BEV', 'Medium']
vehicle_Data_Base['BYD - YUAN PLUS']        = [235801,     0,    0, 0.1556, 1700, 60.5,  'BEV', 'Large']

def veh_data_base():
    return vehicle_Data_Base

