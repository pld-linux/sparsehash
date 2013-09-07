#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	Extremely memory-efficient C++ hash_map implementation
Name:		sparsehash
Version:	2.0.2
Release:	1
License:	BSD
Group:		Development/Libraries
Source0:	http://sparsehash.googlecode.com/files/%{name}-%{version}.tar.gz
# Source0-md5:	1db92ed7f257d9b5f14a309d75e8a1d4
URL:		http://code.google.com/p/sparsehash
%{?with_tests:BuildRequires:	libstdc++-devel}
%{?with_tests:BuildRequires:	libtcmalloc-devel}
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Google SparseHash project contains several C++ template hash-map
implementations with different performance characteristics, including
an implementation that optimizes for space and one that optimizes for
speed.

# all files are in -devel package
%package devel
Summary:	Extremely memory-efficient C++ hash_map implementation
Group:		Development/Libraries
Requires:	libstdc++-devel

%description devel
The Google SparseHash project contains several C++ template hash-map
implementations with different performance characteristics, including
an implementation that optimizes for space and one that optimizes for
speed.

%prep
%setup -q

%build
%configure \
	--host=%{_host} \
	--build=%{_host}

# clearing noinst_PROGRAMS helps not to build targets for tests
%{__make} \
	noinst_PROGRAMS=

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	noinst_PROGRAMS= \
	DESTDIR=$RPM_BUILD_ROOT

# Remove unneeded files
rm $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/INSTALL
rm $RPM_BUILD_ROOT%{_docdir}/%{name}-%{version}/README_windows.txt

# make noarch
install -d $RPM_BUILD_ROOT%{_npkgconfigdir}
mv $RPM_BUILD_ROOT{%{_pkgconfigdir},%{_npkgconfigdir}}/libsparsehash.pc
%{__sed} -i -e '/libdir/d' $RPM_BUILD_ROOT%{_npkgconfigdir}/libsparsehash.pc

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc %{_docdir}/sparsehash-%{version}
%{_includedir}/sparsehash
%{_npkgconfigdir}/libsparsehash.pc

# legacy headers under google subdir
%dir %{_includedir}/google
%{_includedir}/google/dense_hash_map
%{_includedir}/google/dense_hash_set
%{_includedir}/google/sparse_hash_map
%{_includedir}/google/sparse_hash_set
%{_includedir}/google/sparsetable
%{_includedir}/google/template_util.h
%{_includedir}/google/type_traits.h
%{_includedir}/google/sparsehash
