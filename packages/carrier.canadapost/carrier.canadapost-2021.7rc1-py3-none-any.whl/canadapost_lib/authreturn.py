#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
# Generated Wed Jul 14 14:59:25 2021 by generateDS.py version 2.39.2.
# Python 3.8.6 (v3.8.6:db455296be, Sep 23 2020, 13:31:39)  [Clang 6.0 (clang-600.0.57)]
#
# Command line options:
#   ('--no-namespace-defs', '')
#   ('-o', './canadapost_lib/authreturn.py')
#
# Command line arguments:
#   ./schemas/authreturn.xsd
#
# Command line:
#   /Users/danielkobina/Workspace/project/purplship-carriers/.venv/purplship-carriers/bin/generateDS --no-namespace-defs -o "./canadapost_lib/authreturn.py" ./schemas/authreturn.xsd
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


class RelType(str, Enum):
    RETURN_LABEL='returnLabel'


class email_subjectType(str, Enum):
    TRACKING='tracking'
    CUSTOMERREF_1='customer-ref-1'
    CUSTOMERREF_2='customer-ref-2'


class encodingType(str, Enum):
    PDF='PDF'
    ZPL='ZPL'


class output_formatType(str, Enum):
    _8_5_X_11='8.5x11'
    _4_X_6='4x6'
    _3_X_5='3x5'


class AuthorizedReturnInfoType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, tracking_pin=None, public_key_info=None, links=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.tracking_pin = tracking_pin
        self.validate_TrackingPINType(self.tracking_pin)
        self.tracking_pin_nsprefix_ = None
        self.public_key_info = public_key_info
        self.public_key_info_nsprefix_ = None
        self.links = links
        self.links_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AuthorizedReturnInfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AuthorizedReturnInfoType.subclass:
            return AuthorizedReturnInfoType.subclass(*args_, **kwargs_)
        else:
            return AuthorizedReturnInfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_tracking_pin(self):
        return self.tracking_pin
    def set_tracking_pin(self, tracking_pin):
        self.tracking_pin = tracking_pin
    def get_public_key_info(self):
        return self.public_key_info
    def set_public_key_info(self, public_key_info):
        self.public_key_info = public_key_info
    def get_links(self):
        return self.links
    def set_links(self, links):
        self.links = links
    def validate_TrackingPINType(self, value):
        result = True
        # Validate type TrackingPINType, a restriction on xsd:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 16:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on TrackingPINType' % {"value": value, "lineno": lineno} )
                result = False
            if len(value) < 11:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on TrackingPINType' % {"value" : value, "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.tracking_pin is not None or
            self.public_key_info is not None or
            self.links is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AuthorizedReturnInfoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AuthorizedReturnInfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AuthorizedReturnInfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AuthorizedReturnInfoType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AuthorizedReturnInfoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AuthorizedReturnInfoType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AuthorizedReturnInfoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.tracking_pin is not None:
            namespaceprefix_ = self.tracking_pin_nsprefix_ + ':' if (UseCapturedNS_ and self.tracking_pin_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%stracking-pin>%s</%stracking-pin>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.tracking_pin), input_name='tracking-pin')), namespaceprefix_ , eol_))
        if self.public_key_info is not None:
            namespaceprefix_ = self.public_key_info_nsprefix_ + ':' if (UseCapturedNS_ and self.public_key_info_nsprefix_) else ''
            self.public_key_info.export(outfile, level, namespaceprefix_, namespacedef_='', name_='public-key-info', pretty_print=pretty_print)
        if self.links is not None:
            namespaceprefix_ = self.links_nsprefix_ + ':' if (UseCapturedNS_ and self.links_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slinks>%s</%slinks>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.links), input_name='links')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'tracking-pin':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'tracking_pin')
            value_ = self.gds_validate_string(value_, node, 'tracking_pin')
            self.tracking_pin = value_
            self.tracking_pin_nsprefix_ = child_.prefix
            # validate type TrackingPINType
            self.validate_TrackingPINType(self.tracking_pin)
        elif nodeName_ == 'public-key-info':
            obj_ = PublicKeyInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.public_key_info = obj_
            obj_.original_tagname_ = 'public-key-info'
        elif nodeName_ == 'links':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'links')
            value_ = self.gds_validate_string(value_, node, 'links')
            self.links = value_
            self.links_nsprefix_ = child_.prefix
# end class AuthorizedReturnInfoType


class PublicKeyInfoType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, expiry_date=None, url=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if isinstance(expiry_date, BaseStrType_):
            initvalue_ = datetime_.datetime.strptime(expiry_date, '%Y-%m-%dT%H:%M:%S')
        else:
            initvalue_ = expiry_date
        self.expiry_date = initvalue_
        self.expiry_date_nsprefix_ = None
        self.url = url
        self.url_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PublicKeyInfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PublicKeyInfoType.subclass:
            return PublicKeyInfoType.subclass(*args_, **kwargs_)
        else:
            return PublicKeyInfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_expiry_date(self):
        return self.expiry_date
    def set_expiry_date(self, expiry_date):
        self.expiry_date = expiry_date
    def get_url(self):
        return self.url
    def set_url(self, url):
        self.url = url
    def _hasContent(self):
        if (
            self.expiry_date is not None or
            self.url is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PublicKeyInfoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PublicKeyInfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PublicKeyInfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PublicKeyInfoType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PublicKeyInfoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PublicKeyInfoType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PublicKeyInfoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.expiry_date is not None:
            namespaceprefix_ = self.expiry_date_nsprefix_ + ':' if (UseCapturedNS_ and self.expiry_date_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sexpiry-date>%s</%sexpiry-date>%s' % (namespaceprefix_ , self.gds_format_datetime(self.expiry_date, input_name='expiry-date'), namespaceprefix_ , eol_))
        if self.url is not None:
            namespaceprefix_ = self.url_nsprefix_ + ':' if (UseCapturedNS_ and self.url_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%surl>%s</%surl>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.url), input_name='url')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'expiry-date':
            sval_ = child_.text
            dval_ = self.gds_parse_datetime(sval_)
            self.expiry_date = dval_
            self.expiry_date_nsprefix_ = child_.prefix
        elif nodeName_ == 'url':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'url')
            value_ = self.gds_validate_string(value_, node, 'url')
            self.url = value_
            self.url_nsprefix_ = child_.prefix
# end class PublicKeyInfoType


