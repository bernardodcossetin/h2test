import numpy as np

def GHG_ICEV(tipo, yearly_mileage, fuel_eco, W, years, ghg_fuel_e):
    GHG_vehicle = 4.56e3 * W
    GHG_recycling = -2.93e3 * W
    consumo_anual = yearly_mileage / fuel_eco
    GHG_fuel_ano = consumo_anual * ghg_fuel_e
    ghg_acumulado = []
    for ano in range(0, years + 1):
        ghg_total = (GHG_vehicle + GHG_fuel_ano * ano)/ 10**6
        if ano == years:
            ghg_total = (GHG_vehicle + GHG_recycling + GHG_fuel_ano * ano)/ 10**6
        ghg_acumulado.append(ghg_total)
    GHG=(GHG_vehicle+GHG_recycling+GHG_fuel_ano*years)/10**6
    GHG_km=GHG* 10**6/(years*yearly_mileage)

    return [np.array(GHG),np.array(GHG_km),ghg_acumulado]

def TCO_ICEV(veh_cost, yearly_mileage, fuel_eco, years, al, uf, fp, exchange, dolar):
    r = 0.1          
    dr = 0.06412427874061244      
    ins = 0.06       
    C_vehicle = veh_cost
    C_maintenance = 800/dolar
    soma_q=0
    if exchange == 'BRL(R$)':
        C_maintenance = C_maintenance*dolar
    consumo_anual = yearly_mileage / fuel_eco
    C_fuel = fp * consumo_anual
    TCO_acumulado = []
    TCO = C_vehicle  
    for i in range(1, years + 1):
        V_venal = veh_cost * (1 - dr) ** i
        C_insurance = V_venal * ins
        C_taxes = V_venal * al
        fator_desc = 1 / (1 + r) ** i
        custo_anual = (C_maintenance + C_fuel + C_insurance + C_taxes) * fator_desc
        soma_q+= yearly_mileage* fator_desc
        TCO += custo_anual
        if i == years:
            C_resale = -veh_cost * (1 - dr) ** years
            TCO += C_resale / (1 + r) ** years
        TCO_acumulado.append(TCO)
    LCOD=TCO/soma_q

    return [np.array(TCO),np.array(LCOD),TCO_acumulado]

def GHG_BEV(W, yearly_mileage, fuel_eco, years, ghg_kwh, veh_bat_cap):
    grid_losses = 0.15
    ciclos_limite = 1000
    p_veh = 4.56 * 1000  
    p_bat = 83.5 * 1000  
    r_veh = -2.93 * 1000  
    r_bat = -48.4 * 1000  
    prod_emissions_base = W * p_veh + veh_bat_cap * p_bat  
    ghg_ac = []
    total_prod_emissions = prod_emissions_base
    last_extra_bat = 0  
    for y in range(0, years + 1):
        extra_bat = int(yearly_mileage * y * fuel_eco / (ciclos_limite * veh_bat_cap))
        if extra_bat > last_extra_bat:
            total_prod_emissions += (extra_bat - last_extra_bat) * veh_bat_cap * p_bat
            last_extra_bat = extra_bat
        uti_emissions = y * yearly_mileage * ghg_kwh * fuel_eco / (1 - grid_losses)
        if y == years:
            rec_emissions = W * r_veh + (1 + extra_bat) * veh_bat_cap * r_bat
        else:
            rec_emissions = 0
        total_emissions = (total_prod_emissions + uti_emissions + rec_emissions) / 10**6
        if y == 0:
            ghg_ac.append(total_emissions-(uti_emissions/10**6))
        else:
            ghg_ac.append(total_emissions)
    GHG = ghg_ac[-1]
    GHG_km = GHG * 10**6 / (years * yearly_mileage)

    return [np.array(GHG),np.array(GHG_km), ghg_ac]

