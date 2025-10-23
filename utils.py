"""
Utility functions for earthquake data retrieval and graph generation.
Includes functions to fetch top earthquakes, last earthquake, generate plots,
and convert timestamps.
"""
# pylint: disable=E0401,E1101,C0103
# -----------------------------
# Standard library imports
# -----------------------------
import io
from datetime import datetime, timedelta, timezone
from collections import defaultdict

# -----------------------------
# Third-party imports
# -----------------------------
from matplotlib import pyplot as plt
import requests  # HTTP requests

from constants import USGS_URL

# -----------------------------
# Constants
# -----------------------------


# Country configuration for earthquake data
COUNTRIES = {
    "Tel Aviv, Israel": {"lat": 32.0853, "lon": 34.7818, "radius": 100},
    "United States (California)": {"lat": 36.7783, "lon": -119.4179, "radius": 300},
    "Japan": {"lat": 36.2048, "lon": 138.2529, "radius": 300},
    "Indonesia": {"lat": -0.7893, "lon": 113.9213, "radius": 300},
    "Chile": {"lat": -35.6751, "lon": -71.5430, "radius": 300}
}


# -----------------------------
# Utility Functions
# -----------------------------
def generate_graph(days, lat, lon, radius, title_suffix=""):# pylint: disable= R0914
    """
    Generate a PNG graph of earthquake counts per day for a given location and period.

    Args:
        days (int): Number of days to look back from today.
        lat (float): Latitude of location.
        lon (float): Longitude of location.
        radius (float): Maximum radius in km from the location.
        title_suffix (str): Optional suffix for graph title.

    Returns:
        BytesIO: In-memory PNG image of the plot.
    """
    start_time_dt = datetime.now(timezone.utc) - timedelta(days=days)
    start_time_str = start_time_dt.strftime('%Y-%m-%d')

    params = {
        'format': 'geojson',
        'latitude': lat,
        'longitude': lon,
        'maxradiuskm': radius,
        'starttime': start_time_str
    }

    response = requests.get(USGS_URL, params=params, timeout=10)

    plt.figure(figsize=(10, 5))

    if response.status_code != 200:
        plt.text(0.5, 0.5, "Error fetching data", horizontalalignment='center',
                 verticalalignment='center', fontsize=14)
        plt.axis('off')
    else:
        data = response.json()
        counts_by_day = defaultdict(int)

        for feature in data.get('features', []):
            timestamp = feature.get('properties', {}).get('time')
            if timestamp:
                event_date = datetime.fromtimestamp(timestamp / 1000, tz=timezone.utc).date()
                counts_by_day[event_date] += 1

        days_list = sorted(counts_by_day.keys())
        counts = [counts_by_day[day] for day in days_list]

        if days_list:
            plt.bar(days_list, counts)
            plt.xlabel('Date')
            plt.ylabel('Number of Earthquakes')
            plt.title(f'Earthquakes in Last {days} Days {title_suffix}')
            plt.xticks(rotation=45)
            plt.tight_layout()
        else:
            plt.text(0.5, 0.5, "No earthquake data available", horizontalalignment='center',
                     verticalalignment='center', fontsize=14)
            plt.axis('off')

    img = io.BytesIO()
    plt.savefig(img, format='png')
    plt.close()
    img.seek(0)
    return img


def get_top_earthquakes(limit=5):
    """
    Fetch the top earthquakes in the last 30 days sorted by magnitude.

    Args:
        limit (int): Number of top events to return.

    Returns:
        list: List of top earthquake events.
    """
    start_time_str = (datetime.now(timezone.utc) - timedelta(days=30)).strftime('%Y-%m-%d')
    params = {
        'format': 'geojson',
        'starttime': start_time_str,
        'minmagnitude': 1
    }

    response = requests.get(USGS_URL, params=params, timeout=10)

    top_events = []
    if response.status_code == 200:
        data = response.json()
        events = data.get('features', [])
        events = sorted(events, key=lambda f: f.get('properties', {}).get('mag', 0), reverse=True)
        top_events = events[:limit]

    return top_events


def get_last_earthquake():
    """
    Fetch the most recent earthquake in the last 30 days.

    Returns:
        dict or None: The last earthquake event or None if unavailable.
    """
    start_time_str = (datetime.now(timezone.utc) - timedelta(days=30)).strftime('%Y-%m-%d')
    params = {
        'format': 'geojson',
        'starttime': start_time_str,
        'minmagnitude': 1
    }

    response = requests.get(USGS_URL, params=params, timeout=10)

    last_event = None
    if response.status_code == 200:
        data = response.json()
        events = data.get('features', [])
        events = sorted(events, key=lambda f: f.get('properties', {}).get('time', 0), reverse=True)
        if events:
            last_event = events[0]

    return last_event


def timestamp_to_str(ts):
    """
    Convert a Unix timestamp (milliseconds) to a human-readable UTC string.

    Args:
        ts (int): Timestamp in milliseconds.

    Returns:
        str: Formatted date string '%Y-%m-%d %H:%M:%S'.
    """
    return datetime.fromtimestamp(ts / 1000, tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S')
