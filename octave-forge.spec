%define octave_api api-v32

Name:           octave-forge
Version:        20071212
Release:        %mkrel 3
Summary:        Contributed functions for octave

Group:          Sciences/Mathematics
License:        GPLv2+ and Public Domain
URL:            http://octave.sourceforge.net
## Source0:     http://downloads.sourceforge.net/sourceforge/octave/%{name}-bundle-%{version}.tar.gz
## The original sources contain a non-free tree of functions that are
## GPL incompatible. A patched version with the non-free sources removed
## is created as follows:
## tar xzf octave-forge-bundle-%{version}.tar.gz
## rm -Rf octave-forge-bundle-%{version}/nonfree/
## tar czf octave-forge-bundle-%{version}.patched.tar.gz octave-forge-bundle-%{version}
## rm -Rf octave-forge-bundle-%{version}
Source0:        %{name}-bundle-%{version}.patched.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
Requires:       octave(api) = %{octave_api} imagemagick
Requires(post): octave(api) = %{octave_api}
Requires(postun): octave(api) = %{octave_api}
BuildRequires:  octave-devel >= 3.0.0-1
BuildRequires:  tetex gcc-gfortran ginac-devel qhull-devel
BuildRequires:  imagemagick-devel nc-dap-devel pcre-devel gsl-devel
BuildRequires:  libjpeg-devel libpng-devel ncurses-devel
BuildRequires:  openssl-devel java-rpmbuild
Provides: octave-audio = 1.0.2
Provides: octave-combinatorics = 1.0.3
Provides: octave-communications = 1.0.3
Provides: octave-control = 1.0.2
Provides: octave-econometrics = 1.0.3
Provides: octave-fixed = 0.7.3
Provides: octave-general = 1.0.3
Provides: octave-gsl = 1.0.2
Provides: octave-ident = 1.0.2
Provides: octave-image = 1.0.3
Provides: octave-informationtheory = 0.1.2
Provides: octave-io = 1.0.3
Provides: octave-irsa = 1.0.2
Provides: octave-linear-algebra = 1.0.2
Provides: octave-miscellaneous = 1.0.3
Provides: octave-nnet = 0.1.4
Provides: octave-octcdf = 1.0.6
Provides: octave-odebvp = 1.0.1
Provides: octave-odepkg = 0.3.3
Provides: octave-optim = 1.0.0
Provides: octave-optiminterp = 0.2.4
Provides: octave-outliers = 0.13.4
%ifnarch x86_64 ppc64
Provides: octave-parallel = 1.0.3
%endif
Provides: octave-physicalconstants = 0.1.2
Provides: octave-plot = 1.0.2
Provides: octave-signal = 1.0.4
Provides: octave-sockets = 1.0.2
Provides: octave-specfun = 1.0.3
Provides: octave-special-matrix = 1.0.2
Provides: octave-splines = 1.0.2
Provides: octave-statistics = 1.0.3
Provides: octave-strings = 1.0.2
Provides: octave-struct = 1.0.2
Provides: octave-symbolic = 1.0.3
Provides: octave-time = 1.0.2
Provides: octave-vrml = 1.0.3
Provides: octave-zenity = 0.5.2
Provides: octave-bim = 0.0.2
Provides: octave-civil-engineering = 1.0.2
Provides: octave-fpl = 0.0.2
Provides: octave-graceplot = 1.0.2
Provides: octave-integration = 1.0.2
Provides: octave-java = 1.2.1
Provides: octave-mapping = 1.0.2
Provides: octave-msh = 0.0.2
Provides: octave-nan = 1.0.2
Provides: octave-pdb = 1.0.2
Provides: octave-secs1d = 0.0.3
Provides: octave-secs2d = 0.0.3
Provides: octave-symband = 1.0.3
Provides: octave-tcl-octave = 0.1.3
Provides: octave-triangular = 1.0.1
Provides: octave-tsa = 3.10.3
Provides: octave-xraylib = 1.0.3
Provides: octave-language-pt_br = 1.0.3

%description
Octave-forge is a community project for collaborative development of
Octave extensions. The extensions in this package include additional
data types, and functions for a variety of different applications
including signal and image processing, communications, control,
optimization, statistics, and symbolic math.

%prep
%setup -q -n octave-forge-bundle-%{version}
#Not 64-bit safe
%ifarch x86_64 ppc64
rm main/parallel-*.tar.gz
%endif
#Don't install engine - not a real octave package
rm extra/engine-*.tar.gz
#Can't handle jhandles yet
rm extra/jhandles-*.tar.gz
#Not MacOSX
rm extra/macosx-*.tar.gz
#Not Windows
rm extra/windows-*.tar.gz

#Unpack everything
for pkg in main extra language
do
   cd $pkg
   for tgz in *.tar.gz
   do
      tar xzf $tgz

      #Collect provides
      echo $tgz | sed 's/\(.*\)-\([0-9]*\.[0-9]*\.[0-9]*\)\.tar\.gz/Provides: octave-\1 = \2/' >> ../octave-forge-provides
   done
   cd ..
done

# edit.m is now in octave
rm main/miscellaneous-1.0.4/inst/edit.m

#Cleanup some CVS directories
find -name CVS | xargs rm -rf

#Install with -nodeps
sed -i -e "s/pkg('install',/pkg('install','-nodeps',/" */*/Makefile

#Fix permissions
find -name COPYING -o -name INDEX -o -name DESCRIPTION -o -name \*.m | xargs chmod -x

#Fix line endings
find -name \*.m | xargs %{__perl} -pi -e 's/\r$//g'

%build
#Prevents escape sequence from being inserted into octave version string
export TERM=""
export JAVA_HOME=%{java_home}
for pkg in main extra language
do
   cd $pkg
   for dir in *.[0-9]
   do
      cd $dir
      if [ -f configure ]
      then
         %{configure2_5x}
      elif [ -f src/configure ]
      then
         cd src
         %{configure2_5x}
         cd ..
      fi
      if [ -f Makefile ]
      then
         %{__make} TMPDIR=%{_tmppath}
      elif [ -f src/Makefile ]
      then
         cd src
         %{__make} TMPDIR=%{_tmppath}
         cd ..
      fi
      cd ..
   done
   cd ..
done
   
%install
rm -rf $RPM_BUILD_ROOT
export TERM=""

for pkg in main extra language
do
   cd $pkg
   for dir in *.[0-9]
   do
       cd $dir
       %{__make} install TMPDIR=%{_tmppath} DESTDIR=%{buildroot} DISTPKG=mandriva
       cd ..
   done
   cd ..
done

#Move aurecord to arch-dependent dir
archdir=%{_libexecdir}/octave/packages/`octave-config -p CANONICAL_HOST_TYPE`-%{octave_api}
audiover=`basename $RPM_BUILD_ROOT%{_datadir}/octave/packages/audio-*`
mkdir -p $RPM_BUILD_ROOT${archdir}/${audiover}
mv $RPM_BUILD_ROOT%{_datadir}/octave/packages/${audiover}/bin \
   $RPM_BUILD_ROOT${archdir}/${audiover}/

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_bindir}/test -x %{_bindir}/octave && %{_bindir}/octave -q -H --no-site-file --eval "pkg('rebuild');" || :

%postun
%{_bindir}/test -x %{_bindir}/octave && %{_bindir}/octave -q -H --no-site-file --eval "pkg('rebuild');" || :

%files
%defattr(-,root,root,0755)
%dir %{_datadir}/octave/packages
%dir %{_libexecdir}/octave/packages
%{_datadir}/octave/packages/*
%{_libexecdir}/octave/packages/*
