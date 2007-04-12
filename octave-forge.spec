%define octave_version 2.1.73
%define qhull_version 2003.1
# (Abel) GiNaC <= 1.3.0-1mdk placed header at fantastic location
%define ginac_version 1.3.2

Name:		octave-forge
Version:	2006.03.17
Release:	%mkrel 3
Epoch:		0
Summary:	Custom scripts, functions and extensions for GNU Octave
License:	Public Domain
Group:		Sciences/Mathematics
Source0:	http://download.sourceforge.net/octave/%{name}-%{version}.tar.bz2
Patch0:		%{name}-2005.06.13-legend.patch
URL:		http://octave.sourceforge.net/
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot
Requires:	octave >= %{octave_version}
Requires:	libqhull >= %{qhull_version}
BuildRequires:	gsl-devel
BuildRequires:	gcc-c++
BuildRequires:	gcc-gfortran
BuildRequires:	ginac-devel >= %{ginac_version}
BuildRequires:	hdf5-devel
BuildRequires:	jpeg-devel
BuildRequires:	lapack-devel
BuildRequires:	libcln-devel
BuildRequires:	libfftw-devel
BuildRequires:	libqhull-devel >= %{qhull_version}
BuildRequires:	libreadline-devel
BuildRequires:	ncurses-devel
BuildRequires:	octave >= %{octave_version}
BuildRequires:	pcre-devel
BuildRequires:	png-devel
BuildRequires:	termcap-devel
BuildRequires:	texi2html
BuildRequires:	texinfo
Obsoletes:	%{name}-devel
Provides:	%{name}-devel

%description
The octave-forge package contains the source for all the functions plus
build and install scripts. These are designed to work with the latest
development version of Octave (available from
http://www.octave.org/download.html), but most functions will work on
earlier versions of Octave including 2.0.x versions.

%prep
%setup -q
%{__rm} -rf main/sparse
%patch0 -p0 -b .legend

%build
%configure2_5x
%make

%install
%{__rm} -rf %{buildroot}
%makeinstall_std

find %{buildroot}%{_datadir}/octave/%{octave_version}/site/m/%{name} \
  -type f -name "*.m" -exec %{__perl} -pi -e 's|\r$||g' {} \;

find %{buildroot} -type f -name '*.oct' -print0 \
  | xargs -0 -r strip --strip-unneeded

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root,755)
%doc AUTHORS ChangeLog COPYING* README RELEASE-NOTES TODO
%{_bindir}/mex
%{_datadir}/octave
%{_libdir}/octave
%{_mandir}/man1/mex.1*


