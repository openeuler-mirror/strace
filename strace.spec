Name: strace
Version: 4.24
Release: 2
Summary: The linux syscall tracer
License: LGPLv2.1+
URL: https://strace.io
Source0: https://strace.io/files/%{version}/%{name}-%{version}.tar.xz
Source1: strace.patches

%include %{SOURCE1}

#Dependency
BuildRequires: gcc gzip pkgconfig(bluez)
BuildRequires: elfutils-devel binutils-devel

%description
strace is a diagnostic, debugging and instructional userspace utility
for Linux. It is used to monitor and tamper with interactions between
processes and the Linux kernel, which include system calls,signal deliveries,
and changes of process state.

%package_help

#Build sections
%prep
%autosetup -n %{name}-%{version} -p1

%build
CFLAGS_FOR_BUILD="$RPM_OPT_FLAGS"; export CFLAGS_FOR_BUILD
%configure --enable-mpers=check
%make_build

%install
%make_install

%check
make %{?_smp_mflags} check

#Install and uninstall scripts
%pre

%preun

%post

%postun

%files
%defattr(-,root,root)
%doc COPYING CREDITS ChangeLog ChangeLog-CVS NEWS README
%{_bindir}/strace
%{_bindir}/strace-log-merge
%exclude %{_bindir}/strace-graph

%files help
%{_mandir}/man1/*

%changelog
* Wed Jul 18 2018 openEuler Buildteam <buildteam@openeuler.org> - 4.24-2
- Package init
