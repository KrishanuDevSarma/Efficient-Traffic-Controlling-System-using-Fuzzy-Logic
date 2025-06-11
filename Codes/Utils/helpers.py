def validate_input_range(value, name):
    """
    Ensures that the input values for traffic inputs are within 0 to 100.
    Raises ValueError if outside of valid range.
    """
    if not (0 <= value <= 100):
        raise ValueError(f"{name} must be between 0 and 100. Got {value}.")