class AuthorizedReturnType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, create_public_key=None, service_code=None, returner=None, receiver=None, parcel_characteristics=None, print_preferences=None, settlement_info=None, references=None, notifications=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.create_public_key = create_public_key
        self.validate_create_public_keyType(self.create_public_key)
        self.create_public_key_nsprefix_ = None
        self.service_code = service_code
        self.service_code_nsprefix_ = None
        self.returner = returner
        self.returner_nsprefix_ = None
        self.receiver = receiver
        self.receiver_nsprefix_ = None
        self.parcel_characteristics = parcel_characteristics
        self.parcel_characteristics_nsprefix_ = None
        self.print_preferences = print_preferences
        self.print_preferences_nsprefix_ = None
        self.settlement_info = settlement_info
        self.settlement_info_nsprefix_ = None
        self.references = references
        self.references_nsprefix_ = None
        self.notifications = notifications
        self.notifications_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AuthorizedReturnType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AuthorizedReturnType.subclass:
            return AuthorizedReturnType.subclass(*args_, **kwargs_)
        else:
            return AuthorizedReturnType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_create_public_key(self):
        return self.create_public_key
    def set_create_public_key(self, create_public_key):
        self.create_public_key = create_public_key
    def get_service_code(self):
        return self.service_code
    def set_service_code(self, service_code):
        self.service_code = service_code
    def get_returner(self):
        return self.returner
    def set_returner(self, returner):
        self.returner = returner
    def get_receiver(self):
        return self.receiver
    def set_receiver(self, receiver):
        self.receiver = receiver
    def get_parcel_characteristics(self):
        return self.parcel_characteristics
    def set_parcel_characteristics(self, parcel_characteristics):
        self.parcel_characteristics = parcel_characteristics
    def get_print_preferences(self):
        return self.print_preferences
    def set_print_preferences(self, print_preferences):
        self.print_preferences = print_preferences
    def get_settlement_info(self):
        return self.settlement_info
    def set_settlement_info(self, settlement_info):
        self.settlement_info = settlement_info
    def get_references(self):
        return self.references
    def set_references(self, references):
        self.references = references
    def get_notifications(self):
        return self.notifications
    def set_notifications(self, notifications):
        self.notifications = notifications
    def validate_create_public_keyType(self, value):
        result = True
        # Validate type create-public-keyType, a restriction on xsd:boolean.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not self.gds_validate_simple_patterns(
                    self.validate_create_public_keyType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_create_public_keyType_patterns_, ))
                result = False
        return result
    validate_create_public_keyType_patterns_ = [['^(true)$']]
    def _hasContent(self):
        if (
            self.create_public_key is not None or
            self.service_code is not None or
            self.returner is not None or
            self.receiver is not None or
            self.parcel_characteristics is not None or
            self.print_preferences is not None or
            self.settlement_info is not None or
            self.references is not None or
            self.notifications is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AuthorizedReturnType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AuthorizedReturnType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AuthorizedReturnType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AuthorizedReturnType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AuthorizedReturnType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AuthorizedReturnType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AuthorizedReturnType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.create_public_key is not None:
            namespaceprefix_ = self.create_public_key_nsprefix_ + ':' if (UseCapturedNS_ and self.create_public_key_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%screate-public-key>%s</%screate-public-key>%s' % (namespaceprefix_ , self.gds_format_boolean(self.create_public_key, input_name='create-public-key'), namespaceprefix_ , eol_))
        if self.service_code is not None:
            namespaceprefix_ = self.service_code_nsprefix_ + ':' if (UseCapturedNS_ and self.service_code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sservice-code>%s</%sservice-code>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.service_code), input_name='service-code')), namespaceprefix_ , eol_))
        if self.returner is not None:
            namespaceprefix_ = self.returner_nsprefix_ + ':' if (UseCapturedNS_ and self.returner_nsprefix_) else ''
            self.returner.export(outfile, level, namespaceprefix_, namespacedef_='', name_='returner', pretty_print=pretty_print)
        if self.receiver is not None:
            namespaceprefix_ = self.receiver_nsprefix_ + ':' if (UseCapturedNS_ and self.receiver_nsprefix_) else ''
            self.receiver.export(outfile, level, namespaceprefix_, namespacedef_='', name_='receiver', pretty_print=pretty_print)
        if self.parcel_characteristics is not None:
            namespaceprefix_ = self.parcel_characteristics_nsprefix_ + ':' if (UseCapturedNS_ and self.parcel_characteristics_nsprefix_) else ''
            self.parcel_characteristics.export(outfile, level, namespaceprefix_, namespacedef_='', name_='parcel-characteristics', pretty_print=pretty_print)
        if self.print_preferences is not None:
            namespaceprefix_ = self.print_preferences_nsprefix_ + ':' if (UseCapturedNS_ and self.print_preferences_nsprefix_) else ''
            self.print_preferences.export(outfile, level, namespaceprefix_, namespacedef_='', name_='print-preferences', pretty_print=pretty_print)
        if self.settlement_info is not None:
            namespaceprefix_ = self.settlement_info_nsprefix_ + ':' if (UseCapturedNS_ and self.settlement_info_nsprefix_) else ''
            self.settlement_info.export(outfile, level, namespaceprefix_, namespacedef_='', name_='settlement-info', pretty_print=pretty_print)
        if self.references is not None:
            namespaceprefix_ = self.references_nsprefix_ + ':' if (UseCapturedNS_ and self.references_nsprefix_) else ''
            self.references.export(outfile, level, namespaceprefix_, namespacedef_='', name_='references', pretty_print=pretty_print)
        if self.notifications is not None:
            namespaceprefix_ = self.notifications_nsprefix_ + ':' if (UseCapturedNS_ and self.notifications_nsprefix_) else ''
            self.notifications.export(outfile, level, namespaceprefix_, namespacedef_='', name_='notifications', pretty_print=pretty_print)
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
        if nodeName_ == 'create-public-key':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'create_public_key')
            ival_ = self.gds_validate_boolean(ival_, node, 'create_public_key')
            self.create_public_key = ival_
            self.create_public_key_nsprefix_ = child_.prefix
            # validate type create-public-keyType
            self.validate_create_public_keyType(self.create_public_key)
        elif nodeName_ == 'service-code':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'service_code')
            value_ = self.gds_validate_string(value_, node, 'service_code')
            self.service_code = value_
            self.service_code_nsprefix_ = child_.prefix
        elif nodeName_ == 'returner':
            obj_ = ReturnerType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.returner = obj_
            obj_.original_tagname_ = 'returner'
        elif nodeName_ == 'receiver':
            obj_ = ReceiverType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.receiver = obj_
            obj_.original_tagname_ = 'receiver'
        elif nodeName_ == 'parcel-characteristics':
            obj_ = ParcelCharacteristicsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.parcel_characteristics = obj_
            obj_.original_tagname_ = 'parcel-characteristics'
        elif nodeName_ == 'print-preferences':
            obj_ = PrintPreferencesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.print_preferences = obj_
            obj_.original_tagname_ = 'print-preferences'
        elif nodeName_ == 'settlement-info':
            obj_ = AuthSettlementInfoType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.settlement_info = obj_
            obj_.original_tagname_ = 'settlement-info'
        elif nodeName_ == 'references':
            obj_ = ReferencesType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.references = obj_
            obj_.original_tagname_ = 'references'
        elif nodeName_ == 'notifications':
            obj_ = NotificationsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.notifications = obj_
            obj_.original_tagname_ = 'notifications'
