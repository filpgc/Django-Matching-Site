"""
WSGI config for matchingsite project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/howto/deployment/wsgi/
"""

import os
from django.core.wsgi import get_wsgi_application


path = '/Users/bisbis/Desktop/Matching-Site/Matching-Site/matchingsite'
if path not in sys.path:
sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'matchingsite.settings'

# then:

application = get_wsgi_application()
