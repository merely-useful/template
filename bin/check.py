#!/usr/bin/env python

'''
Check the internal consistency of a project.
'''

import sys
import os
import glob
import re
import json
import yaml
from collections import Counter
from util import CHARACTERS, \
    CONFIG_FILE, \
    get_all_docs, \
    get_crossref, \
    get_doc, \
    get_funcs, \
    get_toc, \
    report


CHECK_PREFIX = 'check_'                 # prefix for all checking function names
FIGURE_DIR = 'figures'                  # where figure source is stored
LINK_FILE = '_includes/links.md'        # link definition file
NOT_ALL = {'check_all'}                 # functions to ignore when running all
PROSE_DIR_FMT = '_{}'                   # lesson or appendix directory (%language)
SOURCE_DIR = 'src'                      # source code inclusions


def main(language, verb):
    '''
    Find and call the function the caller wants.
    '''
    verb = CHECK_PREFIX + verb
    funcs = get_funcs(sys.modules['__main__'], CHECK_PREFIX)
    if verb not in funcs:
        _usage()
    funcs[verb](language)


def check_all(language):
    '''
    Check everything.
    '''
    funcs = get_funcs(sys.modules['__main__'], CHECK_PREFIX)
    for (name, func) in funcs.items():
        if name not in NOT_ALL:
            func(language)

    
def check_anchors(language):
    '''
    Check that anchors on H2's are properly formatted and include the chapter slug.
    '''
    header_pat = re.compile(r'^##\s+[^{]+{([^}]+)}\s*$')
    target_pat = re.compile(r'#s:([^-]+)')
    result = set()
    for (slug, filename, body, lines) in get_all_docs(CONFIG_FILE, language):
        for line in lines:
            anchor = header_pat.search(line)
            if not anchor:
                continue
            m = target_pat.search(anchor.group(1))
            if (not m) or (m.group(1) != slug):
                result.add('{}: "{}"'.format(slug, anchor.group(1)))
    report('Anchors', 'mismatched', result)


def check_chars(language):
    '''
    Find and report non-7-bit characters that aren't translated.
    '''
    allowed = set(CHARACTERS.keys())
    result = set()
    for (slug, filename, body, lines) in get_all_docs(CONFIG_FILE, language):
        for (i, line) in enumerate(lines):
            for (j, char) in enumerate(line):
                if (ord(char) > 127) and (char not in allowed):
                    result.add('{} {} {}: {}'.format(filename, i+1, j+1, char))
    report('Characters', 'non-ascii', result)


def check_cites(language):
    '''
    Check for unused and undefined citations.
    '''
    content = get_all_docs(CONFIG_FILE, language)
    used = _match_lines(content, r'\[([^\]]+)\]\(#BIB\)', flatten=',')
    defined = _match_lines(content, r'{:#b:([^}]+)}')
    report('Citations', 'unused', defined - used)
    report('Citations', 'undefined', used - defined)


def check_crossref(language):
    '''
    Check cross-references.
    '''
    content = get_all_docs(CONFIG_FILE, language)
    used = _match_lines(content, r'\[([^\]]+)\]\(#REF\)')
    crossref = get_crossref(language)
    defined = {x for x in crossref.keys() if x.startswith('s:')}
    report('Cross References', 'missing', used - defined)


def check_figref(language):
    '''
    Check figure references.
    '''
    content = get_all_docs(CONFIG_FILE, language)
    used = _match_lines(content, r'\[([^\]]+)\]\(#FIG\)')
    crossref = get_crossref(language)
    defined = {x for x in crossref.keys() if x.startswith('f:')}
    report('Figure References', 'missing', used - defined)
    report('Figure References', 'unused', defined - used)


def check_figures(language):
    '''
    Check included figures.
    '''
    def _ignore(filename):
        return filename.startswith('.') or \
            filename.endswith('.odg') or \
            filename.endswith('.pdf') or \
            filename.endswith('.xml')

    def _redundant(filename, defined):
        return filename.endswith('.png') and \
            filename.replace('.png', '.svg') in defined

    content = get_all_docs(CONFIG_FILE, language)
    used = _match_lines(content, r'{%\s+include\s+figure.html[^%]+src=".+/figures/([^"]+)"')
    defined = {f for f in os.listdir(FIGURE_DIR) if not _ignore(f)}
    defined -= {f for f in defined if _redundant(f, defined)}
    report('Figures', 'unused', defined - used)
    report('Figures', 'missing', used - defined)


