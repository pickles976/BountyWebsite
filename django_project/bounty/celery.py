from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'django_project.settings')

app = Celery('simpletask')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.

app.config_from_object('django.conf:settings', namespace='CELERY')


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))

# Schedule tasks on a beat
app.conf.beat_schedule = {
    #Scheduler Name
    'check_war_ten_minutes': {
        # Task Name (Name Specified in Decorator)
        'task': 'check_war_status',  
        # Schedule      
        'schedule': 3600.0, 
    },
    #Scheduler Name
    'check_bounties_hourly': {
        # Task Name (Name Specified in Decorator)
        'task': 'close_old_bounties',  
        # Schedule      
        'schedule': 3600.0,
        # Function Arguments 
        # 'args': (10,20) 
    },
    'refresh_tokens_hourly': {
        # Task Name (Name Specified in Decorator)
        'task': 'refresh_tokens',  
        # Schedule      
        'schedule': 3600.0,
    },
    # 'test_celery': {
    #     # Task Name (Name Specified in Decorator)
    #     'task': 'test_celery',  
    #     # Schedule      
    #     'schedule': 60.0,
    # },
}  