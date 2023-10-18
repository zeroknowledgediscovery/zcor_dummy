import pandas as pd


def json_to_row(json_obj: dict, TIME_UNIT: str = "WEEK") -> dict:
    """
    Convert a JSON object to a dictionary row representation (convertable to a pd.DataFrame row).

    Args:
        json_obj (dict): JSON object with patient data and records.
        TIME_UNIT (str, optional): Time unit used for date conversion. Choices are "DAY", "MONTH", and "WEEK". Defaults to "WEEK".

    Returns:
        dict: Dictionary row with patient data and formatted records.
    """
    dx_dates = [pd.to_datetime(record['date']) for record in json_obj['DX_record']]
    # Find the earliest date
    start_date = min(dx_dates).strftime('%m-%d-%Y')
    return {
        'patient_id': json_obj['patient_id'],
        'sex': json_obj['sex'],
        'age': json_obj['age'],
        'birth_date': json_obj['birth_date'],
        'fips': json_obj['fips'],
        'start': start_date,
        'DX_record': json_to_record_string(json_obj['DX_record'], start_date, TIME_UNIT),
        'RX_record': json_to_record_string(json_obj['RX_record'], start_date, TIME_UNIT),
        'PROC_record': json_to_record_string(json_obj['PROC_record'], start_date, TIME_UNIT)
    }


def json_to_record_string(records: list, start_date: str, TIME_UNIT: str) -> str:
    """
    Convert a list of JSON record objects into a string representation.

    Args:
        records (list): List of JSON objects with date and code for each record entry.
        start_date (str): Start date for the patient's records in the format '%m-%d-%Y'.
        TIME_UNIT (str): Time unit used for date conversion. Choices are "DAY", "MONTH", and "WEEK".

    Returns:
        str: String representation of records with date offsets and codes.
    """
    offsets = []
    for record in records:
        date_difference = pd.to_datetime(record['date']) - pd.to_datetime(start_date)
        if TIME_UNIT == "DAY":
            offset = date_difference.days
        elif TIME_UNIT == "MONTH":
            offset = date_difference.days // 30
        else:  # Default is "WEEK"
            offset = date_difference.days // 7
        offsets.append(f"{offset}:{record['code']}")
    return '|'.join(offsets)
