FIREWALL
------------------

Iptables configuration for Access apps:

# Ron
sudo ufw allow from 10.7.8.31 to any port 33061
sudo ufw allow from 10.7.8.31 to any port 3306

# Lentz wired
sudo ufw allow from 10.3.0.0/16 to any port 3306
sudo ufw allow from 10.3.0.0/16 to any port 33061
# Clausen wired
sudo ufw allow from 10.9.0.0/16 to any port 33061
sudo ufw allow from 10.9.0.0/16 to any port 3306
# Lentz Carthage-Secure
sudo ufw allow from 10.205.0.0/16 to any port 3306
sudo ufw allow from 10.205.0.0/16 to any port 33061
# Clausen Carthage-Secure
sudo ufw allow from 10.213.0.0/16 to any port 33061
sudo ufw allow from 10.213.0.0/16 to any port 3306