# end class AuthorizedReturnType


class AuthSettlementInfoType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, paid_by_customer=None, contract_id=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.paid_by_customer = paid_by_customer
        self.paid_by_customer_nsprefix_ = None
        self.contract_id = contract_id
        self.contract_id_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, AuthSettlementInfoType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if AuthSettlementInfoType.subclass:
            return AuthSettlementInfoType.subclass(*args_, **kwargs_)
        else:
            return AuthSettlementInfoType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_paid_by_customer(self):
        return self.paid_by_customer
    def set_paid_by_customer(self, paid_by_customer):
        self.paid_by_customer = paid_by_customer
    def get_contract_id(self):
        return self.contract_id
    def set_contract_id(self, contract_id):
        self.contract_id = contract_id
    def _hasContent(self):
        if (
            self.paid_by_customer is not None or
            self.contract_id is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AuthSettlementInfoType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('AuthSettlementInfoType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'AuthSettlementInfoType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='AuthSettlementInfoType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='AuthSettlementInfoType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='AuthSettlementInfoType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='AuthSettlementInfoType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.paid_by_customer is not None:
            namespaceprefix_ = self.paid_by_customer_nsprefix_ + ':' if (UseCapturedNS_ and self.paid_by_customer_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spaid-by-customer>%s</%spaid-by-customer>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.paid_by_customer), input_name='paid-by-customer')), namespaceprefix_ , eol_))
        if self.contract_id is not None:
            namespaceprefix_ = self.contract_id_nsprefix_ + ':' if (UseCapturedNS_ and self.contract_id_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scontract-id>%s</%scontract-id>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.contract_id), input_name='contract-id')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'paid-by-customer':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'paid_by_customer')
            value_ = self.gds_validate_string(value_, node, 'paid_by_customer')
            self.paid_by_customer = value_
            self.paid_by_customer_nsprefix_ = child_.prefix
        elif nodeName_ == 'contract-id':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'contract_id')
            value_ = self.gds_validate_string(value_, node, 'contract_id')
            self.contract_id = value_
            self.contract_id_nsprefix_ = child_.prefix
# end class AuthSettlementInfoType


class ReturnerType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, name=None, company=None, domestic_address=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.name = name
        self.validate_ContactNameType(self.name)
        self.name_nsprefix_ = None
        self.company = company
        self.validate_CompanyNameType(self.company)
        self.company_nsprefix_ = None
        self.domestic_address = domestic_address
        self.domestic_address_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ReturnerType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ReturnerType.subclass:
            return ReturnerType.subclass(*args_, **kwargs_)
        else:
            return ReturnerType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_company(self):
        return self.company
    def set_company(self, company):
        self.company = company
    def get_domestic_address(self):
        return self.domestic_address
    def set_domestic_address(self, domestic_address):
        self.domestic_address = domestic_address
    def validate_ContactNameType(self, value):
        result = True
        # Validate type ContactNameType, a restriction on xsd:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 44:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ContactNameType' % {"value": value, "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on ContactNameType' % {"value" : value, "lineno": lineno} )
                result = False
        return result
    def validate_CompanyNameType(self, value):
        result = True
        # Validate type CompanyNameType, a restriction on xsd:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 44:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on CompanyNameType' % {"value": value, "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on CompanyNameType' % {"value" : value, "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.name is not None or
            self.company is not None or
            self.domestic_address is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReturnerType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ReturnerType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ReturnerType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ReturnerType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ReturnerType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ReturnerType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReturnerType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.name is not None:
            namespaceprefix_ = self.name_nsprefix_ + ':' if (UseCapturedNS_ and self.name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sname>%s</%sname>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.name), input_name='name')), namespaceprefix_ , eol_))
        if self.company is not None:
            namespaceprefix_ = self.company_nsprefix_ + ':' if (UseCapturedNS_ and self.company_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scompany>%s</%scompany>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.company), input_name='company')), namespaceprefix_ , eol_))
        if self.domestic_address is not None:
            namespaceprefix_ = self.domestic_address_nsprefix_ + ':' if (UseCapturedNS_ and self.domestic_address_nsprefix_) else ''
            self.domestic_address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='domestic-address', pretty_print=pretty_print)
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
        if nodeName_ == 'name':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'name')
            value_ = self.gds_validate_string(value_, node, 'name')
            self.name = value_
            self.name_nsprefix_ = child_.prefix
            # validate type ContactNameType
            self.validate_ContactNameType(self.name)
        elif nodeName_ == 'company':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'company')
            value_ = self.gds_validate_string(value_, node, 'company')
            self.company = value_
            self.company_nsprefix_ = child_.prefix
            # validate type CompanyNameType
            self.validate_CompanyNameType(self.company)
        elif nodeName_ == 'domestic-address':
            obj_ = DomesticAddressDetailsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.domestic_address = obj_
            obj_.original_tagname_ = 'domestic-address'
# end class ReturnerType


