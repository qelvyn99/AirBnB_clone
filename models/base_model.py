#!/usr/bin/python3

import uuid
from datetime import datetime


class BaseModel:
    """BaseModel class for creating and managing instances."""

    TIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

    def __init__(self, *args, **kwargs):
        """Initialize a new instance of BaseModel."""
        if kwargs:
            try:
                for key, value in kwargs.items():
                    if key != '__class__':
                        if key in ["created_at", "updated_at"]:
                            value = datetime.strptime(value, self.TIME_FORMAT)
                        setattr(self, key, value)
            except ValueError as e:
                raise ValueError(f"Error parsing datetime: {e}")
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self) -> str:
        """Return a string representation of the instance."""
        class_name = self.__class__.__name__
        return "[{}] ({}) {}".format(class_name, self.id, self.__dict__)

    def save(self):
        """Update the updated_at attribute and save the instance."""
        self.updated_at = datetime.now()

    def _format_datetime(self, dt: datetime) -> str:
        """Format a datetime object to ISO format."""
        return dt.isoformat()

    def to_dict(self) -> dict:
        """Return a dictionary of instance attributes."""
        excluded = ['name', 'my_number']
        result = {k: v for k, v in self.__dict__.items() if k not in excluded}
        result['__class__'] = self.__class__.__name__

        for k, v in result.items():
            if isinstance(v, datetime):
                result[k] = self._format_datetime(v)

        return result
