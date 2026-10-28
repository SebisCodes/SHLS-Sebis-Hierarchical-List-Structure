"""
Tests of SHLSDecoder and SHLSEncoder.

    python3 -m unittest discover tests
"""

import copy
import json
import os
import random
import re
import sys
import threading
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, 'SHLS-Codec-Classes'))

from SHLSDecoder import SHLSDecoder  # noqa: E402
from SHLSEncoder import SHLSEncoder  # noqa: E402


def decode(text, seconds=2):
    """SHLSDecoder().decode(text); fails the test if it does not finish."""
    out = {}

    def run():
        try:
            out['data'] = SHLSDecoder().decode(text)
        except Exception as e:  # reported below
            out['error'] = e

    t = threading.Thread(target=run, daemon=True)
    t.start()
    t.join(seconds)
    if t.is_alive():
        raise AssertionError('the decoder does not finish')
    if 'error' in out:
        raise out['error']
    return out['data']


def encode(data):
    return SHLSEncoder().encode(data)


def read(*path):
    with open(os.path.join(ROOT, *path), encoding='utf-8') as f:
        return f.read()


def as_strings(value):
    """The data as SHLSDecoder gives it back: lists of records, every value a string."""
    if isinstance(value, dict):
        return {k: as_strings(v if isinstance(v, list) else [v]) for k, v in value.items()}
    return [records(v) if isinstance(v, dict) else {'Value': plain(v)} for v in value]


def records(record):
    return {k: as_strings(v) if isinstance(v, list) else as_strings([v]) if isinstance(v, dict) else plain(v) for k, v in record.items()}


def plain(v):
    if isinstance(v, list):
        return as_strings(v)
    return str(v)


EMPLOYEES = [
    {'EmployeeID': '1001', 'Name': 'Alice Smith', 'Role': 'Software Engineer', 'Salary': '90000', 'StartDate': '2019-06-01', 'FullTime': 'true'},
    {'EmployeeID': '1002', 'Name': 'Bob Johnson', 'Role': 'Data Scientist', 'Salary': '95000', 'StartDate': '2020-02-15', 'FullTime': 'true'},
]


class Examples(unittest.TestCase):
    def test_example_files(self):
        a = decode(read('SHLS-Examples', 'Example.shls'))
        b = decode(read('SHLS-Examples', 'Example2.shls'))
        self.assertEqual(a, b)
        self.assertEqual([d['DepartmentName'] for d in a['Company'][0]['Departments']], ['Development', 'Human Resources', 'Marketing'])
        self.assertEqual(a['Company'][0]['Departments'][0]['Employees'], EMPLOYEES)
        self.assertEqual([y['Year'] for y in a['Financials']], ['2021', '2022', '2023'])

    def test_readme_examples(self):
        texts = re.findall(r'```plaintext\n(.*?)```', read('README.md'), re.S)
        self.assertEqual(len(texts), 2)
        first, second = decode(texts[0]), decode(texts[1])
        self.assertEqual(first, second)
        self.assertEqual([p['Name'] for p in first['Product']], ['Smartphone A1', 'Laptop B2', 'Table X5'])
        self.assertEqual(first['Company'][1]['Location'], [{'Country': 'Germany', 'City': 'Berlin'}, {'Country': 'Switzerland', 'City': 'Zürich'}])

    def test_decode_examples(self):
        folder = os.path.join(ROOT, 'SHLS-Codec-Examples')
        texts = [t for f in sorted(os.listdir(folder)) if f.startswith('DecodeExample')
                 for t in re.findall(r'shls_string = """(.*?)"""', read('SHLS-Codec-Examples', f), re.S)]
        self.assertEqual(len(texts), 2)
        for text in texts:
            data = decode(text)
            self.assertEqual([d['DepartmentID'] for d in data['Company'][0]['Departments']], ['001', '002'])
            self.assertEqual(data['Company'][0]['Departments'][0]['Employees'], EMPLOYEES)
            self.assertEqual(len(data['Financials']), 2)

    def test_encode_example(self):
        source = read('SHLS-Codec-Examples', 'EncodeExample.py')
        scope = {}
        exec(source.split('# Initialize the SHLSEncoder')[0].split('from SHLSEncoder import SHLSEncoder')[1], scope)
        data = scope['data']
        kept = copy.deepcopy(data)
        text = encode(data)
        self.assertEqual(data, kept)
        self.assertEqual(decode(text), as_strings(data))


