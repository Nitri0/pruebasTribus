import re, apt_pkg, debian.deb822, hashlib, email
from gatherer import aux

apt_pkg.init()

class packages_gatherer(object):
    "This class imports the data from Packages.gz files into the database"
    # For efficiency, these are dictionaries
    # mandatory: list of fields which each package has to provide
    # non_mandatory: list of fields which are possibly provided by packages
    # ignorable: fields which are not useful for the database,
    #            but for which no warning should be printed
    mandatory = {'Package': 0, 'Version': 0, 'Architecture': 0, 'Maintainer': 0,
        'Description': 0}
    non_mandatory = {'Source': 0, 'Essential': 0, 'Depends': 0, 'Recommends': 0,
        'Suggests': 0, 'Enhances': 0, 'Pre-Depends': 0, 'Breaks':0, 'Installed-Size': 0,
        'Homepage': 0, 'Size': 0, 'Build-Essential':0, 'Origin':0,
        'SHA1':0, 'Replaces':0, 'Section':0, 'MD5sum':0, 'Bugs':0, 'Priority':0,
        'Tag':0, 'Task':0, 'Python-Version':0, 'Ruby-Versions':0, 'Provides':0, 'Conflicts':0,
        'SHA256':0, 'Original-Maintainer':0, 'Description-md5':0}
    ignorable = {'Modaliases':0, 'Filename':0, 'Npp-Filename':0, 'Npp-Name':0, 'Npp-Mimetype':0, 'Npp-Applications':0, 'Python-Runtime':0, 'Npp-File':0, 'Npp-Description':0, 'Url':0, 'Gstreamer-Elements':0, 'Gstreamer-Version':0, 'Gstreamer-Decoders':0, 'Gstreamer-Uri-Sinks':0, 'Gstreamer-Encoders':0, 'Gstreamer-Uri-Sources':0, 'url':0, 'Vdr-PatchLevel':0, 'Vdr-Patchlevel':0, 'originalmaintainer':0, 'Originalmaintainer':0, 'Build-Recommends':0, 'Multi-Arch':0, 'Maintainer-Homepage':0, 'Tads2-Version':0, 'Tads3-Version':0, 'Xul-Appid': 0, 'Subarchitecture':0, 'Package-Type':0, 'Kernel-Version': 0, 'Installer-Menu-Item':0, 'Supported':0, 'subarchitecture':0, 'package-type':0, 'Python3-Version':0, 'Built-Using':0, 'Lua-Versions':0, 'SHA512':0,'Ruby-Version':0, 'MD5Sum': 0, 'Apport':0, 'Ubuntu-Webapps-Domain':0, 'Ubuntu-Webapps-Name':0, 'Ubuntu-Webapps-Includes':0 }
    ignorable_re = re.compile("^(Orig-|Original-|Origianl-|Orginal-|Orignal-|Orgiinal-|Orginial-|Debian-|X-Original-|Upstream-)")
    
    pkgquery = """EXECUTE package_insert
        (%(Package)s, %(Version)s, %(Architecture)s, %(Maintainer)s, %(maintainer_name)s, %(maintainer_email)s,
        %(Description)s, %(Description-md5)s, %(Source)s, %(Source_Version)s, %(Essential)s,
        %(Depends)s, %(Recommends)s, %(Suggests)s, %(Enhances)s,
        %(Pre-Depends)s, %(Breaks)s, %(Installed-Size)s, %(Homepage)s, %(Size)s,
        %(Build-Essential)s, %(Origin)s, %(SHA1)s,
        %(Replaces)s, %(Section)s, %(MD5sum)s, %(Bugs)s, %(Priority)s,
        %(Tag)s, %(Task)s, %(Python-Version)s, %(Ruby-Versions)s, %(Provides)s,
        %(Conflicts)s, %(SHA256)s, %(Original-Maintainer)s)"""
    
    descriptionquery = """EXECUTE description_insert
        (%(Package)s, %(Language)s,
        %(Description)s, %(Long_Description)s, %(Description-md5)s)"""
    
    def __init__(self):
        #gatherer.__init__(self, connection, config, source)
        # The ID for the distribution we want to include
        self._distr = None
        #self.assert_my_config('directory', 'archs', 'release', 'components', 'distribution', 'packages-table', 'packages-schema')
        self.warned_about = {}
        # A mapping from <package-name><version> to 1 If <package-name><version> is
        # included in this dictionary, this means, that we've already added this
        # package with this version for architecture 'all' to the database. Needed
        # because different architectures include packages for architecture 'all'
        # with the same version, and we don't want these duplicate entries
        self.imported_all_pkgs = {}
        self.add_descriptions = False
        
    def assert_my_config(self, *keywords):
        for k in keywords:
            if not k in self.my_config:
                raise aux.ConfigException("%s not specified for source %s" % (k, self.source))
        
    def build_dict(self, control):
        """
        Build a dictionary from the control dictionary.
        Influenced by class variables mandatory, non_mandatory and ignorable
        """
        d = {}
        for k in packages_gatherer.mandatory:
            if k not in control:
                print "Mandatory field %s not specified" % k
            d[k] = control[k]
        for k in packages_gatherer.non_mandatory:
            if k in control:
                d[k] = control[k]
            else:
                d[k] = None
        for k in control.iterkeys():
            if k not in packages_gatherer.non_mandatory and k not in packages_gatherer.mandatory and k not in packages_gatherer.ignorable and not (packages_gatherer.ignorable_re.match(k)):
                if k not in self.warned_about:
                    self.warned_about[k] = 1
                else:
                    self.warned_about[k] += 1
        return d
    
    def import_packages(self, sequence, cur = None):
        """
        Import the packages from the sequence into the database-connection
        conn. Sequence has to have an iterator interface, that yields a line every time
        it is called.The Format of the sequence is expected to be that of a debian packages file.
        """
        pkgs = []
        pkgdescs = []
        # The fields that are to be read. Other fields are ignored
        for control in debian.deb822.Packages.iter_paragraphs(sequence):
        # Check whether packages with architectue 'all' have already been
        # imported
            t = control['Package'] + '_' + control['Version'] + '_' + control['Architecture']
            if t in self.imported_all_pkgs:
                continue
            self.imported_all_pkgs[t] = 1
            d = self.build_dict(control)
            
            # We split the description
            if 'Description' in d:
                if self.add_descriptions and ('Description-md5' not in d or not d['Description-md5']):
                    try:
                        d['Description-md5'] = hashlib.md5((d['Description']+"\n").encode('utf-8')).hexdigest()
                        d['Language'] = 'en'
                        pkgdescs.append(d)
                    except UnicodeEncodeError:
                        self.warned_about['%s description encoding' % d['Package']] = 1
            if len(d['Description'].split("\n",1)) > 1:
                d['Long_Description'] = d['Description'].split("\n",1)[1]
            else:
                d['Long_Description'] = ''
            d['Description'] = d['Description'].split("\n",1)[0]
            # Calculate Description-md5 for releases that don't include it
    
            # Convert numbers to numbers
            for f in ['Installed-Size', 'Size']:
                if d[f] is not None:
                    d[f] = int(d[f])
            
            # Source is non-mandatory, but we don't want it to be NULL
#             if d['Source'] is None:
#                 d['Source'] = d['Package']
#                 d['Source_Version'] = d['Version']
#             else:
#                 split = d['Source'].strip("'").split()
#             if len(split) == 1:
#                 d['Source_Version'] = d['Version']
#             else:
#                 d['Source'] = split[0]
#                 d['Source_Version'] = split[1].strip("()")
 
            d['maintainer_name'], d['maintainer_email'] = email.Utils.parseaddr(d['Maintainer'])
            pkgs.append(d)
        
        return pkgs, pkgdescs 

#a1 = file('/home/fran/Packages')
#pg = packages_gatherer()
#pq, pqd = pg.import_packages(a1)
#print "Termine =)"
#for i in pq:
#    print i



