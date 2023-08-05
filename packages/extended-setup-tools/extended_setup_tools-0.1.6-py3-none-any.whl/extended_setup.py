import os
import re
import sys
import unittest
from collections import namedtuple
from distutils.core import Command
from functools import partial
from glob import iglob
from io import StringIO
from typing import *
from unittest import TextTestRunner, TestResult

from setuptools import setup as setuptools_setup, find_packages
from typing.io import *

try:
    from typing import Literal
except ImportError:
    class _LiteralMeta(type):
        __slots__ = tuple()
        def __getitem__(self, item):
            if (not (isinstance(item, tuple))):
                item = (item, )
            return _Literal(*item)
    class _Literal(metaclass=_LiteralMeta):
        __slots__ = ('items', )
        def __init__(self, *items):
            self.items = items
        def __repr__(self) -> str:
            return f"Literal[{','.join(map(repr, self.items))}]"
    Literal = _Literal

_MISSING = object()

try:
    from functools import cached_property
except ImportError:
    from functools import wraps
    def cached_property(prop_func: Callable[[Any], Any]):
        @property
        @wraps(prop_func)
        def wrapper(self):
            cache_dict = getattr(self, '__cached_prop_cache__', _MISSING)
            if (cache_dict is _MISSING):
                cache_dict = dict()
                self.__cached_prop_cache__ = cache_dict
            
            cache = cache_dict.get(prop_func.__name__, _MISSING)
            if (cache is _MISSING):
                result = prop_func(self)
                cache_dict[prop_func.__name__] = result
            else:
                result = cache
            
            return result
        return wrapper

Version = Union[Tuple[int, ...], str]

