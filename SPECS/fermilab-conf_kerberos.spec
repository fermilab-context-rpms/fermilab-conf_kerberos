%define package_version 5.3
%define package_release 1.6.1


%if 0%{?rhel} >= 7 
Name:		fermilab-conf_kerberos
%else
Name:		krb5-fermi-krb5.conf
%endif

Version:	%{package_version}
Release:	%{package_release}
Summary:	A krb5.conf file setup to work with the FNAL.GOV kerberos realm

Packager:	Fermilab Authentication Services

Group:		Fermilab
License:	MIT, freely distributable
URL:		http://helpdesk.fnal.gov
Source0:	http://computing.fnal.gov/authentication/krb5conf/Linux/krb5.conf
Source1:	config-krb5.conf

# el6 sources
Source10:	makehostkeys
Source11:	make-cron-keytab
Source12:	krb5-fermi-config.tar.gz

BuildArch:	noarch
BuildRequires:	coreutils augeas
Requires:	krb5-libs coreutils policycoreutils
%if 0%{?rhel} >= 7 
Obsoletes:	krb5-fermi-krb5.conf krb5-fermi-config
%else
Conflicts:	krb5-fermi-config
%endif

%description
This rpm provides a krb5.conf file setup to work with the FNAL.GOV
kerberos realm.

You can automatically customize your default KDCs by placing them one per
line in %{_sysconfdir}/krb5.kdclist


%if 0%{?rhel} < 7 
%package -n krb5-fermi-config
Conflicts:	krb5-fermi-krb5.conf
Packager:	Fermilab Authentication Services
Summary:	Configuration scripts make your Kerberos Installation Fermilab-compatible
Requires:	krb5-libs coreutils policycoreutils

%description -n krb5-fermi-config
This rpm provides a krb5.conf file setup to work with the FNAL.GOV
kerberos realm.

You can automatically customize your default KDCs by placing them one per
line in %{_sysconfdir}/krb5.kdclist

The config set's up config files so that a machine is ready to
be in Fermilab's kerberos realm
%endif

###############################################################################
%prep
%{__cp} %{SOURCE0} krb5.conf.template

###############################################################################
%build
TMPFILE='augtool.script'
FILENAME=$(readlink -f krb5.conf.template)
cat > ${TMPFILE} <<EOF
set /augeas/load/Krb5/incl "${FILENAME}"
load

get /files/${FILENAME}/realms/realm[. = 'FNAL.GOV']
EOF

augtool --noload < ${TMPFILE} > parse.out
if [[ $? -ne 0 ]]; then
    exit 1
fi
rm -rf %{buildroot}
mkdir -p %{buildroot}

###############################################################################
%install

%if 0%{?rhel} >= 7
%{__install} -D %{SOURCE1} %{buildroot}/%{_libexecdir}/%{name}/config-krb5.conf
%{__install} -D krb5.conf.template %{buildroot}/%{_libexecdir}/%{name}/krb5.conf.template

