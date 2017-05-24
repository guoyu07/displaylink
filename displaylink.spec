Name:           displaylink
Version:        1.3.52
Release:        1%{?dist}
Summary:        DisplayLink USB Graphics Software
License:        Proprietary
URL:            http://www.displaylink.com/
ExclusiveArch:  %{ix86} x86_64

# http://www.displaylink.com/downloads/file?id=744
Source0:        %{name}-driver-%{version}.zip
Source1:        %{name}.service
Source4:        99-%{name}.rules

Provides:       %{name}-kmod-common = %{?epoch:%{epoch}:}%{version}-%{release}

# UDev rule location (_udevrulesdir) and systemd macros
BuildRequires:  systemd

%{?systemd_requires}

%description
The Extensible Virtual Display Interface (EVDI) is a Linux® kernel module that
enables management of multiple screens, allowing user-space programs to take
control over what happens with the image. It is essentially a virtual display
you can add, remove and receive screen updates for, in an application that uses
the libevdi library.

This open-source project includes source code for both the evdi kernel module
and a wrapper libevdi library that can be used by applications like
DisplayLink's user mode driver to send and receive information from and to the
kernel module.

%prep
%setup -c -n %{name}-%{version}
./%{name}-driver-%{version}.run --target . --noexec

%install
mkdir -p %{buildroot}%{_libdir}/displaylink
mkdir -p %{buildroot}%{_modprobe_d}/
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_udevrulesdir}

# Install displaylink service and target
install -p -m 0644 %{SOURCE1} %{buildroot}%{_unitdir}

sed -i -e 's|LIBDIR|%{_libdir}|g' %{buildroot}%{_unitdir}/%{name}.service

# Udev rules
install -p -m 0644 %{SOURCE4} %{buildroot}%{_udevrulesdir}

sed -i -e 's|LIBDIR|%{_libdir}|g' %{buildroot}%{_udevrulesdir}/*.rules

# Binary components
%ifarch %{ix86}
ARCH="x86"
%endif

%ifarch x86_64
ARCH="x64"
%endif

install -m 755 -p $ARCH-ubuntu-1604/DisplayLinkManager %{buildroot}%{_libdir}/displaylink/
install -m 644 -p *.spkg %{buildroot}%{_libdir}/displaylink/

%post
%systemd_post nvidia-fallback.service

%preun
%systemd_preun nvidia-fallback.service

%postun
%systemd_postun nvidia-fallback.service

%files
%license LICENSE
%{_libdir}/displaylink
%{_unitdir}/%{name}.service
%{_udevrulesdir}/*-%{name}.rules

%changelog
* Tue May 23 2017 Simone Caronni <negativo17@gmail.com> - 1.3.52-1
- First build.
