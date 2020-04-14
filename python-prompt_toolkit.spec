#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_without	tests	# unit tests
%bcond_without	python2 # CPython 2.x module
%bcond_without	python3 # CPython 3.x module

%define 	module	prompt_toolkit
Summary:	Library for building powerful interactive command lines in Python
Summary(pl.UTF-8):	Biblioteka do budowania interaktywnych wierszy poleceń w Pythonie
Name:		python-%{module}
# keep 1.x here (2.x is not supported by ipython for python2, 3.x drops python2 support)
Version:	1.0.18
Release:	1
License:	BSD
Group:		Libraries/Python
#Source0Download: https://github.com/prompt-toolkit/python-prompt-toolkit/releases
Source0:	https://github.com/jonathanslenders/python-prompt-toolkit/archive/%{version}/python-prompt-toolkit-%{version}.tar.gz
# Source0-md5:	1b800e5f190572d7a13bda45b7de058a
URL:		https://github.com/jonathanslenders/python-prompt-toolkit
%if %{with python2}
BuildRequires:	python-modules >= 1:2.6
BuildRequires:	python-setuptools
BuildRequires:	python-six >= 1.9.0
BuildRequires:	python-wcwidth
%if %{with tests}
BuildRequires:	python-pytest
%endif
%endif
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools
BuildRequires:	python3-six >= 1.9.0
BuildRequires:	python3-wcwidth
%if %{with tests}
BuildRequires:	python3-pytest
%endif
%endif
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.714
BuildRequires:	sed >= 4.0
%if %{with doc}
BuildRequires:	sphinx-pdg
%endif
Requires:	python-modules >= 1:2.6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
prompt_toolkit is a library for building powerful interactive command
lines and terminal applications in Python.

%description -l pl.UTF-8
prompt_toolkit to biblioteka do tworzenia interaktywnych wierwszy
poleceń i aplikacji terminalowych w Pythonie.

%package -n python3-%{module}
Summary:	Library for building powerful interactive command lines in Python
Summary(pl.UTF-8):	Biblioteka do budowania interaktywnych wierszy poleceń w Pythonie
Group:		Libraries/Python
Requires:	python3-modules >= 1:3.3

%description -n python3-%{module}
prompt_toolkit is a library for building powerful interactive command
lines and terminal applications in Python.

%description -n python3-%{module} -l pl.UTF-8
prompt_toolkit to biblioteka do tworzenia interaktywnych wierwszy
poleceń i aplikacji terminalowych w Pythonie.

%package apidocs
Summary:	API documentation for prompt_toolkit module
Summary(pl.UTF-8):	Dokumentacja API modułu prompt_toolkit
Group:		Documentation

%description apidocs
API documentation for prompt_toolkit module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu prompt_toolkit.

%prep
%setup -q -n python-prompt-toolkit-%{version}

%build
%if %{with python2}
%py_build

%if %{with tests}
# tests expect 
TERM=xterm \
%{__python} -m pytest tests
%endif
%endif

%if %{with python3}
%py3_build

%if %{with tests}
# test_print_tokens expects sequences emitted for xterm
TERM=xterm \
%{__python3} -m pytest tests
%endif
%endif

%if %{with doc}
%{__make} -C docs html
%endif

%install
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%py_install

%py_postclean
%endif

%if %{with python3}
%py3_install
%endif

%if %{with python2}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
cp -pr examples/* $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|/usr/bin/env python|%{__python}|'
%endif
%if %{with python3}
install -d $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
cp -pr examples/* $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version}
find $RPM_BUILD_ROOT%{_examplesdir}/python3-%{module}-%{version} -name '*.py' \
	| xargs sed -i '1s|/usr/bin/env python|%{__python3}|'
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%if %{with python2}
%files
%defattr(644,root,root,755)
%doc AUTHORS.rst CHANGELOG LICENSE README.rst
%{py_sitescriptdir}/prompt_toolkit
%{py_sitescriptdir}/prompt_toolkit-%{version}-py*.egg-info
%{_examplesdir}/python-%{module}-%{version}
%endif

%if %{with python3}
%files -n python3-%{module}
%defattr(644,root,root,755)
%doc AUTHORS.rst CHANGELOG LICENSE README.rst
%{py3_sitescriptdir}/prompt_toolkit
%{py3_sitescriptdir}/prompt_toolkit-%{version}-py*.egg-info
%{_examplesdir}/python3-%{module}-%{version}
%endif

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/_build/html/{_images,_static,pages,*.html,*.js}
%endif
