# utils_formatter_br

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install utils_formatter_br

```bash
pip install utils-formatter-br
```

## Usage

```python
#format to currency pt-br
from utils_formatter_br import formatters as ft

num = 1000.5
ft.currency_format(num)
# Output: 'R$ 1.000,50'
```

```python
#format to date pt-br
from utils_formatter_br import formatters as ft
from datetime import date

date = date.fromisoformat('2021-07-19')
ft.date_format(date)
# Output: '19/07/2021'
```

```python
#format to porcent pt-br
from utils_formatter_br import formatters as ft

num = 1 / 5 
ft.porcent_format(num)
# Output: '20,00%'
```

## Author
Juan de Oliveira Farias

## License
[MIT](https://choosealicense.com/licenses/mit/)
