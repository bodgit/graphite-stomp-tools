Name		: graphite-stomp-tools
Version		: 0.1
Release		: 1.20130816gitXXXXXXXX
Summary		: Graphite STOMP Tools
Group		: Applications/Internet

Source0		: %{name}-%{version}.tar.gz
URL		: https://github.com/bodgit/graphite-stomp-tools
License		: BSD
Packager	: Matt Dainty <matt@bodgit-n-scarper.com>

BuildRoot	: %{_tmppath}/%{name}-%{version}-root
%if %{?el5:1}0
BuildRequires	: cmake28 >= 2.8.8
%elseif %{?el6:1}0
BuildRequires	: cmake28 >= 2.8.8
%else
BuildRequires	: cmake >= 2.8.8
%endif
BuildRequires	: libevent-devel >= 2
BuildRequires	: openssl-devel
BuildRequires	: bison
BuildRequires	: pcre-devel

%description
Graphite STOMP Tools is a set of tools for getting Graphite data in and
out of STOMP message brokers.

%prep
%setup -q

%build
%if %{?el5:1}0
%cmake28 .
%elseif %{?el6:1}0
%cmake28 .
%else
%cmake .
%endif
make %{?_smp_mflags}

%install
%{__rm} -rf %{buildroot}
make install DESTDIR=%{buildroot}
%{__mkdir_p} %{buildroot}%{_sysconfdir}/sysconfig
%{__mkdir_p} %{buildroot}%{_sysconfdir}/rc.d/init.d
for i in graphite-{dequeue,enqueue,rewrite} ; do
	%{__install} -m 0644 packaging/rpm/${i}.sysconfig \
		%{buildroot}%{_sysconfdir}/sysconfig/${i}
	%{__install} -m 0755 packaging/rpm/${i}.init \
		%{buildroot}%{_sysconfdir}/rc.d/init.d/${i}
done

%posttrans
/sbin/service graphite-dequeue condrestart >/dev/null 2>&1 || :
/sbin/service graphite-enqueue condrestart >/dev/null 2>&1 || :
/sbin/service graphite-rewrite condrestart >/dev/null 2>&1 || :

%clean
%{__rm} -rf %{buildroot}

%files
%defattr(-,root,root)
%config(noreplace) %attr(0640,-,-) %{_sysconfdir}/graphite-*.conf
%config(noreplace) %{_sysconfdir}/sysconfig/graphite-*
%{_sysconfdir}/rc.d/init.d/graphite-*
%{_sbindir}/graphite-*
%doc %{_mandir}/man5/graphite-*.5*
%doc %{_mandir}/man8/graphite-*.8*

%changelog
* Fri Aug 16 2013 Matt Dainty <matt@bodgit-n-scarper.com> 0.1-1.20130816gitXXXXXXXX
- Initial version 0.1-1.20130816gitXXXXXXXX.
