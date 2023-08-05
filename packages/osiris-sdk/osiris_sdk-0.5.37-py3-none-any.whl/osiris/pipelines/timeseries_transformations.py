"""
Module to handle pipeline for timeseries
"""
from abc import ABC
from datetime import datetime
from typing import List, Tuple

import pandas as pd
import apache_beam.transforms.core as beam_core
from azure.core.exceptions import ResourceNotFoundError

from ..core.enums import TimeResolution
from .azure_data_storage import _DataSets


class _ConvertEventToTuple(beam_core.DoFn, ABC):
    """
    Takes a list of events and converts them to a list of tuples (datetime, event)
    """
    def __init__(self, date_key_name: str, date_format: str, time_resolution: TimeResolution):
        super().__init__()

        self.date_key_name = date_key_name
        self.date_format = date_format
        self.time_resolution = time_resolution

    def process(self, element, *args, **kwargs) -> List:
        """
        Overwrites beam.DoFn process.
        """
        res = []
        for event in element:
            datetime_obj = pd.to_datetime(event[self.date_key_name], format=self.date_format)
            res.append((str(self.__convert_datetime_to_time_resolution(datetime_obj)), event))

        return res

    def __convert_datetime_to_time_resolution(self, datetime_obj: datetime):
        if self.time_resolution == TimeResolution.NONE:
            return datetime_obj.replace(year=1970, month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        if self.time_resolution == TimeResolution.YEAR:
            return datetime_obj.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)
        if self.time_resolution == TimeResolution.MONTH:
            return datetime_obj.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if self.time_resolution == TimeResolution.DAY:
            return datetime_obj.replace(hour=0, minute=0, second=0, microsecond=0)
        if self.time_resolution == TimeResolution.HOUR:
            return datetime_obj.replace(minute=0, second=0, microsecond=0)
        if self.time_resolution == TimeResolution.MINUTE:
            return datetime_obj.replace(second=0, microsecond=0)
        message = 'Unknown enum type'
        raise ValueError(message)


class _JoinUniqueEventData(beam_core.DoFn, ABC):
    """"
    Takes a list of events and join it with processed events, if such exists, for the particular event time.
    It will only keep unique pairs.
    """
    def __init__(self, datasets: _DataSets):
        super().__init__()

        self.datasets = datasets

    def process(self, element, *args, **kwargs) -> List[Tuple]:
        """
        Overwrites beam.DoFn process.
        """
        date = pd.to_datetime(element[0])
        events = element[1]
        try:
            processed_events = self.datasets.read_events_from_destination(date)
            joined_events = events + processed_events
            # Only keep unique elements in the list
            joined_events = [i for n, i in enumerate(joined_events) if i not in joined_events[n + 1:]]

            return [(date, joined_events)]
        except ResourceNotFoundError:
            return [(date, events)]


class _UploadEventsToDestination(beam_core.DoFn, ABC):
    """
    Uploads events to destination
    """

    def __init__(self, datasets: _DataSets):
        super().__init__()
        self.datasets = datasets

    def process(self, element, *args, **kwargs):
        """
        Overwrites beam.DoFn process.
        """
        date = element[0]
        events = element[1]

        self.datasets.upload_events_to_destination_json(date, events)
