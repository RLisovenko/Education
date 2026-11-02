"""Static checks on the synthetic sources; does not require Docker, Spark or dbt."""
import csv
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]

class SourceSamplesTest(unittest.TestCase):
    def test_production_orders_have_unique_ids(self):
        with (ROOT/'data/raw/production_orders.csv').open(newline='',encoding='utf-8') as f:
            rows=list(csv.DictReader(f))
        self.assertEqual(len(rows),12)
        self.assertEqual(len({row['order_id'] for row in rows}),12)
        self.assertEqual({row['production_date'] for row in rows},{'2026-10-30','2026-10-31'})

    def test_machine_event_ids_and_references(self):
        p=ROOT/'data/raw/machine_operations.jsonl'
        rows=[json.loads(line) for line in p.read_text(encoding='utf8').splitlines()]
        self.assertEqual(len(rows),12)
        self.assertEqual(len({r['operation_id'] for r in rows}),12)

    def test_quality_seed(self):
        p=ROOT/'data/seed/quality_inspections.jsonl'
        rows=[json.loads(line) for line in p.read_text(encoding='utf8').splitlines()]
        self.assertEqual(len(rows),12)
        self.assertTrue(all(r['rejected_units']<=r['inspected_units'] for r in rows))

    def test_dag_compiles(self):
        path=ROOT/'dags/novaforge_manufacturing_lakehouse.py'
        compile(path.read_text(encoding='utf8'),str(path),'exec')

if __name__=='__main__':
    unittest.main()