class ReceiverType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, name=None, company=None, email=None, receiver_voice_number=None, domestic_address=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.name = name
        self.validate_ContactNameType(self.name)
        self.name_nsprefix_ = None
        self.company = company
        self.validate_CompanyNameType(self.company)
        self.company_nsprefix_ = None
        self.email = email
        self.validate_EmailType(self.email)
        self.email_nsprefix_ = None
        self.receiver_voice_number = receiver_voice_number
        self.receiver_voice_number_nsprefix_ = None
        self.domestic_address = domestic_address
        self.domestic_address_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ReceiverType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ReceiverType.subclass:
            return ReceiverType.subclass(*args_, **kwargs_)
        else:
            return ReceiverType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_name(self):
        return self.name
    def set_name(self, name):
        self.name = name
    def get_company(self):
        return self.company
    def set_company(self, company):
        self.company = company
    def get_email(self):
        return self.email
    def set_email(self, email):
        self.email = email
    def get_receiver_voice_number(self):
        return self.receiver_voice_number
    def set_receiver_voice_number(self, receiver_voice_number):
        self.receiver_voice_number = receiver_voice_number
    def get_domestic_address(self):
        return self.domestic_address
    def set_domestic_address(self, domestic_address):
        self.domestic_address = domestic_address
    def validate_ContactNameType(self, value):
        result = True
        # Validate type ContactNameType, a restriction on xsd:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 44:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on ContactNameType' % {"value": value, "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on ContactNameType' % {"value" : value, "lineno": lineno} )
                result = False
        return result
    def validate_CompanyNameType(self, value):
        result = True
        # Validate type CompanyNameType, a restriction on xsd:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 44:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on CompanyNameType' % {"value": value, "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on CompanyNameType' % {"value" : value, "lineno": lineno} )
                result = False
        return result
    def validate_EmailType(self, value):
        result = True
        # Validate type EmailType, a restriction on xsd:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 60:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on EmailType' % {"value": value, "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_EmailType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_EmailType_patterns_, ))
                result = False
        return result
    validate_EmailType_patterns_ = [["^((['_A-Za-z0-9\\-\\+]+)(\\.['_A-Za-z0-9\\-\\+]+)*@([A-Za-z0-9-]+)(\\.[A-Za-z0-9-]+)*(\\.[A-Za-z]{2,5}))$"]]
    def _hasContent(self):
        if (
            self.name is not None or
            self.company is not None or
            self.email is not None or
            self.receiver_voice_number is not None or
            self.domestic_address is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReceiverType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ReceiverType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ReceiverType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ReceiverType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ReceiverType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ReceiverType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReceiverType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.name is not None:
            namespaceprefix_ = self.name_nsprefix_ + ':' if (UseCapturedNS_ and self.name_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sname>%s</%sname>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.name), input_name='name')), namespaceprefix_ , eol_))
        if self.company is not None:
            namespaceprefix_ = self.company_nsprefix_ + ':' if (UseCapturedNS_ and self.company_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scompany>%s</%scompany>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.company), input_name='company')), namespaceprefix_ , eol_))
        if self.email is not None:
            namespaceprefix_ = self.email_nsprefix_ + ':' if (UseCapturedNS_ and self.email_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%semail>%s</%semail>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.email), input_name='email')), namespaceprefix_ , eol_))
        if self.receiver_voice_number is not None:
            namespaceprefix_ = self.receiver_voice_number_nsprefix_ + ':' if (UseCapturedNS_ and self.receiver_voice_number_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sreceiver-voice-number>%s</%sreceiver-voice-number>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.receiver_voice_number), input_name='receiver-voice-number')), namespaceprefix_ , eol_))
        if self.domestic_address is not None:
            namespaceprefix_ = self.domestic_address_nsprefix_ + ':' if (UseCapturedNS_ and self.domestic_address_nsprefix_) else ''
            self.domestic_address.export(outfile, level, namespaceprefix_, namespacedef_='', name_='domestic-address', pretty_print=pretty_print)
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
        if nodeName_ == 'name':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'name')
            value_ = self.gds_validate_string(value_, node, 'name')
            self.name = value_
            self.name_nsprefix_ = child_.prefix
            # validate type ContactNameType
            self.validate_ContactNameType(self.name)
        elif nodeName_ == 'company':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'company')
            value_ = self.gds_validate_string(value_, node, 'company')
            self.company = value_
            self.company_nsprefix_ = child_.prefix
            # validate type CompanyNameType
            self.validate_CompanyNameType(self.company)
        elif nodeName_ == 'email':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'email')
            value_ = self.gds_validate_string(value_, node, 'email')
            self.email = value_
            self.email_nsprefix_ = child_.prefix
            # validate type EmailType
            self.validate_EmailType(self.email)
        elif nodeName_ == 'receiver-voice-number':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'receiver_voice_number')
            value_ = self.gds_validate_string(value_, node, 'receiver_voice_number')
            self.receiver_voice_number = value_
            self.receiver_voice_number_nsprefix_ = child_.prefix
        elif nodeName_ == 'domestic-address':
            obj_ = DomesticAddressDetailsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.domestic_address = obj_
            obj_.original_tagname_ = 'domestic-address'
# end class ReceiverType


class ReferencesType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, customer_ref_1=None, customer_ref_2=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.customer_ref_1 = customer_ref_1
        self.validate_customer_ref_1Type(self.customer_ref_1)
        self.customer_ref_1_nsprefix_ = None
        self.customer_ref_2 = customer_ref_2
        self.validate_customer_ref_2Type(self.customer_ref_2)
        self.customer_ref_2_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ReferencesType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ReferencesType.subclass:
            return ReferencesType.subclass(*args_, **kwargs_)
        else:
            return ReferencesType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_customer_ref_1(self):
        return self.customer_ref_1
    def set_customer_ref_1(self, customer_ref_1):
        self.customer_ref_1 = customer_ref_1
    def get_customer_ref_2(self):
        return self.customer_ref_2
    def set_customer_ref_2(self, customer_ref_2):
        self.customer_ref_2 = customer_ref_2
    def validate_customer_ref_1Type(self, value):
        result = True
        # Validate type customer-ref-1Type, a restriction on xsd:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on customer-ref-1Type' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_customer_ref_2Type(self, value):
        result = True
        # Validate type customer-ref-2Type, a restriction on xsd:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 35:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on customer-ref-2Type' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.customer_ref_1 is not None or
            self.customer_ref_2 is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReferencesType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ReferencesType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ReferencesType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ReferencesType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ReferencesType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ReferencesType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ReferencesType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.customer_ref_1 is not None:
            namespaceprefix_ = self.customer_ref_1_nsprefix_ + ':' if (UseCapturedNS_ and self.customer_ref_1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scustomer-ref-1>%s</%scustomer-ref-1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.customer_ref_1), input_name='customer-ref-1')), namespaceprefix_ , eol_))
        if self.customer_ref_2 is not None:
            namespaceprefix_ = self.customer_ref_2_nsprefix_ + ':' if (UseCapturedNS_ and self.customer_ref_2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scustomer-ref-2>%s</%scustomer-ref-2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.customer_ref_2), input_name='customer-ref-2')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'customer-ref-1':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'customer_ref_1')
            value_ = self.gds_validate_string(value_, node, 'customer_ref_1')
            self.customer_ref_1 = value_
            self.customer_ref_1_nsprefix_ = child_.prefix
            # validate type customer-ref-1Type
            self.validate_customer_ref_1Type(self.customer_ref_1)
        elif nodeName_ == 'customer-ref-2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'customer_ref_2')
            value_ = self.gds_validate_string(value_, node, 'customer_ref_2')
            self.customer_ref_2 = value_
            self.customer_ref_2_nsprefix_ = child_.prefix
            # validate type customer-ref-2Type
            self.validate_customer_ref_2Type(self.customer_ref_2)
