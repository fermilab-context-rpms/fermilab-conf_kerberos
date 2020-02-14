_default:
	@echo "make"
sources:
	@echo "make sources"
	cd SOURCES && tar acf krb5-fermi-config.tar.gz --exclude 'CVS' krb5-fermi-config
	cd SOURCES && tar acf krb5.conf.d.tar.gz --exclude 'CVS' krb5.conf.d
	rpmbuild -bs --define "%_topdir `pwd`" SPECS/fermilab-conf_kerberos.spec
rpm:
	rpmbuild -ba --define "%_topdir `pwd`" SPECS/fermilab-conf_kerberos.spec
