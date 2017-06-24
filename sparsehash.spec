#
# Conditional build:
%bcond_without	tests		# build without tests

Summary:	C++ associative containers
Summary(pl.UTF-8):	Kontenery asocjacyjne dla C++
Name:		sparsehash
Version:	2.0.3
Release:	1
License:	BSD
Group:		Development/Libraries
#Source0Download: https://github.com/sparsehash/sparsehash/releases
Source0:	https://github.com/sparsehash/sparsehash/archive/%{name}-%{version}.tar.gz
# Source0-md5:	d8d5e2538c1c25577b3f066d7a55e99e
URL:		https://github.com/sparsehash/sparsehash
%{?with_tests:BuildRequires:	libstdc++-devel}
%{?with_tests:BuildRequires:	libtcmalloc-devel}
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%if %{_host_cpu} == "x32"
%define build_arch %{_target_platform}
%else
%define build_arch %{_host}
%endif

%description
The Google SparseHash project contains several C++ template hash-map
implementations with different performance characteristics, including
an implementation that optimizes for space and one that optimizes for
speed.

%description -l pl.UTF-8
Projekt Google SparseHash zawiera kilka implementacji struktury
hash-map w szablonach C++ z różną charakterystyką wydajności, w tym
implementację zoptymalizowaną pod kątem miejsca oraz drugą,
zoptymalizowaną pod kątem szybkości.

# all files are in -devel package
%package devel
Summary:	C++ associative containers
Summary(pl.UTF-8):	Kontenery asocjacyjne dla C++
Group:		Development/Libraries
Requires:	libstdc++-devel

%description devel
The Google SparseHash project contains several C++ template hash-map
implementations with different performance characteristics, including
an implementation that optimizes for space and one that optimizes for
speed.

%description devel -l pl.UTF-8
Projekt Google SparseHash zawiera kilka implementacji struktury
hash-map w szablonach C++ z różną charakterystyką wydajności, w tym
implementację zoptymalizowaną pod kątem miejsca oraz drugą,
zoptymalizowaną pod kątem szybkości.

%prep
%setup -q -n %{name}-%{name}-%{version}

%build
%configure \
	ac_cv_header_google_malloc_extension_h=no \
	--host=%{build_arch} \
	--build=%{build_arch}

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

# packaged as %doc
%{__rm} -r $RPM_BUILD_ROOT%{_docdir}/%{name}-2.0.2

# make noarch
install -d $RPM_BUILD_ROOT%{_npkgconfigdir}
%{__mv} $RPM_BUILD_ROOT{%{_pkgconfigdir},%{_npkgconfigdir}}/libsparsehash.pc
%{__sed} -i -e '/libdir/d' $RPM_BUILD_ROOT%{_npkgconfigdir}/libsparsehash.pc

%clean
rm -rf $RPM_BUILD_ROOT

%files devel
%defattr(644,root,root,755)
%doc AUTHORS COPYING ChangeLog NEWS README TODO doc/*
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
