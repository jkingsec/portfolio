nmap -n -sL $(cat subs.txt) |  awk '/Nmap scan report/{print $NF}' | grep \( | sed 's/\(|\)//' | sort -u > ips.txt
