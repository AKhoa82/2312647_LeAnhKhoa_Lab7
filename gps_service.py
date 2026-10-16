class GPSSignalLostError(Exception):
    """Ngoai le khi thiet bi mat tin hieu GPS."""
    pass


def get_current_location():
    """
    Mo phong dich vu GPS.
    """
    return (10.0, 105.0)