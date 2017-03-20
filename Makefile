_default:
	@echo "make"
sources:
	@echo "make sources"
	tar cf - krb5-fermi-config | gzip --best > krb5-fermi-config.tar.gz
