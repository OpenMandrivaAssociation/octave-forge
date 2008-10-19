%define octave_api api-v32

Name:           octave-forge
Version:        20080831
Release:        %mkrel 1
Summary:        Contributed functions for octave

Group:          Applications/Engineering
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
Patch0:         octave-forge-20080831-octgpr-1.1.4.patch
Patch1:         octave-forge-20080831-image-1.0.8.patch
Patch2:         octave-forge-20080831-audio-1.1.2.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root

Requires(post): octave(api) = %{octave_api}
Requires(postun): octave(api) = %{octave_api}
Requires:      octave(api) = %{octave_api} imagemagick
BuildRequires:  octave-devel >= 3.0.0-1
BuildRequires:  tetex gcc-gfortran ginac-devel qhull-devel
BuildRequires:  imagemagick-devel nc-dap-devel pcre-devel gsl-devel
BuildRequires:  libjpeg-devel libpng-devel ncurses-devel ftp-devel
BuildRequires:  openssl-devel java-rpmbuild
Provides: octave-ann = 1.0.1
Provides: octave-audio = 1.1.2
Provides: octave-benchmark = 1.0.0
Provides: octave-bioinfo = 0.1.1
Provides: octave-combinatorics = 1.0.7
Provides: octave-communications = 1.0.8
Provides: octave-control = 1.0.7
Provides: octave-data-smoothing = 1.1.1
Provides: octave-econometrics = 1.0.7
Provides: octave-financial = 0.3.0
Provides: octave-fixed = 0.7.8
Provides: octave-ftp = 1.0.1
Provides: octave-ga = 0.9.4
Provides: octave-general = 1.0.7
Provides: octave-gsl = 1.0.7
Provides: octave-ident = 1.0.6
Provides: octave-image = 1.0.8
Provides: octave-informationtheory = 0.1.6
Provides: octave-io = 1.0.7
Provides: octave-irsa = 1.0.6
Provides: octave-linear-algebra = 1.0.6
Provides: octave-miscellaneous = 1.0.7
Provides: octave-missing-functions = 1.0.1
Provides: octave-nnet = 0.1.8
Provides: octave-octcdf = 1.0.11
Provides: octave-octgpr = 1.1.4
Provides: octave-odebvp = 1.0.5
Provides: octave-odepkg = 0.6.4
Provides: octave-optim = 1.0.4
Provides: octave-optiminterp = 0.3.1
Provides: octave-outliers = 0.13.8
Provides: octave-parallel = 1.0.7
Provides: octave-physicalconstants = 0.1.6
Provides: octave-plot = 1.0.6
Provides: octave-signal = 1.0.8
Provides: octave-sockets = 1.0.5
Provides: octave-specfun = 1.0.7
Provides: octave-special-matrix = 1.0.6
Provides: octave-splines = 1.0.6
Provides: octave-statistics = 1.0.7
Provides: octave-strings = 1.0.6
Provides: octave-struct = 1.0.6
Provides: octave-symbolic = 1.0.7
Provides: octave-time = 1.0.8
Provides: octave-vrml = 1.0.8
Provides: octave-zenity = 0.5.6
Provides: octave-ad = 1.0.4
Provides: octave-bim = 0.0.7
Provides: octave-civil-engineering = 1.0.6
Provides: octave-fpl = 0.1.3
Provides: octave-graceplot = 1.0.6
Provides: octave-integration = 1.0.6
Provides: octave-java = 1.2.5
Provides: octave-mapping = 1.0.6
Provides: octave-msh = 0.0.7
Provides: octave-multicore = 0.2.13
Provides: octave-nan = 1.0.7
Provides: octave-nlwing2 = 1.0.1
Provides: octave-ocs = 0.0.2
Provides: octave-pdb = 1.0.6
Provides: octave-secs1d = 0.0.7
Provides: octave-secs2d = 0.0.7
Provides: octave-symband = 1.0.8
Provides: octave-tcl-octave = 0.1.7
Provides: octave-tsa = 4.0.0
Provides: octave-xraylib = 1.0.7
Provides: octave-pt_br = 1.0.7


%description
Octave-forge is a community project for collaborative development of
Octave extensions. The extensions in this package include additional
data types, and functions for a variety of different applications
including signal and image processing, communications, control,
optimization, statistics, and symbolic math.


%prep
%setup -q -n octave-forge-bundle-%{version}
# The scripts below will build everything automatically, so first
# remove some packages that we don't want to build:
# 1. video stuff requires non-free libraries
rm main/video-*.tar.gz
# 2. engine is not a real octave package
rm extra/engine-*.tar.gz
# 3. jhandles depends on jogl, which is forbidden from Fedora
rm extra/jhandles-*.tar.gz
# 4. other OS stuff
rm extra/windows-*.tar.gz
# 5. exclude database stuff--it should be in its own package
rm main/database-*.tar.gz

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

%patch0 -p1
%patch1 -p1
%patch2 -p1

#Install with -nodeps
sed -i -e "s/pkg('install',/pkg('install','-nodeps',/" */*/Makefile


%build
# Prevents escape sequence from being inserted into octave version string
export TERM=""
# For the java package
export JAVA_HOME=%{java_home}
for pkg in main extra language
do
   cd $pkg
   for dir in *.[0-9]
   do
      cd $dir
      if [ -f configure ]
      then
         %configure2_5x
      elif [ -f src/configure ]
      then
         cd src
         %configure2_5x
         cd ..
      fi
      if [ -f Makefile ]
      then
         %__make TMPDIR=%{_tmppath}
      elif [ -f src/Makefile ]
      then
         cd src
         %__make TMPDIR=%{_tmppath}
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
       %{makeinstall_std} TMPDIR=%{_tmppath} DISTPKG=mandriva
       cd ..
   done
   cd ..
done


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{_bindir}/test -x %{_bindir}/octave && %{_bindir}/octave -q -H --no-site-file --eval "pkg('rebuild');" || :

%postun
%{_bindir}/test -x %{_bindir}/octave && %{_bindir}/octave -q -H --no-site-file --eval "pkg('rebuild');" || :


%files
%defattr(-,root,root,0755)
%{_datadir}/octave/packages/*
%{_libexecdir}/octave/packages/*
