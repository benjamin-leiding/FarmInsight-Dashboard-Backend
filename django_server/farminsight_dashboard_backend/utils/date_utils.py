from datetime import datetime, timedelta
from django.conf import settings

def get_date_range(from_date=None, to_date=None):
    """
    Returns a tuple (from_date_iso, to_date_iso) in ISO 8601 UTC format (YYYY-MM-DDTHH:MM:SSZ).
    If from_date or to_date is None, defaults are set to the set amount of days in the .env file
    before now and now, respectively.
    """
    if not from_date:
        from_date_iso = (datetime.utcnow() - timedelta(days=int(getattr(settings, 'FALLBACK_DATA_RETRIEVAL_IN_DAYS', {})))).isoformat(timespec="seconds") + "Z"
    else:
        from_date_iso = from_date.isoformat(timespec="seconds").replace("+00:00", "Z")

    if not to_date:
        to_date_iso = datetime.utcnow().isoformat(timespec="seconds") + "Z"
    else:
        to_date_iso = to_date.isoformat(timespec="seconds").replace("+00:00", "Z")

    return from_date_iso, to_date_iso
