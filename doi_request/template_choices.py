FEEDBACK_STATUS_TO_TEMPLATE = {
    'waiting': ('warning', 'orange', 'fa-minus'),
    'warning': ('danger', 'red', 'fa-close'),
    'error': ('danger', 'red', 'fa-close'),
    'success': ('success', 'green', 'fa-check'),
    'unknow': ('default', 'gray', 'fa-info'),
    'failure': ('danger', 'red', 'fa-close'),
    'info': ('waiting', 'gray', 'fa-info'),
    'notapplicable': ('default', 'gray', 'fa-info')
}

SUBMISSION_STATUS_TO_TEMPLATE = {
    'waiting': ('warning', 'orange', 'fa-minus'),
    'error': ('danger', 'red', 'fa-close'),
    'success': ('success', 'green', 'fa-check'),
    'unknow': ('default', 'gray', 'fa-info'),
    'info': ('waiting', 'gray', 'fa-info'),
    'notapplicable': ('default', 'gray', 'fa-info')
}

TIMELINE_STATUS_TO_TEMPLATE = {**FEEDBACK_STATUS_TO_TEMPLATE, **SUBMISSION_STATUS_TO_TEMPLATE}