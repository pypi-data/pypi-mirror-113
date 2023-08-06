"""Common utils and constants"""
import re

BASE_TESTER_NAME = 'BddTester'

COMPLETION_MSG = 'All scenarios ran!'
OK, FAIL, PENDING, TO = '✔', '✖', '❓', '↦'
BOLD = {OK: '✅', FAIL: '❌'}

PARAM_REGEX = r'\$([a-zA-Z_]+)'
I_REGEX = r'\$\(([^\$]+)\)'
O_REGEX = r'`([^`\$]+)`'


def to_sentence(name):
    return name.replace('_', ' ').capitalize()


def sentence_to_name(text):
    return '_'.join([re.sub(r'\W+', '', t).lower() for t in text.split()])


def strip_lines(lines):
    return list(filter(None, map(str.strip, lines)))


def extract_name(test_class_name):
    return test_class_name[4:] if test_class_name.startswith('Test') else test_class_name


def indent(text, tabs=1):
    newspace = ' '*4*tabs
    text = text.replace('\n', '\n' + newspace)

    return newspace + text


def make_doc(*lines):
    text = '\n'.join(line.strip() for line in lines)

    return f'"""\n{text}\n"""' if text else ''


def decorate(target, decorators):
    return '\n'.join([f'@{decorator}' for decorator in decorators] + [target])


def make_def_content(*doc_lines, body=''):
    return indent('\n'.join(([make_doc(*doc_lines)] if doc_lines else []) +
                            ([body] if body else []) or ['pass']))


def make_class_head(name, bases=(), decorators=()):
    inheritance = f'({", ".join(map(str.strip, bases))})' if bases else ''

    return decorate(f'class {name}{inheritance}', decorators)


def make_class(name, *doc_lines, bases=(), decorators=(), body=''):
    return '\n'.join([f'{make_class_head(name, bases, decorators)}:',
                      make_def_content(*doc_lines, body=body)])


def make_method(name, *doc_lines, args_text='', decorators=(), body=''):
    return '\n'.join([decorate(f'def {name}(self{args_text}):', decorators),
                      make_def_content(*doc_lines, body=body)])


def rstrip(text):
    return '\n'.join(list(map(str.rstrip, text.splitlines()))).lstrip('\n')
