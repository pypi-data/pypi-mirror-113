import json


def create_aggregate(files: list, aggregate_out_file):
    aggregate = []
    for fp in files:
        with open(fp, 'r') as f:
            aggregate += json.load(f)
    with open(aggregate_out_file, 'w+') as f:
        f.write(json.dumps(aggregate))


def reformat(form: str):
    if form.lower().replace(' ', '').replace('-', '') == 'testrail':
        print('reformat for testrail')
    raise NotImplementedError


def sync(sync_to: str) -> None:
    raise NotImplementedError