# end class ReferencesType


class DomesticAddressDetailsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, address_line_1=None, address_line_2=None, city=None, province=None, postal_code=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.address_line_1 = address_line_1
        self.validate_address_line_1Type(self.address_line_1)
        self.address_line_1_nsprefix_ = None
        self.address_line_2 = address_line_2
        self.validate_address_line_2Type(self.address_line_2)
        self.address_line_2_nsprefix_ = None
        self.city = city
        self.validate_cityType(self.city)
        self.city_nsprefix_ = None
        self.province = province
        self.province_nsprefix_ = None
        self.postal_code = postal_code
        self.postal_code_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, DomesticAddressDetailsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if DomesticAddressDetailsType.subclass:
            return DomesticAddressDetailsType.subclass(*args_, **kwargs_)
        else:
            return DomesticAddressDetailsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_address_line_1(self):
        return self.address_line_1
    def set_address_line_1(self, address_line_1):
        self.address_line_1 = address_line_1
    def get_address_line_2(self):
        return self.address_line_2
    def set_address_line_2(self, address_line_2):
        self.address_line_2 = address_line_2
    def get_city(self):
        return self.city
    def set_city(self, city):
        self.city = city
    def get_province(self):
        return self.province
    def set_province(self, province):
        self.province = province
    def get_postal_code(self):
        return self.postal_code
    def set_postal_code(self, postal_code):
        self.postal_code = postal_code
    def validate_address_line_1Type(self, value):
        result = True
        # Validate type address-line-1Type, a restriction on xsd:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 44:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on address-line-1Type' % {"value": value, "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on address-line-1Type' % {"value" : value, "lineno": lineno} )
                result = False
        return result
    def validate_address_line_2Type(self, value):
        result = True
        # Validate type address-line-2Type, a restriction on xsd:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 44:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on address-line-2Type' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def validate_cityType(self, value):
        result = True
        # Validate type cityType, a restriction on xsd:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 40:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on cityType' % {"value": value, "lineno": lineno} )
                result = False
            if len(value) < 1:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minLength restriction on cityType' % {"value" : value, "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.address_line_1 is not None or
            self.address_line_2 is not None or
            self.city is not None or
            self.province is not None or
            self.postal_code is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DomesticAddressDetailsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('DomesticAddressDetailsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'DomesticAddressDetailsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='DomesticAddressDetailsType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='DomesticAddressDetailsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='DomesticAddressDetailsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='DomesticAddressDetailsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.address_line_1 is not None:
            namespaceprefix_ = self.address_line_1_nsprefix_ + ':' if (UseCapturedNS_ and self.address_line_1_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%saddress-line-1>%s</%saddress-line-1>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.address_line_1), input_name='address-line-1')), namespaceprefix_ , eol_))
        if self.address_line_2 is not None:
            namespaceprefix_ = self.address_line_2_nsprefix_ + ':' if (UseCapturedNS_ and self.address_line_2_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%saddress-line-2>%s</%saddress-line-2>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.address_line_2), input_name='address-line-2')), namespaceprefix_ , eol_))
        if self.city is not None:
            namespaceprefix_ = self.city_nsprefix_ + ':' if (UseCapturedNS_ and self.city_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%scity>%s</%scity>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.city), input_name='city')), namespaceprefix_ , eol_))
        if self.province is not None:
            namespaceprefix_ = self.province_nsprefix_ + ':' if (UseCapturedNS_ and self.province_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sprovince>%s</%sprovince>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.province), input_name='province')), namespaceprefix_ , eol_))
        if self.postal_code is not None:
            namespaceprefix_ = self.postal_code_nsprefix_ + ':' if (UseCapturedNS_ and self.postal_code_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%spostal-code>%s</%spostal-code>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.postal_code), input_name='postal-code')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'address-line-1':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'address_line_1')
            value_ = self.gds_validate_string(value_, node, 'address_line_1')
            self.address_line_1 = value_
            self.address_line_1_nsprefix_ = child_.prefix
            # validate type address-line-1Type
            self.validate_address_line_1Type(self.address_line_1)
        elif nodeName_ == 'address-line-2':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'address_line_2')
            value_ = self.gds_validate_string(value_, node, 'address_line_2')
            self.address_line_2 = value_
            self.address_line_2_nsprefix_ = child_.prefix
            # validate type address-line-2Type
            self.validate_address_line_2Type(self.address_line_2)
        elif nodeName_ == 'city':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'city')
            value_ = self.gds_validate_string(value_, node, 'city')
            self.city = value_
            self.city_nsprefix_ = child_.prefix
            # validate type cityType
            self.validate_cityType(self.city)
        elif nodeName_ == 'province':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'province')
            value_ = self.gds_validate_string(value_, node, 'province')
            self.province = value_
            self.province_nsprefix_ = child_.prefix
        elif nodeName_ == 'postal-code':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'postal_code')
            value_ = self.gds_validate_string(value_, node, 'postal_code')
            self.postal_code = value_
            self.postal_code_nsprefix_ = child_.prefix
# end class DomesticAddressDetailsType


class ParcelCharacteristicsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, weight=None, dimensions=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.weight = weight
        self.validate_weightType(self.weight)
        self.weight_nsprefix_ = None
        self.dimensions = dimensions
        self.dimensions_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, ParcelCharacteristicsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if ParcelCharacteristicsType.subclass:
            return ParcelCharacteristicsType.subclass(*args_, **kwargs_)
        else:
            return ParcelCharacteristicsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_weight(self):
        return self.weight
    def set_weight(self, weight):
        self.weight = weight
    def get_dimensions(self):
        return self.dimensions
    def set_dimensions(self, dimensions):
        self.dimensions = dimensions
    def validate_weightType(self, value):
        result = True
        # Validate type weightType, a restriction on xsd:decimal.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, decimal_.Decimal):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (decimal_.Decimal)' % {"value": value, "lineno": lineno, })
                return False
            if value > 999.999:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxInclusive restriction on weightType' % {"value": value, "lineno": lineno} )
                result = False
            if value <= 0:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd minExclusive restriction on weightType' % {"value": value, "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.weight is not None or
            self.dimensions is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ParcelCharacteristicsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('ParcelCharacteristicsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'ParcelCharacteristicsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='ParcelCharacteristicsType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='ParcelCharacteristicsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='ParcelCharacteristicsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='ParcelCharacteristicsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.weight is not None:
            namespaceprefix_ = self.weight_nsprefix_ + ':' if (UseCapturedNS_ and self.weight_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sweight>%s</%sweight>%s' % (namespaceprefix_ , self.gds_format_decimal(self.weight, input_name='weight'), namespaceprefix_ , eol_))
        if self.dimensions is not None:
            namespaceprefix_ = self.dimensions_nsprefix_ + ':' if (UseCapturedNS_ and self.dimensions_nsprefix_) else ''
            self.dimensions.export(outfile, level, namespaceprefix_, namespacedef_='', name_='dimensions', pretty_print=pretty_print)
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
        if nodeName_ == 'weight' and child_.text:
            sval_ = child_.text
            fval_ = self.gds_parse_decimal(sval_, node, 'weight')
            fval_ = self.gds_validate_decimal(fval_, node, 'weight')
            self.weight = fval_
            self.weight_nsprefix_ = child_.prefix
            # validate type weightType
            self.validate_weightType(self.weight)
        elif nodeName_ == 'dimensions':
            obj_ = dimensionsType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.dimensions = obj_
            obj_.original_tagname_ = 'dimensions'
# end class ParcelCharacteristicsType


class PrintPreferencesType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, output_format=None, encoding=None, show_packing_instructions=True, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.output_format = output_format
        self.validate_output_formatType(self.output_format)
        self.output_format_nsprefix_ = None
        self.encoding = encoding
        self.validate_encodingType(self.encoding)
        self.encoding_nsprefix_ = None
        self.show_packing_instructions = show_packing_instructions
        self.show_packing_instructions_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, PrintPreferencesType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if PrintPreferencesType.subclass:
            return PrintPreferencesType.subclass(*args_, **kwargs_)
        else:
            return PrintPreferencesType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_output_format(self):
        return self.output_format
    def set_output_format(self, output_format):
        self.output_format = output_format
    def get_encoding(self):
        return self.encoding
    def set_encoding(self, encoding):
        self.encoding = encoding
    def get_show_packing_instructions(self):
        return self.show_packing_instructions
    def set_show_packing_instructions(self, show_packing_instructions):
        self.show_packing_instructions = show_packing_instructions
    def validate_output_formatType(self, value):
        result = True
        # Validate type output-formatType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['8.5x11', '4x6', '3x5']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on output-formatType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def validate_encodingType(self, value):
        result = True
        # Validate type encodingType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['PDF', 'ZPL']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on encodingType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.output_format is not None or
            self.encoding is not None or
            not self.show_packing_instructions
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PrintPreferencesType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('PrintPreferencesType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'PrintPreferencesType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='PrintPreferencesType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='PrintPreferencesType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='PrintPreferencesType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='PrintPreferencesType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.output_format is not None:
            namespaceprefix_ = self.output_format_nsprefix_ + ':' if (UseCapturedNS_ and self.output_format_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%soutput-format>%s</%soutput-format>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.output_format), input_name='output-format')), namespaceprefix_ , eol_))
        if self.encoding is not None:
            namespaceprefix_ = self.encoding_nsprefix_ + ':' if (UseCapturedNS_ and self.encoding_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sencoding>%s</%sencoding>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.encoding), input_name='encoding')), namespaceprefix_ , eol_))
        if not self.show_packing_instructions:
            namespaceprefix_ = self.show_packing_instructions_nsprefix_ + ':' if (UseCapturedNS_ and self.show_packing_instructions_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sshow-packing-instructions>%s</%sshow-packing-instructions>%s' % (namespaceprefix_ , self.gds_format_boolean(self.show_packing_instructions, input_name='show-packing-instructions'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'output-format':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'output_format')
            value_ = self.gds_validate_string(value_, node, 'output_format')
            self.output_format = value_
            self.output_format_nsprefix_ = child_.prefix
            # validate type output-formatType
            self.validate_output_formatType(self.output_format)
        elif nodeName_ == 'encoding':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'encoding')
            value_ = self.gds_validate_string(value_, node, 'encoding')
            self.encoding = value_
            self.encoding_nsprefix_ = child_.prefix
            # validate type encodingType
            self.validate_encodingType(self.encoding)
        elif nodeName_ == 'show-packing-instructions':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'show_packing_instructions')
            ival_ = self.gds_validate_boolean(ival_, node, 'show_packing_instructions')
            self.show_packing_instructions = ival_
            self.show_packing_instructions_nsprefix_ = child_.prefix
# end class PrintPreferencesType


class NotificationsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, notification=None, email_subject=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        if notification is None:
            self.notification = []
        else:
            self.notification = notification
        self.notification_nsprefix_ = None
        self.email_subject = email_subject
        self.validate_email_subjectType(self.email_subject)
        self.email_subject_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, NotificationsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if NotificationsType.subclass:
            return NotificationsType.subclass(*args_, **kwargs_)
        else:
            return NotificationsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_notification(self):
        return self.notification
    def set_notification(self, notification):
        self.notification = notification
    def add_notification(self, value):
        self.notification.append(value)
    def insert_notification_at(self, index, value):
        self.notification.insert(index, value)
    def replace_notification_at(self, index, value):
        self.notification[index] = value
    def get_email_subject(self):
        return self.email_subject
    def set_email_subject(self, email_subject):
        self.email_subject = email_subject
    def validate_email_subjectType(self, value):
        result = True
        # Validate type email-subjectType, a restriction on xsd:string.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            value = value
            enumerations = ['tracking', 'customer-ref-1', 'customer-ref-2']
            if value not in enumerations:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd enumeration restriction on email-subjectType' % {"value" : encode_str_2_3(value), "lineno": lineno} )
                result = False
        return result
    def _hasContent(self):
        if (
            self.notification or
            self.email_subject is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NotificationsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('NotificationsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'NotificationsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='NotificationsType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='NotificationsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='NotificationsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='NotificationsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        for notification_ in self.notification:
            namespaceprefix_ = self.notification_nsprefix_ + ':' if (UseCapturedNS_ and self.notification_nsprefix_) else ''
            notification_.export(outfile, level, namespaceprefix_, namespacedef_='', name_='notification', pretty_print=pretty_print)
        if self.email_subject is not None:
            namespaceprefix_ = self.email_subject_nsprefix_ + ':' if (UseCapturedNS_ and self.email_subject_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%semail-subject>%s</%semail-subject>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.email_subject), input_name='email-subject')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'notification':
            obj_ = notificationType.factory(parent_object_=self)
            obj_.build(child_, gds_collector_=gds_collector_)
            self.notification.append(obj_)
            obj_.original_tagname_ = 'notification'
        elif nodeName_ == 'email-subject':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'email_subject')
            value_ = self.gds_validate_string(value_, node, 'email_subject')
            self.email_subject = value_
            self.email_subject_nsprefix_ = child_.prefix
            # validate type email-subjectType
            self.validate_email_subjectType(self.email_subject)
