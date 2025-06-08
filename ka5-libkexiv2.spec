#
# Conditional build:
%bcond_with	tests		# test suite

%define		kf_ver		5.94.0
%define		qt_ver		5.15.2
%define		kaname		libkexiv2
Summary:	libkexiv2 - KDE Exiv2 wrapper
Summary(pl.UTF-8):	libexiv2 - obudowanie Exiv2 dla KDE
Name:		ka5-%{kaname}
Version:	23.08.5
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{version}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	fbb745604cccbec99980cd702eb50684
URL:		https://kde.org/
BuildRequires:	Qt5Core-devel >= %{qt_ver}
BuildRequires:	Qt5Gui-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.20
BuildRequires:	exiv2-devel >= 0.25
BuildRequires:	kf5-extra-cmake-modules >= %{kf_ver}
BuildRequires:	libstdc++-devel >= 6:5
BuildRequires:	ninja
BuildRequires:	qt5-build >= %{qt_ver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires:	Qt5Core >= %{qt_ver}
Requires:	Qt5Gui >= %{qt_ver}
Requires:	exiv2 >= 0.25
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libkexiv2 is a wrapper around Exiv2.

%description -l pl.UTF-8
Libkexiv2 jest wraperem wokół Exiv2.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt5Core-devel >= %{qt_ver}
Requires:	Qt5Gui-devel >= %{qt_ver}
Requires:	libstdc++-devel >= 6:5

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DHTML_INSTALL_DIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libKF5KExiv2.so.5.*.*
# soname symlink
%{_libdir}/libKF5KExiv2.so.15.0.0
%{_datadir}/qlogging-categories5/libkexiv2.categories

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKF5KExiv2.so
%{_includedir}/KF5/KExiv2
%{_libdir}/cmake/KF5KExiv2