TestReportFormat = Literal['xml', 'junit', 'html', 'default', 'text']
class ExtendedSetupManager:
    root_module_name: str
    sources_dir: str
    test_report_format: TestReportFormat
    
    def __init__(self, root_module_name: str, sources_dir: str = 'src', test_report_format: TestReportFormat = 'xml'):
        self.root_module_name = root_module_name
        self.sources_dir = sources_dir
        self.test_report_format = test_report_format
    
    def __repr__(self):
        fields = ', '.join(f'{f}={getattr(self, f)!r}' for f in self.__annotations__.keys())
        return f'{type(self).__qualname__}({fields})'
    
    # region Requirements
    @cached_property
    def requirements(self) -> List[str]:
        requirements = [ ]
        for r in [ 'requirements/requirements.txt', 'requirements.txt' ]:
            if (os.path.isfile(r)):
                with open(r) as f:
                    requirements = [ l.strip() for l in f ]
        
        return requirements
    
    @cached_property
    def setup_requirements(self) -> List[str]:
        setup_requires = [ 'wheel' ]
        for r in [ 'requirements/setup-requirements.txt', 'setup-requirements.txt' ]:
            if (os.path.isfile(r)):
                with open(r) as f:
                    setup_requires = [ l.strip() for l in f ]
        
        return setup_requires
    
    @property
    def default_test_requirements(self) -> List[str]:
        if (self.test_report_format in ('default', 'text')):
            return self.text_test_requirements
        elif (self.test_report_format in ('xml', 'junit')):
            return self.xml_test_requirements
        elif (self.test_report_format == 'html'):
            return self.html_test_requirements
        else:
            raise ValueError(f"Unsupported test report format: {self.test_report_format!r}")

    @property
    def text_test_requirements(self) -> List[str]:
        return [ ]
    
    @property
    def xml_test_requirements(self) -> List[str]:
        return [ 'lxml', 'unittest-xml-reporting' ]
    
    @property
    def html_test_requirements(self) -> List[str]:
        return [ 'html-testRunner' ]
    
    @cached_property
    def test_requirements(self) -> List[str]:
        tests_require = [ ]
        for r in [ 'requirements/test-requirements.txt', 'test-requirements.txt' ]:
            if (os.path.isfile(r)):
                with open(r) as f:
                    tests_require = [ l.strip() for l in f ]
        
        base_reqs = set(map(partial(re.compile(r'^([\w\-]+).*$', flags=re.M).sub, r'\1'), tests_require))
        for req in self.default_test_requirements:
            if (req not in base_reqs):
                tests_require.append(req)
        
        return tests_require
    
    @cached_property
    def extra_requirements(self) -> Dict[str, List[str]]:
        extras_require = { }
        for r in iglob('requirements/requirements-*.txt'):
            with open(r) as f:
                reqs = [ l.strip() for l in f ]
                feature_name = re.match(r'requirements-(.*)\.txt', os.path.basename(r)).group(1).title()
                extras_require[feature_name] = reqs
        extras_require.setdefault('test', self.test_requirements)
        extras_require.setdefault('all', sum(extras_require.values(), list()))
        
        return extras_require
    # endregion
    
    # region Init Script
    @property
    def init_script_file(self) -> TextIO:
        return open(os.path.join(self.sources_dir, self.root_module_name, '__init__.py'), 'rt')
    
    @cached_property
    def init_script_content(self) -> str:
        with self.init_script_file as f:
            return f.read()
    
    def find_in_init(self, key: str) -> Optional[str]:
        p = re.compile(rf'^__{key}__\s*=\s*(?P<quote>[\'"])(?P<data>.*?(?!(?P=quote)).)?(?P=quote)', re.MULTILINE)
        m = p.search(self.init_script_content)
        return m and m.group('data')
    
    @cached_property
    def name(self) -> str:
        return self.find_in_init('title')
    
    @cached_property
    def author(self) -> str:
        return self.find_in_init('author')
    
    @cached_property
    def raw_version(self) -> str:
        return self.find_in_init('version')
    
    @cached_property
    def version(self) -> str:
        version = self.raw_version
        if (version.endswith(('a', 'b', 'rc'))):
            # append version identifier based on commit count
            try:
                import subprocess
                p = subprocess.Popen(['git', 'rev-list', '--count', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = p.communicate()
                if out:
                    version += out.decode('utf-8').strip()
                p = subprocess.Popen(['git', 'rev-parse', '--short', 'HEAD'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = p.communicate()
                if out:
                    version += '+g' + out.decode('utf-8').strip()
            except Exception:
                pass
        
        return version

    @cached_property
    def licence(self) -> str:
        return self.find_in_init('license')
    # endregion
    
    # region Descriptions
    @property
    def readme_file(self) -> TextIO:
        for f in os.listdir('.'):
            name, sep, ext = f.rpartition('.')
            if (not sep): continue
            if (ext.lower() not in { 'md', 'markdown' }): continue
            if (name.lower() != 'readme'): continue
            
            return open(f, 'rt')
        # noinspection PyTypeChecker
        return StringIO \
(f'''
# Package {self.name}
 - Version: {self.version}
 - ReadMe: **TBD**
''')
    @cached_property
    def readme(self) -> str:
        with self.readme_file as f:
            return f.read()
    
    @cached_property
    def url_prefix(self):
        return 'https://gitlab.com/Hares-Lab/libraries/'
    @cached_property
    def url(self):
        return self.url_prefix + self.name
    # endregion
    
    # region Tests
    @property
    def test_output_dir(self) -> str:
        return os.path.abspath(os.path.join(self.root_dir, 'reports'))
    
    @property
    def test_runner(self) -> TextTestRunner:
        if (self.test_report_format in ('default', 'text')):
            return self.text_test_runner
        elif (self.test_report_format in ('xml', 'junit')):
            return self.xml_test_runner
        elif (self.test_report_format == 'html'):
            return self.html_test_runner
        else:
            raise ValueError(f"Unsupported test report format: {self.test_report_format!r}")
    
    @property
    def text_test_runner(self) -> TextTestRunner:
        return TextTestRunner()
    
    @property
    def xml_test_runner(self) -> TextTestRunner:
        from xmlrunner import XMLTestRunner
        
        test_runner = XMLTestRunner(output=self.test_output_dir)
        return test_runner
    
    @property
    def html_test_runner(self) -> TextTestRunner:
        from HtmlTestRunner.runner import HTMLTestRunner
        
        template = os.path.join(self.root_dir, 'test', 'report-template.html')
        if (not os.path.isfile(template)): template = None
        test_runner = HTMLTestRunner(template=template, combine_reports=False, output=self.test_output_dir)
        
        return test_runner
    
    def discover_and_run_tests(self, test_runner: TextTestRunner) -> TestResult:
        # get setup.py directory
        test_loader = unittest.defaultTestLoader
        test_suite = test_loader.discover(self.root_dir)
        test_result = test_runner.run(test_suite)
        
        return test_result
    
    @property
    def run_tests_command(self):
        def wrapper(_):
            test_runner = self.test_runner
            test_result = self.discover_and_run_tests(test_runner)
            exit(int(not test_result.wasSuccessful()))
        return wrapper
    
    @property
    def TestCommand(self) -> Type[Command]:
        manager = self
        
        try: from setuptools.command.test import test as _TestCommand
        except ImportError:
            from distutils.core import Command
            class TestCommandClass(Command):
                user_options = list()
                def initialize_options(self): pass
                def finalize_options(self): pass
                run = manager.run_tests_command
            _TestCommand = TestCommandClass
        
        else:
            class TestCommandClass(_TestCommand):
                def finalize_options(self):
                    super().finalize_options()
                    self.test_args = []
                    self.test_suite = True
                run_tests = manager.run_tests_command
        
        return TestCommandClass
    # endregion
    
    # region Dist Utils
    @cached_property
    def setup_file(self) -> str:
        return sys.modules['__main__'].__file__
    @cached_property
    def root_dir(self) -> str:
        return os.path.abspath(os.path.dirname(self.setup_file))
    
    @cached_property
    def packages(self) -> List[str]:
        return find_packages(self.sources_dir)
    
    @cached_property
    def packages_dir(self) -> Dict[str, str]:
        return { '': self.sources_dir }
    
    @cached_property
    def commands(self) -> Dict[str, Type[Command]]:
        return dict(test=self.TestCommand)
    # endregion
    
    def make_setup_kwargs(self, *, short_description: str, min_python_version: Optional[Version], namespace_packages: List[str] = _MISSING, **kwargs):
        own_kwargs = dict \
        (
            name = self.name,
            url = self.url,
            author = self.author,
            maintainer = self.author,
            version = self.version,
            license = self.licence,
            packages = self.packages,
            package_dir = self.packages_dir,
            cmdclass = self.commands,
            description = short_description,
            long_description = self.readme,
            long_description_content_type = 'text/markdown',
            include_package_data = True,
            setup_requires = self.setup_requirements,
            install_requires = self.requirements,
            tests_require = self.test_requirements,
            extras_require = self.extra_requirements,
        )
        
        if (isinstance(min_python_version, tuple)):
            min_python_version = '.'.join(min_python_version)
        if (isinstance(min_python_version, str)):
            own_kwargs['python_requires'] = f'>={min_python_version}'
        if (namespace_packages is not _MISSING):
            own_kwargs['packages'] = list(set(self.packages) - set(namespace_packages)),
            own_kwargs['namespace_packages'] = namespace_packages
        
        own_kwargs.update(kwargs)
        
        author_email = kwargs.get('author_email', _MISSING)
        maintainer_email = kwargs.get('maintainer_email', _MISSING)
        if (author_email is _MISSING != maintainer_email is _MISSING and own_kwargs['author'] == own_kwargs['maintainer']):
            if (author_email is _MISSING):
                own_kwargs['author_email'] = own_kwargs['maintainer_email']
            else:
                own_kwargs['maintainer_email'] = own_kwargs['author_email']
        
        return own_kwargs
    
    def setup(self, *, short_description: str, classifiers: List[str], min_python_version: Optional[Version] = None, **kwargs):
        return setuptools_setup(**self.make_setup_kwargs(short_description=short_description, classifiers=classifiers, min_python_version=min_python_version, **kwargs))


class SingleScriptModuleSetup(ExtendedSetupManager):
    script_name: str
    
    def __init__(self, script_name: str):
        super(SingleScriptModuleSetup, self).__init__(script_name, '.')
        self.script_name = script_name
    
    @property
    def init_script_file(self) -> TextIO:
        return open(f'{self.script_name}.py')
    
    def make_setup_kwargs(self, **kwargs):
        result = super().make_setup_kwargs(**kwargs)
        result.pop('packages', None)
        result.pop('package_dir', None)
        result.setdefault('py_modules', [ self.script_name ])
        return result


__title__ = 'extended-setup-tools'
__author__ = 'Peter Zaitcev / USSX Hares'
__license__ = 'BSD 2-clause'
__copyright__ = 'Copyright 2021 Peter Zaitcev'
__version__ = '0.1.6'

VersionInfo = namedtuple('VersionInfo', 'major minor micro releaselevel serial')
version_info = VersionInfo(*__version__.split('.'), releaselevel='alpha', serial=0)


__all__ = \
[
    'version_info',
    '__title__',
    '__author__',
    '__license__',
    '__copyright__',
    '__version__',
    
    'ExtendedSetupManager',
    'SingleScriptModuleSetup',
]


# The following fields are still missing:
# - author_email = None     | These are half-supported.
# - maintainer = None       | These are half-supported. Same as Author
# - maintainer_email = None | These are half-supported. Author email and Maintainer email are synchronized if Author and Maintainer are the same person
# - download_url = None
# - keywords = None
# - license = None
# - license_file = None
# - license_files = [ 'LICENSE' ]
# - obsoletes = None
# - platforms = None
# - project_urls = {}
# - provides = None
# - provides_extras = OrderedSet()
# - requires = None
