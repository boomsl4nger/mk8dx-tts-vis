from datetime import timedelta
import re

class TrackTime:
    """Class for handling the time formats in MK8DX time trials. Support for addition, subtraction,
    and stringify functions using `datetime`.
    
    The format is `M:SS.sss`, for example, `1:06.243` and `0:59.100` are possible times.
    """
    TIME_FORMAT_REGEX = r"^(\d+):(\d{2})\.(\d{3})$"

    def __init__(self, time_str: str):
        """Initialises a `TrackTime` object.

        Args:
            time (str): The time in the format `M:SS.sss`.
        """
        if not self.validate_format(time_str):
            raise ValueError("Time format is invalid, should be 'M:SS.sss'")
        self.time = self._parse_time_string(time_str)

    @staticmethod
    def validate_format(time_str: str) -> bool:
        """Check if the given string matches the format `M:SS.sss`.

        Args:
            time_str (str): raw time string

        Returns:
            bool: true if the format matches, otherwise false
        """
        return bool(re.match(TrackTime.TIME_FORMAT_REGEX, time_str))

    @staticmethod
    def _parse_time_string(time_str: str) -> timedelta:
        """Convert a time string in `M:SS.sss` format to a `timedelta` object.
        
        Args:
            time_str (str): Time as a string.
        """
        minutes, seconds = map(float, time_str.split(':'))
        return timedelta(minutes=int(minutes), seconds=seconds)

    @staticmethod
    def _format_timedelta(td: timedelta) -> str:
        """Convert a `timedelta` object to `M:SS.sss` format.
        
        Args:
            td (timedelta): `timedelta` object to convert back to custom format."""
        total_seconds = int(td.total_seconds())
        milliseconds = int(td.microseconds / 1000)
        minutes, seconds = divmod(total_seconds, 60)
        return f"{minutes:01}:{seconds:02}.{milliseconds:03}"
    
    @staticmethod
    def _format_seconds(s: float) -> str:
        """Converts a time float in seconds to a formatted string.

        Args:
            s (float): Time (seconds). Should be a positive float.

        Returns:
            str: Formatted time string.
        """
        if s < 0:
            raise ValueError(f"Time should be positive.")
        return TrackTime._format_timedelta(timedelta(seconds=s))
    
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
    
    def get_timedelta(self) -> timedelta:
        return self.time

    def __add__(self, other):
        other = self._ensure_track_time(other)
        return TrackTime(self._format_timedelta(self.time + other.time))

    def __sub__(self, other):
        other = self._ensure_track_time(other)
        if self.time < other.time:
            # TODO this is a bit jank
            return TrackTime("0:00.000")
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
    
class TrackTimeExt(TrackTime):
    """Extension of TrackTime class to support hours in the format. Format is:
    `H:MM:SS.sss`
    """
    TIME_FORMAT_REGEX = r"^(\d+):(\d{2}):(\d{2})\.(\d{3})$"

    def __init__(self, time_str: str):
        """Initialises a `TrackTimeExt` object.

        Args:
            time (str): The time in the format `H:MM:SS.sss`.
        """
        if not self.validate_format(time_str):
            raise ValueError("Time format is invalid, should be 'H:MM:SS.sss'")
        self.time = self._parse_time_string(time_str)

    @staticmethod
    def validate_format(time_str: str) -> bool:
        """Check if the given string matches the format `M:SS.sss`.

        Args:
            time_str (str): raw time string

        Returns:
            bool: true if the format matches, otherwise false
        """
        return bool(re.match(TrackTimeExt.TIME_FORMAT_REGEX, time_str))

    @staticmethod
    def _parse_time_string(time_str: str) -> timedelta:
        """Convert a time string in `M:SS.sss` format to a `timedelta` object.
        
        Args:
            time_str (str): Time as a string.
        """
        hours, minutes, seconds = map(float, time_str.split(':'))
        return timedelta(hours=int(hours), minutes=int(minutes), seconds=seconds)

    @staticmethod
    def _format_timedelta(td: timedelta) -> str:
        """Convert a `timedelta` object to `M:SS.sss` format.
        
        Args:
            td (timedelta): `timedelta` object to convert back to custom format."""
        total_seconds = int(td.total_seconds())
        milliseconds = int(td.microseconds / 1000)
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:01}:{minutes:02}:{seconds:02}.{milliseconds:03}"
    
    @staticmethod
    def _format_seconds(s: float) -> str:
        return TrackTimeExt._format_timedelta(timedelta(seconds=s))
    
    def _ensure_track_time(self, other):
        """Ensure the other object is either a TrackTimeExt or a valid time string."""
        if isinstance(other, TrackTimeExt):
            return other
        elif isinstance(other, str) and self.validate_format(other):
            return TrackTimeExt(other)
        raise TypeError("Unsupported type. Must be TrackTimeExt or valid time string format.")

    def __repr__(self):
        return f"TrackTimeExt({self})"