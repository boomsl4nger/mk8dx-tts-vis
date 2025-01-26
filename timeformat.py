from datetime import timedelta
import re

class TrackTime:
    """Class for handling the time formats in MK8DX time trials. Support for addition, subtraction,
    and stringify functions using `datetime`.
    
    The format is `M:SS.mmm`, for example, `1:06.243` and `0:59.100` are possible times.
    """
    TIME_FORMAT_REGEX = r"^(\d+):(\d{2})\.(\d{3})$"

    def __init__(self, time_str: str):
        """Initialises a `TrackTime` object.

        Args:
            time (str): The time in the format `M:SS.mmm`.
        """
        if not self.validate_format(time_str):
            raise ValueError("Time format is invalid, should be 'M:SS.mmm'")
        self.time = self._parse_time_string(time_str)

    @staticmethod
    def validate_format(time_str: str) -> bool:
        """Check if the given string matches the format `M:SS.mmm`.

        Args:
            time_str (str): raw time string

        Returns:
            bool: true if the format matches, otherwise false
        """
        return bool(re.match(TrackTime.TIME_FORMAT_REGEX, time_str))

    @staticmethod
    def _parse_time_string(time_str: str) -> timedelta:
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
    
    def _ensure_track_time(self, other):
        """Ensure the other object is either a TrackTime or a valid time string."""
        if isinstance(other, TrackTime):
            return other
        elif isinstance(other, str) and self.validate_format(other):
            return TrackTime(other)
        raise TypeError("Unsupported type. Must be TrackTime or valid time string format.")

    def get_seconds(self) -> float:
        """Get the time as a number of seconds (as a float).

        Returns:
            float: time in seconds
        """
        return self.time.seconds + self.time.microseconds / 1e6
    
    def get_timedelta(self):
        return self.time

    def __add__(self, other):
        other = self._ensure_track_time(other)
        return TrackTime(self._format_timedelta(self.time + other.time))

    def __sub__(self, other):
        other = self._ensure_track_time(other)
        return TrackTime(self._format_timedelta(self.time - other.time))

    def __eq__(self, other):
        other = self._ensure_track_time(other)
        return self.time == other.time

    def __ge__(self, other):
        other = self._ensure_track_time(other)
        return self.time >= other.time

    def __le__(self, other):
        other = self._ensure_track_time(other)
        return self.time <= other.time

    def __lt__(self, other):
        other = self._ensure_track_time(other)
        return self.time < other.time

    def __gt__(self, other):
        other = self._ensure_track_time(other)
        return self.time > other.time

    def __str__(self):
        return self._format_timedelta(self.time)

    def __repr__(self):
        return f"TrackTime({self})"