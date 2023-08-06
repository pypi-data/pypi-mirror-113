# Copyright Iris contributors
#
# This file is part of Iris and is released under the LGPL license.
# See COPYING and COPYING.LESSER in the root of the repository for full
# licensing details.
"""
Provides the framework to support the encoding of metarelate mapping
translations.

"""

from abc import ABCMeta, abstractmethod
from collections import deque, namedtuple
import copy
from queue import Queue
import re
from threading import Thread
import warnings

from metarelate.fuseki import FusekiServer, WorkerThread, MAXTHREADS
import metarelate

# known format identifier URIs
FORMAT_URIS = {'cff': '<http://def.scitools.org.uk/cfdatamodel/Field>',
               'gribm': '<http://codes.wmo.int/def/codeform/GRIB-message>',
               'umf': '<http://reference.metoffice.gov.uk/um/f3/UMField>'}

CFName = namedtuple('CFName', 'standard_name long_name units')
DimensionCoordinate = namedtuple('DimensionCoordinate',
                                 'standard_name units points')
G1LocalParam = namedtuple('G1LocalParam', 'edition t2version centre iParam')
G2Param = namedtuple('G2Param', 'edition discipline category number')


class MappingEncodeWorker(WorkerThread):
    """Worker thread class for handling EncodableMap instances"""
    def dowork(self, resource):
        resource.encode(self.fuseki_process)


class EncodableMap:
    """
    A metarelate mapping able to encode itself as a string for use in Iris,
    as defined by a translator Mappings subclass

    """
    def __init__(self, mapping, sourcemsg, targetmsg, sourceid, targetid):
        """
        Args:
        * mapping:
            A :class:`metarelate.Mapping` instance representing a translation.
        * sourcemsg:
            The code snippet message for the source of the translation for
            formatting
        * targetmsg:
            The code snippet message for the target of the translation for
            formatting
        * sourceid:
            A dictionary of required key:value pairs required by the sourcemsg
        * targetid:
            A dictionary of required key:value pairs required by the targetmsg

        """
        self.mapping = mapping
        self.sourcemsg = sourcemsg
        self.targetmsg = targetmsg
        self.sourceid = sourceid
        self.targetid = targetid
        self.encoding = None

    def encode(self, fuseki_process):
        """
        Return a string of the Python source code required to represent an
        entry in a dictionary mapping source to target.

        Args:
        * fuseki_process:
            A :class:`metarelate.fuseki.FusekiServer` instance.

        """
        sids, tids = self.mapping.get_identifiers(fuseki_process)
        self.sourceid.update(sids)
        self.targetid.update(tids)
        self.encoding = '{}: {}'.format(self.sourcemsg.format(**self.sourceid),
                                        self.targetmsg.format(**self.targetid))


