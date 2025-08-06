def GHG_ICEV(tipo, yearly_mileage, fuel_eco, W, years, ghg_fuel_e):
    GHG_vehicle=4.56*(10**3)*W
    GHG_recycling=-2.93*(10**3)*W
    consumo_anual=yearly_mileage/fuel_eco
    GHG_fuel=consumo_anual*ghg_fuel_e
    GHG=GHG_vehicle+GHG_recycling+GHG_fuel*years
    GHG_km=GHG/(years*yearly_mileage)

    return [GHG, GHG_km, ghg_fuel_e] 

def TCO_ICEV(veh_cost, yearly_mileage, fuel_eco, years, al, uf, fp, r=0.1, dr=0.0641, ins=0.06):
    C_vehicle=veh_cost
    C_resale=-veh_cost*(1-dr)**years
    C_maintenance=160
    consumo_anual=yearly_mileage/fuel_eco
    C_fuel=fp*consumo_anual
    TCO=C_vehicle+C_resale/(1+r)**years
    soma_fuel = 0
    soma_maint = 0
    soma_ins = 0
    soma_tax = 0
    soma_q=0
    for i in range(1, int(years) + 1):
         V_venal = veh_cost * (1 - dr)**i
         V_venal = float(V_venal)
         C_insurance = V_venal * ins
         C_taxes = V_venal * al
         fator_desc = 1 / (1 + r)**i
         soma_fuel += C_fuel * fator_desc
         soma_maint += C_maintenance * fator_desc
         soma_ins += C_insurance * fator_desc
         soma_tax += C_taxes * fator_desc
         soma_q+= yearly_mileage* fator_desc
         TCO += (C_maintenance + C_fuel + C_insurance + C_taxes) * fator_desc
    LCOD=TCO/soma_q

    return [TCO, LCOD]

def GHG_ICEV_ac(tipo, yearly_mileage, fuel_eco, W, years, ghg_fuel_e):
    GHG_vehicle = 4.56e3 * W
    GHG_recycling = -2.93e3 * W
    consumo_anual = yearly_mileage / fuel_eco
    GHG_fuel_ano = consumo_anual * ghg_fuel_e
    ghg_acumulado = []
    for ano in range(1, years + 1):
        ghg_total = GHG_vehicle + GHG_recycling + GHG_fuel_ano * ano
        ghg_acumulado.append(ghg_total)

    return [ghg_acumulado]

def TCO_ICEV_ac(veh_cost, yearly_mileage, fuel_eco, years, al, uf, fp):
    r = 0.1          
    dr = 0.0641      
    ins = 0.06       
    C_vehicle = veh_cost
    C_maintenance = 160
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
        TCO += custo_anual
        if i == years:
            C_resale = -veh_cost * (1 - dr) ** years
            TCO += C_resale / (1 + r) ** years

        TCO_acumulado.append(TCO)

    return [TCO_acumulado]



