
cd /home/jay/Documents/scrapy/wy163/

path=`pwd`
dt=`date +%y%m%d`
spider=${path##*/}
index=/tmp/$spider"_index.bf"
#echo $path
#echo $spider

if [ -f $index ]
then
    rm $index
fi

scrapy crawl $spider 2>log
cp log /home/jay/Documents/backup/log/$spider/$dt


