class CyberWizEmailClientError(Exception):
    """An error while pc api call."""

    def __init__(self, end_point, status_code):
        self.end_point = end_point
        self.status_code = status_code
