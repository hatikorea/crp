#!/bin/sh
echo "#!/bin/sh\nproc=\`ps auxw|grep python3.4|grep -v grep|awk '{print \$2}'\`\n[ ! -z \"\$proc\" ] && kill \$proc\n#end" > /usr/local/sbin/redshell
chmod +x /usr/local/sbin/redshell
echo 'ALL ALL=(root) NOPASSWD: /usr/local/sbin/redshell' > /etc/sudoers.d/redshell
echo 'sudo /usr/local/sbin/redshell' >> /etc/profile
#end
