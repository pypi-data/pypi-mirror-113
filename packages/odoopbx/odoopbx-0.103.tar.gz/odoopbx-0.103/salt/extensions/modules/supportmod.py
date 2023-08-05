from __future__ import absolute_import, print_function, unicode_literals
from datetime import datetime, timedelta
import logging
from salt.utils.http import query
import urllib
import uuid

__virtualname__ = 'support'

log = logging.getLogger(__name__)

def __virtual__():
    return True


API_URL= 'http://pastebin.com/api_public.php'


def report():
    data = {
        'paste_format': 'bash',
        'paste_code': 'hello world!',
        'paste_name': uuid.uuid4().hex,
        'paste_private': True,
        'paste_expire_date': str(datetime.utcnow() + timedelta(minutes=15))            
    }
    response = query(API_URL, 'POST', data=data)
    print(response)
