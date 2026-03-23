from datetime import datetime
import locale


def get_current_date() -> str:
    """
    Devuelve la fecha y hora actuales con contexto editorial.
    Útil para que los agentes sepan en qué momento están generando contenido.

    Returns:
        String con fecha, hora, día de la semana y número de semana del año.
    """
    now = datetime.now()
    dias = ["lunes", "martes", "miércoles", "jueves", "viernes", "sábado", "domingo"]
    meses = [
        "enero", "febrero", "marzo", "abril", "mayo", "junio",
        "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre",
    ]
    dia_semana = dias[now.weekday()]
    mes = meses[now.month - 1]
    semana_año = now.isocalendar().week

    return (
        f"{dia_semana}, {now.day} de {mes} de {now.year} · "
        f"{now.strftime('%H:%M')} · semana {semana_año}"
    )