class Mappings(metaclass=ABCMeta):
    """
    Abstract base class to support the encoding of specific metarelate
    mapping translations.

    """

    def __init__(self, mappings):
        """
        Filter the given sequence of mappings for those member
        :class:`metarelate.Mapping` translations containing a source
        :class:`metarelate.Component` with a matching
        :attribute:`Mapping.source_scheme` and a target
        :class:`metarelate.Component` with a matching
        :attribute:`Mapping.target_scheme`.

        Also see :method:`Mapping.valid_mapping` for further matching
        criterion for candidate metarelate mapping translations.

        Args:
        * mappings:
            Iterator of :class:`metarelate.Mapping` instances.

        """
        temp = []
        # Filter the mappings for the required type of translations.
        for mapping in mappings:
            source = mapping.source
            target = mapping.target
            sourcemsg, targetmsg = self.msg_strings()
            sourceid, targetid = self.get_initial_id_nones()
            if source.com_type == self.source_scheme and \
                    target.com_type == self.target_scheme and \
                    self.valid_mapping(mapping):
                temp.append(EncodableMap(mapping, sourcemsg, targetmsg,
                                         sourceid, targetid))
        self.mappings = temp
        if len(self) == 0:
            msg = '{!r} contains no mappings.'
            warnings.warn(msg.format(self.__class__.__name__))

    def _sort_lines(self, payload):
        """
        Return the payload, unsorted.

        """
        return payload

    def lines(self, fuseki_process):
        """
        Provides an iterator generating the encoded string representation
        of each member of this metarelate mapping translation.

        Returns:
            An iterator of string.

        """
        msg = '\tGenerating phenomenon translation {!r}.'
        print(msg.format(self.mapping_name))
        lines = ['\n%s = {\n' % self.mapping_name]
        # Retrieve encodings for the collection of mapping instances.
        # Retrieval is threaded as it is heavily bound by resource resolution
        # over http.
        # Queue for metarelate mapping instances
        mapenc_queue = Queue()
        for mapping in self.mappings:
            mapenc_queue.put(mapping)
        # deque to contain the results of the jobs processed from the queue
        mapencs = deque()
        # run worker threads
        for i in range(MAXTHREADS):
            MappingEncodeWorker(mapenc_queue, mapencs, fuseki_process).start()
        # block progress until the queue is empty
        mapenc_queue.join()
        # end of threaded retrieval process.

        # now sort the payload
        payload = [mapenc.encoding for mapenc in mapencs]
        payload.sort(key=self._key)
        lines.extend(payload)
        lines.append('    }\n')
        return iter(lines)

    def __len__(self):
        return len(self.mappings)

    def _key(self, line):
        """Method to provide the sort key of the mappings order."""
        return line

    @property
    @abstractmethod
    def mapping_name(self):
        """
        Abstract property that specifies the name of the dictionary
        to contain the encoding of this metarelate mapping translation.

        """

    @property
    @abstractmethod
    def source_scheme(self):
        """
        Abstract property that specifies the name of the scheme for
        the source :class:`metarelate.Component` defining this metarelate
        mapping translation.

        """

    @property
    @abstractmethod
    def target_scheme(self):
        """
        Abstract property that specifies the name of the scheme for
        the target :class:`metarelate.Component` defining this metarelate
        mapping translation.

        """

    @abstractmethod
    def valid_mapping(self, mapping):
        """
        Abstract method that determines whether the provided
        :class:`metarelate.Mapping` is a translation from the required
        source :class:`metarelate.Component` to the required target
        :class:`metarelate.Component`.

        """

    def get_initial_id_nones(self):
        """
        Return the identifier items which may not exist, in the translation
        database, and are needed for a msg_string.  These must exist, even
        even if not written from the database.

        Returns two dictionaries to use as the start point for
        population from the database.

        """
        sourceid = {}
        targetid = {}
        return sourceid, targetid

    def is_cf(self, comp):
        """
        Determines whether the provided component from a mapping
        represents a simple CF component of the given kind.

        Args:
        * component:
            A :class:`metarelate.Component` or
            :class:`metarelate.Component` instance.

        Returns:
            Boolean.

        """
        kind = FORMAT_URIS['cff']
        result = False
        result = hasattr(comp, 'com_type') and \
            comp.com_type == kind and \
            hasattr(comp, 'units') and \
            len(comp) in [1, 2]
        return result

    def is_cf_constrained(self, comp):
        """
        Determines whether the provided component from a mapping
        represents a compound CF component for a phenomenon and
        one, single valued dimension coordinate.

        Args:
        * component:
            A :class:`metarelate.Component` instance.

        Returns:
            Boolean.

        """
        ftype = FORMAT_URIS['cff']
        result = False
        cffield = hasattr(comp, 'com_type') and comp.com_type == ftype and \
            hasattr(comp, 'units') and (hasattr(comp, 'standard_name') or
                                        hasattr(comp, 'long_name'))
        dimcoord = hasattr(comp, 'dim_coord') and \
            isinstance(comp.dim_coord, metarelate.ComponentProperty) and \
            comp.dim_coord.component.com_type.notation == 'DimCoord'
        result = cffield and dimcoord
        return result

    def is_cf_height_constrained(self, comp):
        item_sn = metarelate.Item(('<http://def.scitools.org.uk/cfdatamodel/'
                                   'standard_name>'),
                                  'standard_name')
        item_h = metarelate.Item(('<http://vocab.nerc.ac.uk/standard_name/'
                                  'height>'),
                                 'height')
        snprop = metarelate.StatementProperty(item_sn, item_h)
        item_u = metarelate.Item(('<http://def.scitools.org.uk/cfdatamodel/'
                                  'units>'),
                                 'units')
        uprop = metarelate.StatementProperty(item_u,
                                             metarelate.Item('"m"', 'm'))
        pts_pred = metarelate.Item(('<http://def.scitools.org.uk/cfdatamodel/'
                                    'points>'),
                                   'points')
        result = False
        if self.is_cf_constrained(comp):
            props = comp.dim_coord.component.properties
            if len(props) == 3:
                if snprop in props and uprop in props:
                    preds = [prop.predicate for prop in props]
                    if pts_pred in preds:
                        result = True
        return result

    def is_fieldcode(self, component):
        """
        Determines whether the provided concept from a mapping
        represents a simple UM concept for a field-code.

        Args:
        * concept:
            A :class:`metarelate.Component` instance.

        Returns:
            Boolean.

        """
        result = False
        result = hasattr(component, 'lbfc') and len(component) == 1
        return result

    def is_grib1_local_param(self, component):
        """
        Determines whether the provided component from a mapping
        represents a simple GRIB edition 1 component for a local
        parameter.

        Args:
        * component:
            A :class:`metarelate.Component` instance.

        Returns:
            Boolean.

        """
        result = len(component) == 1 and hasattr(component, 'grib1_parameter')
        return result

    def is_grib2_param(self, component):
        """
        Determines whether the provided component from a mapping
        represents a simple GRIB edition 2 component for a parameter.

        Args:
        * component:
            A :class:`metarelate.Component` instance.

        Returns:
            Boolean.

        """

        result = len(component) == 1 and hasattr(component, 'grib2_parameter')
        return result

    def is_stash(self, component):
        """
        Determines whether the provided concept for a mapping
        represents a simple UM concept for a stash-code.

        Args:
        * concept:
            A :class:`metarelate.Component` instance.

        Returns:
            Boolean.

        """
        result = False
        result = hasattr(component, 'stash') and len(component) == 1
        return result


