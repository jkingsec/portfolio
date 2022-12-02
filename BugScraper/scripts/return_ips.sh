nmap -n -sL  |  awk '/Nmap scan report/{print }' | grep \( | sed 's/\(|\)//' | sort -u > ips.txt
