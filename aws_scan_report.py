#!/usr/bin/python

#  Desenvolvimento Eduardo Penetta
#  Date: 07/06/2016
#  CSC 
#

import boto.s3
import boto.rds
import boto.ec2
import boto.ec2.elb
import boto.vpc
import getopt
import sys
import time
import datetime
import re

version = '1.0'
verbose = False

#print 'ARGV      :', sys.argv[1:]
region = ''
id     = ''
key    = ''
server = ''
option = ''
address= ''
filter = ''
day    = ''

def usage():
    msg = """

    -o --option 	      Option [ scan_ec2 | scan_rds | scan_s3 | scan_images | scan_snapshot | scan_volumes 
                                       scan_security_group | scan_loadbalance | scan_all_address | scan_all_key_pairs | scan_all_aws ]

    -r --region   	      AWS Region (us-east-1 = USA / sa-east-1 = BR / us-west-2 = OREGON )
    -i --id               AWS Access Key ID
    -k --key              AWS Secret Access Key
 
    Exemplo:
 
	1) OPTIONS 
	    ./aws_scan_report.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -o scan_ec2
	    ./aws_scan_report.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -o scan_rds 
	    ./aws_scan_report.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -o scan_s3



    """
    print msg
    #print (time.strftime("%d-%m-%Y %H:%M:%S"))
    sys.exit(1)

try:
   options, args = getopt.gnu_getopt(sys.argv[1:], 'r:i:k:s:h:o:a:f:d:c:', ['region=','id=','key=','server=','help=','option=','address=','filter=','days=','account=',])

except getopt.GetoptError as err:
        # print help information and exit:
        #print(err) # will print something like "option -a not recognized"
	usage();
        sys.exit(2)

for opt, arg in options:
    
    if opt in ('-r', '--region'):
        region = arg
    elif opt in ('-i', '--id'):
        id = arg
    elif opt in ('-k', '--key'):
        key = arg
    elif opt in ('-o', '--option'):
        option = arg
    elif opt in ('-d', '--days'):
        day = arg 
    elif opt in ('-h', '--help'):
        usage()
    else: 
	usage()

if region == '' or id == '' or key == '' :
  print ""
  print "----  CAMPOS INVALIDOS / VAZIOS --" 
  usage()
else:
  print ''
  print ''
  print 'REGION    :', region
  print 'ID        :', id
  print 'KEY       :', key
  print 'OPTION    :', option


#### Conecte AWS 
conn = boto.ec2.connect_to_region(region,aws_access_key_id=id,aws_secret_access_key=key)
conn_rds = boto.rds.connect_to_region(region,aws_access_key_id=id,aws_secret_access_key=key)
conn_elb = boto.ec2.elb.connect_to_region(region,aws_access_key_id=id,aws_secret_access_key=key)
conn_s3  = boto.s3.connect_to_region(region,aws_access_key_id=id,aws_secret_access_key=key)
conn_vpc = boto.vpc.connect_to_region(region,aws_access_key_id=id,aws_secret_access_key=key)

