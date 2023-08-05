from typing import List

import pandas as pd
import requests
import archimedes
from archimedes.configuration import api_config
from archimedes.auth import archimedes_auth, NoneAuth

API_URL = api_config.url


def get_api(
    series_ids: List[str],
    price_areas: List[str] = None,
    start: str = None,
    end: str = None,
):
    """Get any number of time series.

    This function can be used to fetch time series from the Archimedes Database.
    To see which series are available, use `list_ids()`.

    Example:
        >>> archimedes.get_api(
        >>>     series_ids=["NP/AreaPrices"],
        >>>     price_areas=["NO1", "NO2"],
        >>>     start="2020-06-20T04:00:00+00:00",
        >>>     end="2020-06-28T04:00:00+00:00",
        >>> )
        series_id                 NP/AreaPrices
        price_area                          NO1   NO2
        from_dt
        2020-06-20T04:00:00+00:00          1.30  1.30
        2020-06-20T05:00:00+00:00          1.35  1.35
        ...                                 ...   ...
        2020-06-28T03:00:00+00:00          0.53  0.53
        2020-06-28T04:00:00+00:00          0.55  0.55

    Args:
        series_ids (List[str]): The series ids to get.
        price_areas (List[str], optional): The price areas to pick, all price areas if None. Defaults to None.
        start (str, optional): The first datetime to fetch (inclusive). Returns all if None. Defaults to None.
        end (str, optional): The last datetime to fetch (exclusive). Returns all if None. Defaults to None.

    Returns:
        DataFrame with all the time series data
    """

    if isinstance(series_ids, str):
        series_ids = [series_ids]

    if isinstance(price_areas, str):
        price_areas = [price_areas]

    if start is None:
        start = archimedes.constants.DATE_LOW
    else:
        start = pd.to_datetime(start)

    if end is None:
        end = archimedes.constants.DATE_HIGH
    else:
        end = pd.to_datetime(end)

    query = {
        "series_ids": series_ids,
        "price_areas": price_areas,
        "start": start,
        "end": end,
        "flatten_columns": True,
    }

    access_token = get_access_token()

    r = requests.get(
        f"{API_URL}/data/get",
        params=query,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    r.raise_for_status()
    jdata = r.json()

    df = pd.DataFrame.from_dict(jdata)

    return df


def get_predictions_api(
    series_ids: List[str], start: str = None, end: str = None
) -> List:
    """Get any number of predictions

    This function can be used to fetch predictions from the Archimedes Database.

    Unlike `archimedes.get`, this will return a list, not a dataframe.

    @TODO: It could be that this function should also return a pd.DataFrame,
    where the user can choose whether to have the 'wide' or 'long' format returned.

    Example:
        >>> archimedes.get_predictions_api(
            series_ids=["PX/rk-naive"],
            start="2020"
        )
        >>> [...]

    Args:
        series_ids (List[str]): The series ids to get.
        start (str, optional):
            The first datetime to fetch (inclusive). Returns all if None. Defaults to None.
        end (str, optional):
            The last datetime to fetch (exclusive). Returns all if None. Defaults to None.

    Returns:
        List with all the prediction data
    """
    if isinstance(series_ids, str):
        series_ids = [series_ids]

    if start is None:
        start = archimedes.constants.DATE_LOW
    else:
        start = pd.to_datetime(start)

    if end is None:
        end = archimedes.constants.DATE_HIGH
    else:
        end = pd.to_datetime(end)

    query = {"series_ids": series_ids, "start": start, "end": end}

    access_token = get_access_token()

    r = requests.get(
        f"{API_URL}/data/get_predictions",
        params=query,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    r.raise_for_status()
    jdata = r.json()

    return jdata

    # df = pd.DataFrame.from_dict(jdata)

    # return [record.as_dict() for record in rows.all()]


def get_access_token():
    access_token = archimedes_auth.get_access_token_silent()

    if access_token is None:
        raise NoneAuth(
            "User not logged in. Please log in using `arcl auth login <organization_id>`."
        )

    return access_token