%else
(cd %{buildroot} ; tar xvf %{SOURCE12} ; mv krb5-fermi-config/* . ; rmdir krb5-fermi-config )
%{__install} -D %{SOURCE1} %{buildroot}/usr/krb5/config/config-krb5.conf
%{__install} -D %{SOURCE10} %{buildroot}/usr/krb5/config/makehostkeys
%{__install} -D %{SOURCE11} %{buildroot}/usr/krb5/config/make-cron-keytab
%{__install} -D krb5.conf.template %{buildroot}/usr/krb5/config/krb5.conf.template
%endif

###############################################################################
%check
%if 0%{?rhel} >= 7
bash -n %{buildroot}/%{_libexecdir}/%{name}/config-krb5.conf
%else
bash -n %{buildroot}/usr/krb5/config/config-krb5.conf
%endif

###############################################################################
%post -p /bin/bash
if [[ -f %{_sysconfdir}/krb5.conf ]]; then
%if 0%{?rhel} < 7
    echo "   We need a fresh krb5.conf, moving old krb5.conf to %{_sysconfdir}/krb5.conf.save.pre-%{name}-%{version}-%{release}"
%endif
    %{__mv} %{_sysconfdir}/krb5.conf %{_sysconfdir}/krb5.conf.save.pre-%{name}-%{version}-%{release}
fi

%if 0%{?rhel} < 7
%{__cat} /usr/krb5/config/krb5.conf.template > %{_sysconfdir}/krb5.conf
%else
%{__cat} %{_libexecdir}/%{name}/krb5.conf.template > %{_sysconfdir}/krb5.conf
%endif

%if 0%{?rhel} >= 7
%{_libexecdir}/%{name}/config-krb5.conf %{version}
%else
/usr/krb5/config/config-krb5.conf %{version}
%endif

%{_fixperms} %{_sysconfdir}/krb5.conf
restorecon -F %{_sysconfdir}/krb5.conf

%if 0%{?rhel} < 7 
%post -n krb5-fermi-config
if [[ -f %{_sysconfdir}/krb5.conf ]]; then
    echo "   We need a fresh krb5.conf, moving old krb5.conf to %{_sysconfdir}/krb5.conf.save.pre-%{name}-%{version}-%{release}"
    %{__mv} %{_sysconfdir}/krb5.conf %{_sysconfdir}/krb5.conf.save.pre-%{name}-%{version}-%{release}
fi
%{__cat} /usr/krb5/config/krb5.conf.template > %{_sysconfdir}/krb5.conf

/usr/krb5/config/config-krb5.conf %{version}

%{_fixperms} %{_sysconfdir}/krb5.conf
restorecon -F %{_sysconfdir}/krb5.conf

if [ -f /etc/inetd.conf ] ; then
        /usr/krb5/config/config-inetd.conf %{version}
fi
if [ -d /etc/xinetd.d ] ; then
        if [ -e /etc/xinetd.d/ekrb5-telnet ] ; then
                # SLF 5.x or later, server options changed so switch files
                mv  /usr/krb5/config/ftp.xinetd  /usr/krb5/config/old-ftp.xinetd
                mv  /usr/krb5/config/ftp.xinetd.on  /usr/krb5/config/old-ftp.xinetd.on
                mv  /usr/krb5/config/telnet.xinetd  /usr/krb5/config/old-telnet.xinetd
                mv  /usr/krb5/config/telnet.xinetd.on  /usr/krb5/config/old-telnet.xinetd.on
                mv  /usr/krb5/config/gssftp.xinetd  /usr/krb5/config/ftp.xinetd
                mv  /usr/krb5/config/gssftp.xinetd.on  /usr/krb5/config/ftp.xinetd.on
                mv  /usr/krb5/config/ekrb5-telnet.xinetd  /usr/krb5/config/telnet.xinetd
                mv  /usr/krb5/config/ekrb5-telnet.xinetd.on  /usr/krb5/config/telnet.xinetd.on
        fi
        /usr/krb5/config/config-xinetd %{version}
fi
/usr/krb5/config/config-services %{version}
if [ -f /etc/sshd_conf ] ; then
        /usr/krb5/config/config-sshd_config %{version}
fi
echo "   Your computer is now configured to run Kerberos"
echo "   If you need a host principal you should run '/usr/krb5/config/makehostkeys'"

%triggerin -n krb5-fermi-config -- krb5-workstation
if [ -d /etc/xinetd.d ] ; then
        /usr/krb5/config/config-xinetd %{version} >> /tmp/fermi.krb5.config.xinetd
fi

%triggerin -n krb5-fermi-config -- krb5-libs
if [ -f /etc/krb5.conf ] ; then
        grep -q 'EXAMPLE' /etc/krb5.conf
        if [ "$?" -eq 0 ] ; then
                echo "   Your krb5.conf is the original version from RedHat"
                echo "    ... moving krb5.conf out of the way and putting in Fermilabs"
                /bin/mv -f /etc/krb5.conf /etc/krb5.conf.save.%{name}.%{version}.%{release}
                /usr/krb5/config/config-krb5.conf %{version}
        fi
fi

%triggerpostun -n krb5-fermi-config -- krb5-workstation
if [ -d /etc/xinetd.d ] ; then
        /usr/krb5/config/config-xinetd %{version} >> /tmp/fermi.krb5.config.xinetd
fi


%endif

###############################################################################
%files
%defattr(0644,root,root,0755)
%if 0%{?rhel} >= 7
%attr(0700,root,root) %{_libexecdir}/%{name}/config-krb5.conf
%{_libexecdir}/%{name}/krb5.conf.template
%else
%attr(0700,root,root) /usr/krb5/config/config-krb5.conf
%attr(0755,root,root) /usr/krb5/config/makehostkeys
%attr(0755,root,root) /usr/krb5/config/make-cron-keytab
/usr/krb5/config/krb5.conf.template
%endif

%if 0%{?rhel} < 7 
%files -n krb5-fermi-config
%defattr(0644,root,root,0755)
/usr/krb5/config/*
%attr(0700,root,root) /usr/krb5/config/config-krb5.conf
%attr(0755,root,root) /usr/krb5/config/makehostkeys
%attr(0755,root,root) /usr/krb5/config/make-cron-keytab
%attr(0700,root,root) /usr/krb5/config/config-hostkeys
%attr(0700,root,root) /usr/krb5/config/config-inetd.conf
%attr(0700,root,root) /usr/krb5/config/config-services
%attr(0700,root,root) /usr/krb5/config/config-sshd_config
%attr(0700,root,root) /usr/krb5/config/config-xinetd
%endif

%changelog
* Tue Jan 23 2018 Pat Riehecky <riehecky@fnal.gov> 5.3-1.6.1
- Add missing mkdir_p to config-krb5.conf script

* Wed Jan 17 2018 Pat Riehecky <riehecky@fnal.gov> 5.3-1.6
- Fix permissions error in SLF6 packages
- Move important items out of docdir for docker usage

* Tue Jan 16 2018 Olga Terlyga <terlyga@fnal.gov> 5.3-1.5
- Removed i-krb-6/8/17 from the list of KDCs
- Edited [capath] section to reflect direct(only) trust between Windows domain and MIT realm
- Added pingdev.fnal.gov and prinprod.fnal.gov to [domain_realm] section
- Removed non-existent dns records from [domain_realm] section
- Removed [instancemapping] section since there is no Fermi AFS

* Wed Feb 10 2016 Frank Nagy <nagy@fnal.gov> 5.2-1.4
- Accepted by Authentication Services

* Wed Feb 10 2016 Frank Nagy <nagy@fnal.gov> 5.2-1.3
- Initial evaluation by Authentication Services

* Tue Oct 20 2015 Pat Riehecky <riehecky@fnal.gov> 5.2-1.2
- Switch back to Frank's scripts

* Fri Aug 7 2015 Pat Riehecky <riehecky@fnal.gov> 5.2-1
- Initial build for EL7