def send_alert_gmail(scan_ec2,scan_images,scan_volumes,scan_snapshot,scan_security_group,scan_loadbalance,scan_rds,scan_s3,scan_all_address,scan_all_key_pairs,scan_all_vpc):

   import smtplib
   from email.MIMEMultipart import MIMEMultipart
   from email.MIMEText import MIMEText

   # Date time
   now = datetime.datetime.now()
   date_time = now.strftime("%Y-%m-%d %H:%M")

   # Specifying the from and to addresses

   fromaddr = 'eduardo@penetta.com'
   toaddrs  = 'eduardo@penetta.com'

   msg = MIMEMultipart()
   msg['From'] = fromaddr
   msg['To'] = toaddrs
   msg['Subject'] = "REPORT AWS TODAY"

   # Writing the message (this message will appear in the email)

   body = """                                                                                                                                                              <!DOCTYPE html PUBLIC '-//W3C//DTD XHTML 1.0 Transitional//EN' 'http://zabbix.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd'><html xmlns='http://zabbix.w3.org/1999/xhtml'><head>
<meta http-equiv='Content-Type' content='text/html; charset=iso-8859-1'>
<title>CSC - AWS</title>
</head>

<body>
<table width='555' border='0' cellspacing='0' cellpadding='0'>
  <tr>
    <td colspan='2'><img src='http://zabbix.cscm3.com.br/alerta/cabecalho1.jpg' width='555' height='49'></td>
  </tr>
  <tr>
    <td width='38' height='40' style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:10px;'><img src='http://zabbix.cscm3.com.br/alerta/EC2.png' width='23' height='23'></td>
    <td width='517' style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat; padding-left:3px; font-family:Verdana, Geneva, sans-serif; font-size:14px;'>Total EC2: %s</td>
  </tr>   
<tr>
    <td height='40'  style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:10px;'><img src='http://zabbix.cscm3.com.br/alerta/ELASTIC.png' width='23' height='22' /></td>
    <td height='40'  style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:3px;padding-left:3px; font-family:Verdana, Geneva, sans-serif; font-size:14px;'>Total Elastic IP: %s</td>
</tr>
<tr>
    <td height='40' style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:10px;'><img src='http://zabbix.cscm3.com.br/alerta/KEYPAIRS.png' width='23' height='20'></td>
    <td height='40' style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:3px;padding-left:3px; font-family:Verdana, Geneva, sans-serif; font-size:14px;'>Total Key Pairs: %s</td>
  </tr>

<tr>
    <td height='40' style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:10px;'><img src='http://zabbix.cscm3.com.br/alerta/IMAGES.png' width='23' height='20'></td>
    <td height='40' style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:3px;padding-left:3px; font-family:Verdana, Geneva, sans-serif; font-size:14px;'>Total AMIs: %s</td>
  </tr>
<tr>
    <td height='40'  style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:10px;'><img src='http://zabbix.cscm3.com.br/alerta/VOLUMES.png' width='23' height='22' /></td>
    <td height='40'  style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:3px;padding-left:3px; font-family:Verdana, Geneva, sans-serif; font-size:14px;'>Total Volumes: %s</td>
</tr>
<tr>
    <td height='40'  style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:10px;'><img src='http://zabbix.cscm3.com.br/alerta/SNAPSHOT.png' width='23' height='22' /></td>
    <td height='40'  style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:3px;padding-left:3px; font-family:Verdana, Geneva, sans-serif; font-size:14px;'>Total Snapshot: %s</td>
</tr>
<tr>
    <td height='40'  style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:10px;'><img src='http://zabbix.cscm3.com.br/alerta/SECURITY.png' width='23' height='22' /></td>
    <td height='40'  style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:3px;padding-left:3px; font-family:Verdana, Geneva, sans-serif; font-size:14px;'>Total Security Group: %s</td>
</tr>
<tr>
    <td height='40'  style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:10px;'><img src='http://zabbix.cscm3.com.br/alerta/LOADBALANCE.png' width='23' height='22' /></td>
    <td height='40'  style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:3px;padding-left:3px; font-family:Verdana, Geneva, sans-serif; font-size:14px;'>Total Load Balancers: %s</td>
</tr>
<tr>
    <td height='40'  style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:10px;'><img src='http://zabbix.cscm3.com.br/alerta/VPC.png' width='26' height='18' /></td>
    <td height='40'  style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:3px;padding-left:3px; font-family:Verdana, Geneva, sans-serif; font-size:14px;'>Total VPC: %s</td>
</tr>
<tr>
    <td height='40'  style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:10px;'><img src='http://zabbix.cscm3.com.br/alerta/RDS.png' width='22' height='22' /></td>
    <td height='40'  style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:3px;padding-left:3px; font-family:Verdana, Geneva, sans-serif; font-size:14px;'>Total RDS: %s</td>
</tr>
<tr>
    <td height='40'  style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:10px;'><img src='http://zabbix.cscm3.com.br/alerta/S3.png' width='23' height='22' /></td>
    <td height='40'  style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:3px;padding-left:3px; font-family:Verdana, Geneva, sans-serif; font-size:14px;'>Total S3 Bucket: %s</td>
</tr>
<tr>
    <td height='40'  style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:10px;'><img src='http://zabbix.cscm3.com.br/alerta/DATE.png' width='23' height='22' /></td>
    <td height='40'  style='background-image:url(http://zabbix.cscm3.com.br/alerta/bg.jpg); background-repeat:no-repeat;  padding-left:3px;padding-left:3px; font-family:Verdana, Geneva, sans-serif; font-size:14px;'><b>Atualizado: %s By Penetta</b></td>
</tr>
</table>
</body>
</html>""" % (scan_ec2,scan_all_address,scan_all_key_pairs,scan_images,scan_volumes,scan_snapshot,scan_security_group,scan_loadbalance,scan_all_vpc,scan_rds,scan_s3, date_time) 



   #msg.attach(MIMEText(body, 'plain'))
   msg.attach(MIMEText(body, 'html'))
   
   # Gmail Login
    
   username = 'eduardo@test.com'
   password = 'password_this'

   # Sending the mail

   server = smtplib.SMTP('smtp.gmail.com:587')
   server.starttls()
   server.login(username,password)
   text = msg.as_string()
   server.sendmail(fromaddr, toaddrs, text)
   server.quit()



def scan_ec2 ():

   list_instances = conn.get_all_instances()

   for res in list_instances:
      for inst in res.instances:
         name = inst.tags['Name'] if 'Name' in inst.tags else 'Unknown'
         print "%s (%s) [%s] {%s} [%s]" % (name, inst.id, inst.state, inst.image_id, inst.ip_address   )

   result = "%s"  % len(list_instances)
   print " ' ---- Total 'de EC2 = %s ----"  % len(list_instances)
   return result

