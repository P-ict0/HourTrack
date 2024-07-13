import platform
from datetime import datetime


#########################################################################
######################## Check the OS ###################################
#########################################################################
def is_windows() -> bool:
    """
    Check the OS and send the notification

    :return: True if the OS is Windows, False otherwise
    """
    return True if platform.system() == "Windows" else False


#########################################################################
######################## User input #####################################
#########################################################################
def ask_yes_no(question: str) -> bool:
    """
    Ask a yes/no question with a default to yes

    :param question: The question to ask
    :return: True if the user answers yes, False otherwise
    """
    while True:
        answer = input(f"{question} [Y]es/[n]o: ").strip().lower()
        if answer in ["y", "yes", ""]:
            return True
        elif answer in ["n", "no"]:
            return False
        else:
            print("Please enter 'yes', 'no', or leave blank for 'yes'.")


#########################################################################
######################## Time formatting ################################
#########################################################################
def format_time(seconds: int, mode: str) -> str:
    """
    Format seconds into a human-readable time string. It goes up to months

    :param seconds: The number of seconds to format
    :param mode: The mode to use for formatting
        - "smart": Display in the most appropriate units (e.g. 1 hour, 30 minues)
        - "full": Display in full (e.g. 1 hour, 30 minutes, 15 seconds)
        - "short": Display in short (e.g. 1h 30m 15s)
        - "hours": Display only in hours (e.g. 1)

    :return: The formatted time string
    """

    # Constants for time units
    SECONDS_PER_MINUTE = 60
    SECONDS_PER_HOUR = 3600
    SECONDS_PER_DAY = 86400
    SECONDS_PER_WEEK = 604800
    SECONDS_PER_MONTH = 2592000  # Approximated as 30 days for simplicity

    months, remainder = divmod(seconds, SECONDS_PER_MONTH)
    weeks, remainder = divmod(remainder, SECONDS_PER_WEEK)
    days, remainder = divmod(remainder, SECONDS_PER_DAY)
    hours, remainder = divmod(remainder, SECONDS_PER_HOUR)
    minutes, seconds = divmod(remainder, SECONDS_PER_MINUTE)

    def format_full() -> str:
        """
        Format the time string in a full format
        """
        parts = []
        if months > 0:
            parts.append(f"{months} month{'s' if months > 1 else ''}")
        if weeks > 0:
            parts.append(f"{weeks} week{'s' if weeks > 1 else ''}")
        if days > 0:
            parts.append(f"{days} day{'s' if days > 1 else ''}")
        if hours > 0:
            parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
        if minutes > 0:
            parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
        if seconds > 0 or not parts:
            parts.append(f"{seconds} second{'s' if seconds > 1 else ''}")
        return ", ".join(parts)

    def format_short() -> str:
        """
        Format the time string in a short format
        """
        parts = []
        if months > 0:
            parts.append(f"{months}mo")
        if weeks > 0:
            parts.append(f"{weeks}w")
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if seconds > 0 or not parts:
            parts.append(f"{seconds}s")
        return " ".join(parts)

    def format_smart() -> str:
        """
        Smartly format the time string based on the largest unit available
        """
        if months > 0:
            parts = [f"{months} month{'s' if months > 1 else ''}"]
            if weeks > 0:
                parts.append(f"{weeks} week{'s' if weeks > 1 else ''}")
            if days > 0:
                parts.append(f"{days} day{'s' if days > 1 else ''}")
            if hours > 0:
                parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
            return ", ".join(parts)
        elif weeks > 0:
            parts = [f"{weeks} week{'s' if weeks > 1 else ''}"]
            if days > 0:
                parts.append(f"{days} day{'s' if days > 1 else ''}")
            if hours > 0:
                parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
            return ", ".join(parts)
        elif days > 0:
            parts = [f"{days} day{'s' if days > 1 else ''}"]
            if hours > 0:
                parts.append(f"{hours} hour{'s' if hours > 1 else ''}")
            if minutes > 0:
                parts.append(f"{minutes} minute{'s' if minutes > 1 else ''}")
            return ", ".join(parts)
        elif hours > 0:
            return f"{hours} hour{'s' if hours > 1 else ''}, {minutes} minute{'s' if minutes > 1 else ''}"
        elif minutes > 0:
            return f"{minutes} minute{'s' if minutes > 1 else ''}, {seconds} second{'s' if seconds > 1 else ''}"
        return f"{seconds} second{'s' if seconds > 1 else ''}"

    def format_hours() -> str:
        """
        Format the time string in hours with one decimal place

        Returns:
        str: The formatted time string in hours
        """
        total_hours = (
            months * (30 * 24)
            + weeks * (7 * 24)
            + days * 24
            + hours
            + minutes / 60
            + seconds / 3600
        )
        return f"{round(total_hours, 1)} hours"

    if mode == "full":
        return format_full()
    elif mode == "short":
        return format_short()
    elif mode == "smart":
        return format_smart()
    elif mode == "hours":
        return format_hours()
    else:
        print("Error: Invalid format: {mode}")
        print("Valid formats: 'smart', 'full', 'short', 'hours'")


def format_timestamp(timestamp: str) -> str:
    """
    Format the given timestamp to a human-readable format.

    Parameters:
    timestamp (str): The timestamp to format.

    Returns:
    str: The formatted timestamp.
    """
    # Parse the timestamp to a datetime object
    dt = datetime.fromisoformat(timestamp)

    # Format the datetime object to a human-readable string
    human_readable = dt.strftime("%d-%m-%Y %H:%M:%S")

    return human_readable