def _cfn(line):
    """
    Helper function to parse dictionary lines using the CFName named tuple.
    Matches to the line '    CFName({standard_name}, {long_name}, {units}:*)
    giving access to these named parts

    """
    match = re.match('^    CFName\((.+), (.+), (.+)\):.+,', line)
    if match is None:
        raise ValueError('encoding not sortable')
    standard_name, long_name, units = match.groups()
    if standard_name == 'None':
        standard_name = None
    if long_name == 'None':
        long_name = None
    return [standard_name, long_name, units]


class CFFieldcodeMappings(Mappings):
    """
    Represents a container for CF phenomenon to UM field-code metarelate
    mapping translations.

    Encoding support is provided to generate the Python dictionary source
    code representation of these mappings from CF standard name, long name,
    and units to UM field-code.

    """
    def _key(self, line):
        """Provides the sort key of the mappings order."""
        return _cfn(line)

    def msg_strings(self):
        return ('    CFName({standard_name!r}, {long_name!r}, '
                '{units!r})',
                '{lbfc},\n')

    def get_initial_id_nones(self):
        sourceid = {'standard_name': None, 'long_name': None}
        targetid = {}
        return sourceid, targetid

    @property
    def mapping_name(self):
        """
        Property that specifies the name of the dictionary to contain the
        encoding of this metarelate mapping translation.

        """
        return 'CF_TO_LBFC'

    @property
    def source_scheme(self):
        """
        Property that specifies the name of the scheme for the source
        :class:`metarelate.Component` defining this metarelate mapping
        translation.

        """
        return FORMAT_URIS['cff']

    @property
    def target_scheme(self):
        """
        Property that specifies the name of the scheme for the target
        :class:`metarelate.Component` defining this metarelate mapping
        translation.

        """
        return FORMAT_URIS['umf']

    def valid_mapping(self, mapping):
        """
        Determine whether the provided :class:`metarelate.Mapping` represents a
        CF to UM field-code translation.

        Args:
        * mapping:
            A :class:`metarelate.Mapping` instance.

        Returns:
            Boolean.

        """
        return self.is_cf(mapping.source) and self.is_fieldcode(mapping.target)


