from datetime import date, timedelta


def remove_days_outside_scope(data: dict, start_date: date, end_date: date) -> dict:
    delta = end_date - start_date
    dates = list()
    mid_date = start_date

    for i in range(delta.days):
        mid_date += timedelta(days=i)
        if mid_date < end_date:
            dates.append(mid_date.isoformat())

    for data_date in data.copy().items():
        if data_date[0] not in dates:
            data.pop(data_date[0])

    return data


def remove_days_from_other_years(year: int, near_earth_objects: dict) -> dict:
    for near_earth_object in near_earth_objects.copy().items():
        if str(year) not in near_earth_object[0]:
            near_earth_objects.pop(near_earth_object[0])

    return near_earth_objects


def reduce_response_data(data: dict, data_key: str) -> dict:
    reduced_data = dict()
    reduced_data[data_key] = data[data_key].copy()

    for data_date in data[data_key]:
        reduced_data[data_key][data_date] = list()

        for item in data[data_key][data_date]:
            reduced_data[data_key][data_date].append({
                "id": item["id"],
                "estimated_diameter": {
                    "meters": {
                        "estimated_diameter_max": item["estimated_diameter"]["meters"]["estimated_diameter_max"]
                    }
                },
                "close_approach_data": [
                    {
                        "miss_distance": {
                            "kilometers": item["close_approach_data"][0]["miss_distance"]["kilometers"]
                        }
                    }
                ]
            })

    return reduced_data
