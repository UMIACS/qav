%define name qav
%define unmangled_name qav
%define release 1

Summary: Question Answer Validation
Name: %{python}-%{name}
Version: %{version}
Release: %{release}
Source0: %{unmangled_name}-%{version}.tar.gz
License: LGPL v2.1
Group: Development/Libraries
BuildRoot: %{_tmppath}/%{unmangled_name}-%{version}-%{release}-buildroot
Requires: %{python}
Requires: %{python}-netaddr
Prefix: %{_prefix}
BuildArch: noarch
Vendor: UMIACS Staff <staff@umiacs.umd.edu>
Url: https://github.com/UMIACS/qav

%description
qav is a Python library for console-based question and answering, with the
ability to validate input.

%prep
%setup -n %{unmangled_name}-%{version}

%build
%{python} setup.py build

%install
%{python} setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT --record=INSTALLED_FILES

%clean
rm -rf $RPM_BUILD_ROOT

%files -f INSTALLED_FILES
%defattr(-,root,root)
