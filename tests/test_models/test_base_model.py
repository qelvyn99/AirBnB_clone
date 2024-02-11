#!/usr/bin/python3
"""
Unittest for BaseModel class
"""

import unittest
from datetime import datetime
from models.base_model import BaseModel


class TestBaseModel(unittest.TestCase):

    def setUp(self):
        # Initialize a BaseModel instance for testing
        self.base_model = BaseModel()

    def test_init(self):
        # Test if a new instance is created with the correct attributes
        self.assertIsNotNone(self.base_model.id)
        self.assertIsInstance(self.base_model.created_at, datetime)
        self.assertIsInstance(self.base_model.updated_at, datetime)

    def test_checking_for_functions(self):
        self.assertIsNotNone(BaseModel.__doc__)
        self.assertIsNotNone(BaseModel.save.__doc__)
        self.assertIsNotNone(BaseModel.to_dict.__doc__)

    def test_attributes(self):
        self.assertTrue(hasattr(BaseModel, "__init__"))
        self.assertTrue(hasattr(BaseModel, "save"))
        self.assertTrue(hasattr(BaseModel, "to_dict"))

    def test_save(self):
        # Test if the `updated_at` attribute is updated after calling save
        original_updated_at = self.base_model.updated_at
        self.base_model.save()
        self.assertNotEqual(original_updated_at, self.base_model.updated_at)

    def test_save_saves_to_storage(self):
        # Test if the object is saved to storage
        from models import storage
        original_storage_count = len(storage.all())
        self.base_model.save()
        new_storage_count = len(storage.all())
        self.assertEqual(new_storage_count, original_storage_count + 1)

    def test_to_dict(self):
        # Test the to_dict method
        data_dict = self.base_model.to_dict()
        self.assertIsInstance(data_dict, dict)
        self.assertEqual(data_dict['__class__'],
                         self.base_model.__class__.__name__)
        self.assertIsInstance(data_dict['created_at'], str)
        self.assertIsInstance(data_dict['updated_at'], str)

    def test_to_dict_datetime_format(self):
        # Test if the datetime format in the to_dict method is correct
        data_dict = self.base_model.to_dict()
        self.assertTrue(datetime.strptime(data_dict['created_at'],
                                          "%Y-%m-%dT%H:%M:%S.%f"))
        self.assertTrue(datetime.strptime(data_dict['updated_at'],
                                          "%Y-%m-%dT%H:%M:%S.%f"))


if __name__ == "__main__":
    unittest.main()
