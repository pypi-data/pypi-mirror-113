#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Wed Jul 14 14:59:25 2021 by generateDS.py version 2.39.2.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './canadapost_lib/address_complete_retrieve.py')
#
# Command line arguments:
#   ./schemas/address_complete_retrieve.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/purplship-carriers/.venv/purplship-carriers/bin/generateDS --no-namespace-defs -o "./canadapost_lib/address_complete_retrieve.py" ./schemas/address_complete_retrieve.xsd
#
# Current working directory (os.getcwd()):
#   canadapost
#

import sys
try:
    ModulenotfoundExp_ = ModuleNotFoundError
except NameError:
    ModulenotfoundExp_ = ImportError
from six.moves import zip_longest
import os
import re as re_
import base64
import datetime as datetime_
import decimal as decimal_
try:
    from lxml import etree as etree_
except ModulenotfoundExp_ :
    from xml.etree import ElementTree as etree_


Validate_simpletypes_ = True
SaveElementTreeNode = True
if sys.version_info.major == 2:
    BaseStrType_ = basestring
else:
    BaseStrType_ = str


def parsexml_(infile, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    try:
        if isinstance(infile, os.PathLike):
            infile = os.path.join(infile)
    except AttributeError:
        pass
    doc = etree_.parse(infile, parser=parser, **kwargs)
    return doc

def parsexmlstring_(instring, parser=None, **kwargs):
    if parser is None:
        # Use the lxml ElementTree compatible parser so that, e.g.,
        #   we ignore comments.
        try:
            parser = etree_.ETCompatXMLParser()
        except AttributeError:
            # fallback to xml.etree
            parser = etree_.XMLParser()
    element = etree_.fromstring(instring, parser=parser, **kwargs)
    return element

#
# Namespace prefix definition table (and other attributes, too)
#
# The module generatedsnamespaces, if it is importable, must contain
# a dictionary named GeneratedsNamespaceDefs.  This Python dictionary
# should map element type names (strings) to XML schema namespace prefix
# definitions.  The export method for any class for which there is
# a namespace prefix definition, will export that definition in the
# XML representation of that element.  See the export method of
# any generated element type class for an example of the use of this
# table.
# A sample table is:
#
#     # File: generatedsnamespaces.py
#
#     GenerateDSNamespaceDefs = {
#         "ElementtypeA": "http://www.xxx.com/namespaceA",
#         "ElementtypeB": "http://www.xxx.com/namespaceB",
#     }
#
# Additionally, the generatedsnamespaces module can contain a python
# dictionary named GenerateDSNamespaceTypePrefixes that associates element
# types with the namespace prefixes that are to be added to the
# "xsi:type" attribute value.  See the _exportAttributes method of
# any generated element type and the generation of "xsi:type" for an
# example of the use of this table.
# An example table:
#
#     # File: generatedsnamespaces.py
#
#     GenerateDSNamespaceTypePrefixes = {
#         "ElementtypeC": "aaa:",
#         "ElementtypeD": "bbb:",
#     }
#

try:
    from generatedsnamespaces import GenerateDSNamespaceDefs as GenerateDSNamespaceDefs_
except ModulenotfoundExp_ :
    GenerateDSNamespaceDefs_ = {}
try:
    from generatedsnamespaces import GenerateDSNamespaceTypePrefixes as GenerateDSNamespaceTypePrefixes_
except ModulenotfoundExp_ :
    GenerateDSNamespaceTypePrefixes_ = {}

#
# You can replace the following class definition by defining an
# importable module named "generatedscollector" containing a class
# named "GdsCollector".  See the default class definition below for
# clues about the possible content of that class.
#
try:
    from generatedscollector import GdsCollector as GdsCollector_
except ModulenotfoundExp_ :

    class GdsCollector_(object):

        def __init__(self, messages=None):
            if messages is None:
                self.messages = []
            else:
                self.messages = messages

        def add_message(self, msg):
            self.messages.append(msg)

        def get_messages(self):
            return self.messages

        def clear_messages(self):
            self.messages = []

        def print_messages(self):
            for msg in self.messages:
                print("Warning: {}".format(msg))

        def write_messages(self, outstream):
            for msg in self.messages:
                outstream.write("Warning: {}\n".format(msg))


#
# The super-class for enum types
#

try:
    from enum import Enum
except ModulenotfoundExp_ :
    Enum = object

#
# The root super-class for element type classes
#
# Calls to the methods in these classes are generated by generateDS.py.
# You can replace these methods by re-implementing the following class
#   in a module named generatedssuper.py.

try:
    from generatedssuper import GeneratedsSuper
except ModulenotfoundExp_ as exp:
    try:
        from generatedssupersuper import GeneratedsSuperSuper
    except ModulenotfoundExp_ as exp:
        class GeneratedsSuperSuper(object):
            pass
    
    class GeneratedsSuper(GeneratedsSuperSuper):
        __hash__ = object.__hash__
        tzoff_pattern = re_.compile(r'(\+|-)((0\d|1[0-3]):[0-5]\d|14:00)$')
        class _FixedOffsetTZ(datetime_.tzinfo):
            def __init__(self, offset, name):
                self.__offset = datetime_.timedelta(minutes=offset)
                self.__name = name
            def utcoffset(self, dt):
                return self.__offset
            def tzname(self, dt):
                return self.__name
            def dst(self, dt):
                return None
        def gds_format_string(self, input_data, input_name=''):
            return input_data
        def gds_parse_string(self, input_data, node=None, input_name=''):
            return input_data
        def gds_validate_string(self, input_data, node=None, input_name=''):
            if not input_data:
                return ''
            else:
                return input_data
        def gds_format_base64(self, input_data, input_name=''):
            return base64.b64encode(input_data)
        def gds_validate_base64(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_integer(self, input_data, input_name=''):
            return '%d' % input_data
        def gds_parse_integer(self, input_data, node=None, input_name=''):
            try:
                ival = int(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires integer value: %s' % exp)
            return ival
        def gds_validate_integer(self, input_data, node=None, input_name=''):
            try:
                value = int(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires integer value')
            return value
        def gds_format_integer_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return '%s' % ' '.join(input_data)
        def gds_validate_integer_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    int(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of integer values')
            return values
        def gds_format_float(self, input_data, input_name=''):
            return ('%.15f' % input_data).rstrip('0')
        def gds_parse_float(self, input_data, node=None, input_name=''):
            try:
                fval_ = float(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires float or double value: %s' % exp)
            return fval_
        def gds_validate_float(self, input_data, node=None, input_name=''):
            try:
                value = float(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires float value')
            return value
        def gds_format_float_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return '%s' % ' '.join(input_data)
        def gds_validate_float_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    float(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of float values')
            return values
        def gds_format_decimal(self, input_data, input_name=''):
            return_value = '%s' % input_data
            if '.' in return_value:
                return_value = return_value.rstrip('0')
                if return_value.endswith('.'):
                    return_value = return_value.rstrip('.')
            return return_value
        def gds_parse_decimal(self, input_data, node=None, input_name=''):
            try:
                decimal_value = decimal_.Decimal(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires decimal value')
            return decimal_value
        def gds_validate_decimal(self, input_data, node=None, input_name=''):
            try:
                value = decimal_.Decimal(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires decimal value')
            return value
        def gds_format_decimal_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return ' '.join([self.gds_format_decimal(item) for item in input_data])
        def gds_validate_decimal_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    decimal_.Decimal(value)
                except (TypeError, ValueError):
                    raise_parse_error(node, 'Requires sequence of decimal values')
            return values
        def gds_format_double(self, input_data, input_name=''):
            return '%s' % input_data
        def gds_parse_double(self, input_data, node=None, input_name=''):
            try:
                fval_ = float(input_data)
            except (TypeError, ValueError) as exp:
                raise_parse_error(node, 'Requires double or float value: %s' % exp)
            return fval_
        def gds_validate_double(self, input_data, node=None, input_name=''):
            try:
                value = float(input_data)
            except (TypeError, ValueError):
                raise_parse_error(node, 'Requires double or float value')
            return value
        def gds_format_double_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return '%s' % ' '.join(input_data)
        def gds_validate_double_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                try:
                    float(value)
                except (TypeError, ValueError):
                    raise_parse_error(
                        node, 'Requires sequence of double or float values')
            return values
        def gds_format_boolean(self, input_data, input_name=''):
            return ('%s' % input_data).lower()
        def gds_parse_boolean(self, input_data, node=None, input_name=''):
            if input_data in ('true', '1'):
                bval = True
            elif input_data in ('false', '0'):
                bval = False
            else:
                raise_parse_error(node, 'Requires boolean value')
            return bval
        def gds_validate_boolean(self, input_data, node=None, input_name=''):
            if input_data not in (True, 1, False, 0, ):
                raise_parse_error(
                    node,
                    'Requires boolean value '
                    '(one of True, 1, False, 0)')
            return input_data
        def gds_format_boolean_list(self, input_data, input_name=''):
            if len(input_data) > 0 and not isinstance(input_data[0], BaseStrType_):
                input_data = [str(s) for s in input_data]
            return '%s' % ' '.join(input_data)
        def gds_validate_boolean_list(
                self, input_data, node=None, input_name=''):
            values = input_data.split()
            for value in values:
                value = self.gds_parse_boolean(value, node, input_name)
                if value not in (True, 1, False, 0, ):
                    raise_parse_error(
                        node,
                        'Requires sequence of boolean values '
                        '(one of True, 1, False, 0)')
            return values
        def gds_validate_datetime(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_datetime(self, input_data, input_name=''):
            if input_data.microsecond == 0:
                _svalue = '%04d-%02d-%02dT%02d:%02d:%02d' % (
                    input_data.year,
                    input_data.month,
                    input_data.day,
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                )
            else:
                _svalue = '%04d-%02d-%02dT%02d:%02d:%02d.%s' % (
                    input_data.year,
                    input_data.month,
                    input_data.day,
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                    ('%f' % (float(input_data.microsecond) / 1000000))[2:],
                )
            if input_data.tzinfo is not None:
                tzoff = input_data.tzinfo.utcoffset(input_data)
                if tzoff is not None:
                    total_seconds = tzoff.seconds + (86400 * tzoff.days)
                    if total_seconds == 0:
                        _svalue += 'Z'
                    else:
                        if total_seconds < 0:
                            _svalue += '-'
                            total_seconds *= -1
                        else:
                            _svalue += '+'
                        hours = total_seconds // 3600
                        minutes = (total_seconds - (hours * 3600)) // 60
                        _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
            return _svalue
        @classmethod
        def gds_parse_datetime(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(
                        tzoff, results.group(0))
                    input_data = input_data[:-6]
            time_parts = input_data.split('.')
            if len(time_parts) > 1:
                micro_seconds = int(float('0.' + time_parts[1]) * 1000000)
                input_data = '%s.%s' % (
                    time_parts[0], "{}".format(micro_seconds).rjust(6, "0"), )
                dt = datetime_.datetime.strptime(
                    input_data, '%Y-%m-%dT%H:%M:%S.%f')
            else:
                dt = datetime_.datetime.strptime(
                    input_data, '%Y-%m-%dT%H:%M:%S')
            dt = dt.replace(tzinfo=tz)
            return dt
        def gds_validate_date(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_date(self, input_data, input_name=''):
            _svalue = '%04d-%02d-%02d' % (
                input_data.year,
                input_data.month,
                input_data.day,
            )
            try:
                if input_data.tzinfo is not None:
                    tzoff = input_data.tzinfo.utcoffset(input_data)
                    if tzoff is not None:
                        total_seconds = tzoff.seconds + (86400 * tzoff.days)
                        if total_seconds == 0:
                            _svalue += 'Z'
                        else:
                            if total_seconds < 0:
                                _svalue += '-'
                                total_seconds *= -1
                            else:
                                _svalue += '+'
                            hours = total_seconds // 3600
                            minutes = (total_seconds - (hours * 3600)) // 60
                            _svalue += '{0:02d}:{1:02d}'.format(
                                hours, minutes)
            except AttributeError:
                pass
            return _svalue
        @classmethod
        def gds_parse_date(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(
                        tzoff, results.group(0))
                    input_data = input_data[:-6]
            dt = datetime_.datetime.strptime(input_data, '%Y-%m-%d')
            dt = dt.replace(tzinfo=tz)
            return dt.date()
        def gds_validate_time(self, input_data, node=None, input_name=''):
            return input_data
        def gds_format_time(self, input_data, input_name=''):
            if input_data.microsecond == 0:
                _svalue = '%02d:%02d:%02d' % (
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                )
            else:
                _svalue = '%02d:%02d:%02d.%s' % (
                    input_data.hour,
                    input_data.minute,
                    input_data.second,
                    ('%f' % (float(input_data.microsecond) / 1000000))[2:],
                )
            if input_data.tzinfo is not None:
                tzoff = input_data.tzinfo.utcoffset(input_data)
                if tzoff is not None:
                    total_seconds = tzoff.seconds + (86400 * tzoff.days)
                    if total_seconds == 0:
                        _svalue += 'Z'
                    else:
                        if total_seconds < 0:
                            _svalue += '-'
                            total_seconds *= -1
                        else:
                            _svalue += '+'
                        hours = total_seconds // 3600
                        minutes = (total_seconds - (hours * 3600)) // 60
                        _svalue += '{0:02d}:{1:02d}'.format(hours, minutes)
            return _svalue
        def gds_validate_simple_patterns(self, patterns, target):
            # pat is a list of lists of strings/patterns.
            # The target value must match at least one of the patterns
            # in order for the test to succeed.
            found1 = True
            for patterns1 in patterns:
                found2 = False
                for patterns2 in patterns1:
                    mo = re_.search(patterns2, target)
                    if mo is not None and len(mo.group(0)) == len(target):
                        found2 = True
                        break
                if not found2:
                    found1 = False
                    break
            return found1
        @classmethod
        def gds_parse_time(cls, input_data):
            tz = None
            if input_data[-1] == 'Z':
                tz = GeneratedsSuper._FixedOffsetTZ(0, 'UTC')
                input_data = input_data[:-1]
            else:
                results = GeneratedsSuper.tzoff_pattern.search(input_data)
                if results is not None:
                    tzoff_parts = results.group(2).split(':')
                    tzoff = int(tzoff_parts[0]) * 60 + int(tzoff_parts[1])
                    if results.group(1) == '-':
                        tzoff *= -1
                    tz = GeneratedsSuper._FixedOffsetTZ(
                        tzoff, results.group(0))
                    input_data = input_data[:-6]
            if len(input_data.split('.')) > 1:
                dt = datetime_.datetime.strptime(input_data, '%H:%M:%S.%f')
            else:
                dt = datetime_.datetime.strptime(input_data, '%H:%M:%S')
            dt = dt.replace(tzinfo=tz)
            return dt.time()
        def gds_check_cardinality_(
                self, value, input_name,
                min_occurs=0, max_occurs=1, required=None):
            if value is None:
                length = 0
            elif isinstance(value, list):
                length = len(value)
            else:
                length = 1
            if required is not None :
                if required and length < 1:
                    self.gds_collector_.add_message(
                        "Required value {}{} is missing".format(
                            input_name, self.gds_get_node_lineno_()))
            if length < min_occurs:
                self.gds_collector_.add_message(
                    "Number of values for {}{} is below "
                    "the minimum allowed, "
                    "expected at least {}, found {}".format(
                        input_name, self.gds_get_node_lineno_(),
                        min_occurs, length))
            elif length > max_occurs:
                self.gds_collector_.add_message(
                    "Number of values for {}{} is above "
                    "the maximum allowed, "
                    "expected at most {}, found {}".format(
                        input_name, self.gds_get_node_lineno_(),
                        max_occurs, length))
        def gds_validate_builtin_ST_(
                self, validator, value, input_name,
                min_occurs=None, max_occurs=None, required=None):
            if value is not None:
                try:
                    validator(value, input_name=input_name)
                except GDSParseError as parse_error:
                    self.gds_collector_.add_message(str(parse_error))
        def gds_validate_defined_ST_(
                self, validator, value, input_name,
                min_occurs=None, max_occurs=None, required=None):
            if value is not None:
                try:
                    validator(value)
                except GDSParseError as parse_error:
                    self.gds_collector_.add_message(str(parse_error))
        def gds_str_lower(self, instring):
            return instring.lower()
        def get_path_(self, node):
            path_list = []
            self.get_path_list_(node, path_list)
            path_list.reverse()
            path = '/'.join(path_list)
            return path
        Tag_strip_pattern_ = re_.compile(r'\{.*\}')
        def get_path_list_(self, node, path_list):
            if node is None:
                return
            tag = GeneratedsSuper.Tag_strip_pattern_.sub('', node.tag)
            if tag:
                path_list.append(tag)
            self.get_path_list_(node.getparent(), path_list)
        def get_class_obj_(self, node, default_class=None):
            class_obj1 = default_class
            if 'xsi' in node.nsmap:
                classname = node.get('{%s}type' % node.nsmap['xsi'])
                if classname is not None:
                    names = classname.split(':')
                    if len(names) == 2:
                        classname = names[1]
                    class_obj2 = globals().get(classname)
                    if class_obj2 is not None:
                        class_obj1 = class_obj2
            return class_obj1
        def gds_build_any(self, node, type_name=None):
            # provide default value in case option --disable-xml is used.
            content = ""
            content = etree_.tostring(node, encoding="unicode")
            return content
        @classmethod
        def gds_reverse_node_mapping(cls, mapping):
            return dict(((v, k) for k, v in mapping.items()))
        @staticmethod
        def gds_encode(instring):
            if sys.version_info.major == 2:
                if ExternalEncoding:
                    encoding = ExternalEncoding
                else:
                    encoding = 'utf-8'
                return instring.encode(encoding)
            else:
                return instring
        @staticmethod
        def convert_unicode(instring):
            if isinstance(instring, str):
                result = quote_xml(instring)
            elif sys.version_info.major == 2 and isinstance(instring, unicode):
                result = quote_xml(instring).encode('utf8')
            else:
                result = GeneratedsSuper.gds_encode(str(instring))
            return result
        def __eq__(self, other):
            def excl_select_objs_(obj):
                return (obj[0] != 'parent_object_' and
                        obj[0] != 'gds_collector_')
            if type(self) != type(other):
                return False
            return all(x == y for x, y in zip_longest(
                filter(excl_select_objs_, self.__dict__.items()),
                filter(excl_select_objs_, other.__dict__.items())))
        def __ne__(self, other):
            return not self.__eq__(other)
        # Django ETL transform hooks.
        def gds_djo_etl_transform(self):
            pass
        def gds_djo_etl_transform_db_obj(self, dbobj):
            pass
        # SQLAlchemy ETL transform hooks.
        def gds_sqa_etl_transform(self):
            return 0, None
        def gds_sqa_etl_transform_db_obj(self, dbobj):
            pass
        def gds_get_node_lineno_(self):
            if (hasattr(self, "gds_elementtree_node_") and
                    self.gds_elementtree_node_ is not None):
                return ' near line {}'.format(
                    self.gds_elementtree_node_.sourceline)
            else:
                return ""
    
    
    def getSubclassFromModule_(module, class_):
        '''Get the subclass of a class from a specific module.'''
        name = class_.__name__ + 'Sub'
        if hasattr(module, name):
            return getattr(module, name)
        else:
            return None


#
# If you have installed IPython you can uncomment and use the following.
# IPython is available from http://ipython.scipy.org/.
#

## from IPython.Shell import IPShellEmbed
## args = ''
## ipshell = IPShellEmbed(args,
##     banner = 'Dropping into IPython',
##     exit_msg = 'Leaving Interpreter, back to program.')

# Then use the following line where and when you want to drop into the
# IPython shell:
#    ipshell('<some message> -- Entering ipshell.\nHit Ctrl-D to exit')

#
# Globals
#

ExternalEncoding = ''
# Set this to false in order to deactivate during export, the use of
# name space prefixes captured from the input document.
UseCapturedNS_ = True
CapturedNsmap_ = {}
Tag_pattern_ = re_.compile(r'({.*})?(.*)')
String_cleanup_pat_ = re_.compile(r"[\n\r\s]+")
Namespace_extract_pat_ = re_.compile(r'{(.*)}(.*)')
CDATA_pattern_ = re_.compile(r"<!\[CDATA\[.*?\]\]>", re_.DOTALL)

# Change this to redirect the generated superclass module to use a
# specific subclass module.
CurrentSubclassModule_ = None

#
# Support/utility functions.
#


def showIndent(outfile, level, pretty_print=True):
    if pretty_print:
        for idx in range(level):
            outfile.write('    ')


def quote_xml(inStr):
    "Escape markup chars, but do not modify CDATA sections."
    if not inStr:
        return ''
    s1 = (isinstance(inStr, BaseStrType_) and inStr or '%s' % inStr)
    s2 = ''
    pos = 0
    matchobjects = CDATA_pattern_.finditer(s1)
    for mo in matchobjects:
        s3 = s1[pos:mo.start()]
        s2 += quote_xml_aux(s3)
        s2 += s1[mo.start():mo.end()]
        pos = mo.end()
    s3 = s1[pos:]
    s2 += quote_xml_aux(s3)
    return s2


def quote_xml_aux(inStr):
    s1 = inStr.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    return s1


def quote_attrib(inStr):
    s1 = (isinstance(inStr, BaseStrType_) and inStr or '%s' % inStr)
    s1 = s1.replace('&', '&amp;')
    s1 = s1.replace('<', '&lt;')
    s1 = s1.replace('>', '&gt;')
    if '"' in s1:
        if "'" in s1:
            s1 = '"%s"' % s1.replace('"', "&quot;")
        else:
            s1 = "'%s'" % s1
    else:
        s1 = '"%s"' % s1
    return s1


def quote_python(inStr):
    s1 = inStr
    if s1.find("'") == -1:
        if s1.find('\n') == -1:
            return "'%s'" % s1
        else:
            return "'''%s'''" % s1
    else:
        if s1.find('"') != -1:
            s1 = s1.replace('"', '\\"')
        if s1.find('\n') == -1:
            return '"%s"' % s1
        else:
            return '"""%s"""' % s1


def get_all_text_(node):
    if node.text is not None:
        text = node.text
    else:
        text = ''
    for child in node:
        if child.tail is not None:
            text += child.tail
    return text


def find_attr_value_(attr_name, node):
    attrs = node.attrib
    attr_parts = attr_name.split(':')
    value = None
    if len(attr_parts) == 1:
        value = attrs.get(attr_name)
    elif len(attr_parts) == 2:
        prefix, name = attr_parts
        if prefix == 'xml':
            namespace = 'http://www.w3.org/XML/1998/namespace'
        else:
            namespace = node.nsmap.get(prefix)
        if namespace is not None:
            value = attrs.get('{%s}%s' % (namespace, name, ))
    return value


def encode_str_2_3(instr):
    return instr


class GDSParseError(Exception):
    pass


def raise_parse_error(node, msg):
    if node is not None:
        msg = '%s (element %s/line %d)' % (msg, node.tag, node.sourceline, )
    raise GDSParseError(msg)


class MixedContainer:
    # Constants for category:
    CategoryNone = 0
    CategoryText = 1
    CategorySimple = 2
    CategoryComplex = 3
    # Constants for content_type:
    TypeNone = 0
    TypeText = 1
    TypeString = 2
    TypeInteger = 3
    TypeFloat = 4
    TypeDecimal = 5
    TypeDouble = 6
    TypeBoolean = 7
    TypeBase64 = 8
    def __init__(self, category, content_type, name, value):
        self.category = category
        self.content_type = content_type
        self.name = name
        self.value = value
    def getCategory(self):
        return self.category
    def getContenttype(self, content_type):
        return self.content_type
    def getValue(self):
        return self.value
    def getName(self):
        return self.name
    def export(self, outfile, level, name, namespace,
               pretty_print=True):
        if self.category == MixedContainer.CategoryText:
            # Prevent exporting empty content as empty lines.
            if self.value.strip():
                outfile.write(self.value)
        elif self.category == MixedContainer.CategorySimple:
            self.exportSimple(outfile, level, name)
        else:    # category == MixedContainer.CategoryComplex
            self.value.export(
                outfile, level, namespace, name_=name,
                pretty_print=pretty_print)
    def exportSimple(self, outfile, level, name):
        if self.content_type == MixedContainer.TypeString:
            outfile.write('<%s>%s</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeInteger or \
                self.content_type == MixedContainer.TypeBoolean:
            outfile.write('<%s>%d</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeFloat or \
                self.content_type == MixedContainer.TypeDecimal:
            outfile.write('<%s>%f</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeDouble:
            outfile.write('<%s>%g</%s>' % (
                self.name, self.value, self.name))
        elif self.content_type == MixedContainer.TypeBase64:
            outfile.write('<%s>%s</%s>' % (
                self.name,
                base64.b64encode(self.value),
                self.name))
    def to_etree(self, element, mapping_=None, nsmap_=None):
        if self.category == MixedContainer.CategoryText:
            # Prevent exporting empty content as empty lines.
            if self.value.strip():
                if len(element) > 0:
                    if element[-1].tail is None:
                        element[-1].tail = self.value
                    else:
                        element[-1].tail += self.value
                else:
                    if element.text is None:
                        element.text = self.value
                    else:
                        element.text += self.value
        elif self.category == MixedContainer.CategorySimple:
            subelement = etree_.SubElement(
                element, '%s' % self.name)
            subelement.text = self.to_etree_simple()
        else:    # category == MixedContainer.CategoryComplex
            self.value.to_etree(element)
    def to_etree_simple(self, mapping_=None, nsmap_=None):
        if self.content_type == MixedContainer.TypeString:
            text = self.value
        elif (self.content_type == MixedContainer.TypeInteger or
                self.content_type == MixedContainer.TypeBoolean):
            text = '%d' % self.value
        elif (self.content_type == MixedContainer.TypeFloat or
                self.content_type == MixedContainer.TypeDecimal):
            text = '%f' % self.value
        elif self.content_type == MixedContainer.TypeDouble:
            text = '%g' % self.value
        elif self.content_type == MixedContainer.TypeBase64:
            text = '%s' % base64.b64encode(self.value)
        return text
    def exportLiteral(self, outfile, level, name):
        if self.category == MixedContainer.CategoryText:
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s", "%s"),\n' % (
                    self.category, self.content_type,
                    self.name, self.value))
        elif self.category == MixedContainer.CategorySimple:
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s", "%s"),\n' % (
                    self.category, self.content_type,
                    self.name, self.value))
        else:    # category == MixedContainer.CategoryComplex
            showIndent(outfile, level)
            outfile.write(
                'model_.MixedContainer(%d, %d, "%s",\n' % (
                    self.category, self.content_type, self.name,))
            self.value.exportLiteral(outfile, level + 1)
            showIndent(outfile, level)
            outfile.write(')\n')


class MemberSpec_(object):
    def __init__(self, name='', data_type='', container=0,
            optional=0, child_attrs=None, choice=None):
        self.name = name
        self.data_type = data_type
        self.container = container
        self.child_attrs = child_attrs
        self.choice = choice
        self.optional = optional
    def set_name(self, name): self.name = name
    def get_name(self): return self.name
    def set_data_type(self, data_type): self.data_type = data_type
    def get_data_type_chain(self): return self.data_type
    def get_data_type(self):
        if isinstance(self.data_type, list):
            if len(self.data_type) > 0:
                return self.data_type[-1]
            else:
                return 'xs:string'
        else:
            return self.data_type
    def set_container(self, container): self.container = container
    def get_container(self): return self.container
    def set_child_attrs(self, child_attrs): self.child_attrs = child_attrs
    def get_child_attrs(self): return self.child_attrs
    def set_choice(self, choice): self.choice = choice
    def get_choice(self): return self.choice
    def set_optional(self, optional): self.optional = optional
    def get_optional(self): return self.optional


def _cast(typ, value):
    if typ is None or value is None:
        return value
    return typ(value)

#
# Data representation classes.
#


class AddressComplete_Interactive_Retrieve_v2_11(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Key=None, Id=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Key = Key
        self.Key_nsprefix_ = None
        self.Id = Id
        self.Id_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AddressComplete_Interactive_Retrieve_v2_11)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AddressComplete_Interactive_Retrieve_v2_11.subclass:
            return AddressComplete_Interactive_Retrieve_v2_11.subclass(*args_, **kwargs_)
        else:
            return AddressComplete_Interactive_Retrieve_v2_11(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Key(self):
        return self.Key
    def set_Key(self, Key):
        self.Key = Key
    def get_Id(self):
        return self.Id
    def set_Id(self, Id):
        self.Id = Id
    def _hasContent(self):
        if (
            self.Key is not None or
            self.Id is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressComplete_Interactive_Retrieve_v2_11', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AddressComplete_Interactive_Retrieve_v2_11')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AddressComplete_Interactive_Retrieve_v2_11':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AddressComplete_Interactive_Retrieve_v2_11')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AddressComplete_Interactive_Retrieve_v2_11', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AddressComplete_Interactive_Retrieve_v2_11'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressComplete_Interactive_Retrieve_v2_11', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Key is not None:
            namespaceprefix_ = self.Key_nsprefix_ + ':' if (UseCapturedNS_ and self.Key_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sKey>%s</%sKey>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Key), input_name='Key')), namespaceprefix_ , eol_))
        if self.Id is not None:
            namespaceprefix_ = self.Id_nsprefix_ + ':' if (UseCapturedNS_ and self.Id_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sId>%s</%sId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Id), input_name='Id')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Key':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Key')
            value_ = self.gds_validate_string(value_, node, 'Key')
            self.Key = value_
            self.Key_nsprefix_ = child_.prefix
        elif nodeName_ == 'Id':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Id')
            value_ = self.gds_validate_string(value_, node, 'Id')
            self.Id = value_
            self.Id_nsprefix_ = child_.prefix
# end class AddressComplete_Interactive_Retrieve_v2_11


class AddressComplete_Interactive_Retrieve_v2_11_Response(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AddressComplete_Interactive_Retrieve_v2_11_Result=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.AddressComplete_Interactive_Retrieve_v2_11_Result = AddressComplete_Interactive_Retrieve_v2_11_Result
        self.AddressComplete_Interactive_Retrieve_v2_11_Result_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AddressComplete_Interactive_Retrieve_v2_11_Response)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AddressComplete_Interactive_Retrieve_v2_11_Response.subclass:
            return AddressComplete_Interactive_Retrieve_v2_11_Response.subclass(*args_, **kwargs_)
        else:
            return AddressComplete_Interactive_Retrieve_v2_11_Response(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_AddressComplete_Interactive_Retrieve_v2_11_Result(self):
        return self.AddressComplete_Interactive_Retrieve_v2_11_Result
    def set_AddressComplete_Interactive_Retrieve_v2_11_Result(self, AddressComplete_Interactive_Retrieve_v2_11_Result):
        self.AddressComplete_Interactive_Retrieve_v2_11_Result = AddressComplete_Interactive_Retrieve_v2_11_Result
    def _hasContent(self):
        if (
            self.AddressComplete_Interactive_Retrieve_v2_11_Result is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressComplete_Interactive_Retrieve_v2_11_Response', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AddressComplete_Interactive_Retrieve_v2_11_Response')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AddressComplete_Interactive_Retrieve_v2_11_Response':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AddressComplete_Interactive_Retrieve_v2_11_Response')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AddressComplete_Interactive_Retrieve_v2_11_Response', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AddressComplete_Interactive_Retrieve_v2_11_Response'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressComplete_Interactive_Retrieve_v2_11_Response', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.AddressComplete_Interactive_Retrieve_v2_11_Result is not None:
            namespaceprefix_ = self.AddressComplete_Interactive_Retrieve_v2_11_Result_nsprefix_ + ':' if (UseCapturedNS_ and self.AddressComplete_Interactive_Retrieve_v2_11_Result_nsprefix_) else ''
            self.AddressComplete_Interactive_Retrieve_v2_11_Result.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AddressComplete_Interactive_Retrieve_v2_11_Result', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'AddressComplete_Interactive_Retrieve_v2_11_Result':
            obj_ = AddressComplete_Interactive_Retrieve_v2_11_ArrayOfResults.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AddressComplete_Interactive_Retrieve_v2_11_Result = obj_
            obj_.original_tagname_ = 'AddressComplete_Interactive_Retrieve_v2_11_Result'
# end class AddressComplete_Interactive_Retrieve_v2_11_Response


class AddressComplete_Interactive_Retrieve_v2_11_ArrayOfResults(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, AddressComplete_Interactive_Retrieve_v2_11_Results=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if AddressComplete_Interactive_Retrieve_v2_11_Results is None:
            self.AddressComplete_Interactive_Retrieve_v2_11_Results = []
        else:
            self.AddressComplete_Interactive_Retrieve_v2_11_Results = AddressComplete_Interactive_Retrieve_v2_11_Results
        self.AddressComplete_Interactive_Retrieve_v2_11_Results_nsprefix_ = "tns"
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AddressComplete_Interactive_Retrieve_v2_11_ArrayOfResults)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AddressComplete_Interactive_Retrieve_v2_11_ArrayOfResults.subclass:
            return AddressComplete_Interactive_Retrieve_v2_11_ArrayOfResults.subclass(*args_, **kwargs_)
        else:
            return AddressComplete_Interactive_Retrieve_v2_11_ArrayOfResults(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_AddressComplete_Interactive_Retrieve_v2_11_Results(self):
        return self.AddressComplete_Interactive_Retrieve_v2_11_Results
    def set_AddressComplete_Interactive_Retrieve_v2_11_Results(self, AddressComplete_Interactive_Retrieve_v2_11_Results):
        self.AddressComplete_Interactive_Retrieve_v2_11_Results = AddressComplete_Interactive_Retrieve_v2_11_Results
    def add_AddressComplete_Interactive_Retrieve_v2_11_Results(self, value):
        self.AddressComplete_Interactive_Retrieve_v2_11_Results.append(value)
    def insert_AddressComplete_Interactive_Retrieve_v2_11_Results_at(self, index, value):
        self.AddressComplete_Interactive_Retrieve_v2_11_Results.insert(index, value)
    def replace_AddressComplete_Interactive_Retrieve_v2_11_Results_at(self, index, value):
        self.AddressComplete_Interactive_Retrieve_v2_11_Results[index] = value
    def _hasContent(self):
        if (
            self.AddressComplete_Interactive_Retrieve_v2_11_Results
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressComplete_Interactive_Retrieve_v2_11_ArrayOfResults', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AddressComplete_Interactive_Retrieve_v2_11_ArrayOfResults')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AddressComplete_Interactive_Retrieve_v2_11_ArrayOfResults':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AddressComplete_Interactive_Retrieve_v2_11_ArrayOfResults')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AddressComplete_Interactive_Retrieve_v2_11_ArrayOfResults', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AddressComplete_Interactive_Retrieve_v2_11_ArrayOfResults'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressComplete_Interactive_Retrieve_v2_11_ArrayOfResults', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for AddressComplete_Interactive_Retrieve_v2_11_Results_ in self.AddressComplete_Interactive_Retrieve_v2_11_Results:
            namespaceprefix_ = self.AddressComplete_Interactive_Retrieve_v2_11_Results_nsprefix_ + ':' if (UseCapturedNS_ and self.AddressComplete_Interactive_Retrieve_v2_11_Results_nsprefix_) else ''
            AddressComplete_Interactive_Retrieve_v2_11_Results_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='AddressComplete_Interactive_Retrieve_v2_11_Results', pretty_print=pretty_print)
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'AddressComplete_Interactive_Retrieve_v2_11_Results':
            obj_ = AddressComplete_Interactive_Retrieve_v2_11_Results.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.AddressComplete_Interactive_Retrieve_v2_11_Results.append(obj_)
            obj_.original_tagname_ = 'AddressComplete_Interactive_Retrieve_v2_11_Results'
# end class AddressComplete_Interactive_Retrieve_v2_11_ArrayOfResults


class AddressComplete_Interactive_Retrieve_v2_11_Results(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, Id=None, DomesticId=None, Language=None, LanguageAlternatives=None, Department=None, Company=None, SubBuilding=None, BuildingNumber=None, BuildingName=None, SecondaryStreet=None, Street=None, Block=None, Neighbourhood=None, District=None, City=None, Line1=None, Line2=None, Line3=None, Line4=None, Line5=None, AdminAreaName=None, AdminAreaCode=None, Province=None, ProvinceName=None, ProvinceCode=None, PostalCode=None, CountryName=None, CountryIso2=None, CountryIso3=None, CountryIsoNumber=None, SortingNumber1=None, SortingNumber2=None, Barcode=None, POBoxNumber=None, Label=None, Type=None, DataLevel=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.Id = Id
        self.Id_nsprefix_ = None
        self.DomesticId = DomesticId
        self.DomesticId_nsprefix_ = None
        self.Language = Language
        self.Language_nsprefix_ = None
        self.LanguageAlternatives = LanguageAlternatives
        self.LanguageAlternatives_nsprefix_ = None
        self.Department = Department
        self.Department_nsprefix_ = None
        self.Company = Company
        self.Company_nsprefix_ = None
        self.SubBuilding = SubBuilding
        self.SubBuilding_nsprefix_ = None
        self.BuildingNumber = BuildingNumber
        self.BuildingNumber_nsprefix_ = None
        self.BuildingName = BuildingName
        self.BuildingName_nsprefix_ = None
        self.SecondaryStreet = SecondaryStreet
        self.SecondaryStreet_nsprefix_ = None
        self.Street = Street
        self.Street_nsprefix_ = None
        self.Block = Block
        self.Block_nsprefix_ = None
        self.Neighbourhood = Neighbourhood
        self.Neighbourhood_nsprefix_ = None
        self.District = District
        self.District_nsprefix_ = None
        self.City = City
        self.City_nsprefix_ = None
        self.Line1 = Line1
        self.Line1_nsprefix_ = None
        self.Line2 = Line2
        self.Line2_nsprefix_ = None
        self.Line3 = Line3
        self.Line3_nsprefix_ = None
        self.Line4 = Line4
        self.Line4_nsprefix_ = None
        self.Line5 = Line5
        self.Line5_nsprefix_ = None
        self.AdminAreaName = AdminAreaName
        self.AdminAreaName_nsprefix_ = None
        self.AdminAreaCode = AdminAreaCode
        self.AdminAreaCode_nsprefix_ = None
        self.Province = Province
        self.Province_nsprefix_ = None
        self.ProvinceName = ProvinceName
        self.ProvinceName_nsprefix_ = None
        self.ProvinceCode = ProvinceCode
        self.ProvinceCode_nsprefix_ = None
        self.PostalCode = PostalCode
        self.PostalCode_nsprefix_ = None
        self.CountryName = CountryName
        self.CountryName_nsprefix_ = None
        self.CountryIso2 = CountryIso2
        self.CountryIso2_nsprefix_ = None
        self.CountryIso3 = CountryIso3
        self.CountryIso3_nsprefix_ = None
        self.CountryIsoNumber = CountryIsoNumber
        self.CountryIsoNumber_nsprefix_ = None
        self.SortingNumber1 = SortingNumber1
        self.SortingNumber1_nsprefix_ = None
        self.SortingNumber2 = SortingNumber2
        self.SortingNumber2_nsprefix_ = None
        self.Barcode = Barcode
        self.Barcode_nsprefix_ = None
        self.POBoxNumber = POBoxNumber
        self.POBoxNumber_nsprefix_ = None
        self.Label = Label
        self.Label_nsprefix_ = None
        self.Type = Type
        self.Type_nsprefix_ = None
        self.DataLevel = DataLevel
        self.DataLevel_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AddressComplete_Interactive_Retrieve_v2_11_Results)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AddressComplete_Interactive_Retrieve_v2_11_Results.subclass:
            return AddressComplete_Interactive_Retrieve_v2_11_Results.subclass(*args_, **kwargs_)
        else:
            return AddressComplete_Interactive_Retrieve_v2_11_Results(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_Id(self):
        return self.Id
    def set_Id(self, Id):
        self.Id = Id
    def get_DomesticId(self):
        return self.DomesticId
    def set_DomesticId(self, DomesticId):
        self.DomesticId = DomesticId
    def get_Language(self):
        return self.Language
    def set_Language(self, Language):
        self.Language = Language
    def get_LanguageAlternatives(self):
        return self.LanguageAlternatives
    def set_LanguageAlternatives(self, LanguageAlternatives):
        self.LanguageAlternatives = LanguageAlternatives
    def get_Department(self):
        return self.Department
    def set_Department(self, Department):
        self.Department = Department
    def get_Company(self):
        return self.Company
    def set_Company(self, Company):
        self.Company = Company
    def get_SubBuilding(self):
        return self.SubBuilding
    def set_SubBuilding(self, SubBuilding):
        self.SubBuilding = SubBuilding
    def get_BuildingNumber(self):
        return self.BuildingNumber
    def set_BuildingNumber(self, BuildingNumber):
        self.BuildingNumber = BuildingNumber
    def get_BuildingName(self):
        return self.BuildingName
    def set_BuildingName(self, BuildingName):
        self.BuildingName = BuildingName
    def get_SecondaryStreet(self):
        return self.SecondaryStreet
    def set_SecondaryStreet(self, SecondaryStreet):
        self.SecondaryStreet = SecondaryStreet
    def get_Street(self):
        return self.Street
    def set_Street(self, Street):
        self.Street = Street
    def get_Block(self):
        return self.Block
    def set_Block(self, Block):
        self.Block = Block
    def get_Neighbourhood(self):
        return self.Neighbourhood
    def set_Neighbourhood(self, Neighbourhood):
        self.Neighbourhood = Neighbourhood
    def get_District(self):
        return self.District
    def set_District(self, District):
        self.District = District
    def get_City(self):
        return self.City
    def set_City(self, City):
        self.City = City
    def get_Line1(self):
        return self.Line1
    def set_Line1(self, Line1):
        self.Line1 = Line1
    def get_Line2(self):
        return self.Line2
    def set_Line2(self, Line2):
        self.Line2 = Line2
    def get_Line3(self):
        return self.Line3
    def set_Line3(self, Line3):
        self.Line3 = Line3
    def get_Line4(self):
        return self.Line4
    def set_Line4(self, Line4):
        self.Line4 = Line4
    def get_Line5(self):
        return self.Line5
    def set_Line5(self, Line5):
        self.Line5 = Line5
    def get_AdminAreaName(self):
        return self.AdminAreaName
    def set_AdminAreaName(self, AdminAreaName):
        self.AdminAreaName = AdminAreaName
    def get_AdminAreaCode(self):
        return self.AdminAreaCode
    def set_AdminAreaCode(self, AdminAreaCode):
        self.AdminAreaCode = AdminAreaCode
    def get_Province(self):
        return self.Province
    def set_Province(self, Province):
        self.Province = Province
    def get_ProvinceName(self):
        return self.ProvinceName
    def set_ProvinceName(self, ProvinceName):
        self.ProvinceName = ProvinceName
    def get_ProvinceCode(self):
        return self.ProvinceCode
    def set_ProvinceCode(self, ProvinceCode):
        self.ProvinceCode = ProvinceCode
    def get_PostalCode(self):
        return self.PostalCode
    def set_PostalCode(self, PostalCode):
        self.PostalCode = PostalCode
    def get_CountryName(self):
        return self.CountryName
    def set_CountryName(self, CountryName):
        self.CountryName = CountryName
    def get_CountryIso2(self):
        return self.CountryIso2
    def set_CountryIso2(self, CountryIso2):
        self.CountryIso2 = CountryIso2
    def get_CountryIso3(self):
        return self.CountryIso3
    def set_CountryIso3(self, CountryIso3):
        self.CountryIso3 = CountryIso3
    def get_CountryIsoNumber(self):
        return self.CountryIsoNumber
    def set_CountryIsoNumber(self, CountryIsoNumber):
        self.CountryIsoNumber = CountryIsoNumber
    def get_SortingNumber1(self):
        return self.SortingNumber1
    def set_SortingNumber1(self, SortingNumber1):
        self.SortingNumber1 = SortingNumber1
    def get_SortingNumber2(self):
        return self.SortingNumber2
    def set_SortingNumber2(self, SortingNumber2):
        self.SortingNumber2 = SortingNumber2
    def get_Barcode(self):
        return self.Barcode
    def set_Barcode(self, Barcode):
        self.Barcode = Barcode
    def get_POBoxNumber(self):
        return self.POBoxNumber
    def set_POBoxNumber(self, POBoxNumber):
        self.POBoxNumber = POBoxNumber
    def get_Label(self):
        return self.Label
    def set_Label(self, Label):
        self.Label = Label
    def get_Type(self):
        return self.Type
    def set_Type(self, Type):
        self.Type = Type
    def get_DataLevel(self):
        return self.DataLevel
    def set_DataLevel(self, DataLevel):
        self.DataLevel = DataLevel
    def _hasContent(self):
        if (
            self.Id is not None or
            self.DomesticId is not None or
            self.Language is not None or
            self.LanguageAlternatives is not None or
            self.Department is not None or
            self.Company is not None or
            self.SubBuilding is not None or
            self.BuildingNumber is not None or
            self.BuildingName is not None or
            self.SecondaryStreet is not None or
            self.Street is not None or
            self.Block is not None or
            self.Neighbourhood is not None or
            self.District is not None or
            self.City is not None or
            self.Line1 is not None or
            self.Line2 is not None or
            self.Line3 is not None or
            self.Line4 is not None or
            self.Line5 is not None or
            self.AdminAreaName is not None or
            self.AdminAreaCode is not None or
            self.Province is not None or
            self.ProvinceName is not None or
            self.ProvinceCode is not None or
            self.PostalCode is not None or
            self.CountryName is not None or
            self.CountryIso2 is not None or
            self.CountryIso3 is not None or
            self.CountryIsoNumber is not None or
            self.SortingNumber1 is not None or
            self.SortingNumber2 is not None or
            self.Barcode is not None or
            self.POBoxNumber is not None or
            self.Label is not None or
            self.Type is not None or
            self.DataLevel is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressComplete_Interactive_Retrieve_v2_11_Results', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AddressComplete_Interactive_Retrieve_v2_11_Results')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AddressComplete_Interactive_Retrieve_v2_11_Results':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AddressComplete_Interactive_Retrieve_v2_11_Results')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AddressComplete_Interactive_Retrieve_v2_11_Results', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AddressComplete_Interactive_Retrieve_v2_11_Results'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AddressComplete_Interactive_Retrieve_v2_11_Results', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.Id is not None:
            namespaceprefix_ = self.Id_nsprefix_ + ':' if (UseCapturedNS_ and self.Id_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sId>%s</%sId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Id), input_name='Id')), namespaceprefix_ , eol_))
        if self.DomesticId is not None:
            namespaceprefix_ = self.DomesticId_nsprefix_ + ':' if (UseCapturedNS_ and self.DomesticId_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDomesticId>%s</%sDomesticId>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DomesticId), input_name='DomesticId')), namespaceprefix_ , eol_))
        if self.Language is not None:
            namespaceprefix_ = self.Language_nsprefix_ + ':' if (UseCapturedNS_ and self.Language_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLanguage>%s</%sLanguage>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Language), input_name='Language')), namespaceprefix_ , eol_))
        if self.LanguageAlternatives is not None:
            namespaceprefix_ = self.LanguageAlternatives_nsprefix_ + ':' if (UseCapturedNS_ and self.LanguageAlternatives_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLanguageAlternatives>%s</%sLanguageAlternatives>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.LanguageAlternatives), input_name='LanguageAlternatives')), namespaceprefix_ , eol_))
        if self.Department is not None:
            namespaceprefix_ = self.Department_nsprefix_ + ':' if (UseCapturedNS_ and self.Department_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDepartment>%s</%sDepartment>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Department), input_name='Department')), namespaceprefix_ , eol_))
        if self.Company is not None:
            namespaceprefix_ = self.Company_nsprefix_ + ':' if (UseCapturedNS_ and self.Company_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCompany>%s</%sCompany>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Company), input_name='Company')), namespaceprefix_ , eol_))
        if self.SubBuilding is not None:
            namespaceprefix_ = self.SubBuilding_nsprefix_ + ':' if (UseCapturedNS_ and self.SubBuilding_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSubBuilding>%s</%sSubBuilding>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SubBuilding), input_name='SubBuilding')), namespaceprefix_ , eol_))
        if self.BuildingNumber is not None:
            namespaceprefix_ = self.BuildingNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.BuildingNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBuildingNumber>%s</%sBuildingNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BuildingNumber), input_name='BuildingNumber')), namespaceprefix_ , eol_))
        if self.BuildingName is not None:
            namespaceprefix_ = self.BuildingName_nsprefix_ + ':' if (UseCapturedNS_ and self.BuildingName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBuildingName>%s</%sBuildingName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.BuildingName), input_name='BuildingName')), namespaceprefix_ , eol_))
        if self.SecondaryStreet is not None:
            namespaceprefix_ = self.SecondaryStreet_nsprefix_ + ':' if (UseCapturedNS_ and self.SecondaryStreet_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSecondaryStreet>%s</%sSecondaryStreet>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SecondaryStreet), input_name='SecondaryStreet')), namespaceprefix_ , eol_))
        if self.Street is not None:
            namespaceprefix_ = self.Street_nsprefix_ + ':' if (UseCapturedNS_ and self.Street_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sStreet>%s</%sStreet>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Street), input_name='Street')), namespaceprefix_ , eol_))
        if self.Block is not None:
            namespaceprefix_ = self.Block_nsprefix_ + ':' if (UseCapturedNS_ and self.Block_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBlock>%s</%sBlock>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Block), input_name='Block')), namespaceprefix_ , eol_))
        if self.Neighbourhood is not None:
            namespaceprefix_ = self.Neighbourhood_nsprefix_ + ':' if (UseCapturedNS_ and self.Neighbourhood_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sNeighbourhood>%s</%sNeighbourhood>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Neighbourhood), input_name='Neighbourhood')), namespaceprefix_ , eol_))
        if self.District is not None:
            namespaceprefix_ = self.District_nsprefix_ + ':' if (UseCapturedNS_ and self.District_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDistrict>%s</%sDistrict>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.District), input_name='District')), namespaceprefix_ , eol_))
        if self.City is not None:
            namespaceprefix_ = self.City_nsprefix_ + ':' if (UseCapturedNS_ and self.City_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCity>%s</%sCity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.City), input_name='City')), namespaceprefix_ , eol_))
        if self.Line1 is not None:
            namespaceprefix_ = self.Line1_nsprefix_ + ':' if (UseCapturedNS_ and self.Line1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLine1>%s</%sLine1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Line1), input_name='Line1')), namespaceprefix_ , eol_))
        if self.Line2 is not None:
            namespaceprefix_ = self.Line2_nsprefix_ + ':' if (UseCapturedNS_ and self.Line2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLine2>%s</%sLine2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Line2), input_name='Line2')), namespaceprefix_ , eol_))
        if self.Line3 is not None:
            namespaceprefix_ = self.Line3_nsprefix_ + ':' if (UseCapturedNS_ and self.Line3_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLine3>%s</%sLine3>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Line3), input_name='Line3')), namespaceprefix_ , eol_))
        if self.Line4 is not None:
            namespaceprefix_ = self.Line4_nsprefix_ + ':' if (UseCapturedNS_ and self.Line4_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLine4>%s</%sLine4>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Line4), input_name='Line4')), namespaceprefix_ , eol_))
        if self.Line5 is not None:
            namespaceprefix_ = self.Line5_nsprefix_ + ':' if (UseCapturedNS_ and self.Line5_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLine5>%s</%sLine5>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Line5), input_name='Line5')), namespaceprefix_ , eol_))
        if self.AdminAreaName is not None:
            namespaceprefix_ = self.AdminAreaName_nsprefix_ + ':' if (UseCapturedNS_ and self.AdminAreaName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAdminAreaName>%s</%sAdminAreaName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AdminAreaName), input_name='AdminAreaName')), namespaceprefix_ , eol_))
        if self.AdminAreaCode is not None:
            namespaceprefix_ = self.AdminAreaCode_nsprefix_ + ':' if (UseCapturedNS_ and self.AdminAreaCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sAdminAreaCode>%s</%sAdminAreaCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.AdminAreaCode), input_name='AdminAreaCode')), namespaceprefix_ , eol_))
        if self.Province is not None:
            namespaceprefix_ = self.Province_nsprefix_ + ':' if (UseCapturedNS_ and self.Province_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProvince>%s</%sProvince>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Province), input_name='Province')), namespaceprefix_ , eol_))
        if self.ProvinceName is not None:
            namespaceprefix_ = self.ProvinceName_nsprefix_ + ':' if (UseCapturedNS_ and self.ProvinceName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProvinceName>%s</%sProvinceName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ProvinceName), input_name='ProvinceName')), namespaceprefix_ , eol_))
        if self.ProvinceCode is not None:
            namespaceprefix_ = self.ProvinceCode_nsprefix_ + ':' if (UseCapturedNS_ and self.ProvinceCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sProvinceCode>%s</%sProvinceCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.ProvinceCode), input_name='ProvinceCode')), namespaceprefix_ , eol_))
        if self.PostalCode is not None:
            namespaceprefix_ = self.PostalCode_nsprefix_ + ':' if (UseCapturedNS_ and self.PostalCode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPostalCode>%s</%sPostalCode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.PostalCode), input_name='PostalCode')), namespaceprefix_ , eol_))
        if self.CountryName is not None:
            namespaceprefix_ = self.CountryName_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryName_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryName>%s</%sCountryName>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryName), input_name='CountryName')), namespaceprefix_ , eol_))
        if self.CountryIso2 is not None:
            namespaceprefix_ = self.CountryIso2_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryIso2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryIso2>%s</%sCountryIso2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryIso2), input_name='CountryIso2')), namespaceprefix_ , eol_))
        if self.CountryIso3 is not None:
            namespaceprefix_ = self.CountryIso3_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryIso3_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryIso3>%s</%sCountryIso3>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.CountryIso3), input_name='CountryIso3')), namespaceprefix_ , eol_))
        if self.CountryIsoNumber is not None:
            namespaceprefix_ = self.CountryIsoNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.CountryIsoNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sCountryIsoNumber>%s</%sCountryIsoNumber>%s' % (namespaceprefix_ , self.gds_format_integer(self.CountryIsoNumber, input_name='CountryIsoNumber'), namespaceprefix_ , eol_))
        if self.SortingNumber1 is not None:
            namespaceprefix_ = self.SortingNumber1_nsprefix_ + ':' if (UseCapturedNS_ and self.SortingNumber1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSortingNumber1>%s</%sSortingNumber1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SortingNumber1), input_name='SortingNumber1')), namespaceprefix_ , eol_))
        if self.SortingNumber2 is not None:
            namespaceprefix_ = self.SortingNumber2_nsprefix_ + ':' if (UseCapturedNS_ and self.SortingNumber2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sSortingNumber2>%s</%sSortingNumber2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.SortingNumber2), input_name='SortingNumber2')), namespaceprefix_ , eol_))
        if self.Barcode is not None:
            namespaceprefix_ = self.Barcode_nsprefix_ + ':' if (UseCapturedNS_ and self.Barcode_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sBarcode>%s</%sBarcode>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Barcode), input_name='Barcode')), namespaceprefix_ , eol_))
        if self.POBoxNumber is not None:
            namespaceprefix_ = self.POBoxNumber_nsprefix_ + ':' if (UseCapturedNS_ and self.POBoxNumber_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sPOBoxNumber>%s</%sPOBoxNumber>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.POBoxNumber), input_name='POBoxNumber')), namespaceprefix_ , eol_))
        if self.Label is not None:
            namespaceprefix_ = self.Label_nsprefix_ + ':' if (UseCapturedNS_ and self.Label_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sLabel>%s</%sLabel>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Label), input_name='Label')), namespaceprefix_ , eol_))
        if self.Type is not None:
            namespaceprefix_ = self.Type_nsprefix_ + ':' if (UseCapturedNS_ and self.Type_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sType>%s</%sType>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.Type), input_name='Type')), namespaceprefix_ , eol_))
        if self.DataLevel is not None:
            namespaceprefix_ = self.DataLevel_nsprefix_ + ':' if (UseCapturedNS_ and self.DataLevel_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sDataLevel>%s</%sDataLevel>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.DataLevel), input_name='DataLevel')), namespaceprefix_ , eol_))
    def build(self, node, gds_collector_=None):
        self.gds_collector_ = gds_collector_
        if SaveElementTreeNode:
            self.gds_elementtree_node_ = node
        already_processed = set()
        self.ns_prefix_ = node.prefix
        self._buildAttributes(node, node.attrib, already_processed)
        for child in node:
            nodeName_ = Tag_pattern_.match(child.tag).groups()[-1]
            self._buildChildren(child, node, nodeName_, gds_collector_=gds_collector_)
        return self
    def _buildAttributes(self, node, attrs, already_processed):
        pass
    def _buildChildren(self, child_, node, nodeName_, fromsubclass_=False, gds_collector_=None):
        if nodeName_ == 'Id':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Id')
            value_ = self.gds_validate_string(value_, node, 'Id')
            self.Id = value_
            self.Id_nsprefix_ = child_.prefix
        elif nodeName_ == 'DomesticId':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DomesticId')
            value_ = self.gds_validate_string(value_, node, 'DomesticId')
            self.DomesticId = value_
            self.DomesticId_nsprefix_ = child_.prefix
        elif nodeName_ == 'Language':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Language')
            value_ = self.gds_validate_string(value_, node, 'Language')
            self.Language = value_
            self.Language_nsprefix_ = child_.prefix
        elif nodeName_ == 'LanguageAlternatives':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'LanguageAlternatives')
            value_ = self.gds_validate_string(value_, node, 'LanguageAlternatives')
            self.LanguageAlternatives = value_
            self.LanguageAlternatives_nsprefix_ = child_.prefix
        elif nodeName_ == 'Department':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Department')
            value_ = self.gds_validate_string(value_, node, 'Department')
            self.Department = value_
            self.Department_nsprefix_ = child_.prefix
        elif nodeName_ == 'Company':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Company')
            value_ = self.gds_validate_string(value_, node, 'Company')
            self.Company = value_
            self.Company_nsprefix_ = child_.prefix
        elif nodeName_ == 'SubBuilding':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SubBuilding')
            value_ = self.gds_validate_string(value_, node, 'SubBuilding')
            self.SubBuilding = value_
            self.SubBuilding_nsprefix_ = child_.prefix
        elif nodeName_ == 'BuildingNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BuildingNumber')
            value_ = self.gds_validate_string(value_, node, 'BuildingNumber')
            self.BuildingNumber = value_
            self.BuildingNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'BuildingName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'BuildingName')
            value_ = self.gds_validate_string(value_, node, 'BuildingName')
            self.BuildingName = value_
            self.BuildingName_nsprefix_ = child_.prefix
        elif nodeName_ == 'SecondaryStreet':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SecondaryStreet')
            value_ = self.gds_validate_string(value_, node, 'SecondaryStreet')
            self.SecondaryStreet = value_
            self.SecondaryStreet_nsprefix_ = child_.prefix
        elif nodeName_ == 'Street':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Street')
            value_ = self.gds_validate_string(value_, node, 'Street')
            self.Street = value_
            self.Street_nsprefix_ = child_.prefix
        elif nodeName_ == 'Block':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Block')
            value_ = self.gds_validate_string(value_, node, 'Block')
            self.Block = value_
            self.Block_nsprefix_ = child_.prefix
        elif nodeName_ == 'Neighbourhood':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Neighbourhood')
            value_ = self.gds_validate_string(value_, node, 'Neighbourhood')
            self.Neighbourhood = value_
            self.Neighbourhood_nsprefix_ = child_.prefix
        elif nodeName_ == 'District':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'District')
            value_ = self.gds_validate_string(value_, node, 'District')
            self.District = value_
            self.District_nsprefix_ = child_.prefix
        elif nodeName_ == 'City':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'City')
            value_ = self.gds_validate_string(value_, node, 'City')
            self.City = value_
            self.City_nsprefix_ = child_.prefix
        elif nodeName_ == 'Line1':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Line1')
            value_ = self.gds_validate_string(value_, node, 'Line1')
            self.Line1 = value_
            self.Line1_nsprefix_ = child_.prefix
        elif nodeName_ == 'Line2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Line2')
            value_ = self.gds_validate_string(value_, node, 'Line2')
            self.Line2 = value_
            self.Line2_nsprefix_ = child_.prefix
        elif nodeName_ == 'Line3':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Line3')
            value_ = self.gds_validate_string(value_, node, 'Line3')
            self.Line3 = value_
            self.Line3_nsprefix_ = child_.prefix
        elif nodeName_ == 'Line4':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Line4')
            value_ = self.gds_validate_string(value_, node, 'Line4')
            self.Line4 = value_
            self.Line4_nsprefix_ = child_.prefix
        elif nodeName_ == 'Line5':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Line5')
            value_ = self.gds_validate_string(value_, node, 'Line5')
            self.Line5 = value_
            self.Line5_nsprefix_ = child_.prefix
        elif nodeName_ == 'AdminAreaName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AdminAreaName')
            value_ = self.gds_validate_string(value_, node, 'AdminAreaName')
            self.AdminAreaName = value_
            self.AdminAreaName_nsprefix_ = child_.prefix
        elif nodeName_ == 'AdminAreaCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'AdminAreaCode')
            value_ = self.gds_validate_string(value_, node, 'AdminAreaCode')
            self.AdminAreaCode = value_
            self.AdminAreaCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'Province':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Province')
            value_ = self.gds_validate_string(value_, node, 'Province')
            self.Province = value_
            self.Province_nsprefix_ = child_.prefix
        elif nodeName_ == 'ProvinceName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ProvinceName')
            value_ = self.gds_validate_string(value_, node, 'ProvinceName')
            self.ProvinceName = value_
            self.ProvinceName_nsprefix_ = child_.prefix
        elif nodeName_ == 'ProvinceCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'ProvinceCode')
            value_ = self.gds_validate_string(value_, node, 'ProvinceCode')
            self.ProvinceCode = value_
            self.ProvinceCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'PostalCode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'PostalCode')
            value_ = self.gds_validate_string(value_, node, 'PostalCode')
            self.PostalCode = value_
            self.PostalCode_nsprefix_ = child_.prefix
        elif nodeName_ == 'CountryName':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryName')
            value_ = self.gds_validate_string(value_, node, 'CountryName')
            self.CountryName = value_
            self.CountryName_nsprefix_ = child_.prefix
        elif nodeName_ == 'CountryIso2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryIso2')
            value_ = self.gds_validate_string(value_, node, 'CountryIso2')
            self.CountryIso2 = value_
            self.CountryIso2_nsprefix_ = child_.prefix
        elif nodeName_ == 'CountryIso3':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'CountryIso3')
            value_ = self.gds_validate_string(value_, node, 'CountryIso3')
            self.CountryIso3 = value_
            self.CountryIso3_nsprefix_ = child_.prefix
        elif nodeName_ == 'CountryIsoNumber' and child_.text:
            sval_ = child_.text
            ival_ = self.gds_parse_integer(sval_, node, 'CountryIsoNumber')
            ival_ = self.gds_validate_integer(ival_, node, 'CountryIsoNumber')
            self.CountryIsoNumber = ival_
            self.CountryIsoNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'SortingNumber1':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SortingNumber1')
            value_ = self.gds_validate_string(value_, node, 'SortingNumber1')
            self.SortingNumber1 = value_
            self.SortingNumber1_nsprefix_ = child_.prefix
        elif nodeName_ == 'SortingNumber2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'SortingNumber2')
            value_ = self.gds_validate_string(value_, node, 'SortingNumber2')
            self.SortingNumber2 = value_
            self.SortingNumber2_nsprefix_ = child_.prefix
        elif nodeName_ == 'Barcode':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Barcode')
            value_ = self.gds_validate_string(value_, node, 'Barcode')
            self.Barcode = value_
            self.Barcode_nsprefix_ = child_.prefix
        elif nodeName_ == 'POBoxNumber':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'POBoxNumber')
            value_ = self.gds_validate_string(value_, node, 'POBoxNumber')
            self.POBoxNumber = value_
            self.POBoxNumber_nsprefix_ = child_.prefix
        elif nodeName_ == 'Label':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Label')
            value_ = self.gds_validate_string(value_, node, 'Label')
            self.Label = value_
            self.Label_nsprefix_ = child_.prefix
        elif nodeName_ == 'Type':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'Type')
            value_ = self.gds_validate_string(value_, node, 'Type')
            self.Type = value_
            self.Type_nsprefix_ = child_.prefix
        elif nodeName_ == 'DataLevel':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'DataLevel')
            value_ = self.gds_validate_string(value_, node, 'DataLevel')
            self.DataLevel = value_
            self.DataLevel_nsprefix_ = child_.prefix
