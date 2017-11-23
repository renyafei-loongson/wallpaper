VERSION=`cat opt/wallpaper/VERSION`

#STATUS_FILE=opt/app/db/999999
#rm -f $STATUS_FILE
#echo "999999:${VERSION}:installed:`date`" > $STATUS_FILE

O=wallpaper-${VERSION}.sh

echo "Buidling $O..."

cp -rf  ../wallpaper.py opt/wallpaper/  
cp -rf  ../.wallpaper.conf opt/wallpaper/  
cp -rf  ../changeconfig.py opt/wallpaper/  

# App files
FILES=" opt HOME install.sh "
tar zcfh /tmp/INSTALL.tgz ${FILES}

rm -rf opt/wallpaper/wallpaper.py
rm -rf opt/wallpaper/.wallpaper.conf
rm -rf opt/wallpaper/changeconfig.py
# header
# https://zhangge.net/266.html

cat _header.sh /tmp/INSTALL.tgz > $O

chmod +x $O
exit 0
