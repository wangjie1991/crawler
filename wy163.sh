#scrapy crawl wy163 2>&1 | tee log
scrapy crawl wy163 2>log/wy163.log

dt=`date +%y%m%d`
echo $dt
:<<EOF
dir="~/Music/raw/"$dt
if [ ! -d $dir ]
then
    mkdir $dir
fi
mv ~/Documents/corpus/wy163 $dir
EOF

