#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = "Kevin Borgolte <kevin@borgolte.me>"

from xml.etree import ElementTree
from xml.etree.ElementTree import Element

from .common.data import data_from_xml
from .common.helper import element_or_xml
from .common.var import var_from_xml


class Assign(object):
    def __init__(self, var, substr):
        """Assign the value of a read (possibly restricted through a substr) to
        variable.

        See section 2.5 of pov-markup-spec.txt

        :param var: variable declaration.
        :param substr: how to mangle the read (slice or PCRE)
        """
        self.var = var
        self.substr = substr

    def __eq__(self, other):
        return self.var == other.var and self.substr == other.substr

    def to_xml(self):
        tag = Element('assign')
        tag.append(self.var.to_xml())
        if self.substr is not None:
            tag.append(self.substr.to_xml())

        return tag

    def __repr__(self):
        return ElementTree.tostring(self.to_xml())


@element_or_xml
def assign_from_xml(assign):
    slice = assign.find('slice')
    pcre = assign.find('pcre')
    var = assign.find('var')

    if slice is not None:
        substr = slice_from_xml(slice)
    elif pcre is not None:
        substr = pcre_from_xml(pcre)

    return Assign(var_from_xml(var), substr)


class Delim(object):
    def __init__(self, delim, format=None):
        """Restrict a read by a delimiter instead of a length.

        See section 2.5 of pov-markup-spec.txt

        :param delim: the delimiter
        :param format: the format the delimiter is in
                       (asciic or hex; defaults to asciic)
        """
        self.delim = delim.decode('hex') if format == 'hex' else delim
        self.format = format

    def __eq__(self, other):
        return self.delim == other.delim

    def to_xml(self):
        tag = Element('delim')
        if self.format is not None:
            delim = self.delim.decode('hex') if format == 'hex' else self.delim
            tag.set('format', self.format)
            tag.text = delim
        else:
            tag.text = self.delim

        return tag

    def __repr__(self):
        return ElementTree.tostring(self.to_xml())


@element_or_xml
def delim_from_xml(delim):
    return Delim(delim.text, delim.get('format'))


class Match(object):
    def __init__(self, criterias, invert=None):
        """Ensures that a read matches all criterias (which are concatenated
        together).

        The order is important and one should be careful about greedy PCREs.

        See section 2.6 of pov-markup-spec.txt

        :param criterias: a list of data, var, and PCRE elements that
                          must be matched
        :param invert: optional flag indicating if the match should be inverted
                       (implicit false)
        """
        self.criterias = criterias
        self.invert = invert

    def __eq__(self, other):
        return self.criterias == other.criterias and self.invert == other.invert

    def to_xml(self):
        tag = Element('match')
        if self.invert is not None:
            tag.set('invert', str(self.invert).lower())
        for criteria in self.criterias:
            tag.append(criteria.to_xml())

        return tag

    def __repr__(self):
        return ElementTree.tostring(self.to_xml())


@element_or_xml
def match_from_xml(match):
    criterias = []
    for entry in match:
        if entry.tag == 'data':
            criterias.append(data_from_xml(entry))
        elif entry.tag == 'var':
            criterias.append(var_from_xml(entry))
        elif entry.tag == 'pcre':
            criterias.append(pcre_from_xml(entry))
    return Match(criterias, match.get('invert'))


class PCRE(object):
    def __init__(self, pattern, group=None):
        """Restrict the assignment of a read through a perl-compatible regular
        expression.

        See section 2.5 of pov-markup-spec.txt

        :param pattern: PCRE-style pattern to match
        :param group: optional group number to assign from specific group in
                      regex (implicit 0)
        """
        self.pattern = pattern
        self.group = group

    def __eq__(self, other):
        # We are not actually comparing regular expressions here, for which we
        # would need to construct their DFA, minimize it, and then compare DFAs.
        # This is too much.
        return self.pattern == other.pattern and self.group == other.group

    def __repr__(self):
        if self.group is not None:
            return "<pcre group='{0.group}'>{0.pattern}</pcre>".format(self)
        else:
            return "<pcre>{}</pcre>".format(self.pattern)


