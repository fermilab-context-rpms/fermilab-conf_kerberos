_default:
	@echo "make"
sources:
	@echo "make sources"
	cd SOURCES && tar acf krb5-fermi-config.tar.gz --exclude 'CVS' krb5-fermi-config
	cd SOURCES && tar acf krb5.conf.d.tar.gz --exclude 'CVS' krb5.conf.d
	rpmbuild -bs --define "%_topdir `pwd`" SPECS/fermilab-conf_kerberos.spec
rpm:
	rpmbuild -ba --define "%_topdir `pwd`" SPECS/fermilab-conf_kerberos.spec
krb5conf:
	@rm -rf /tmp/krb5conf_all_in_one
	@mkdir -p /tmp/krb5conf_all_in_one
	@cp SOURCES/krb5.conf.d/*.conf /tmp/krb5conf_all_in_one/
	@for snippet in `cd SOURCES/krb5.conf.d/; ls 25-fermilab-realm*`; do cat SOURCES/krb5.conf.d/$$snippet | grep -v '\[realms\]' > /tmp/krb5conf_all_in_one/$$snippet; done
	@echo '[realms]' > /tmp/krb5conf_all_in_one/24-fermilab-realm.conf
	@sed -e 's/.*FNAL.GOV.*=.*{/&\n\n#BEGINTAG-KDCLIST\n/' /tmp/krb5conf_all_in_one/25-fermilab-realm-fnal_gov.conf | sed '/\skdc[^\n]*/,$$!b;//{x;//p;g};//!H;$$!d;x;s//&\n\n#ENDTAG-KDCLIST\n/' > /tmp/outfile
	@mv /tmp/outfile /tmp/krb5conf_all_in_one/25-fermilab-realm-fnal_gov.conf
	@cat SOURCES/EL7_header
	@cat /tmp/krb5conf_all_in_one/*conf
	@rm -rf /tmp/krb5conf_all_in_one