# end class NotificationsType


class dimensionsType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, length=None, width=None, height=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.length = length
        self.length_nsprefix_ = None
        self.width = width
        self.width_nsprefix_ = None
        self.height = height
        self.height_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, dimensionsType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if dimensionsType.subclass:
            return dimensionsType.subclass(*args_, **kwargs_)
        else:
            return dimensionsType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_length(self):
        return self.length
    def set_length(self, length):
        self.length = length
    def get_width(self):
        return self.width
    def set_width(self, width):
        self.width = width
    def get_height(self):
        return self.height
    def set_height(self, height):
        self.height = height
    def _hasContent(self):
        if (
            self.length is not None or
            self.width is not None or
            self.height is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='dimensionsType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('dimensionsType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'dimensionsType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='dimensionsType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='dimensionsType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='dimensionsType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='dimensionsType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.length is not None:
            namespaceprefix_ = self.length_nsprefix_ + ':' if (UseCapturedNS_ and self.length_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%slength>%s</%slength>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.length), input_name='length')), namespaceprefix_ , eol_))
        if self.width is not None:
            namespaceprefix_ = self.width_nsprefix_ + ':' if (UseCapturedNS_ and self.width_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%swidth>%s</%swidth>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.width), input_name='width')), namespaceprefix_ , eol_))
        if self.height is not None:
            namespaceprefix_ = self.height_nsprefix_ + ':' if (UseCapturedNS_ and self.height_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%sheight>%s</%sheight>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.height), input_name='height')), namespaceprefix_ , eol_))
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
        if nodeName_ == 'length':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'length')
            value_ = self.gds_validate_string(value_, node, 'length')
            self.length = value_
            self.length_nsprefix_ = child_.prefix
        elif nodeName_ == 'width':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'width')
            value_ = self.gds_validate_string(value_, node, 'width')
            self.width = value_
            self.width_nsprefix_ = child_.prefix
        elif nodeName_ == 'height':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'height')
            value_ = self.gds_validate_string(value_, node, 'height')
            self.height = value_
            self.height_nsprefix_ = child_.prefix
# end class dimensionsType