# end class AddressComplete_Interactive_Retrieve_v2_11_Results


GDSClassesMapping = {
}


USAGE_TEXT = """
Usage: python <Parser>.py [ -s ] <in_xml_file>
"""


def usage():
    print(USAGE_TEXT)
    sys.exit(1)


def get_root_tag(node):
    tag = Tag_pattern_.match(node.tag).groups()[-1]
    rootClass = GDSClassesMapping.get(tag)
    if rootClass is None:
        rootClass = globals().get(tag)
    return tag, rootClass


def get_required_ns_prefix_defs(rootNode):
    '''Get all name space prefix definitions required in this XML doc.
    Return a dictionary of definitions and a char string of definitions.
    '''
    nsmap = {
        prefix: uri
        for node in rootNode.iter()
        for (prefix, uri) in node.nsmap.items()
        if prefix is not None
    }
    namespacedefs = ' '.join([
        'xmlns:{}="{}"'.format(prefix, uri)
        for prefix, uri in nsmap.items()
    ])
    return nsmap, namespacedefs


def parse(inFileName, silence=False, print_warnings=True):
    global CapturedNsmap_
    gds_collector = GdsCollector_()
    parser = None
    doc = parsexml_(inFileName, parser)
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'AddressComplete_Interactive_Retrieve_v2_11'
        rootClass = AddressComplete_Interactive_Retrieve_v2_11
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    CapturedNsmap_, namespacedefs = get_required_ns_prefix_defs(rootNode)
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_=namespacedefs,
            pretty_print=True)
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def parseEtree(inFileName, silence=False, print_warnings=True,
               mapping=None, nsmap=None):
    parser = None
    doc = parsexml_(inFileName, parser)
    gds_collector = GdsCollector_()
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'AddressComplete_Interactive_Retrieve_v2_11'
        rootClass = AddressComplete_Interactive_Retrieve_v2_11
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if mapping is None:
        mapping = {}
    rootElement = rootObj.to_etree(
        None, name_=rootTag, mapping_=mapping, nsmap_=nsmap)
    reverse_mapping = rootObj.gds_reverse_node_mapping(mapping)
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        content = etree_.tostring(
            rootElement, pretty_print=True,
            xml_declaration=True, encoding="utf-8")
        sys.stdout.write(str(content))
        sys.stdout.write('\n')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj, rootElement, mapping, reverse_mapping


