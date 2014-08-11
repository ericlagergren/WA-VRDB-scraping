{
	cp -r src/vrdb-scraper/ /usr/share/ &&
	cp src/scraper ~/bin
} || {
	echo "Where would you prefer to install VRDB-Scraper? (Type full path and press [Enter]:"
	read path
	cp -r src/vrdb-scraper path
	cp src/scraper ~/bin
}

exit 0