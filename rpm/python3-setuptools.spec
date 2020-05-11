Name:           python3-setuptools
# When updating, update the bundled libraries versions bellow!
Version:        46.1.3
Release:        1
Summary:        Easily build and distribute Python packages
# setuptools is MIT
# packaging is BSD or ASL 2.0
# pyparsing is MIT
# six is MIT
# ordered-set is MIT
License:        MIT and (BSD or ASL 2.0)
URL:            https://pypi.python.org/pypi/setuptools
Source0:        %{name}-%{version}.tar.gz

BuildArch:      noarch

BuildRequires:  gcc

BuildRequires:  python3-devel
BuildRequires:  python3-rpm-macros

%description
Setuptools is a collection of enhancements to the Python distutils that allow
you to more easily build and distribute Python packages, especially ones that
have dependencies on other packages.

This package also contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.

# Virtual provides for the packages bundled by setuptools.
# You can find the versions in setuptools/setuptools/_vendor/vendored.txt
%global bundled %{expand:
Provides: bundled(python3dist(packaging)) = 19.2
Provides: bundled(python3dist(pyparsing)) = 2.2.1
Provides: bundled(python3dist(six)) = 1.10.0
Provides: bundled(python3dist(ordered-set)) = 3.1.1
}

Summary:        Easily build and distribute Python 3 packages
Conflicts:      python-setuptools < %{version}-%{release}
%{?python_provide:%python_provide python3-setuptools}
%{bundled}

Provides:       python3dist(setuptools) = %{version}
Provides:       python%{python3_version}dist(setuptools) = %{version}


Setuptools is a collection of enhancements to the Python 3 distutils that allow
you to more easily build and distribute Python 3 packages, especially ones that
have dependencies on other packages.

This package also contains the runtime components of setuptools, necessary to
execute the software that requires pkg_resources.

%prep
%autosetup -p1 -n %{name}-%{version}/setuptools

# Strip shbang
find setuptools pkg_resources -name \*.py | xargs sed -i -e '1 {/^#!\//d}'
# Remove bundled exes
rm -f setuptools/*.exe
# These tests require internet connection
rm setuptools/tests/test_integration.py 
# We don't do linting here
sed -i 's/ --flake8//' pytest.ini

%build
# Warning, different bootstrap meaning here, has nothing to do with our bcond
# This bootstraps .egg-info directory needed to build setuptools
%{__python3} bootstrap.py

%py3_build

%install
%py3_install

# This is not installed (in 45.2.0 anyway), but better be safe than sorry
rm -rf %{buildroot}%{python3_sitelib}/{setuptools,pkg_resources}/tests

find %{buildroot}%{python3_sitelib} -name '*.exe' | xargs rm -f

%files
%license LICENSE
%{python3_sitelib}/easy_install.py
%{python3_sitelib}/pkg_resources/
%{python3_sitelib}/setuptools*/
%{python3_sitelib}/__pycache__/*
%{_bindir}/easy_install
%{_bindir}/easy_install-3.*