def parseString(inString, silence=False, print_warnings=True):
    '''Parse a string, create the object tree, and export it.

    Arguments:
    - inString -- A string.  This XML fragment should not start
      with an XML declaration containing an encoding.
    - silence -- A boolean.  If False, export the object.
    Returns -- The root object in the tree.
    '''
    parser = None
    rootNode= parsexmlstring_(inString, parser)
    gds_collector = GdsCollector_()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'AddressComplete_Interactive_Retrieve_v2_11'
        rootClass = AddressComplete_Interactive_Retrieve_v2_11
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='xmlns:tns="http://ws1.postescanada-canadapost.ca/"')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def parseLiteral(inFileName, silence=False, print_warnings=True):
    parser = None
    doc = parsexml_(inFileName, parser)
    gds_collector = GdsCollector_()
    rootNode = doc.getroot()
    rootTag, rootClass = get_root_tag(rootNode)
    if rootClass is None:
        rootTag = 'AddressComplete_Interactive_Retrieve_v2_11'
        rootClass = AddressComplete_Interactive_Retrieve_v2_11
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from address_complete_retrieve import *\n\n')
        sys.stdout.write('import address_complete_retrieve as model_\n\n')
        sys.stdout.write('rootObj = model_.rootClass(\n')
        rootObj.exportLiteral(sys.stdout, 0, name_=rootTag)
        sys.stdout.write(')\n')
    if print_warnings and len(gds_collector.get_messages()) > 0:
        separator = ('-' * 50) + '\n'
        sys.stderr.write(separator)
        sys.stderr.write('----- Warnings -- count: {} -----\n'.format(
            len(gds_collector.get_messages()), ))
        gds_collector.write_messages(sys.stderr)
        sys.stderr.write(separator)
    return rootObj


def main():
    args = sys.argv[1:]
    if len(args) == 1:
        parse(args[0])
    else:
        usage()


if __name__ == '__main__':
    #import pdb; pdb.set_trace()
    main()

RenameMappings_ = {
}

#
# Mapping of namespaces to types defined in them
# and the file in which each is defined.
# simpleTypes are marked "ST" and complexTypes "CT".
NamespaceToDefMappings_ = {'http://ws1.postescanada-canadapost.ca/': [('AddressComplete_Interactive_Retrieve_v2_11_ArrayOfResults',
                                             './schemas/address_complete_retrieve.xsd',
                                             'CT'),
                                            ('AddressComplete_Interactive_Retrieve_v2_11_Results',
                                             './schemas/address_complete_retrieve.xsd',
                                             'CT')]}

__all__ = [
    "AddressComplete_Interactive_Retrieve_v2_11",
    "AddressComplete_Interactive_Retrieve_v2_11_ArrayOfResults",
    "AddressComplete_Interactive_Retrieve_v2_11_Response",
    "AddressComplete_Interactive_Retrieve_v2_11_Results"
]
