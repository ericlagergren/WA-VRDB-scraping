set -e

TMP_INSTALL_DIR=~/.vrdbscraper.tmp

mkdir -p $TMP_INSTALL_DIR && git clone https://github.com/EricLagerg/WA-VRDB-scraping.git $TMP_INSTALL_DIR

cd $TMP_INSTALL_DIR

{
	cp -r src/vrdb-scraper/ /usr/share/ &&
	cp src/scraper ~/bin
} || {
	read -p "Where would you prefer to install VRDB-Scraper? Type full path and press [Enter]: " filepath
	if [ ! -d $filepath ]; then
		mkdir -p $filepath &&
		cp -r src/vrdb-scraper/ $filepath &&
		echo -e "#!/bin/bash\n\n"$filepath"/src/scraper.py" > src/scraper &&
		cp src/scraper ~/bin
	else
		cp -r src/vrdb-scraper/ $filepath &&
		cp src/scraper ~/bin
	fi
}

rm -rf $TMP_INSTALL_DIR

exit 0