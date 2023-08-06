# eventor-py
Python 3 api wrapper for eventor


## Download using pip

> pip install sthlmkollektivtrafik


## Resources
- https://eventor.orientering.se/api/documentation
- https://eventor.orientering.se/Documents/Guide_Eventor_-_Hamta_data_via_API.pdf

## Examples

```python
from eventor_py import Eventor
import os

apikey = os.environ.get('eventorAPI')
eventor = Eventor(apikey, True)

response = eventor.get_events(fromDate="2021-01-01", toDate="2021-12-31")

print(response.content)

```
