import os, sys
# add the hellodjango project path into the sys.path
sys.path.append('/usr/local/lib/python2.7/site-packages')
sys.path.append('/usr/local/ansible_task')

# add the virtualenv site-packages path to the sys.path
#sys.path.append('<PATH_TO_VIRTUALENV>/Lib/site-packages')

# poiting to the project settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ansible_task.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