def scan_images ():

    list_imagens = conn.get_all_images(owners='self')
    for images in list_imagens:
          print "Imagens: (%s) - %s  - [%s] - {%s} (%s) ... " % (images.id,images.name, images.description,images.state,images.location)

    result = "%s"  % len(list_imagens)
    print " ---- Total de Imagens = %s ----"  % len(list_imagens)
    return result

def scan_volumes():

    list_volumes = conn.get_all_volumes(volume_ids=None, filters=None)
    for volume in list_volumes:
        print "Volumes: "+ volume.id, volume.status

    result = "%s" % len(list_volumes)
    print " ---- Total de Volumes = %s ----"  % len(list_volumes)
    return result

def scan_snapshot():

    list_snapshot = conn.get_all_snapshots(owner='self')
    for snapshot in list_snapshot:
        print "SnapShot: "+ snapshot.id, snapshot.status

    result = "%s"  % len(list_snapshot)
    print " ---- Total de SnapShot = %s ----"  % len(list_snapshot)
    return result

def scan_security_group():

    list_security = conn.get_all_security_groups()
    for security in list_security:
        print "Security Group: "+ security.name

    result = "%s"  % len(list_security)
    print " ---- Total de Security Group = %s ----"  % len(list_security)
    return result

def scan_loadbalance():

    list_loadbalance = conn_elb.get_all_load_balancers()
    for load in list_loadbalance:
        print "Load Balance: "+ load.id

    result = "%s"  % len(list_loadbalance)
    print " ---- Total de Load Balance = %s ----"  % len(list_loadbalance)
    return result

def scan_rds():

    list_rds = conn_rds.get_all_dbinstances()
    for rds in list_rds:
        print "RDS : "+ rds.name

    result = "%s"  % len(list_rds)
    print " ---- Total de RDS = %s ----"  % len(list_rds)
    return result

def sizeof(num):
   for x in ['bytes','KB','MB','GB','TB']:
       if num < 1024.0:
           return "%3.1f %s" % (num, x)
       num /= 1024.0

def scan_s3():

    list_s3 = conn_s3.get_all_buckets()

    #print list_s3
    for s3 in list_s3:
    
        print "S3 Bucket: %s " %  (s3.name)
    
    result = "%s"  % len(list_s3)
    print " ---- Total de S3 Bucket = %s ----"  % len(list_s3)
    return result


def scan_all_address():

    list_address = conn.get_all_addresses()
    for address in list_address:
        print "Address: "+ address.public_ip

    result = "%s"  % len(list_address)
    print " ---- Total de All Address = %s ----"  % len(list_address)
    return result

def scan_all_key_pairs():

    list_keypairs = conn.get_all_key_pairs()
    for keypairs in list_keypairs:
        print "Key Pairs: "+ keypairs.name

    result = "%s"  % len(list_keypairs)
    print " ---- Total de All Key Pairs = %s ----"  % len(list_keypairs)
    return result

def scan_all_vpc():

    list_vpc = conn_vpc.get_all_vpcs()
    for vpc in list_vpc:
        print "Key Pairs: "+ vpc.id

    result = "%s"  % len(list_vpc)
    print " ---- Total de All VPCs = %s ----"  % len(list_vpc)
    return result

##### CHAMANDO AS FUNCOES
if option in ('scan_ec2'):
   scan_ec2()

elif option in ('scan_images'):
   scan_images()

elif option in ('scan_volumes'):
   scan_volumes()

elif option in ('scan_snapshot'):
   scan_snapshot()

elif option in ('scan_security_group'):
   scan_security_group()

elif option in ('scan_loadbalance'):
    scan_loadbalance()

elif option in ('scan_rds'):
    scan_rds()

elif option in ('scan_s3'):
    scan_s3()

elif option in ('scan_all_address'):
    scan_all_address()

elif option in ('scan_all_key_pairs'):
    scan_all_key_pairs()

elif option in ('scan_all_vpc'):
    scan_all_vpc()

elif option in ('scan_all_aws'):
   #scan_all  = '<b>%s</b> \n %s \n %s \n %s \n %s \n %s \n %s \n %s \n %s \n %s \n %s'  % (scan_ec2(),scan_images(),scan_volumes(),scan_snapshot(),scan_security_group(),scan_loadbalance(),scan_rds(),scan_s3(),scan_all_address(),scan_all_key_pairs(), scan_all_vpc())
   send_alert_gmail (scan_ec2(),scan_images(),scan_volumes(),scan_snapshot(),scan_security_group(),scan_loadbalance(),scan_rds(),scan_s3(),scan_all_address(),scan_all_key_pairs(), scan_all_vpc())
 
else:
   #print "OPCAO ESCOLHIDA ERRADA!"
   print "----  CAMPOS INVALIDOS --" 
   usage()



