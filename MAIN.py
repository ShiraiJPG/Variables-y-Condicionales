# Constantes
TSS_SFS_RATE = 0.0304   # Seguro Familiar de Salud
TSS_SVDS_RATE = 0.0287  # AFP (Pensión)
BONIFICACION_RATE = 1 / 12  # Regalía Pascual (si aplica)

# Tramos de ISR anual (2024-2025)
ISR_TRAMOS = [
    (416220.00, 0.00, 0.00),  # Exento
    (624329.00, 0.15, 416220.01),
    (867123.00, 0.20, 624329.01, 31216.00),
    (float('inf'), 0.25, 867123.01, 79776.00),
]

def calcular_tss(sueldo_bruto):
    """Calcula el descuento total por TSS (SFS + AFP)"""
    return sueldo_bruto * (TSS_SFS_RATE + TSS_SVDS_RATE)

def calcular_isr_anual(sueldo_anual):
    """Calcula el ISR anual basado en tramos simplificados"""
    if sueldo_anual <= ISR_TRAMOS[0][0]:
        return 0.0
    elif sueldo_anual <= ISR_TRAMOS[1][0]:
        excedente = sueldo_anual - ISR_TRAMOS[1][2]
        return excedente * ISR_TRAMOS[1][1]
    elif sueldo_anual <= ISR_TRAMOS[2][0]:
        excedente = sueldo_anual - ISR_TRAMOS[2][2]
        return ISR_TRAMOS[2][3] + excedente * ISR_TRAMOS[2][1]
    else:
        excedente = sueldo_anual - ISR_TRAMOS[3][2]
        return ISR_TRAMOS[3][3] + excedente * ISR_TRAMOS[3][1]

def calcular_bonificacion(sueldo_bruto):
    """Calcula la bonificación proporcional al sueldo"""
    return sueldo_bruto * BONIFICACION_RATE

def validar_entrada(valor):
    try:
        val = float(valor)
        if val < 0:
            raise ValueError("Debe ser un número positivo.")
        return val
    except ValueError:
        print("Entrada inválida. Por favor, introduce un número válido.")
        return None

def main():
    print("=== Calculadora de Sueldo Neto (RD) ===")

    while True:
        bruto_input = input("Introduce el sueldo bruto mensual (RD$): ")
        sueldo_bruto = validar_entrada(bruto_input)
        if sueldo_bruto is not None:
            break

    while True:
        otros_input = input("Introduce otros descuentos mensuales (RD$): ")
        otros_descuentos = validar_entrada(otros_input)
        if otros_descuentos is not None:
            break

    tss = calcular_tss(sueldo_bruto)
    sueldo_anual = (sueldo_bruto - tss) * 12
    isr = calcular_isr_anual(sueldo_anual) / 12  # ISR mensual
    bonificacion = calcular_bonificacion(sueldo_bruto)

    sueldo_neto = sueldo_bruto - tss - isr - otros_descuentos + bonificacion

    # Resultados
    print("\n--- Resultado del Cálculo ---")
    print(f"Sueldo Bruto:         RD$ {sueldo_bruto:,.2f}")
    print(f"- Seguridad Social:   RD$ {tss:,.2f}")
    print(f"- ISR Mensual:        RD$ {isr:,.2f}")
    print(f"- Otros Descuentos:   RD$ {otros_descuentos:,.2f}")
    print(f"+ Bonificación:       RD$ {bonificacion:,.2f}")
    print(f"= Sueldo Neto:        RD$ {sueldo_neto:,.2f}")
    print("-------------------------------")

if __name__ == "__main__":
    main()