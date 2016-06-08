# AWS-Reports

<b>Options Script: </b><br>
	. Count EC2 <br>
	. Count RDS <br>
	. Count S3 <br>
	. Count IMAGES <br>
	. Count SNAPSHOT <br>
	. Count VOLUMES <br>
	. Count SECURITY GROUP <br>
	. Count LOAD BALANCE <br>
	. Count ELASTIC IP <br>
	. Count KEY PAIRS <br>
	. Count ALL AWS (Above) Send Email with report, image PrintScreen_send_email_example.png <br>	


<b>Examples:</b>

    -o --option 	      Option [ scan_ec2 | scan_rds | scan_s3 | scan_images | scan_snapshot | scan_volumes 
                                       scan_security_group | scan_loadbalance | scan_all_address | scan_all_key_pairs | scan_all_aws ]

    -r --region   	      AWS Region (us-east-1 = USA / sa-east-1 = BR / us-west-2 = OREGON )
    -i --id               AWS Access Key ID
    -k --key              AWS Secret Access Key
 
    Exemplo:
 
	1) OPTIONS 
	    ./ec2-penetta.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -o scan_ec2
	    ./ec2-penetta.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -o scan_rds 
	    ./ec2-penetta.py -r us-east-1 -i YUYUQWMNBBMLZSDAS -k 3jk3ioueqwehkl -o scan_s3


For more information, my contact: eduardo@penetta.com

Thanks & regards
