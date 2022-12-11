
def format_currency(number: int, locale='es'):
    from babel.numbers import format_decimal

    return "$ " + format_decimal(float(number), format='#,##0.##;-#', locale=locale)