def TCO_BEV(veh_cost, fuel_eco, years, yearly_mileage, tf, al, dolar, exchange, veh_bat_cap):
    i = 0
    d = 0.1
    ins_pct = 0.06
    C_mnt_BEV = 400
    dp_BEV = 0.139
    bat_cost = 115 * dolar
    ciclos_limite = 1000
    if exchange == 'USD($)':
        veh_cost *= dolar
    def PW(y, i, d=10):
        if i > 1:
            i = i / 100
        if d > 1:
            d = d / 100
        return ((1 + i) ** (y - 1)) * (1 + d) ** (-y)
    def PWF(N, i, d):
        if i > 1:
            i = i / 100
        if d > 1:
            d = d / 100
        if i == d:
            return N / (i + 1)
        else:
            return (1 / (d - i)) * (1 - ((1 + i) / (1 + d)) ** N)
    tco_ac = []
    for year in range(1, years + 1):
        extra_bat = int(yearly_mileage * year * fuel_eco / (ciclos_limite * veh_bat_cap))
        fuel_cost = (yearly_mileage * tf * fuel_eco) * PWF(year, i, d)
        mnt_cost = C_mnt_BEV * PWF(year, i, d) + extra_bat * veh_bat_cap * bat_cost
        resale = veh_cost * (1 - dp_BEV) ** year * PW(year, i, d)
        IPVA_cost = 0
        ins_cost = 0
        for y in range(1, year + 1):
            IPVA_cost += al * veh_cost * (1 - dp_BEV) ** y * PW(y, i, d)
            ins_cost += ins_pct * veh_cost * (1 - dp_BEV) ** y * PW(y, i, d)
        capex = veh_cost
        opex = fuel_cost + IPVA_cost + ins_cost + mnt_cost
        TCO = capex + opex
        if exchange == 'USD($)':
            TCO /= dolar
        if year == years:
            TCO = capex + opex - resale
            if exchange == 'USD($)':
                TCO /= dolar
        LCOD = TCO / (yearly_mileage * PWF(year, i, d))
        tco_ac.append(TCO)

    return [np.array(TCO),np.array(LCOD),tco_ac]

def GHG_FCEV(tipo, yearly_mileage, fuel_eco, W, years):
    GHG_vehicle = 4.56 * (10 ** 3) * W 
    GHG_recycling = -2.93 * (10 ** 3) * W 
    GHG_FC = 128 * 9.21 * 1000 
    if tipo == 'H2':
        LHV = 54 
        d = 1
        wtw = (157.5/1000 * 23.5/20 + 0) * 1000
    consumo_anual = yearly_mileage / fuel_eco
    GHG_fuel_ano = consumo_anual * LHV * d * wtw
    ghg_acumulado = []
    for ano in range(0, years + 1):
        if ano < 10:
            ghg_total = (GHG_vehicle + GHG_fuel_ano * ano) / 10 ** 6
        elif ano == 10:
            ghg_total = (GHG_vehicle + GHG_FC + GHG_fuel_ano * ano) / 10 ** 6
        elif ano < 20:
            ghg_total = (GHG_vehicle + GHG_FC + GHG_fuel_ano * ano) / 10 ** 6
        else:
            ghg_total = (GHG_vehicle + GHG_FC + GHG_recycling + GHG_fuel_ano * ano) / 10 ** 6
        ghg_acumulado.append(ghg_total)
    GHG = (GHG_vehicle + GHG_recycling + GHG_FC + GHG_fuel_ano * years)/10**6
    GHG_km = GHG* 10**6 / (years * yearly_mileage)

    return [np.array(GHG),np.array(GHG_km),ghg_acumulado]

def TCO_FCEV(veh_cost, yearly_mileage, fuel_eco, years, fp, al, exchange, dolar):
    r = 0.1
    dr = 0.135
    ins = 0.072
    C_vehicle = veh_cost
    C_replaceFC = 128 * 45 
    C_maintenance = 170
    soma_q = 0
    if exchange == 'BRL(R$)':
        C_maintenance *= dolar
    consumo_anual = yearly_mileage / fuel_eco
    C_fuel = fp * consumo_anual
    TCO = C_vehicle
    TCO_acumulado = []
    for i in range(1, years + 1):
        V_venal = veh_cost * (1 - dr) ** i
        C_insurance = V_venal * ins
        C_taxes = V_venal * al
        fator_desc = 1 / (1 + r) ** i
        custo_anual = (C_maintenance + C_fuel + C_insurance + C_taxes) * fator_desc
        soma_q+= yearly_mileage* fator_desc
        TCO += custo_anual
        if i == 10:
            TCO += C_replaceFC * fator_desc
        if i == years:
            C_resale = -veh_cost * (1 - dr) ** years
            TCO += (C_resale / (1 + r) ** years)
        TCO_acumulado.append(TCO)
    LCOD=TCO/soma_q

    return [np.array(TCO),np.array(LCOD),TCO_acumulado]