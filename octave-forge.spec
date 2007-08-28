Name:           octave-forge
Version:        2006.07.09
Release:        %mkrel 2
Epoch:          0
Summary:        Contributed functions for octave
Group:          Sciences/Mathematics
License:        Public Domain
URL:            http://octave.sourceforge.net/
## Source0:     http://umn.dl.sourceforge.net/sourceforge/octave/%{name}-%{version}.tar.gz
## The original sources contain a non-free tree of functions that are
## GPL incompatible. A patched version with the non-free sources removed
## is created as follows:
## tar xf octave-forge-%{version}.tar.gz
## rm -r octave-forge-%{version}/nonfree/
## tar czf octave-forge-%{version}.patched.tar.gz octave-forge-%{version}
## rm -r octave-forge-%{version}
Source0:        %{name}-%{version}.patched.tar.gz
Patch0:         octave-forge-2006.07.09-legend.patch
Patch1:         octave-forge-2006.07.09-imread.patch
Patch2:         octave-forge-2006.07.09-path.patch
Requires:       ImageMagick
Requires:       octave3
#Requires:      octave(api) = api-v24
BuildRequires:  gcc-gfortran
BuildRequires:  ginac-devel
BuildRequires:  gsl-devel
BuildRequires:  ImageMagick-devel
BuildRequires:  libjpeg-devel
BuildRequires:  libnc-dap-devel
BuildRequires:  libpng-devel
BuildRequires:  ncurses-devel
BuildRequires:  octave3-devel
BuildRequires:  pcre-devel
BuildRequires:  qhull-devel
BuildRequires:  tetex
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
%patch0 -p0
%patch1 -p0
%patch2 -p0
# For octave >= 2.9.7, don't install the mex stuff or path stuff
touch extra/mex/NOINSTALL
touch main/path/NOINSTALL

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

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%doc COPYING* README RELEASE-NOTES TODO
%doc doc/*.html doc/coda/*.sgml doc/coda/appendices/*.sgml
%doc doc/coda/oct/*.sgml doc/coda/standalone/*.sgml
%{_datadir}/octave/*
%{_libexecdir}/octave/*