class Decoder(unittest.TestCase):
    def test_nested_key_as_last_line(self):
        self.assertEqual(decode('S\n a\n L\n  x\n\n 1\n L\n'), {'S': [{'a': '1', 'L': []}]})

    def test_empty_nested_list_at_the_end(self):
        self.assertEqual(decode('S\n a\n L\n  x\n\n 1\n L\n\n'), {'S': [{'a': '1', 'L': []}]})
        self.assertEqual(decode('S\n L\n  x\n a\n\n L\n 1\n'), {'S': [{'L': [], 'a': '1'}]})

    def test_empty_nested_list_between_records(self):
        text = 'S\n a\n L\n  x\n\n 1\n L\n\n 2\n L\n  y\n'
        self.assertEqual(decode(text), {'S': [{'a': '1', 'L': []}, {'a': '2', 'L': [{'x': 'y'}]}]})

    def test_blank_lines_with_spaces(self):
        self.assertEqual(decode('S\n a\n b\n \n 1\n 2\n'), {'S': [{'a': '1', 'b': '2'}]})
        self.assertEqual(decode('S\n a\n b\n\n 1\n   \n 2\n'), {'S': [{'a': '1', 'b': '2'}]})
        self.assertEqual(decode('S\n a\n L\n  x\n\n 1\n L\n  \n  y\n'), {'S': [{'a': '1', 'L': [{'x': 'y'}]}]})
        self.assertEqual(decode('S\n a\n L\n  x\n\n 1\n L\n\n  y\n'), {'S': [{'a': '1', 'L': [{'x': 'y'}]}]})

    def test_incomplete_last_record(self):
        self.assertEqual(decode('S\n a\n b\n c\n\n 1\n 2\n 3\n 4\n'), {'S': [{'a': '1', 'b': '2', 'c': '3'}, {'a': '4'}]})
        nested = decode('S\n a\n L\n  x\n  y\n b\n\n 1\n L\n  p\n  q\n  r\n 2\n')
        self.assertEqual(nested, {'S': [{'a': '1', 'L': [{'x': 'p', 'y': 'q'}, {'x': 'r'}], 'b': '2'}]})

    def test_all_data_blocks(self):
        text = 'P\n a\n b\n\nQ\n c\n\nP\n 1\n 2\n 3\n 4\n\nQ\n x\n\nP\n 9\n 8\n'
        self.assertEqual(decode(text), {'P': [{'a': '1', 'b': '2'}, {'a': '3', 'b': '4'}, {'a': '9', 'b': '8'}], 'Q': [{'c': 'x'}]})
        self.assertEqual(decode('P\n a\n\n 1\n\nP\n 2\n'), {'P': [{'a': '1'}, {'a': '2'}]})

    def test_keys_named_like_numbers(self):
        self.assertEqual(decode('S\n 1\n 0\n  x\n\n a\n b\n  c\n'), {'S': [{'1': 'a', '0': [{'x': 'c'}]}]})
        self.assertEqual(decode('S\n 0\n 1\n 2\n\n a\n b\n c\n'), {'S': [{'0': 'a', '1': 'b', '2': 'c'}]})

    def test_only_a_key_block(self):
        self.assertEqual(decode('S\n a\n b\n'), {'S': []})

    def test_lines_that_are_not_used(self):
        self.assertEqual(decode('S\n a\n\n 1\n  stray\n 2\n'), {'S': [{'a': '1'}, {'a': '2'}]})
        self.assertEqual(decode('S\n a\n b\n\n 1\n   deeper\n 2\n'), {'S': [{'a': '1', 'b': '2'}]})
        self.assertEqual(decode('S\n  a\n  b\n    c\n\n  1\n  B\n    2\n    3\n'), {'S': [{'a': '1', 'b': [{'c': '2'}, {'c': '3'}]}]})
        self.assertEqual(decode('S\r\n a\r\n b\r\n\r\n 1\r\n 2\r\n'), {'S': [{'a': '1', 'b': '2'}]})

    def test_empty_text(self):
        self.assertEqual(decode(''), {})
        self.assertEqual(decode('\n  \n'), {})


