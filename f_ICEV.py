"""
Funções ICEV

GHG_ICEV
inputs
tipo -  E100 ou E27
yearly_mileage - Q -  Quilometragem anual (km)
fuel_eco - fe - fuel economy do veículo (km/L)
W - Massa do veículo (kg)
years - n - Tempo da análise (anos)
outputs
GHG - Emissões totais ao longo do ciclo de vida (gCO2eq)
GHG_km - GHG normalizada pela quilometragem rodada no ciclo de vida (gCO2eq/km)


TCO_ICEV
inputs
veh_cost - PA - Preço de aquisição do veículo (USD)
r - taxa de desconto (-)
fp - preço do combustível na bomba (USD/L)
al - alíquota IPVA (-)
dr - taxa de depreciação anual média do veículo (-)
ins - porcentagem do valor venal do veículo que equivale ao valor do seguro (-)
yearly_mileage - Q -  Quilometragem anual (km)
fuel_eco - fe - fuel economy do veículo (km/L)
years - n - Tempo da análise (anos)

outputs
TCO - Custo total ao longo do ciclo de vida (USD)
LCOD - Levelized Cost of Driving (USD/km)

"""

def GHG_ICEV(tipo, yearly_mileage, fuel_eco, W, years, verbose=False):
    GHG_vehicle=4.56*(10**3)*W
    GHG_recycling=-2.93*(10**3)*W
    if tipo == 'E100':
        LHV=26.35
        d=0.809
        wtw=(29.46111111111111+0.66) #Média Brasil
        #wtw=(27.7+0.66)
    elif tipo == 'E27':
        LHV=39.32
        d=0.754
        wtw=(75.07)
  
    if tipo not in ['E100', 'E27']:
        raise ValueError(f"Tipo '{tipo}' inválido. Use 'E100' ou 'E27'.")
     
    consumo_anual=yearly_mileage/fuel_eco
    GHG_fuel=consumo_anual*LHV*d*wtw
    GHG=GHG_vehicle+GHG_recycling+GHG_fuel*years
    GHG_km=GHG/(years*yearly_mileage)
    if verbose:
      print("Consumo total (L/ano):", consumo_anual)
      print("GHG produção veículo:", GHG_vehicle)
      print("GHG reciclagem veículo:", GHG_recycling)
      print("GHG combustível:", GHG_fuel)

    return [GHG, GHG_km, GHG_fuel] #gCO2eq, gCO2eq/km

def TCO_ICEV(veh_cost, yearly_mileage, fuel_eco, years, r=0.1, fp= 3.689/4.98, al=0.04,dr=0.0641, ins=0.06, verbose=False):
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
        C_insurance = V_venal * ins
        C_taxes = V_venal * al

        # Custo total anual descontado
        fator_desc = 1 / (1 + r)**i
        soma_fuel += C_fuel * fator_desc
        soma_maint += C_maintenance * fator_desc
        soma_ins += C_insurance * fator_desc
        soma_tax += C_taxes * fator_desc
        soma_q+= yearly_mileage* fator_desc
        TCO += (C_maintenance + C_fuel + C_insurance + C_taxes) * fator_desc
    LCOD=TCO/soma_q
    if verbose:
      print("Consumo total (L/ano):", consumo_anual)
      print("Custo de aquisição do veículo:", C_vehicle)
      print("Receita revenda do veículo:", C_resale)
      print("Custo anual com combustível:", C_fuel)
      print("Custo anual com manutenção:", C_maintenance)
      print("Custo anual com seguro:", C_insurance)
      print("Custo anual com impostos:", C_taxes)

    return [TCO, LCOD, {
        'combustivel': soma_fuel,
        'manutencao': soma_maint,
        'seguro': soma_ins,
        'impostos': soma_tax
    }] #USD, USD/km

def GHG_ICEV_ac(tipo, yearly_mileage, fuel_eco=9.3, W=1034, years=20, verbose=False):
    GHG_vehicle = 4.56e3 * W
    GHG_recycling = -2.93e3 * W
    if tipo == 'E100':
        LHV = 26.35
        d = 0.809
        wtw = 29.46111111111111 + 0.66
    elif tipo == 'E27':
        LHV = 39.32
        d = 0.754
        wtw = 75.07
    else:
        raise ValueError(f"Tipo '{tipo}' inválido. Use 'E100' ou 'E27'.")
    consumo_anual = yearly_mileage / fuel_eco
    GHG_fuel_ano = consumo_anual * LHV * d * wtw
    ghg_acumulado = []
    for ano in range(1, years + 1):
        ghg_total = GHG_vehicle + GHG_recycling + GHG_fuel_ano * ano
        ghg_acumulado.append(ghg_total)

    return [ghg_acumulado]


a=GHG_ICEV('E100',12900,9.3,1034,20)
b=TCO_ICEV(16969,12900,9.3,20,0.1,3.689/4.98,0.04,0.0641,0.06)








