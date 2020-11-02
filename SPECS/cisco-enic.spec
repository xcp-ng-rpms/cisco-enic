%define vendor_name Cisco
%define vendor_label cisco
%define driver_name enic

%if %undefined module_dir
%define module_dir updates
%endif

Summary: %{vendor_name} %{driver_name} device drivers
Name: %{vendor_label}-%{driver_name}
Epoch: 1
Version: 4.0.0.11
Release: 1%{?dist}
License: GPL

Source0: https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-cisco-enic/archive?at=4.0.0.11&format=tgz&prefix=driver-cisco-enic-4.0.0.11#/cisco-enic-4.0.0.11.tar.gz


Provides: gitsha(https://code.citrite.net/rest/archive/latest/projects/XS/repos/driver-cisco-enic/archive?at=4.0.0.11&format=tgz&prefix=driver-cisco-enic-4.0.0.11#/cisco-enic-4.0.0.11.tar.gz) = ab4e6583efb5c8358c60344ad124ee54220b8897


BuildRequires: kernel-devel
Provides: vendor-driver
Requires: kernel-uname-r = %{kernel_version}
Requires(post): /usr/sbin/depmod
Requires(postun): /usr/sbin/depmod

%description
%{vendor_name} %{driver_name} device drivers for the Linux Kernel
version %{kernel_version}.

%prep
%autosetup -p1 -n driver-%{name}-%{version}

%build
%{?cov_wrap} %{make_build} -C /lib/modules/%{kernel_version}/build M=$(pwd) KSRC=/lib/modules/%{kernel_version}/build modules

%install
%{?cov_wrap} %{__make} %{?_smp_mflags} -C /lib/modules/%{kernel_version}/build M=$(pwd) INSTALL_MOD_PATH=%{buildroot} INSTALL_MOD_DIR=%{module_dir} DEPMOD=/bin/true modules_install

# mark modules executable so that strip-to-file can strip them
find %{buildroot}/lib/modules/%{kernel_version} -name "*.ko" -type f | xargs chmod u+x

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

%changelog
* Wed Jul 29 2020 Deli Zhang <deli.zhang@citrix.com> - 1:4.0.0.11-1
- CP-34509: Update enic driver to 1:4.0.0.11-1

* Tue Nov 05 2019 Ming Lu <ming.lu@citrix.com> - 1:3.2.210.27-1
- CP-32342: Update enic driver to version 1:3.2.210.27

* Wed Jan 23 2019 Deli Zhang <deli.zhang@citrix.com> - 1:3.2.189.0-1
- CP-30068: Upgrade enic driver to version 1:3.2.189.0
