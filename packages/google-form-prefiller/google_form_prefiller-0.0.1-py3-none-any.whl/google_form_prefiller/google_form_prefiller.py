#! python3
import argparse
import re
import subprocess, sys
import urllib.request
import yaml

def main():
    parser = argparse.ArgumentParser(description='Prefill Google forms from a YAML configuration file')
    parser.add_argument('file', type=str, help='Form configuration file')

    args = parser.parse_args()

    with open(args.file, 'r') as stream:
        try:
            yml = yaml.safe_load(stream)
            form = "https://docs.google.com/forms/d/e/%s/viewform?" % yml['form_id']
            date_pattern = re.compile(r"^(?P<year>\d+)-(?P<day>\d+)-(?P<month>\d+)\s(?P<hour>\d+):(?P<minute>\d+)$")
            for entry in yml['entries']:
                if entry['id'] is not None:
                    if isinstance(entry['value'], (list)):
                        for value in entry['value']:
                            form = form + ("entry.%s=%s&" % (entry['id'], urllib.request.pathname2url(str(value))))
                    elif isinstance(entry['value'], (str)) and re.match(date_pattern, entry['value']):
                        m = re.match(date_pattern, entry['value'])
                        for field in ['hour','minute','year','month','day']:
                            form = form + ("entry.%s_%s=%s&" % (entry['id'], field, urllib.request.pathname2url(str(m.group(field)))))
                    else:
                        form = form + ("entry.%s=%s&" % (entry['id'], urllib.request.pathname2url(str(entry['value']))))
            subprocess.call(
                [
                    "open" if sys.platform == "darwin" else "xdg-open",
                    form[:-1]
                ]
            )
        except yaml.YAMLError as err:
            print(err)

if __name__ == "__main__":
    main()
