import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pprint import pprint

from utils import functions as F

from .inverted_index import InvertedIndex
from .occurrence import Occurrence


class KnowledgeBase:
    """A KnowledgeBase has the following properties:

    Attributes:
        k_base: A dict representing the attributes and their list of terms
        inverted_k_base: A dict representing the all terms of the Knowledge
        Base and the attributes they are present
    """

    def __init__(self, kb_file):
        """Return a Knowledge Base object"""
        self.k_base = {}
        self.init_kb(kb_file)
        self.inverted_k_base = InvertedIndex(self.k_base).inverted_k_base

    def init_kb(self, kb_file):
        '''Parse Knowledge Base and prepare it to extract
        the content-based features'''
        tree = ET.parse(kb_file)
        root = tree.getroot()
        for item in root:
            attribute = F.normalize_str(item.tag)
            term = F.normalize_str(item.text)
            occurrence = Occurrence(term)

            if attribute in self.k_base:
                if term not in [obj.term for obj in self.k_base[attribute]]:
                    self.k_base[attribute].append(occurrence)
                else:
                    occ = [v for v in self.k_base[attribute] if v.term == term]
                    occ[0].number += 1
            else:
                self.k_base[attribute] = [occurrence]

    def get_terms_by_attribute(self, attr):
        '''Get the list of terms of an attribute'''
        attr_terms = []
        for attr in self.k_base[F.normalize_str(attr)]:
            attr_terms += attr.term.split()
        return attr_terms

    def get_most_common_term_by_attribute(self, attr):
        '''Get the highest frequency of any term among the values of A'''
        return Counter(self.get_terms_by_attribute(attr)).most_common(1)[0]

    def get_term_frequency_by_attribute(self, term, attr):
        '''Get the number of distinct values of attribute that contain the term t'''
        return self.get_terms_by_attribute(attr).count(term)

    def get_term_occurrence_number(self, term):
        '''Get the total number of occurrences of the term t in all attributes'''
        occ = 0
        keys = [k for k in self.inverted_k_base if term in k]
        for key in keys:
            occ += len(self.inverted_k_base[key])
        return occ