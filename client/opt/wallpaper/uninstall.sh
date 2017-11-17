# 注意：由于是使用root运行的，所以一定要获得实际登录用户
ALL_HOME=`cut -d: -f6 /etc/passwd | grep -E   'root|home' | sort | uniq`

for home in $ALL_HOME; do
  USER=`basename $home`

  for dir in "桌面"  "Desktop" ; do
    if [ -d "$home/$dir/" ]; then
      rm -f HOME/*  $home/$dir/wallpaper.desktop
    fi
  done
done

rm -f  /etc/skel/Desktop/wallpaper.desktop
rm -f  /etc/skel/桌面/wallpaper.desktop

# 删除安装文件
rm -rf /opt/wallpaper
