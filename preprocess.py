from ftplib import FTP


URL = "/pub/home/obs/kp-ap/wdc/"

ftp = FTP('ftp.gfz-potsdam.de')
ftp.login()
ftp.cwd(URL)
name = 'kp2019.wdc'
data = ftp.retrbinary('RETR ' + name, open(name, 'wb').write)

ftp.close()