class FieldcodeCFMappings(Mappings):
    """
    Represents a container for UM field-code to CF phenomenon metarelate
    mapping translations.

    Encoding support is provided to generate the Python dictionary source
    code representation of these mappings from UM field-code to
    CF standard name, long name, and units.

    """
    def _key(self, line):
        """Provides the sort key of the mappings order."""
        return int(line.split(':')[0].strip())

    def msg_strings(self):
        return ('    {lbfc}',
                'CFName({standard_name!r}, {long_name!r}, {units!r}),\n')

    def get_initial_id_nones(self):
        sourceid = {}
        targetid = {'standard_name': None, 'long_name': None}
        return sourceid, targetid

    @property
    def mapping_name(self):
        """
        Property that specifies the name of the dictionary to contain the
        encoding of this metarelate mapping translation.

        """
        return 'LBFC_TO_CF'

    @property
    def source_scheme(self):
        """
        Property that specifies the name of the scheme for the source
        :class:`metarelate.Component` defining this metarelate mapping
        translation.

        """
        return FORMAT_URIS['umf']

    @property
    def target_scheme(self):
        """
        Property that specifies the name of the scheme for the target
        :class:`metarelate.Component` defining this metarelate mapping
        translation.

        """
        return FORMAT_URIS['cff']

    def valid_mapping(self, mapping):
        """
        Determine whether the provided :class:`metarelate.Mapping` represents a
        UM field-code to CF translation.

        Args:
        * mapping:
            A :class:`metarelate.Mapping` instance.

        Returns:
            Boolean.

        """
        return self.is_fieldcode(mapping.source) and self.is_cf(mapping.target)


class StashCFNameMappings(Mappings):
    """
    Represents a container for UM stash-code to CF phenomenon metarelate
    mapping translations.

    Encoding support is provided to generate the Python dictionary source
    code representation of these mappings from UM stash-code to CF
    standard name, long name, and units.

    """
    def _key(self, line):
        """Provides the sort key of the mappings order."""
        return line.split(':')[0].strip()

    def msg_strings(self):
        return('    {stash!r}',
               'CFName({standard_name!r}, '
               '{long_name!r}, {units!r}),\n')

    def get_initial_id_nones(self):
        sourceid = {}
        targetid = {'standard_name': None, 'long_name': None}
        return sourceid, targetid

    @property
    def mapping_name(self):
        """
        Property that specifies the name of the dictionary to contain the
        encoding of this metarelate mapping translation.

        """
        return 'STASH_TO_CF'

    @property
    def source_scheme(self):
        """
        Property that specifies the name of the scheme for the source
        :class:`metarelate.Component` defining this metarelate mapping
        translation.

        """
        return FORMAT_URIS['umf']

    @property
    def target_scheme(self):
        """
        Property that specifies the name of the scheme for the target
        :class:`metarelate.Component` defining this metarelate mapping
        translation.

        """
        return FORMAT_URIS['cff']

    def valid_mapping(self, mapping):
        """
        Determine whether the provided :class:`metarelate.Mapping` represents a
        UM stash-code to CF translation.

        Args:
        * mapping:
            A :class:`metarelate.Mapping` instance.

        Returns:
            Boolean.

        """
        return (self.is_stash(mapping.source) and
                (self.is_cf(mapping.target) or
                 self.is_cf_constrained(mapping.target)))


class StashCFHeightConstraintMappings(Mappings):
    """
    Represents a container for UM stash-code to CF phenomenon metarelate
    mapping translations where a singular height constraint is defined by
    the STASH code.

    Encoding support is provided to generate the Python dictionary source
    code representation of these mappings from UM stash-code to CF
    standard name, long name, and units.

    """
    def _key(self, line):
        """Provides the sort key of the mappings order."""
        return line.split(':')[0].strip()

    def msg_strings(self):
        return('    {stash!r}',
               '{dim_coord[points]},\n')

    def get_initial_id_nones(self):
        sourceid = {}
        targetid = {}
        return sourceid, targetid

    @property
    def mapping_name(self):
        """
        Property that specifies the name of the dictionary to contain the
        encoding of this metarelate mapping translation.

        """
        return 'STASHCODE_IMPLIED_HEIGHTS'

    @property
    def source_scheme(self):
        """
        Property that specifies the name of the scheme for the source
        :class:`metarelate.Component` defining this metarelate mapping
        translation.

        """
        return FORMAT_URIS['umf']

    @property
    def target_scheme(self):
        """
        Property that specifies the name of the scheme for the target
        :class:`metarelate.Component` defining this metarelate mapping
        translation.

        """
        return FORMAT_URIS['cff']

    def valid_mapping(self, mapping):
        """
        Determine whether the provided :class:`metarelate.Mapping` represents a
        UM stash-code to CF translation.

        Args:
        * mapping:
            A :class:`metarelate.Mapping` instance.

        Returns:
            Boolean.

        """
        return (self.is_stash(mapping.source) and
                self.is_cf_height_constrained(mapping.target))