@element_or_xml
def pcre_from_xml(pcre):
    return PCRE(pcre.text, pcre.get('group'))


class Slice(object):
    def __init__(self, begin=None, end=None):
        """Restrict a read to a slice (Python-style).

        See section 2.5 of pov-markup-spec.txt

        :param begin: beginning of the slice (optional and inclusive,
                      implicit start)
        :param end: end of the slice (optional and exclusive, implicit end)
        """
        self.begin = begin
        self.end = end

    def __eq__(self, other):
        # We are not doign comparisons to the implicit values here, we might
        # need to later.
        return self.begin == other.begin and self.end == other.end

    def to_xml(self):
        tag = Element('slice')
        if self.begin is not None:
            tag.set('begin', str(self.begin))
        if self.end is not None:
            tag.set('end', str(self.end))

        return tag

    def __repr__(self):
        return ElementTree.tostring(self.to_xml())


@element_or_xml
def slice_from_xml(slice):
    return Slice(slice.get('begin'), slice.get('end'))


class InvalidReadException(Exception):
    pass


class Read(object):
    def __init__(self, length=None, delim=None, assign=None, match=None,
                 timeout=None, echo=None):
        """Create a read element in a POV.

        See section 2.5 of pov-markup-spec.txt

        Read elements *must* have either a length or a delimiter, but not both
        can be used.

        :param length: number of bytes to read (character)
        :param delim: delimiter (alternative to length), all bytes up to this
                      sequence will be read, can be multi-character
                      (Delim object)
        :param assign: a variable to which it the read value will be assigned
                       if you use assign, you must specify what you want to
                       assign (e.g. through a PCRE or Python-style slice)
                       (Assign object)
        :param match:
        :param timeout: a timeout in milliseconds the read is allowed to wait
                        (integer)
        :param echo: should the read be echoed back the user? yes/no/ascii,
                     (default: no, debugging feature); yes corresponds to hex
        """
        # Required elements, one or the other
        self._length = length
        self._delim = delim
        if length is None and delim is None:
            raise InvalidReadException("You must specify delim or length")
        if length is not None and delim is not None:
            raise InvalidReadException("You cannot specify both delim and length")

        # Optional elements
        self.match = match
        self.assign = assign
        self.timeout = timeout

        # Attributes
        self.echo = echo

    @property
    def length(self):
        return self._length

    @length.setter
    def length(self, length):
        if self._delim is not None:
            raise InvalidReadException("You cannot set the length for a delim read")
        self._length = length

    @property
    def delim(self):
        return self._delim

    @delim.setter
    def delim(self, delim):
        if self._length is not None:
            raise InvalidReadException("You cannot set the length for a delim read")
        self._delim = delim

    def to_xml(self):
        read = Element('read')

        if self.echo is not None:
            read.set('echo', self.echo)

        if self.length is not None:
            length = Element('length')
            length.text = str(self.length)
            read.append(length)

        for thing in ('delim', 'match', 'assign'):
            if getattr(self, thing) is not None:
                read.append(getattr(self, thing).to_xml())

        if self.timeout is not None:
            timeout = Element('timeout')
            timeout.text = str(self.timeout)
            read.append(timeout)

        return read

    def __repr__(self):
        return ElementTree.tostring(self.to_xml())


@element_or_xml
def read_from_xml(read):
    length, delim, assign, match, timeout = (None,) * 5
    for entry in read:
        if entry.tag == 'length':
            length = int(entry.text)
        elif entry.tag == 'delim':
            delim = delim_from_xml(entry)
        elif entry.tag == 'assign':
            assign = assign_from_xml(entry)
        elif entry.tag == 'match':
            match = match_from_xml(entry)
        elif entry.tag == 'timeout':
            timeout = int(entry.text)
    return Read(length, delim, assign, match, timeout, read.get('echo'))
