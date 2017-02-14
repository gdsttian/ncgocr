# -*- coding: utf-8 -*-

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *
from txttk.nlptools import slim_stem
from txttk import retools
from collections import defaultdict
import re

def _regex(snippet):
    return snippet.replace('_', r'\S{0,6}').replace(' ', r'[\ \-]?')

def _unit_regex_out(lemma, snippets):
    regs = [_regex(snippet) for snippet in snippets]
    regs.sort(key=len, reverse=True)
    large_snippet = retools.nocatch(retools.parallel(regs))
    return r'(?P<{}>{})'.format(lemma, large_snippet)

def _unit_regex_in(lemma, snippets):
    medium_regs = []
    for snippet in snippets:
        reg = _regex(snippet)
        medium_regs.append(r'^(?:{0})\b'.format(reg))
        medium_regs.append(r'\b(?:{0})$'.format(reg))
    large_snippet = retools.nocatch(retools.parallel(medium_regs))
    return r'(?P<{}>{})'.format(lemma, large_snippet)

class PatternManager(object):
    def __init__(self):
        self.lemma2snippets = defaultdict(set)
        self.lemma2broad = defaultdict(set)
        
        
    def _sorted_lemma_n_snippets(self):
        lemma_n_snippets = self.lemma2snippets.items()
        key = lambda item: len(item[0])
        return sorted(lemma_n_snippets, key=key, reverse=True)
        
    def add_snippet(self, snippet, lemma):
        """
        Add a snippet to the lemma
        """
        self.lemma2snippets[lemma].add(snippet)
    
    def add_snippets(self, snippets, lemma):
        for snippet in snippets:
            self.add_snippet(snippet, lemma)


    def regex_out(self, lemma2snippet_more=dict()):
        """
        Return a long regex for pattern extraction in journal paper
        """
        lemma_n_snippets = self._sorted_lemma_n_snippets()
        regex = retools.parallel([_unit_regex_out(lemma, sorted(list(snippets))) for lemma, snippets in lemma_n_snippets], sort=True)
        
        wrapper = r'(?i)\b(?:{0})\b'
        return wrapper.format(regex)
    
    def regex_in(self):
        """
        Return a long regex for pattern extraction in GO definition
        """
        lemma_n_snippet = self._sorted_lemma_n_snippets()
        regex = retools.parallel([_unit_regex_in(lemma, snippet) for lemma, snippet in lemma_n_snippet])
        
        wrapper = r'(?:{0})'
        return wrapper.format(regex)
    

    def get_extractor(self):
        """
        Make a soft extractor based on given regular exrepssion. We use regex_out from PatternManager
        """
        regex = self.regex_out()
        
        def extractor(sentence, start):
            """
            Extract soft concepts (pattern) from given sentnece
            """
            results = []
            for m in re.finditer(regex, sentence):
                lemma = list(filter(lambda item: item[1] is not None, m.groupdict().items()))[0][0]
                pattern_start = m.start()
                pattern_end = m.end()
                results.append((lemma, start+pattern_start, start+pattern_end))
            return results
        return extractor
    
    
    @classmethod
    def from_definition(cls, definition_fp):
        """
        Return a PatternManager ojbect from give pattern difinition file
        """
        pm = cls()
        with open(definition_fp) as f:
            pattern_lines = filter(lambda x: x[0] != '#', f.read().split('\n'))
            
        for line in pattern_lines:
            lemma, sep, tail = line.partition(':')
            snippets = tail.split(';')
            pm.add_snippets(snippets, lemma)
        return pm