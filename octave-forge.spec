%define octave_api api-v32

Name:           octave-forge
Version:        2006.07.09
Release:        %mkrel 6
Epoch:          0
Summary:        Contributed functions for octave
Group:          Sciences/Mathematics
License:        Public Domain
URL:            http://octave.sourceforge.net/
Source0:        %{name}-%{version}.patched.tar.gz
Patch0:         octave-forge-2006.07.09-legend.patch
Patch1:         octave-forge-2006.07.09-imread.patch
Patch2:         octave-forge-2006.07.09-path.patch
Patch3:         octave-forge-2006.07.09-configure.patch
Patch4:         octave-forge-2006.07.09-octave3.patch
Requires:       ImageMagick
Requires:       octave3
Requires:       octave(api) = %{octave_api}
BuildRequires:  cvs2cl
BuildRequires:  gcc-gfortran
BuildRequires:  ginac-devel
BuildRequires:  gsl-devel
BuildRequires:  ImageMagick-devel
BuildRequires:  latex2html
BuildRequires:  jpeg-devel
BuildRequires:  nc-dap-devel
BuildRequires:  ncurses-devel
BuildRequires:  png-devel
BuildRequires:  octave-devel
BuildRequires:  octave(api) = %{octave_api}
BuildRequires:  pcre-devel
BuildRequires:  qhull-devel
BuildRequires:  tetex
BuildRequires:  tetex-latex
BuildRequires:  tetex-dvipdfm
BuildRequires:  tetex-dvips
BuildRequires:  tetex-texi2html
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

%description
Octave-forge is a community project for collaborative development of
octave extensions. The extensions in this package include additional
data types such as sparse matrices, and functions for a variety of
different applications including signal and image processing,
communications, control, optimization, statistics, geometry, and
symbolic math.

%prep
%setup -q
%{_bindir}/find . -name '*.cc' | %{_bindir}/xargs -t %{__perl} -pi -e 's|HAVE_OCTAVE_29|HAVE_OCTAVE_30|g'
%patch0 -p0
%patch1 -p0
%patch2 -p0
%patch3 -p0
%patch4 -p0
/bin/touch extra/MacOSX/NOINSTALL
/bin/touch extra/testfun/NOINSTALL
/bin/touch extra/mex/NOINSTALL

%build
ALTMPATHNAME=%{_datadir}/octave/site/octave-forge-alternatives/m/octave-forge
XPATHNAME=`%{_bindir}/octave-config -p LOCALARCHLIBDIR`/octave-forge
%{configure2_5x} --with-altmpath=$ALTMPATHNAME --with-xpath=$XPATHNAME
%{make}

%install
%{__rm} -rf %{buildroot}

ALTPATHNAME=octave/site/octave-forge-alternatives
HOSTTYPE=`%{_bindir}/octave-config -p CANONICAL_HOST_TYPE`
%{makeinstall_std} \
  MPATH=`%{_bindir}/octave-config -p LOCALFCNFILEDIR`/octave-forge \
  OPATH=`%{_bindir}/octave-config -p LOCALAPIOCTFILEDIR`/octave-forge \
  XPATH=`%{_bindir}/octave-config -p LOCALARCHLIBDIR`/octave-forge \
  ALTPATH=%{_datadir}/$ALTPATHNAME/m \
  ALTMPATH=%{_datadir}/$ALTPATHNAME/m/octave-forge \
  ALTOPATH=%{_libexecdir}/$ALTPATHNAME/oct/$HOSTTYPE

# XXX: see http://qa.mandriva.com/show_bug.cgi?id=35790
%{__rm} %{buildroot}%{_datadir}/octave/site/m/octave-forge/plot/drawnow.m

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING* README RELEASE-NOTES TODO
%doc doc/*.html doc/coda/*.sgml doc/coda/appendices/*.sgml
%doc doc/coda/oct/*.sgml doc/coda/standalone/*.sgml
%{_datadir}/octave/*
%{_libexecdir}/octave/*
