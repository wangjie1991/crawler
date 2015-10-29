
path=`pwd`
dt=`date +%y%m%d`
spider=${path##*/}
index=/tmp/$spider"_index.bf"
#echo $path
#echo $dt
#echo $spider
#echo $index

if [ -f $index ]
then
    rm $index
    #echo "rm index"
fi

scrapy crawl $spider 2>log
cp log ~/Documents/backup/log/$spider/$dt


