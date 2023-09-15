%global package_speccommit 8f667a5abffbf8a23c36eb0a8a06de2fd93162c7
%global usver 4.4.0.1
%global xsver 1
%global xsrel %{xsver}%{?xscount}%{?xshash}
%global package_srccommit 4.4.0.1
%define vendor_name Cisco
%define vendor_label cisco
%define driver_name enic

%if %undefined module_dir
%define module_dir updates
%endif

## kernel_version will be set during build because then kernel-devel
## package installs an RPM macro which sets it. This check keeps
## rpmlint happy.
%if %undefined kernel_version
%define kernel_version dummy
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Epoch: 1
Version: 4.4.0.1
Release: %{?xsrel}%{?dist}
License: GPL
Source0: cisco-enic-4.4.0.1.tar.gz

BuildRequires: gcc
BuildRequires: kernel-devel
%{?_cov_buildrequires}
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n %{name}-%{version}
%{?_cov_prepare}

%build
%{?_cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{?_cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

%{?_cov_install}

%post
/sbin/depmod %{kernel_version}
%{regenerate_initrd_post}

%postun
/sbin/depmod %{kernel_version}
%{regenerate_initrd_postun}

%posttrans
%{regenerate_initrd_posttrans}

%files
/lib/modules/%{kernel_version}/*/*.ko

%{?_cov_results_package}

%changelog
* Thu Jun 01 2023 Stephen Cheng <stephen.cheng@citrix.com> - 4.4.0.1-1
- CP-41863: Upgrade enic driver to version 1:4.4.0.1

* Thu Oct 06 2022 Zhuangxuan Fei <zhuangxuan.fei@citrix.com> - 4.2.0.26-1
- CP-40434: Upgrade enic driver to version 1:4.2.0.26

* Mon Feb 14 2022 Ross Lagerwall <ross.lagerwall@citrix.com> - 4.0.0.11-2
- CP-38416: Enable static analysis

* Mon Jan 17 2022 Deli Zhang <deli.zhang@citrix.com> - 1:4.0.0.11-1
- CP-37628: Upgrade enic driver to version 1:4.0.0.11

* Wed Dec 02 2020 Ross Lagerwall <ross.lagerwall@citrix.com> - 3.2.189.0-2
- CP-35517: Fix the build for koji

* Wed Jan 23 2019 Deli Zhang <deli.zhang@citrix.com> - 1:3.2.189.0-1
- CP-30068: Upgrade enic driver to version 1:3.2.189.0
