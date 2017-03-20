_default:
	@echo "make"
sources:
	@echo "make sources"
	cd SOURCES && tar acf krb5-fermi-config.tar.gz --exclude 'CVS' krb5-fermi-config
