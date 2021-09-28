#needsrootforbuild
# This spec file is from upstream.
Summary: Tracks and displays system calls associated with a running process
Name: strace
Version: 5.6
Release: 3
# The test suite is GPLv2+, all the rest is LGPLv2.1+.
License: LGPL-2.0+ and GPL-2.0
# Some distros require Group tag to be present,
# some require Group tag to be absent,
# some do not care about Group tag at all,
# and we have to cater for all of them.
URL: https://strace.io
%if 0%{?fedora} >= 12 || 0%{?centos} >= 6 || 0%{?rhel} >= 6 || 0%{?suse_version} >= 1200 || 0%{?openEuler} >= 1
Source: https://strace.io/files/%{version}/strace-%{version}.tar.xz
BuildRequires: xz
%else
Source: strace-%{version}.tar.gz
%endif
BuildRequires: gcc gzip

# Install Bluetooth headers for AF_BLUETOOTH sockets decoding.
%if 0%{?fedora} >= 18 || 0%{?centos} >= 6 || 0%{?rhel} >= 8 || 0%{?suse_version} >= 1200 || 0%{?openEuler} >= 1
BuildRequires: pkgconfig(bluez)
%endif

Patch:    0000-strace-fix-failed-tests.patch
Patch:    0001-io_uring-Remove-struct-io_cqring_offsets-compile-tim.patch
Patch:    0002-io_uring-Add-io_cqring_offset-flags.patch
Patch:    0003-build-regenerate-build-deps.patch

# Install elfutils-devel or libdw-devel to enable strace -k option.
# Install binutils-devel to enable symbol demangling.
%if 0%{?fedora} >= 20 || 0%{?centos} >= 6 || 0%{?rhel} >= 6 || 0%{?openEuler} >= 1
%define buildrequires_stacktrace BuildRequires: elfutils-devel binutils-devel
%endif
%if 0%{?suse_version} >= 1100
%define buildrequires_stacktrace BuildRequires: libdw-devel binutils-devel
%endif
%{?buildrequires_stacktrace}

# OBS compatibility
%{?!buildroot:BuildRoot: %_tmppath/buildroot-%name-%version-%release}
%define maybe_use_defattr %{?suse_version:%%defattr(-,root,root)}

%description
The strace program intercepts and records the system calls called and
received by a running process.  Strace can print a record of each
system call, its arguments and its return value.  Strace is useful for
diagnosing problems and debugging, as well as for instructional
purposes.

Install strace if you need a tool to track the system calls made and
received by a process.

%prep
%autosetup -p1
echo -n %version-%release > .tarball-version
echo -n 2020 > .year
echo -n 2020-04-06 > .strace.1.in.date

%build
echo 'BEGIN OF BUILD ENVIRONMENT INFORMATION'
uname -a |head -1
libc="$(ldd /bin/sh |sed -n 's|^[^/]*\(/[^ ]*/libc\.so[^ ]*\).*|\1|p' |head -1)"
$libc |head -1
file -L /bin/sh
gcc --version |head -1
ld --version |head -1
kver="$(printf '%%s\n%%s\n' '#include <linux/version.h>' 'LINUX_VERSION_CODE' | gcc -E -P -)"
printf 'kernel-headers %%s.%%s.%%s\n' $(($kver/65536)) $(($kver/256%%256)) $(($kver%%256))
echo 'END OF BUILD ENVIRONMENT INFORMATION'

CFLAGS_FOR_BUILD="$RPM_OPT_FLAGS"; export CFLAGS_FOR_BUILD
%configure --enable-mpers=check
make %{?_smp_mflags}

%install
make DESTDIR=%{buildroot} install

# remove unpackaged files from the buildroot
rm -f %{buildroot}%{_bindir}/strace-graph

# some say uncompressed changelog files are too big
for f in ChangeLog ChangeLog-CVS; do
	gzip -9n < "$f" > "$f".gz &
done
wait

%files
%maybe_use_defattr
%doc CREDITS ChangeLog.gz ChangeLog-CVS.gz COPYING NEWS README
%{_bindir}/strace
%{_bindir}/strace-log-merge
%{_mandir}/man1/*

%changelog
* Tue Sep 28 2021 fu.lin <fulin10@huawei.com> - 5.6-3
- tests: disable to prevent build failure

* Wed Apr 28 2021 fu.lin <fulin10@huawei.com> - 5.6-2
- build: fix build error when the strace is builded in the environment with io_uring feature kernel devel package 

* Fri Apr 24 2020 shikemeng<shikemeng@huawei.com> - 5.6-1
- Upgrade strace version to 5.6

* Wed Jan  8 2020 openEuler Buildteam <buildteam@openeuler.org> - 5.0-2
- Upgrade strace version to 5.0

* Tue Mar 19 2019 strace-devel@lists.strace.io - 5.0-1
- strace 5.0 snapshot.
