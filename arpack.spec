%global commit 8fc8fbe34991b97fb4326d7d34c3ff37c94cc770
%global shortcommit %(c=%{commit}; echo ${c:0:7})

Name:		arpack
Version:	3.2.0
Release:	1.%{shortcommit}git%{?dist}
Summary:	Fortran 77 subroutines for solving large scale eigenvalue problems
License:	BSD
Group:		Development/Libraries
URL:		https://github.com/opencollab/arpack-ng
Source0:	https://github.com/opencollab/arpack-ng/archive/%{commit}/arpack-ng-%{commit}.tar.gz
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)

BuildRequires:	gcc-gfortran
BuildRequires:	atlas-devel
Provides:	arpack-ng = %{version}-%{release}

%description
ARPACK is a collection of Fortran 77 subroutines designed to solve large 
scale eigenvalue problems. 

The package is designed to compute a few eigenvalues and corresponding
eigenvectors of a general n by n matrix A. It is most appropriate for
large sparse or structured matrices A where structured means that a
matrix-vector product w <- Av requires order n rather than the usual
order n**2 floating point operations. This software is based upon an
algorithmic variant of the Arnoldi process called the Implicitly
Restarted Arnoldi Method (IRAM).

%package devel
Summary:	Files needed for developing arpack based applications
Group:		Development/Libraries
Requires:	arpack = %{version}-%{release}
Provides:	arpack-ng-devel = %{version}-%{release}

%description devel
ARPACK is a collection of Fortran 77 subroutines designed to solve
large scale eigenvalue problems. This package contains the so
library links used for building arpack based applications.

%package doc
Summary:	Examples for the use of arpack
Group:		Documentation
%if 0%{?rhel} > 5 || 0%{?fedora} > 12
BuildArch: noarch
%endif

%description doc
This package contains examples for the use of arpack.

%package static
Summary:	Static library for developing arpack based applications
Group:		Development/Libraries
Requires:	arpack-devel = %{version}-%{release}
Provides:	arpack-ng-static = %{version}-%{release}

%description static
ARPACK is a collection of Fortran 77 subroutines designed to solve
large scale eigenvalue problems. This package contains the static
library and so links used for building arpack based applications.

%prep
%setup -q -n arpack-ng-%{commit} 

%build
export F77=gfortran
%if 0%{?fedora} >= 21 || 0%{?rhel} >= 7
%global atlaslib -L%{_libdir}/atlas -ltatlas
%else
%global atlaslib -L%{_libdir}/atlas -lf77blas -latlas
%endif
%configure --enable-shared --enable-static \
    --with-blas="%{atlaslib}" \
    --with-lapack="%{atlaslib}"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
make install DESTDIR=%{buildroot}
# Get rid of .la files
rm -r %{buildroot}%{_libdir}/*.la

%check
make %{?_smp_mflags} check
pushd EXAMPLES ; make clean ; popd

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(-,root,root,-)
%doc CHANGES COPYING
%{_libdir}/libarpack.so.*

%files devel
%defattr(-,root,root,-)
%{_libdir}/pkgconfig/arpack.pc
%{_libdir}/libarpack.so

%files doc
%defattr(-,root,root,-)
%doc EXAMPLES/ DOCUMENTS/

%files static
%defattr(-,root,root,-)
%{_libdir}/libarpack.a

%changelog
* Mon Sep 21 2015 Susi Lehtola <jussilehtola@fedoraproject.org> - 3.2.0-1.8fc8fbe3git
- Update source URL.
- Update to 3.2.0.

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.5-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Mar 06 2015 Dominik Mierzejewski <rpm@greysector.net> - 3.1.5-1
- update to 3.1.5
- fix source URL
- example binary is no longer installed by default
- enable tests
- don't duplicate documentation and examples in -devel
- clean binaries in EXAMPLES after running testsuite

* Fri Aug 15 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Sat Sep 21 2013 Orion Poplawski <orion@cora.nwra.com> - 3.1.3-2
- Rebuild for atlas 3.10 using threaded library

* Thu Sep 05 2013 Susi Lehtola <jussilehtola@fedoraproject.org> - 3.1.3-1
- Update to 3.1.3.

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed Feb 13 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Thu Jan 12 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.0.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Tue Dec 13 2011 Jussi Lehtola <jussilehtola@fedoraproject.org> - 3.0.1-1
- Change sources to arpack-ng, which provides an up-to-date version of ARPACK.
- Include examples and documentation in a new -doc package.

* Mon Feb 07 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.1-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Wed Jul  7 2010 Jussi Lehtola <jussilehtola@fedoraproject.org> - 2.1-12
- Bump spec to fix update path.

* Wed Apr  7 2010 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.1-11
- Change license to BSD (see RH bugs #234191 and #578873).

* Wed Sep 24 2008 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 2.1-10
- fix libarpack.so: undefined reference to `etime_' with recent gfortran

* Mon Aug 25 2008 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.1-9
- Patch0 and %%patch make recent rpm silenty fail.

* Wed May 21 2008 Tom "spot" Callaway <tcallawa@redhat.com> 2.1-8
- fix license tag

* Wed Oct 24 2007 Dominik 'Rathann' Mierzejewski <rpm@greysector.net> 2.1-7
- apply Frederic Hecht's patch for eigenvalue bug
- move static libs to separate package

* Mon Mar 26 2007 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.1-6
- Add license and clarification note
- Add lapack support

* Thu Nov  9 2006 Axel Thimm <Axel.Thimm@ATrpms.net> - 2.1-4
- Freshen up for submitting to fedora extras.
- Fix permissions of so file.
- Add forgotten ldconfig
- Remove dot from summaries.

* Wed Jul 16 2003 Axel Thimm <Axel.Thimm@ATrpms.net>
- Initial build.
