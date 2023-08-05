#!/usr/bin/env python3

import rappislack
from datetime import date

def makeLog(webhook, module, project, function, error):
    try:
        logDate = date.today()
        logDate = logDate.strftime('%d-%m-%Y')

        rappislack.incomingWebhook(webhook, ':alert: ERROR :alert:\n\nMódulo: {}\nProyecto: {}\nFunción: {}\nFecha: {}\nError: {}'.format(module, project, function, logDate, error))
    except Exception as e:
        rappislack.incomingWebhook(webhook, 'LOG MAKER ERROR: {}'.format(e))