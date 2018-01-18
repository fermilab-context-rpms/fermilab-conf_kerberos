_default:
	@echo "make"
sources:
	@echo "make sources"
	cd SOURCES && tar acf krb5-fermi-config.tar.gz --exclude 'CVS' krb5-fermi-config
	rpmbuild -bs --define "%_topdir `pwd`" SPECS/fermilab-conf_kerberos.spec
rpm:
	rpmbuild -ba --define "%_topdir `pwd`" SPECS/fermilab-conf_kerberos.spec
