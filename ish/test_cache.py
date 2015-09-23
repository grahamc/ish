
import unittest
import ish.cache
import os
import tempfile
from unittest.mock import Mock


class TestCache(unittest.TestCase):
    def test_needs_new_file_missing(self):
        self.assertTrue(ish.cache.needs_new('/this/file/does/not/exist', 60))

    def test_needs_new_file_old(self):
        tf = tempfile.NamedTemporaryFile()
        os.utime(tf.name, (0, 0))
        self.assertTrue(ish.cache.needs_new(tf.name, 60))

    def test_needs_new_file_new(self):
        tf = tempfile.NamedTemporaryFile()
        os.utime(tf.name, None)
        self.assertFalse(ish.cache.needs_new(tf.name, 60))

    def test_load_or_old_file(self):
        tf = tempfile.NamedTemporaryFile()
        os.utime(tf.name, (0, 0))
        stub = Mock(return_value={'foo': 'bar'})
        ish.cache.load_or(tf.name, stub)
        stub.assert_called_with()

    def test_load_or_new_valid_file(self):
        tf = tempfile.NamedTemporaryFile()
        tf.write(bytes('{"foo": "bar"}', 'UTF-8'))
        tf.seek(0)
        stub = Mock(return_value={'foo': 'bar'})
        self.assertEqual(
            {'foo': 'bar'},
            ish.cache.load_or(tf.name, stub)
        )
        self.assertFalse(stub.called)

    def test_load_or_new_invalid_file(self):
        tf = tempfile.NamedTemporaryFile()
        tf.write(bytes('{"foo": "ba', 'UTF-8'))
        tf.seek(0)
        stub = Mock(return_value={'foo': 'bar'})
        self.assertEqual(
            {'foo': 'bar'},
            ish.cache.load_or(tf.name, stub)
        )
        self.assertTrue(stub.called)
