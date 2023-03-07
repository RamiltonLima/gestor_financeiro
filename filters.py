
import locale

def format_date(date, format='%d/%m/%Y %H:%M'):
    return date.strftime(format)

def format_currency(value):
    return "R$ {:,.2f}".format(value)

def print_debug(value):
    print(value)
    return ''

def float_reais(value):
    locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')
    return locale.currency(value, grouping=True, symbol=True)

def float_porcentagem(value):
    return "{:,.0f}%".format(float(value)*100)