class GRIB1LocalParamCFMappings(Mappings):
    """
    Represents a container for GRIB (edition 1) local parameter to
    CF phenomenon metarelate mapping translations.

    Encoding support is provided to generate the Python dictionary source
    code representation of these mappings from GRIB1 edition, table II version,
    centre and indicator of parameter to CF standard name, long name and units.

    """
    def _key(self, line):
        """Provides the sort key of the mappings order."""
        matchstr = ('^    G1LocalParam\(([0-9]+), ([0-9]+), '
                    '([0-9]+), ([0-9]+)\):.*')
        match = re.match(matchstr, line)
        if match is None:
            raise ValueError('encoding not sortable')
        return [int(i) for i in match.groups()]

    def msg_strings(self):
        return ('    G1LocalParam({editionNumber}, {table2version}, '
                '{centre}, {indicatorOfParameter})',
                'CFName({standard_name!r}, '
                '{long_name!r}, {units!r}),\n')

    def get_initial_id_nones(self):
        sourceid = {}
        targetid = {'standard_name': None, 'long_name': None}
        return sourceid, targetid

    @property
    def mapping_name(self):
        """
        Property that specifies the name of the dictionary to contain the
        encoding of this metarelate mapping translation.

        """
        return 'GRIB1_LOCAL_TO_CF'

    @property
    def source_scheme(self):
        """
        Property that specifies the name of the scheme for the source
        :class:`metarelate.Component` defining this metarelate mapping
        translation.

        """
        return FORMAT_URIS['gribm']

    @property
    def target_scheme(self):
        """
        Property that specifies the name of the scheme for the target
        :class:`metarelate.Component` defining this metarelate mapping
        translation.

        """
        return FORMAT_URIS['cff']

    def valid_mapping(self, mapping):
        """
        Determine whether the provided :class:`metarelate.Mapping` represents a
        GRIB1 local parameter to CF phenomenon translation.

        Args:
        * mapping:
            A :class:`metarelate.Mapping` instance.

        Returns:
            Boolean.

        """
        return self.is_grib1_local_param(mapping.source) and \
            self.is_cf(mapping.target)


class CFGRIB1LocalParamMappings(Mappings):
    """
    Represents a container for CF phenomenon to GRIB (edition 1) local
    parameter metarelate mapping translations.

    Encoding support is provided to generate the Python dictionary source
    code representation of these mappings from CF standard name, long name
    and units to GRIB1 edition, table II version, centre and indicator of
    parameter.

    """
    def _key(self, line):
        """Provides the sort key of the mappings order."""
        return _cfn(line)

    def msg_strings(self):
        return ('    CFName({standard_name!r}, {long_name!r}, '
                '{units!r})',
                'G1LocalParam({editionNumber}, {table2version}, '
                '{centre}, {indicatorOfParameter}),\n')

    def get_initial_id_nones(self):
        sourceid = {'standard_name': None, 'long_name': None}
        targetid = {}
        return sourceid, targetid

    @property
    def mapping_name(self):
        """
        Property that specifies the name of the dictionary to contain the
        encoding of this metarelate mapping translation.

        """
        return 'CF_TO_GRIB1_LOCAL'

    @property
    def source_scheme(self):
        """
        Property that specifies the name of the scheme for the source
        :class:`metarelate.Component` defining this metarelate mapping
        translation.

        """
        return FORMAT_URIS['cff']

    @property
    def target_scheme(self):
        """
        Property that specifies the name of the scheme for the target
        :class:`metarelate.Component` defining this metarelate mapping
        translation.

        """
        return FORMAT_URIS['gribm']

    def valid_mapping(self, mapping):
        """
        Determine whether the provided :class:`metarelate.Mapping` represents a
        CF phenomenon to GRIB1 local parameter translation.

        Args:
        * mapping:
            A :class:`metarelate.Mapping` instance.

        Returns:
            Boolean.

        """
        return self.is_cf(mapping.source) and \
            self.is_grib1_local_param(mapping.target)


