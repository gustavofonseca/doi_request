import os

from datetime import datetime
from datetime import timedelta


def check_session(wrapped):
    """
        Decorator to check and update session attributes.
    """

    def check(request, *arg, **kwargs):
        to_date = datetime.now() + timedelta(days=1)
        from_date = to_date - timedelta(days=30)
        default_date_range = ' - '.join([
            from_date.strftime('%m/%d/%Y')[:10],
            to_date.strftime('%m/%d/%Y')[:10]]
        )
        filter_issn = request.GET.get(
            'filter_issn',
            request.session.get('filter_issn', '')
        )
        locale = request.GET.get(
            '_LOCALE_',
            request.session.get('_LOCALE_', request.locale_name)
        )
        filter_submission_status = request.GET.get(
            'filter_submission_status',
            request.session.get('filter_submission_status', '')
        )
        filter_feedback_status = request.GET.get(
            'filter_feedback_status',
            request.session.get('filter_feedback_status', '')
        )
        filter_start_range = request.GET.get(
            'filter_start_range',
            request.session.get('filter_start_range', default_date_range)
        )
        filter_prefix = request.GET.get(
            'filter_prefix',
            request.session.get('filter_prefix', '')
        )
        offset = request.GET.get(
            'offset',
            request.session.get('offset', 0)
        )
        request.session['offset'] = int(offset)
        request.session['filter_issn'] = filter_issn
        request.session['filter_submission_status'] = filter_submission_status
        request.session['filter_feedback_status'] = filter_feedback_status
        request.session['filter_start_range'] = filter_start_range
        request.session['filter_prefix'] = filter_prefix
        request.session['_LOCALE_'] = locale

        return wrapped(request, *arg, **kwargs)

    check.__doc__ = wrapped.__doc__

    return check


def base_data_manager(wrapped):
    """
        Decorator to load common data used by all views
    """

    def check(request, *arg, **kwargs):

        data = {}
        data['crossref_prefix'] = os.environ.get('CROSSREF_PREFIX', 'não definido')
        data['crossref_user_api'] = os.environ.get('CROSSREF_API_USER', 'não definido')
        data['crossref_depositor_name'] = os.environ.get('CROSSREF_DEPOSITOR_NAME', 'não definido')
        data['crossref_depositor_email'] = os.environ.get('CROSSREF_DEPOSITOR_EMAIL', 'não definido')
        data['version'] = request.version()
        data['locale'] = request.session['_LOCALE_']

        setattr(request, 'data_manager', data)

        return wrapped(request, *arg, **kwargs)

    check.__doc__ = wrapped.__doc__

    return check