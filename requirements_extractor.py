import argparse
import os
import re
import csv

class RequirementsExtractor:

    @staticmethod
    def extract(document):
        """
        Extracts requirement text from a document.

        Args:
            document (string): document text with <req id=n.n.n.rn>...</req> tags surrounding requirements

        Returns:
            list: list of tuples of (id, requirement)
        """
        pattern = "<\s*req id=(?P<uid>(?P<section>\d(\.\w)*)\.r\d+)\s*>(?P<specification>[^<]+)<\/\s*req\s*>"
        requirements = []

        for req in re.finditer(pattern, document, re.MULTILINE):
            requirements.append({
                    'uid': req.group('uid'),
                    'section': req.group('section'),
                    'specification': req.group('specification')
                    })

        return requirements

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Generates compliance matrix from requirement document')
    parser.add_argument('doc_path', help='absolute or relative path to document with requirement tags')
    args = parser.parse_args()

    path = os.path.abspath(args.doc_path)

    requirements = []

    with open(path, 'r') as f:
        requirements = RequirementsExtractor.extract(f.read())

    with open('requirements.csv', 'w+') as csvfile:
        fieldnames = ['uid', 'section', 'specification']
        writer = csv.DictWriter(csvfile, fieldnames)

        writer.writeheader()

        for requirement in requirements:
            writer.writerow(requirement)

    with open('proposal_shell.txt', 'w+') as proposal:
        for req in requirements:
            proposal.write("<req id={0}>{1}\n\nbullets...\n\n</req>\n\n".format(req['uid'], req['specification']))