class Encoder(unittest.TestCase):
    def test_input_unchanged(self):
        data = {'A': {'x': 1}, 'B': [{'y': {'z': 2}}], 'C': 'c'}
        kept = copy.deepcopy(data)
        encode(data)
        self.assertEqual(data, kept)

    def test_object_inside_a_record(self):
        data = {'A': [{'x': '1', 'o': {'p': '2', 'q': '3'}}]}
        self.assertEqual(decode(encode(data)), {'A': [{'x': '1', 'o': [{'p': '2', 'q': '3'}]}]})

    def test_plain_values_in_lists(self):
        data = {'Tags': ['a', 'b'], 'A': [{'x': '1', 't': ['p', 'q']}]}
        text = encode(data)
        self.assertNotIn('\n\n\n', text)
        self.assertEqual(decode(text), {'Tags': [{'Value': 'a'}, {'Value': 'b'}], 'A': [{'x': '1', 't': [{'Value': 'p'}, {'Value': 'q'}]}]})

    def test_header_has_no_empty_lines(self):
        data = {'A': [{'x': '1', 't': [], 'u': ['p']}], 'B': [], 'C': 'c'}
        header = encode(data).split('\n\n')[0]
        self.assertTrue(all(line.strip() for line in header.split('\n')))
        self.assertEqual(decode(encode(data)), as_strings(data))

    def test_keys_of_nested_lists_from_all_records(self):
        data = {'A': [{'x': '1', 'L': []}, {'x': '2', 'L': [{'p': '3'}]}]}
        self.assertEqual(decode(encode(data)), data)

    def test_same_text_as_before_for_records(self):
        data = {'P': [{'a': 'x', 'b': 'y'}, {'a': 'z', 'b': 'w'}]}
        self.assertEqual(encode(data), 'P\n a\n b\n\nP\n x\n y\n z\n w')

    def test_random_structures(self):
        r = random.Random(1411)
        words = ['Name', 'City', 'Price', 'Tag', 'ID', 'Note', 'Color', 'Owner', 'Year', 'Zürich', '0', '1', '2']

        def value():
            return r.choice(['alpha', 'beta two', 'São Paulo', 42, 2.5, True, None, 'x/y'])

        def keys(depth):
            out = []
            for name in r.sample(words, r.randint(1, 4)):
                k = r.random()
                if depth < 3 and k < 0.2:
                    out.append((name, 'list', keys(depth + 1)))
                elif depth < 3 and k < 0.3:
                    out.append((name, 'dict', keys(depth + 1)))
                elif k < 0.38:
                    out.append((name, 'plain list', None))
                else:
                    out.append((name, 'value', None))
            return out

        def make(ks):
            rec = {}
            for name, kind, sub in ks:
                if kind == 'list':
                    rec[name] = [make(sub) for _ in range(r.randint(0, 3))]
                elif kind == 'dict':
                    rec[name] = make(sub)
                elif kind == 'plain list':
                    rec[name] = [value() for _ in range(r.randint(0, 3))]
                else:
                    rec[name] = value()
            return rec

        for _ in range(200):
            data = {}
            for section in r.sample(['Product', 'Company', 'Team', 'Orders', '2024'], r.randint(1, 3)):
                ks = keys(0)
                data[section] = [make(ks) for _ in range(r.randint(0, 3))] if r.random() < 0.8 else make(ks)
            kept = copy.deepcopy(data)
            text = encode(data)
            self.assertEqual(data, kept)
            self.assertEqual(decode(text), json.loads(json.dumps(as_strings(data))), text)


if __name__ == '__main__':
    unittest.main()