class notificationType(GeneratedsSuper):
    __hash__ = GeneratedsSuper.__hash__
    subclass = None
    superclass = None
    def __init__(self, email=None, on_shipment=None, on_exception=None, on_delivery=None, gds_collector_=None, **kwargs_):
        self.gds_collector_ = gds_collector_
        self.gds_elementtree_node_ = None
        self.original_tagname_ = None
        self.parent_object_ = kwargs_.get('parent_object_')
        self.ns_prefix_ = None
        self.email = email
        self.validate_EmailType(self.email)
        self.email_nsprefix_ = None
        self.on_shipment = on_shipment
        self.on_shipment_nsprefix_ = None
        self.on_exception = on_exception
        self.on_exception_nsprefix_ = None
        self.on_delivery = on_delivery
        self.on_delivery_nsprefix_ = None
    def factory(*args_, **kwargs_):
        if CurrentSubclassModule_ is not None:
            subclass = getSubclassFromModule_(
                CurrentSubclassModule_, notificationType)
            if subclass is not None:
                return subclass(*args_, **kwargs_)
        if notificationType.subclass:
            return notificationType.subclass(*args_, **kwargs_)
        else:
            return notificationType(*args_, **kwargs_)
    factory = staticmethod(factory)
    def get_ns_prefix_(self):
        return self.ns_prefix_
    def set_ns_prefix_(self, ns_prefix):
        self.ns_prefix_ = ns_prefix
    def get_email(self):
        return self.email
    def set_email(self, email):
        self.email = email
    def get_on_shipment(self):
        return self.on_shipment
    def set_on_shipment(self, on_shipment):
        self.on_shipment = on_shipment
    def get_on_exception(self):
        return self.on_exception
    def set_on_exception(self, on_exception):
        self.on_exception = on_exception
    def get_on_delivery(self):
        return self.on_delivery
    def set_on_delivery(self, on_delivery):
        self.on_delivery = on_delivery
    def validate_EmailType(self, value):
        result = True
        # Validate type EmailType, a restriction on xsd:normalizedString.
        if value is not None and Validate_simpletypes_ and self.gds_collector_ is not None:
            if not isinstance(value, str):
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s is not of the correct base simple type (str)' % {"value": value, "lineno": lineno, })
                return False
            if len(value) > 60:
                lineno = self.gds_get_node_lineno_()
                self.gds_collector_.add_message('Value "%(value)s"%(lineno)s does not match xsd maxLength restriction on EmailType' % {"value": value, "lineno": lineno} )
                result = False
            if not self.gds_validate_simple_patterns(
                    self.validate_EmailType_patterns_, value):
                self.gds_collector_.add_message('Value "%s" does not match xsd pattern restrictions: %s' % (encode_str_2_3(value), self.validate_EmailType_patterns_, ))
                result = False
        return result
    validate_EmailType_patterns_ = [["^((['_A-Za-z0-9\\-\\+]+)(\\.['_A-Za-z0-9\\-\\+]+)*@([A-Za-z0-9-]+)(\\.[A-Za-z0-9-]+)*(\\.[A-Za-z]{2,5}))$"]]
    def _hasContent(self):
        if (
            self.email is not None or
            self.on_shipment is not None or
            self.on_exception is not None or
            self.on_delivery is not None
        ):
            return True
        else:
            return False
    def export(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='notificationType', pretty_print=True):
        imported_ns_def_ = GenerateDSNamespaceDefs_.get('notificationType')
        if imported_ns_def_ is not None:
            namespacedef_ = imported_ns_def_
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.original_tagname_ is not None and name_ == 'notificationType':
            name_ = self.original_tagname_
        if UseCapturedNS_ and self.ns_prefix_:
            namespaceprefix_ = self.ns_prefix_ + ':'
        showIndent(outfile, level, pretty_print)
        outfile.write('<%s%s%s' % (namespaceprefix_, name_, namespacedef_ and ' ' + namespacedef_ or '', ))
        already_processed = set()
        self._exportAttributes(outfile, level, already_processed, namespaceprefix_, name_='notificationType')
        if self._hasContent():
            outfile.write('>%s' % (eol_, ))
            self._exportChildren(outfile, level + 1, namespaceprefix_, namespacedef_, name_='notificationType', pretty_print=pretty_print)
            showIndent(outfile, level, pretty_print)
            outfile.write('</%s%s>%s' % (namespaceprefix_, name_, eol_))
        else:
            outfile.write('/>%s' % (eol_, ))
    def _exportAttributes(self, outfile, level, already_processed, namespaceprefix_='', name_='notificationType'):
        pass
    def _exportChildren(self, outfile, level, namespaceprefix_='', namespacedef_='', name_='notificationType', fromsubclass_=False, pretty_print=True):
        if pretty_print:
            eol_ = '\n'
        else:
            eol_ = ''
        if self.email is not None:
            namespaceprefix_ = self.email_nsprefix_ + ':' if (UseCapturedNS_ and self.email_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%semail>%s</%semail>%s' % (namespaceprefix_ , self.gds_encode(self.gds_format_string(quote_xml(self.email), input_name='email')), namespaceprefix_ , eol_))
        if self.on_shipment is not None:
            namespaceprefix_ = self.on_shipment_nsprefix_ + ':' if (UseCapturedNS_ and self.on_shipment_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%son-shipment>%s</%son-shipment>%s' % (namespaceprefix_ , self.gds_format_boolean(self.on_shipment, input_name='on-shipment'), namespaceprefix_ , eol_))
        if self.on_exception is not None:
            namespaceprefix_ = self.on_exception_nsprefix_ + ':' if (UseCapturedNS_ and self.on_exception_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%son-exception>%s</%son-exception>%s' % (namespaceprefix_ , self.gds_format_boolean(self.on_exception, input_name='on-exception'), namespaceprefix_ , eol_))
        if self.on_delivery is not None:
            namespaceprefix_ = self.on_delivery_nsprefix_ + ':' if (UseCapturedNS_ and self.on_delivery_nsprefix_) else ''
            showIndent(outfile, level, pretty_print)
            outfile.write('<%son-delivery>%s</%son-delivery>%s' % (namespaceprefix_ , self.gds_format_boolean(self.on_delivery, input_name='on-delivery'), namespaceprefix_ , eol_))
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
        if nodeName_ == 'email':
            value_ = child_.text
            value_ = self.gds_parse_string(value_, node, 'email')
            value_ = self.gds_validate_string(value_, node, 'email')
            self.email = value_
            self.email_nsprefix_ = child_.prefix
            # validate type EmailType
            self.validate_EmailType(self.email)
        elif nodeName_ == 'on-shipment':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'on_shipment')
            ival_ = self.gds_validate_boolean(ival_, node, 'on_shipment')
            self.on_shipment = ival_
            self.on_shipment_nsprefix_ = child_.prefix
        elif nodeName_ == 'on-exception':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'on_exception')
            ival_ = self.gds_validate_boolean(ival_, node, 'on_exception')
            self.on_exception = ival_
            self.on_exception_nsprefix_ = child_.prefix
        elif nodeName_ == 'on-delivery':
            sval_ = child_.text
            ival_ = self.gds_parse_boolean(sval_, node, 'on_delivery')
            ival_ = self.gds_validate_boolean(ival_, node, 'on_delivery')
            self.on_delivery = ival_
            self.on_delivery_nsprefix_ = child_.prefix
# end class notificationType


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
        rootTag = 'AuthorizedReturnType'
        rootClass = AuthorizedReturnType
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
        rootTag = 'AuthorizedReturnType'
        rootClass = AuthorizedReturnType
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
        rootTag = 'AuthorizedReturnType'
        rootClass = AuthorizedReturnType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    if not SaveElementTreeNode:
        rootNode = None
    if not silence:
        sys.stdout.write('<?xml version="1.0" ?>\n')
        rootObj.export(
            sys.stdout, 0, name_=rootTag,
            namespacedef_='')
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
        rootTag = 'AuthorizedReturnType'
        rootClass = AuthorizedReturnType
    rootObj = rootClass.factory()
    rootObj.build(rootNode, gds_collector_=gds_collector)
    # Enable Python to collect the space used by the DOM.
    if not SaveElementTreeNode:
        doc = None
        rootNode = None
    if not silence:
        sys.stdout.write('#from authreturn import *\n\n')
        sys.stdout.write('import authreturn as model_\n\n')
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
NamespaceToDefMappings_ = {'http://www.canadapost.ca/ws/authreturn-v2': [('TrackingPINType',
                                                './schemas/authreturn.xsd',
                                                'ST'),
                                               ('ContactNameType',
                                                './schemas/authreturn.xsd',
                                                'ST'),
                                               ('CompanyNameType',
                                                './schemas/authreturn.xsd',
                                                'ST'),
                                               ('EmailType',
                                                './schemas/authreturn.xsd',
                                                'ST'),
                                               ('ReturnPolicyNumberType',
                                                './schemas/authreturn.xsd',
                                                'ST'),
                                               ('AdditionalOrderInfoLabelEnType',
                                                './schemas/authreturn.xsd',
                                                'ST'),
                                               ('AdditionalOrderInfoLabelFrType',
                                                './schemas/authreturn.xsd',
                                                'ST'),
                                               ('AdditionalOrderInfoType',
                                                './schemas/authreturn.xsd',
                                                'ST'),
                                               ('AuthorizedReturnInfoType',
                                                './schemas/authreturn.xsd',
                                                'CT'),
                                               ('PublicKeyInfoType',
                                                './schemas/authreturn.xsd',
                                                'CT'),
                                               ('AuthorizedReturnType',
                                                './schemas/authreturn.xsd',
                                                'CT'),
                                               ('AuthSettlementInfoType',
                                                './schemas/authreturn.xsd',
                                                'CT'),
                                               ('ReturnerType',
                                                './schemas/authreturn.xsd',
                                                'CT'),
                                               ('ReceiverType',
                                                './schemas/authreturn.xsd',
                                                'CT'),
                                               ('ReferencesType',
                                                './schemas/authreturn.xsd',
                                                'CT'),
                                               ('DomesticAddressDetailsType',
                                                './schemas/authreturn.xsd',
                                                'CT'),
                                               ('ParcelCharacteristicsType',
                                                './schemas/authreturn.xsd',
                                                'CT'),
                                               ('PrintPreferencesType',
                                                './schemas/authreturn.xsd',
                                                'CT'),
                                               ('NotificationsType',
                                                './schemas/authreturn.xsd',
                                                'CT')]}

__all__ = [
    "AuthSettlementInfoType",
    "AuthorizedReturnInfoType",
    "AuthorizedReturnType",
    "DomesticAddressDetailsType",
    "NotificationsType",
    "ParcelCharacteristicsType",
    "PrintPreferencesType",
    "PublicKeyInfoType",
    "ReceiverType",
    "ReferencesType",
    "ReturnerType",
    "dimensionsType",
    "notificationType"
]
