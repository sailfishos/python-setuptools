Name:           python3-setuptools
# When updating, update the bundled libraries versions bellow!
Version:        69.0.2
Release:        1
Summary:        Easily build and distribute Python packages
# setuptools is MIT
# platformdirs is MIT
# more-itertools is MIT
# ordered-set is MIT
# packaging is BSD-2-Clause OR Apache-2.0
# importlib-metadata is Apache-2.0
# importlib-resources is Apache-2.0
# jaraco.text is MIT
# typing-extensions is Python-2.0.1
# zipp is MIT
# nspektr is MIT
# tomli is MIT
# the setuptools logo is MIT
License:        MIT and (BSD or ASL 2.0)
URL:            https://pypi.python.org/pypi/setuptools
Source0:        %{name}-%{version}.tar.gz
Source1:        bootstrap.py

BuildArch:      noarch

BuildRequires:  gcc

BuildRequires:  python3-devel
BuildRequires:  python3-rpm-macros

# Virtual provides for the packages bundled by setuptools.
# You can find the versions in setuptools/setuptools/_vendor/vendored.txt
%global bundled %{expand:
Provides: bundled(python3dist(importlib_metadata)) = 6.0.0
Provides: bundled(python3dist(importlib_resources)) = 5.10.2
Provides: bundled(python3dist(jaraco.text)) = 3.7.0
Provides: bundled(python3dist(more_itertools)) = 8.8.0
Provides: bundled(python3dist(ordered-set)) = 3.1.1
Provides: bundled(python3dist(packaging)) = 23.1
Provides: bundled(python3dist(tomli)) = 2.0.1
Provides: bundled(python3dist(typing_extensions)) = 4.0.1
Provides: bundled(python3dist(zipp)) = 3.7.0
}

%{bundled}

Provides:       python3dist(setuptools) = %{version}
Provides:       python%{python3_version}dist(setuptools) = %{version}

%description
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
# Simplify egg_info tag to make build reproducible
sed -i 's/tag_build = .post/tag_build =/' setup.cfg
sed -i 's/tag_date = 1/tag_date = 0/' setup.cfg

%{__cp} %{SOURCE1} .

%build
# Warning, different bootstrap meaning here, has nothing to do with our bcond
# This bootstraps .egg-info directory needed to build setuptools
%{__python3} bootstrap.py

%py3_build

%install
%py3_install

# This is not installed (in 45.2.0 anyway), but better be safe than sorry
#rm -rf %{buildroot}%{python3_sitelib}/{setuptools,pkg_resources}/tests

find %{buildroot}%{python3_sitelib} -name '*.exe' | xargs rm -f

%files
%license LICENSE
%{python3_sitelib}/distutils-precedence.pth
%{python3_sitelib}/pkg_resources/
%{python3_sitelib}/setuptools*/
%{python3_sitelib}/_distutils_hack/
