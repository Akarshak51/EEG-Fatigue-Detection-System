def process_eeg_data(data):
    # Example: Normalize incoming EEG data
    return [x / max(data) for x in data] if max(data) != 0 else data
