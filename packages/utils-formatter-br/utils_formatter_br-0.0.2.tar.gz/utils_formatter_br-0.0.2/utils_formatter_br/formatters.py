def currency_format(num):
    return f'R$ {num:,.2f}'. \
        replace(",", ".", 1)[::-1]. \
        replace(".", ",", 1)[::-1]


def date_format(date):
    return date.strftime('%d/%m/%Y')


def porcent_format(num):
    return f'{num*100:.2f}%'.replace('.', ',')