def check_gloss(language):
    '''
    Check for unused and undefined glossary entries.
    '''
    content = get_all_docs(CONFIG_FILE, language)
    used = _match_body(content, r'\[.+?\]\(#(g:.+?)\)')
    defined = _match_lines(content, r'\*\*.+?\*\*{:#(g:.+?)}')
    report('Glossary Entries', 'unused', defined - used)
    report('Glossary Entries', 'missing', used - defined)


def check_langs(language):
    '''
    Check that every fenced code block specifies a language.
    '''
    content = get_all_docs(CONFIG_FILE, language)
    result = set()
    for (slug, filename, body, lines) in content:
        in_block = False
        for (i, line) in enumerate(lines):
            if not line.startswith('```'):
                pass
            elif in_block:
                in_block = False
            else:
                in_block = True
                if line.strip() == '```':
                    result.add('{} {:4d}'.format(filename, i+1))
    report('Code Blocks', 'no language', result)


def check_links(language):
    '''
    Check that external links are defined and used.
    '''
    content = get_all_docs(CONFIG_FILE, language)
    used = _match_body(content, r'\[.+?\]\[(.+?)\]')
    with open(LINK_FILE, 'r') as reader:
        body = reader.read()
    matches = re.findall(r'^\[(.+?)\]', body, flags=re.DOTALL + re.MULTILINE)
    links = Counter(matches)
    duplicate = {key for key in links if links[key] > 1}
    defined = set(links.keys())
    report('External Links', 'unused', defined - used)
    report('External Links', 'undefined', used - defined)
    report('External Links', 'duplicated', duplicate)


def check_src(language):
    '''
    Check external source files referenced in title attributes of code blocks.
    '''
    prefix_len = len(SOURCE_DIR + '/')

    def _unprefix(filename):
        return filename[prefix_len:]

    content = get_all_docs(CONFIG_FILE, language, remove_code_blocks=False)
    referenced = _match_body(content, r'{:\s+title="([^"]+)\s*"}')
    actual = {_unprefix(filename)
              for filename in glob.iglob('{}/**/*.*'.format(SOURCE_DIR), recursive=True)
              if not _ignore_file(filename)}
    report('Source Files', 'unused', actual - referenced)
    report('Source Files', 'missing', referenced - actual)


def check_toc(language):
    '''
    Check that filenames in configuration match actual files.
    '''
    toc = get_toc(CONFIG_FILE)
    defined = {slug for section in toc for slug in toc[section]}
    defined.add('index')
    actual = {filename.replace('.md', '')
              for filename in os.listdir(PROSE_DIR_FMT.format(language))
              if not _ignore_file(filename)}
    report('Table of Contents', 'unused', actual - defined)
    report('Table of Contents', 'missing', defined - actual)


#-------------------------------------------------------------------------------

    
def _ignore_file(x):
    return (x == '.gitkeep') or \
        x.endswith('~') or \
        ('__pycache__' in x)


def _match_body(content, pattern, flatten=None):
    '''
    Find all matches in all bodies, splitting and flattening if asked to do so.
    '''
    pat = re.compile(pattern, re.DOTALL)
    result = set()
    for (slug, filename, body, lines) in content:
        result |= set(pat.findall(body))
    if flatten is not None:
        result = _match_flatten(result, flatten)
    return result


def _match_lines(content, pattern, flatten=None):
    '''
    Find all matches in all lines, splitting and flattening if asked to do so.
    '''
    pat = re.compile(pattern)
    result = set()
    for (slug, filename, body, lines) in content:
        for line in lines:
            result |= set(pat.findall(line))
    if flatten is not None:
        result = _match_flatten(result, flatten)
    return result


def _match_flatten(matches, splitter):
    '''
    Flatten a list of multiple matches.
    '''
    return {individual for group in matches for individual in group.split(splitter)}


def _usage(status=1):
    print('usage: check.py language verb')
    funcs = _get_funcs(CHECK_PREFIX)
    for (name, func) in funcs.items():
        print('{:10s}: {}'.format(name.replace(CHECK_PREFIX, ''), func.__doc__.strip()))
    sys.exit(status)


if __name__ == '__main__':
    if len(sys.argv) != 3:
        _usage()
    main(sys.argv[1], sys.argv[2])
