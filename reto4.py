def inforServicio(lectura: dict, tarifa: dict)->tuple:
   aCalcular = list(filter(lambda evaluar: lectura[evaluar]['estado'] == 'activo', lectura))
   if len(aCalcular) == 0:
       return('Sin lecturas')
   predios = []
   total_consumo = 0
   total_subsidio_consumo = 0
   total_subsidio_cargo = 0
   listPredios = []
   for x in range(0,len(aCalcular)):
       predio = calcularConsumo(lectura[aCalcular[x]],aCalcular[x], tarifa)
       predios.append(predio)
   for y in range(0,len(predios)):
       total_consumo += predios[y][0][1]
       total_subsidio_consumo += predios[y][1][0]
       total_subsidio_cargo += predios[y][1][1]
       listPredios.append(predios[y][0])

   return(listPredios,total_consumo,[total_subsidio_consumo,total_subsidio_cargo])





def calcularConsumo(paraCalc, idPredio, tarifa):
    consumo = paraCalc['toma_lectura'][0]['lec_actual'] - paraCalc['toma_lectura'][0]['lec_anterior']
    if paraCalc['estrato'] == 1:
        subsidio = 0.45
    elif paraCalc['estrato'] == 2:
        subsidio = 0.35
    elif paraCalc['estrato'] == 3:
        subsidio = 0.10
    else:
        subsidio = -0.4

    consumoDescuento = 0
    valorDescuentoConsumo = 0
    valorDescuentCargo = 0
    # print(idPredio, consumo, tarifa['escala_sub'], paraCalc['estrato'])
    # print(tarifa)
    if paraCalc['estrato'] == 1 or paraCalc['estrato'] == 2 or paraCalc['estrato'] == 3:
        if consumo >= tarifa['escala_sub']:
            consumoDescuento = (tarifa['escala_sub'] * tarifa['consumo']) - ((tarifa['escala_sub'] * tarifa['consumo']) * subsidio)
            valorDescuentoConsumo = (tarifa['escala_sub'] * tarifa['consumo']) * subsidio
            consumo = consumo - tarifa['escala_sub']
            valorConsumo = consumo * (tarifa['consumo'])
            valorDescuentCargo = tarifa['cargo_basico'] * subsidio
            cargoBasico = tarifa['cargo_basico'] - (tarifa['cargo_basico'] * subsidio)
        else:
            valorConsumo = consumo * (tarifa['consumo'])
            valorConsumo = valorConsumo - (valorConsumo * subsidio)
            cargoBasico = tarifa['cargo_basico'] - (tarifa['cargo_basico'] * subsidio)
            valorDescuentCargo = tarifa['cargo_basico'] * subsidio
            valorDescuentoConsumo = (tarifa['escala_sub'] * tarifa['consumo']) * subsidio
    else:
        valorConsumo = consumo * (tarifa['consumo'])
        valorConsumo = valorConsumo - (valorConsumo * subsidio)
        cargoBasico = tarifa['cargo_basico'] - (tarifa['cargo_basico'] * subsidio)

    valor = valorConsumo + cargoBasico + consumoDescuento
    return [(idPredio,round(valor,2)),[round(valorDescuentoConsumo,2),round(valorDescuentCargo,2)]]
