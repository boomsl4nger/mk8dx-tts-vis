from datetime import timedelta

class TrackTime:
    """Class for handling the time formats in MK8DX time trials. Support for addition, subtraction,
    and stringify functions using `datetime`.
    
    The format is `M:SS.mmm`, for example, `1:40.243` and `0:59.100` are possible times.
    """
    def __init__(self, time: str):
        """Initialises a `TrackTime` object.

        Args:
            time (str): The time in the format `M:SS.mmm`.
        """
        self.time = self._parse_time(time)

    @staticmethod
    def _parse_time(time_str: str) -> timedelta:
        """Convert a time string in `M:SS.mmm` format to a `timedelta` object.
        
        Args:
            time_str (str): Time as a string.
        """
        minutes, seconds = map(float, time_str.split(':'))
        return timedelta(minutes=int(minutes), seconds=seconds)

    @staticmethod
    def _format_timedelta(td: timedelta):
        """Convert a `timedelta` object to `M:SS.mmm` format.
        
        Args:
            td (timedelta): `timedelta` object to convert back to custom format."""
        total_seconds = int(td.total_seconds())
        milliseconds = int(td.microseconds / 1000)
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes:01}:{seconds:02}.{milliseconds:03}"

    def __str__(self):
        return self._format_timedelta(self.time)