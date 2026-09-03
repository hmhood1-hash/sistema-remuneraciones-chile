# -*- coding: utf-8 -*-
"""Generación de reportes en PDF (reportlab)."""
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

COLOR_ENCABEZADO = colors.HexColor("#1F3A5F")


def _estilo_tabla():
    return TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), COLOR_ENCABEZADO),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#E9EEF3")]),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ])


def exportar_liquidacion_individual_pdf(liquidacion, trabajador, empresa, ruta_archivo):
    """Genera un PDF con el detalle de la liquidación individual de un trabajador."""
    documento = SimpleDocTemplate(ruta_archivo, pagesize=letter)
    estilos = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph("LIQUIDACIÓN DE SUELDO", estilos["Title"]))
    elementos.append(Paragraph(empresa.get("razon_social", "") if empresa else "", estilos["Normal"]))
    elementos.append(Spacer(1, 0.3 * cm))
    elementos.append(Paragraph(
        "Trabajador: {} {} {}".format(
            trabajador.get("nombres", ""), trabajador.get("apellido_paterno", ""),
            trabajador.get("apellido_materno", "") or ""
        ),
        estilos["Normal"],
    ))
    elementos.append(Paragraph("RUT: {}".format(trabajador.get("rut", "")), estilos["Normal"]))
    elementos.append(Paragraph(
        "Período: {}/{}".format(liquidacion.get("mes"), liquidacion.get("anio")), estilos["Normal"]
    ))
    elementos.append(Spacer(1, 0.5 * cm))

    datos_tabla = [["Concepto", "Monto ($)"]]
    conceptos = [
        ("Sueldo Base", "sueldo_base"),
        ("Total Haberes Imponibles", "total_haberes_imponibles"),
        ("Total Haberes No Imponibles", "total_haberes_no_imponibles"),
        ("Total Ingreso Bruto", "total_ingreso_bruto"),
        ("Descuento AFP", "monto_afp"),
        ("Descuento Salud", "monto_salud"),
        ("Descuento Seguro Cesantía", "monto_seguro_cesantia"),
        ("Total Descuentos Previsionales", "total_descuentos_previsionales"),
        ("Base Tributable", "base_tributable"),
        ("Impuesto Único", "impuesto_unico"),
        ("Total Descuentos", "total_descuentos"),
        ("SUELDO LÍQUIDO", "sueldo_liquido"),
    ]
    for etiqueta, llave in conceptos:
        datos_tabla.append([etiqueta, "{:,.0f}".format(liquidacion.get(llave, 0) or 0).replace(",", ".")])

    tabla = Table(datos_tabla, colWidths=[10 * cm, 5 * cm])
    tabla.setStyle(_estilo_tabla())
    elementos.append(tabla)

    documento.build(elementos)
    return ruta_archivo


def exportar_tabla_generica_pdf(titulo, encabezados, filas, ruta_archivo):
    """Genera un PDF genérico tabular; usado por el resto de los informes del sistema."""
    documento = SimpleDocTemplate(ruta_archivo, pagesize=letter)
    estilos = getSampleStyleSheet()
    elementos = [Paragraph(titulo, estilos["Title"]), Spacer(1, 0.4 * cm)]

    datos_tabla = [list(encabezados)] + [[str(valor) for valor in fila] for fila in filas]
    tabla = Table(datos_tabla, repeatRows=1)
    tabla.setStyle(_estilo_tabla())
    elementos.append(tabla)

    documento.build(elementos)
    return ruta_archivo