class GRIB1LocalParamCFConstrainedMappings(Mappings):
    """
    Represents a container for GRIB (edition 1) local parameter to
    CF phenomenon and dimension coordinate constraint metarelate mapping
    translations.

    Encoding support is provided to generate the Python dictionary source
    code representation of these mappings from GRIB1 edition, table II version,
    centre and indicator of parameter to CF phenomenon standard name, long name
    and units, and CF dimension coordinate standard name, units and points.

    """
    def _key(self, line):
        """Provides the sort key of the mappings order."""
        return line.split(':')[0].strip()

    def msg_strings(self):
        return ('    G1LocalParam({editionNumber}, {table2version}, '
                '{centre}, {indicatorOfParameter})',
                '(CFName({standard_name!r}, '
                '{long_name!r}, {units!r}), '
                'DimensionCoordinate({dim_coord[standard_name]!r}, '
                '{dim_coord[units]!r}, {dim_coord[points]})),\n')

    def get_initial_id_nones(self):
        sourceid = {}
        targetid = {'standard_name': None, 'long_name': None}
        return sourceid, targetid

    @property
    def mapping_name(self):
        """
        Property that specifies the name of the dictionary to contain the
        encoding of this metarelate mapping translation.

        """
        return 'GRIB1_LOCAL_TO_CF_CONSTRAINED'

    @property
    def source_scheme(self):
        """
        Property that specifies the name of the scheme for the source
        :class:`metarelate.Component` defining this metarelate mapping
        translation.

        """
        return FORMAT_URIS['gribm']

    @property
    def target_scheme(self):
        """
        Property that specifies the name of the scheme for the target
        :class:`metarelate.Component` defining this metarelate mapping
        translation.

        """
        return FORMAT_URIS['cff']

    def valid_mapping(self, mapping):
        """
        Determine whether the provided :class:`metarelate.Mapping` represents a
        GRIB1 local parameter to CF phenomenon and dimension coordinate
        translation.

        Args:
        * mapping:
            A :class:`metarelate.Mapping` instance.

        Returns:
            Boolean.

        """
        return self.is_grib1_local_param(mapping.source) and \
            self.is_cf_constrained(mapping.target)


class CFConstrainedGRIB1LocalParamMappings(Mappings):
    """
    Represents a container for CF phenomenon and dimension coordinate
    constraint to GRIB (edition 1) local parameter metarelate mapping
    translations.

    Encoding support is provided to generate the Python dictionary source
    code representation of these mappings from CF phenomenon standard name,
    long name and units, and CF dimension coordinate standard name, units and
    points to GRIB1 edition, table II version, centre and indicator of
    parameter.

    """
    def _key(self, line):
        """Provides the sort key of the mappings order."""
        return line.split(':')[0].strip()

    def msg_strings(self):
        return ('    (CFName({standard_name!r}, '
                '{long_name!r}, {units!r}), '
                'DimensionCoordinate({dim_coord[standard_name]!r}, '
                '{dim_coord[units]!r}, {dim_coord[points]}))',
                'G1LocalParam({editionNumber}, {table2version}, '
                '{centre}, {indicatorOfParameter}),\n')

    def get_initial_id_nones(self):
        sourceid = {'standard_name': None, 'long_name': None}
        targetid = {}
        return sourceid, targetid

    @property
    def mapping_name(self):
        """
        Property that specifies the name of the dictionary to contain the
        encoding of this metarelate mapping translation.

        """
        return 'CF_CONSTRAINED_TO_GRIB1_LOCAL'

    @property
    def source_scheme(self):
        """
        Property that specifies the name of the scheme for the source
        :class:`metarelate.Component` defining this metarelate mapping
        translation.

        """
        return FORMAT_URIS['cff']

    @property
    def target_scheme(self):
        """
        Property that specifies the name of the scheme for the target
        :class:`metarelate.Component` defining this metarelate mapping
        translation.

        """
        return FORMAT_URIS['gribm']

    def valid_mapping(self, mapping):
        """
        Determine whether the provided :class:`metarelate.Mapping` represents a
        CF phenomenon and dimension coordinate to GRIB1 local parameter
        translation.

        Args:
        * mapping:
            A :class:`metarelate.Mapping` instance.

        Returns:
            Boolean.

        """
        return self.is_cf_constrained(mapping.source) and \
            self.is_grib1_local_param(mapping.target)


