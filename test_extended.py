import contextlib
import http.client
import io
import json
from pathlib import Path
import sqlite3
import tempfile
import threading
import unittest

from quote import total_cents
from quote_api import create_quote
from quote_batch import save_batch
from quote_store import initialize, save_quote, load_quote
from bounded_tools import execute_plan
from local_server import make_server


class AdditionalRulesTests(unittest.TestCase):
    def test_properties(self):
        for price in (0, 1, 105, 1250, 1_000_000):
            for seats in range(1, 201):
                value = total_cents(price, seats)
                self.assertIs(type(value), int)
                self.assertGreaterEqual(value, 0)
                self.assertLessEqual(value, price * seats)

    def test_tools_reject_unknown_operation(self):
        with self.assertRaises(ValueError):
            execute_plan([{'tool': 'upload_project', 'arguments': {}}])

    def test_tool_valid_calculation(self):
        self.assertEqual(execute_plan([{'tool': 'calculate_total',
            'arguments': {'unit_cents': 105, 'quantity': 11}}]), [1040])

    def test_file_reopen(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / 'quotes.sqlite3'
            db = sqlite3.connect(path)
            try:
                initialize(db)
                expected = save_quote(db, 'persisted', 1250, 10)
            finally:
                db.close()
            db = sqlite3.connect(path)
            try:
                self.assertEqual(load_quote(db, 'persisted'), expected)
            finally:
                db.close()


class AdditionalBatchTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(':memory:')
        initialize(self.db)

    def tearDown(self):
        self.db.close()

    def test_two_successes(self):
        rows = save_batch(self.db, [
            {'record_id': 'one', 'unit_cents': 1250, 'quantity': 4},
            {'record_id': 'two', 'unit_cents': 105, 'quantity': 11}])
        self.assertEqual([r['total_cents'] for r in rows], [5000,1040])

    def test_duplicate_within_batch(self):
        payload = {'record_id': 'dup', 'unit_cents': 1250, 'quantity': 4}
        with self.assertRaises(sqlite3.IntegrityError):
            save_batch(self.db, [payload, payload])
        self.assertIsNone(load_quote(self.db,'dup'))

    def test_invalid_second_record(self):
        with self.assertRaises(ValueError):
            save_batch(self.db, [
                {'record_id': 'first','unit_cents': 1250,'quantity': 4},
                {'record_id': 'second','unit_cents': 1250,'quantity': 0}])
        self.assertIsNone(load_quote(self.db,'first'))

    def test_api_boolean_rejected_without_write(self):
        status, _ = create_quote({'record_id':'bad','unit_cents':1250,
                                  'quantity':True}, self.db)
        self.assertEqual(status,422)
        self.assertIsNone(load_quote(self.db,'bad'))


class LocalHttpTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.server = make_server(Path(self.temp.name)/'demo.db',port=0)
        self.thread = threading.Thread(target=self.server.serve_forever,
                                       daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown()
        self.server.server_close()
        self.thread.join()
        self.temp.cleanup()

    def request(self,method,path,body=None,extra=None):
        client=http.client.HTTPConnection(*self.server.server_address,
                                          timeout=5)
        try:
            headers={'Content-Type':'application/json'}
            headers.update(extra or {})
            client.request(method,path,body=body,headers=headers)
            response=client.getresponse()
            return response.status,response.read()
        finally:
            client.close()

    def test_html_and_create(self):
        status,body=self.request('GET','/')
        self.assertEqual(status,200)
        self.assertIn(b'Create quote record',body)
        request=json.dumps({'record_id':'http-1','unit_cents':1250,
                            'quantity':10})
        status,body=self.request('POST','/quotes',request)
        self.assertEqual(status,201)
        self.assertEqual(json.loads(body)['total_cents'],11250)
        status,_=self.request('POST','/quotes',request)
        self.assertEqual(status,409)

    def test_transport_rejections(self):
        cases=[('{',{},400),
               ('{}',{'Origin':'https://example.invalid'},403),
               ('{}',{'Content-Type':'text/plain'},415),
               ('x'*4097,{},413),
               ('{"quantity":1,"quantity":2}',{},400)]
        for body,headers,wanted in cases:
            with self.subTest(wanted=wanted,body=body[:20]):
                status,_=self.request('POST','/quotes',body,headers)
                self.assertEqual(status,wanted)
