"""Bounded offline review utility. Exit 0 means completed report, never safety."""
import argparse
import json
import math
import sys
from datetime import date, datetime
from pathlib import Path

def strings(value):
    if not isinstance(value,list) or any(not isinstance(x,str) or not x for x in value):
        raise ValueError('expected list of nonempty strings')
    return value

def records(value):
    if not isinstance(value,list) or any(not isinstance(x,dict) for x in value):
        raise ValueError('expected list of objects')
    return value

def text(value):
    if not isinstance(value,str) or not value:
        raise ValueError('expected nonempty text')
    return value

def integer(value):
    if type(value) is not int or value<0:
        raise ValueError('expected nonnegative integer')
    return value

def boolean(value):
    if type(value) is not bool:
        raise ValueError('expected boolean')
    return value

def unique_ids(rows):
    ids=[text(r['id']) for r in rows]
    if len(ids)!=len(set(ids)):
        raise ValueError('duplicate IDs')

def utc(value):
    text(value)
    if not value.endswith('Z') or 'T' not in value:
        raise ValueError('UTC ISO timestamp required')
    return datetime.fromisoformat(value.replace('Z','+00:00'))

def analyze(d):
    operation=text(d['operation']); previous=d['previous']; payload=d['payload']
    supported=boolean(d['idempotency_supported']); receipt=d['receipt']
    if receipt not in ['completed','not_completed','unknown']: raise ValueError('invalid receipt')
    if previous is not None:
        if not isinstance(previous,dict): raise ValueError('previous must be object or null')
        text(previous['operation'])
        if previous['state'] not in ['uncertain','completed','pending']: raise ValueError('invalid prior state')
        if previous['operation']==operation and previous['payload']!=payload:
            return {'decision':'failure','next':'hold','reason':'operation_identity_collision'}
        if previous['operation']!=operation:
            receipt='unknown'
            previous=None
    if receipt=='completed': return {'decision':'complete','next':'do_not_repeat','reason':'authoritative_receipt_model'}
    if previous is not None and previous['state']=='completed':
        return {'decision':'unknown','next':'hold','reason':'completion_evidence_conflict' if receipt=='not_completed' else 'local_completion_requires_reconciliation'}
    if previous is None: return {'decision':'complete','next':'submit_model','reason':'new_operation'}
    if receipt=='not_completed' or supported:
        return {'decision':'complete','next':'retry_same_key_model','reason':'declared_downstream_capability'}
    return {'decision':'unknown','next':'hold','reason':'completion_unresolved'}

def bounded(value, depth=0):
    if depth > 32:
        raise ValueError('nesting exceeds 32')
    if isinstance(value, (list, dict)):
        if len(value) > 1000:
            raise ValueError('container exceeds 1000 entries')
        for child in value.values() if isinstance(value, dict) else value:
            bounded(child, depth + 1)
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError('nonfinite number')


def load(path):
    # Bound bytes read even if a file grows between stat and read.
    with path.open('rb') as stream:
        raw = stream.read(2_000_001)
    if len(raw) > 2_000_000:
        raise ValueError('input exceeds 2MB')
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError('duplicate JSON key')
            out[key] = value
        return out
    value = json.loads(raw, object_pairs_hook=pairs,
                       parse_constant=lambda value: (_ for _ in ()).throw(ValueError('nonfinite JSON')))
    bounded(value)
    if not isinstance(value, dict):
        raise ValueError('input must be object')
    return value


def main(argv=None):
    parser=argparse.ArgumentParser(); parser.add_argument('--input',type=Path,required=True); parser.add_argument('--output',type=Path,required=True); args=parser.parse_args(argv)
    try:
        if args.input.resolve() == args.output.resolve() or (args.output.exists() and args.input.samefile(args.output)):
            raise ValueError('output must not overwrite input')
        raw=load(args.input)
        result=analyze(raw)
        args.output.write_text(json.dumps(result,indent=2,sort_keys=True,allow_nan=False)+'\n')
        return 1 if result['decision']=='failure' else 0
    except (ValueError,TypeError,KeyError,AttributeError,OSError,OverflowError,RecursionError) as exc:
        print(json.dumps({'error':str(exc),'decision':'malformed'}),file=sys.stderr); return 2

if __name__=='__main__': raise SystemExit(main())
