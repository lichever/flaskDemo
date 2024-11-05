from flask import request

import sys
import os
#To resolve the import error, Python needs to recognize min_example as a module by including its directory in sys.path. Here’s a summary of a couple of solutions based on your setup:
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from app import app  # Import directly if `app.py` is in the root `min_example`

print(os.path.join(os.path.dirname(__file__), '..'))


with app.test_request_context('/hello', method='GET'):
    # now you can do something with the request until the
    # end of the with block, such as basic assertions:
    assert request.path == '/hello'
    assert request.method == 'GET'