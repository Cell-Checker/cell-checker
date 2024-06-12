def check_keys_in_list(dict_list, required_keys):
    """
    Check if the required keys are present in the list of dictionaries.

    Parameters:
    dict_list (list): List of dictionaries to check.
    required_keys (set): Set of required keys.

    Returns:
    tuple: (bool, set)
        - bool: True if all required keys are present, False otherwise.
        - set: None if all keys are present, otherwise the set of missing keys.
    """
    # Collect keys from the list of dictionaries
    collected_keys = dict_list.keys()

    # Determine missing keys
    missing_keys = required_keys - collected_keys

    # Check if there are missing keys
    if not missing_keys:
        return True, None
    else:
        return False, missing_keys