class GRIB2ParamCFMappings(Mappings):
    """
    Represents a container for GRIB (edition 2) parameter to CF phenomenon
    metarelate mapping translations.

    Encoding support is provided to generate the Python dictionary source
    code representation of these mappings from GRIB2 edition, discipline,
    parameter category and indicator of parameter to CF standard name,
    long name and units.

    """
    def _key(self, line):
        """Provides the sort key of the mappings order."""
        matchstr = ('^    G2Param\(([0-9]+), ([0-9]+), ([0-9]+), '
                    '([0-9]+)\):.*')
        match = re.match(matchstr, line)
        if match is None:
            raise ValueError('encoding not sortable')
        return [int(i) for i in match.groups()]

    def msg_strings(self):
        return ('    G2Param({editionNumber}, {discipline}, '
                '{parameterCategory}, {parameterNumber})',
                'CFName({standard_name!r}, {long_name!r}, '
                '{units!r}),\n')

    def get_initial_id_nones(self):
        sourceid = {}
        targetid = {'standard_name': None, 'long_name': None}
        return sourceid, targetid

    @property
    def mapping_name(self):
        """
        Property that specifies the name of the dictionary to contain the
        encoding of this metarelate mapping translation.

        """
        return 'GRIB2_TO_CF'

    @property
    def source_scheme(self):
        """
        Property that specifies the name of the scheme for the source
        :class:`metarelate.Component` defining this metarelate mapping
        translation.

        """
        return FORMAT_URIS['gribm']

    @property
    def target_scheme(self):
        """
        Property that specifies the name of the scheme for the target
        :class:`metarelate.Component` defining this metarelate mapping
        translation.

        """
        return FORMAT_URIS['cff']

    def valid_mapping(self, mapping):
        """
        Determine whether the provided :class:`metarelate.Mapping` represents a
        GRIB2 parameter to CF phenomenon translation.

        Args:
        * mapping:
            A :class:`metarelate.Mapping` instance.

        Returns:
            Boolean.

        """
        return self.is_grib2_param(mapping.source) and \
            self.is_cf(mapping.target)


class CFGRIB2ParamMappings(Mappings):
    """
    Represents a container for CF phenomenon to GRIB (edition 2) parameter
    metarelate mapping translations.

    Encoding support is provided to generate the Python dictionary source
    code representation of these mappings from CF standard name, long name
    and units to GRIB2 edition, discipline, parameter category and indicator
    of parameter.

    """
    def _key(self, line):
        """Provides the sort key of the mappings order."""
        return _cfn(line)

    def msg_strings(self):
        return ('    CFName({standard_name!r}, {long_name!r}, '
                '{units!r})',
                'G2Param({editionNumber}, {discipline}, '
                '{parameterCategory}, {parameterNumber}),\n')

    def get_initial_id_nones(self):
        sourceid = {'standard_name': None, 'long_name': None}
        targetid = {}
        return sourceid, targetid

    @property
    def mapping_name(self):
        """
        Property that specifies the name of the dictionary to contain the
        encoding of this metarelate mapping translation.

        """
        return 'CF_TO_GRIB2'

    @property
    def source_scheme(self):
        """
        Property that specifies the name of the scheme for the source
        :class:`metarelate.Component` defining this metarelate mapping
        translation.

        """
        return FORMAT_URIS['cff']

    @property
    def target_scheme(self):
        """
        Property that specifies the name of the scheme for the target
        :class:`metarelate.Component` defining this metarelate mapping
        translation.

        """
        return FORMAT_URIS['gribm']

    def valid_mapping(self, mapping):
        """
        Determine whether the provided :class:`metarelate.Mapping` represents a
        CF phenomenon to GRIB2 parameter translation.

        Args:
        * mapping:
            A :class:`metarelate.Mapping` instance.

        Returns:
            Boolean.

        """
        return self.is_cf(mapping.source) and \
            self.is_grib2_param(mapping.target)
