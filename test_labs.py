from pathlib import Path
import tempfile
import unittest
import json

from cartons import cartons_needed
from catalog_price import parse_catalog_price
from export_record import export_json


class TransferLabTests(unittest.TestCase):
    def test_carton_examples_and_minimality(self):
        self.assertEqual([cartons_needed(n,12) for n in (0,12,13,24)],
                         [0,1,2,2])
        for capacity in (1,2,12,1000):
            for packs in (0,1,12,13,24,999999,1000000):
                cartons=cartons_needed(packs,capacity)
                self.assertGreaterEqual(cartons*capacity,packs)
                if packs:
                    self.assertLess((cartons-1)*capacity,packs)

    def test_carton_rejections(self):
        for args in ((True,1),(1,False),(1.0,12)):
            with self.assertRaises(TypeError):cartons_needed(*args)
        for args in ((-1,1),(1,0),(1,1001),(1000001,1)):
            with self.assertRaises(ValueError):cartons_needed(*args)

    def test_catalog_representation(self):
        for text,value in [('0',0),('1250',1250),('1000000',1000000)]:
            self.assertEqual(parse_catalog_price(text),value)
        for text in ('1_000','','1.0','-1',' 1','1000001','00000000'):
            with self.assertRaises(ValueError):parse_catalog_price(text)

    def test_export_round_trip(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'quote.json'
            record={'record_id':'test-1','total_cents':1040}
            export_json(record,path)
            self.assertEqual(json.loads(path.read_text(encoding='utf-8')),
                             record)

    def test_export_serialization_preserves_destination(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'quote.json'
            path.write_text('sentinel',encoding='utf-8')
            with self.assertRaises(TypeError):export_json({'bad':{1,2}},path)
            self.assertEqual(path.read_text(encoding='utf-8'),'sentinel')

    def test_export_missing_parent(self):
        with tempfile.TemporaryDirectory() as folder:
            path=Path(folder)/'missing'/'quote.json'
            with self.assertRaises(FileNotFoundError):export_json({},path)
            self.assertFalse(path.exists())
