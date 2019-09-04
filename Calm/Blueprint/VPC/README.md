## VPC Blueprint
This Calm blueprint allows the creation of a full Project environnement, including Quota Assignment, environment creation, VLAN creation, Marketplace initialization, User or Group assignment.  It will help customer and partners that needs to create a VPC-like experience in Calm. 

To use this blueprint, import into a Prism Central running >= Calm 2.6.0, and fill in the Credentials and Variables mentioned below.

##### Credentials
* local: The local admin account credentials for your Windows or Linux base image .  This credential will be used when a new app is deployed through the new project.
* Prism_Central : Provide an admin account that will be able to do all the API calls for the VPC creation.

##### Variables
* PC_IP: This should be the IP address of your Prism Central
* Project Name : This should be the name of the new project.
* VLANID: This should be the VLAN ID used for the subnet creation. The last 2 octets of your subnet will be linked to the VLANID.
* DNSIP: This should be the name of the DNS server of your network (Used for the IP Pool) 
* domainSearch : This should be the name of the DNS domain search (Used for the IP Pool) ex : ntnx.local
* domainName : This should be DNS domain name (Used for the IP Pool) ex : ntnx
* UsernameorGroup : This should be the user (UPN) or group that you would like to add with a consumer role during the deployment (user : julien@ntnx.local or group : Devops Groups)
* Image_Name : This should be the image that will be used a template for your Application ( ex : Centos Template )
* clustername : This should be the nutanix cluster name : (Ex : Belux cluster)
* vCPU_Quota : vCPU Quota of your project
* Memory_Quota : Memory quota of your project (GB)
* Storage_Quota : Storage quota of your project  (GB)

##### Custom Actions Available
* Refresh Marketplace: When this action is run, the list of the published application will be refresh in your project.
