class Clock:
    """
    A robust Clock class representing time in hours, minutes, and seconds.
    
    This class provides methods for initializing, displaying, and manipulating
    time values with proper validation according to standard time conventions.
    
    Attributes:
        hours (int): Hours value between 0-23 (24-hour format)
        minutes (int): Minutes value between 0-59
        seconds (int): Seconds value between 0-59
    """

    def __init__(self, hours=0, minutes=0, seconds=0):
        """
        Initialize a new Clock instance with the specified time values.
        
        Args:
            hours (int, optional): Hours value between 0-23. Defaults to 0.
            minutes (int, optional): Minutes value between 0-59. Defaults to 0.
            seconds (int, optional): Seconds value between 0-59. Defaults to 0.
        
        Raises:
            TypeError: If any parameter is not an integer
            ValueError: If any parameter is outside its valid range
        """
        self.set_clock(hours, minutes, seconds)
    
    def set_clock(self, hours, minutes, seconds):
        """
        Set the time of the clock with validation.
        
        Args:
            hours (int): Hours value between 0-23
            minutes (int): Minutes value between 0-59
            seconds (int): Seconds value between 0-59
            
        Returns:
            Clock: Returns self for method chaining
            
        Raises:
            TypeError: If any parameter is not an integer
            ValueError: If any parameter is outside its valid range
        """
        if not all(isinstance(x, int) for x in (hours, minutes, seconds)):
            raise TypeError("All time components must be integers")

        if not 0 <= hours < 24:
            raise ValueError("Hours must be between 0 and 23")
        
        if not 0 <= minutes < 60:
            raise ValueError("Minutes must be between 0 and 59")
            
        if not 0 <= seconds < 60:
            raise ValueError("Seconds must be between 0 and 59")
        
        self.hours = hours
        self.minutes = minutes
        self.seconds = seconds
        
        return self  # Enable method chaining
    
    def __str__(self):
        """
        Return a string representation of the clock in HH:MM:SS format.
        
        Returns:
            str: Formatted time string with leading zeros (e.g., "08:30:05")
        """
        return f"{self.hours:02d}:{self.minutes:02d}:{self.seconds:02d}"
    
    def __repr__(self):
        """
        Return a string that could be used to recreate this Clock instance.
        
        Returns:
            str: A string representation that can be used with eval()
        """
        return f"Clock({self.hours}, {self.minutes}, {self.seconds})"
    
    def add_seconds(self, seconds_to_add):
        """
        Add a specified number of seconds to the clock.
        
        This method handles overflow correctly, adjusting minutes
        and hours as needed.
        
        Args:
            seconds_to_add (int): Number of seconds to add (can be negative)
            
        Returns:
            Clock: Returns self for method chaining
            
        Raises:
            TypeError: If seconds_to_add is not an integer
        """
        if not isinstance(seconds_to_add, int):
            raise TypeError("Seconds to add must be an integer")
            
        # Convert current time to total seconds
        total_seconds = self.hours * 3600 + self.minutes * 60 + self.seconds
        
        # Add the new seconds
        total_seconds += seconds_to_add
        
        # Handle negative values
        while total_seconds < 0:
            total_seconds += 24 * 3600  # Add a full day
        
        # Convert back to h:m:s
        total_seconds %= 24 * 3600  # Ensure we stay within 24 hours
        
        hours = total_seconds // 3600
        remaining = total_seconds % 3600
        minutes = remaining // 60
        seconds = remaining % 60
        
        # Update clock
        return self.set_clock(hours, minutes, seconds)
    
    def __eq__(self, other):
        """
        Compare if this Clock is equal to another Clock instance.
        
        Args:
            other (Clock): Another Clock instance to compare with
            
        Returns:
            bool: True if both clocks show the same time, False otherwise
        """
        if not isinstance(other, Clock):
            return NotImplemented
            
        return (self.hours == other.hours and 
                self.minutes == other.minutes and 
                self.seconds == other.seconds)
    
    def __hash__(self):
        """
        Generate a hash for the Clock instance.
        
        Returns:
            int: Hash value based on time components
        """
        return hash((self.hours, self.minutes, self.seconds))
    
    def to_seconds(self):
        """
        Convert the current time to total seconds since midnight.
        
        Returns:
            int: Total seconds (hours*3600 + minutes*60 + seconds)
        """
        return self.hours * 3600 + self.minutes * 60 + self.seconds
    
    @classmethod
    def from_seconds(cls, total_seconds):
        """
        Create a new Clock instance from total seconds since midnight.
        
        Args:
            total_seconds (int): Total seconds to convert to hours, minutes, seconds
            
        Returns:
            Clock: A new Clock instance set to the calculated time
            
        Raises:
            TypeError: If total_seconds is not an integer
        """
        if not isinstance(total_seconds, int):
            raise TypeError("Total seconds must be an integer")
        
        # Handle negative or very large values
        while total_seconds < 0:
            total_seconds += 24 * 3600
            
        total_seconds %= 24 * 3600
        
        hours = total_seconds // 3600
        remaining = total_seconds % 3600
        minutes = remaining // 60
        seconds = remaining % 60
        
        return cls(hours, minutes, seconds)


if __name__ == "__main__":
    # Example 1
    my_clock = Clock(12, 30, 45)
    print(f"Current time: {my_clock}")
    
    # Add 3665 seconds (1 hour, 1 minute, 5 seconds)
    my_clock.add_seconds(3665)
    print(f"After adding 3665 seconds: {my_clock}")
    
    midnight = Clock.from_seconds(0)
    print(f"Midnight: {midnight}")
    
    clock1 = Clock(9, 30, 0)
    clock2 = Clock(9, 30, 0)
    clock3 = Clock(10, 15, 0)
    
    print(f"Are clock1 and clock2 equal? {clock1 == clock2}")
    print(f"Are clock1 and clock3 equal? {clock1 == clock3}") 

    # Example 2: Demonstrate the use of hash
    clock_dict = {}

    clock1 = Clock(9, 30, 0)
    clock2 = Clock(12, 15, 30)
    clock3 = Clock(9, 30, 0)  # Another instance with the same time as clock1

    clock_dict[clock1] = "Morning Meeting"
    clock_dict[clock2] = "Lunch Break"
    clock_dict[clock3] = "Duplicate Morning Meeting"

    for clock, description in clock_dict.items():
        print(f"{clock}: {description}")

    # Check if clock1 and clock3 are considered equal
    print(f"Are clock1 and clock3 equal? {clock1 == clock3}")
    print(f"Hash of clock1: {hash(clock1)}")
    print(f"Hash of clock3: {hash(clock3)}")