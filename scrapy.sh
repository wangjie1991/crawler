spider=wy163
dt=`date +%y%m%d`

rm /tmp/$spider"_index.bf"
scrapy crawl $spider 2>log

mv ~/Documents/corpus/$spider ~/Music/raw/$spider/$dt
cp log ~/Music/raw/$spider/$dt/


