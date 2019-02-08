import requests
import json
import urllib3
import getpass


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

print("This script will create a K8S cluster on Nutanix using API Call")
PCusername = input("Type PC username : ")
PCpassword = getpass.getpass()
PC = input("Type prism Central IP : ")
PE = input("Type prism element IP : ")

PEUsername = input("Type PE username : ")
PEPassword = getpass.getpass()


Karbonurl ='https://'+PC+':7050/acs/k8s/cluster'
PCUrl = "https://"+PC+":9440/api/nutanix/v3/clusters/list"
Neturl ='https://'+PC+':9440/api/nutanix/v3/subnets/list'
Imageurl ='https://'+PE+':9440/PrismGateway/services/rest/v2.0/images/'


s = requests.Session()
rPC = s.post(PCUrl, auth=(PCusername, PCpassword), verify=False)
cookies = rPC.cookies


def GetNetuuid(NetworkName):
    payload = {"filter": "", "offset": 0, "length": 200 }
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    r = requests.post(Neturl, auth=(PCusername, PCpassword), verify=False, data=json.dumps(payload), headers=headers )
    outputNet = r.json()
    global Netuuid
    for p in outputNet["entities"]:
        if NetworkName == p['status']['name']:
            print('Network found with uuid', p['metadata']['uuid'])
            Netuuid = p['metadata']['uuid']
            return Netuuid
    try:
        Netuuid
    except NameError:
        print('Network', NetworkName, 'not found')


def GetImageuuid(Image):
    global IMGuuid
    headers = {'Accept': 'application/json'}
    r = requests.get(Imageurl, auth=(PEUsername, PEPassword), verify=False, headers=headers)
    outputIMG = r.json()
    for p in outputIMG["entities"]:
        if Image == p['name']:
            print('Image found with uuid', p['uuid'])
            IMGuuid = p['uuid']
            return IMGuuid
    try:
        IMGuuid
    except  NameError:
        print('Image', Image,'not found')


def GetClusteruuid():
    headers = {'Accept': 'application/json'}
    r = requests.get('https://'+PE+':9440/PrismGateway/services/rest/v2.0/cluster', auth=(PEUsername, PEPassword),
                     verify=False, headers=headers)
    output = r.json()
    print('Cluster:', output['name'], 'with uuid :',output['cluster_uuid'])
    clusteruuid = output['cluster_uuid']
    return clusteruuid


def K8sClusterRelease():
    releaseList = ['1.8.13', '1.9.6', '1.10.3']
    global release
    while True:
        print('Kubernetes version', releaseList, ': default is 1.8.13\n')
        release = input('Type version or press ENTER for default :')
        if release in releaseList:
            print('Selected version is : ',release)
            break
        if release == '':
            release = '1.8.13'
            print('Selected version is :',release)
            break
        else:
            print('wrong version selected')
    return release


def Workerconfig():
    print('Worker default config is : 3 Workers, 8 GB of Memory, 120 GB disk and 4 vCPU')
    answer = input('Type yes or no if you want to use default config :\n')
    if answer == 'yes':
        Number = 3
        Memory = 8092
        Disk = 122880
        vcpu = 4
        return Number,Memory,Disk,vcpu
    while True:
        print('Please type number of worker , should be at least 3')
        try:
            Number = int(input('Type number or press ENTER for default [3]\n'))
        except ValueError:
            Number = 3
            break
        if Number >= 3:
            break
    while True:
        print('Please type amount of memory in GB per worker')
        try:
            Memory = int(input('Type number or press ENTER for default [8] GB\n'))
        except ValueError:
            Memory = 8092
            break
        if Memory*1024 >= 4096:
            Memory = Memory*1024
            break
        print('Should be at least 4GB')
    while True:
        print('Please type amount of Disk in GB per worker')
        try:
            Disk = int(input('Type number or press ENTER for default [120] GB\n'))
        except ValueError:
            Disk = 122880
            break
        if Disk*1024 >= 12880:
            Disk = Disk*1024
            break
        print('Should be at least 120GB')
    while True:
        print('Please type number of vCPU , should be at least 2')
        try:
            vcpu = int(input('Type number or press ENTER for default [4]\n'))
        except ValueError:
            vcpu = 4
            break
        if vcpu >= 2:
            break

    return Number, Memory, Disk, vcpu

def Masterconfig():
    print('Master default config is : 1 Master, 4 GB of Memory, 120 GB disk and 2 vCPU')
    answer = input('Type yes or no if you want to use default config :\n')
    if answer == 'yes':
        Memory = 4096
        Disk = 122880
        vcpu = 2
        return Memory,Disk,vcpu
    while True:
        print('Please type amount of memory in GB')
        try:
            Memory = int(input('Type number or press ENTER for default [4]\n'))
        except ValueError:
            Memory = 4096
            break
        if Memory >= 4:
            Memory = Memory*1024
            break
        print('Should be at least 4 GB')
    while True:
        print('Please type amount of Disk in GB ')
        try:
            Disk = int(input('Type number or press ENTER for default [120] GB\n'))
        except ValueError:
            Disk = 122880
            break
        if Disk*1024 >= 12880:
            Disk = Disk*1024
            break
        print('Should be at least 120GB')
    while True:
        print('Please type number of vCPU , should be at least 2')
        try:
            vcpu = int(input('Type number or press ENTER for default [2]\n'))
        except ValueError:
            vcpu = 2
            break
        if vcpu >= 2:
            break

    return Memory, Disk, vcpu


def EtcdConfig():
    print('Etcd ressources default config is : 3 etcd, 8 GB of Memory, 120 GB disk and 2 vCPU')
    answer = input('Type yes or no if you want to use default config :\n')
    if answer == 'yes':
        Number = 3
        Memory = 8092
        Disk = 122880
        vcpu = 2
        return Number,Memory,Disk,vcpu
    while True:
        print('Please type number of worker , should be at least 3')
        try:
            Number = int(input('Type number or press ENTER for default [3]\n'))
        except ValueError:
            Number = 3
            break
        if Number >= 3:
            break
    while True:
        print('Please type amount of memory in GB per worker')
        try:
            Memory = int(input('Type number or press ENTER for default [8] GB\n'))
        except ValueError:
            Memory = 8092
            break
        if Memory*1024 >= 4096:
            Memory = Memory*1024
            break
        print('Should be at least 4GB')
    while True:
        print('Please type amount of Disk in GB per worker')
        try:
            Disk = int(input('Type number or press ENTER for default [120] GB\n'))
        except ValueError:
            Disk = 122880
            break
        if Disk*1024 >= 12880:
            Disk = Disk*1024
            break
        print('Should be at least 120GB')
    while True:
        print('Please type number of vCPU , should be at least 2')
        try:
            vcpu = int(input('Type number or press ENTER for default [2]\n'))
        except ValueError:
            vcpu = 2
            break
        if vcpu >= 2:
            break

    return Number, Memory, Disk, vcpu


def buildpayload():
    ClusterK8SName = input("Type Kubernetes cluster name : ")
    version = K8sClusterRelease()
    osflavor = input("Please type OS Flavor, ubuntu or centos : ")
    image = GetImageuuid("acs-" + osflavor)
    network = input("Type Network name : ")
    container = input("Type container name : ")
    FS  = input("Type FS : ext4 or xfs : ")
    Netuuid = GetNetuuid(network)
    MasterMem, MasterDisk, MasterCPU = Masterconfig()
    etcdnumber, etcdmem, etcdDisk, etcdCPU = EtcdConfig()
    clusteruuid = GetClusteruuid()

    data = {
        "name":ClusterK8SName,
        "description": "",
        "vm_network":Netuuid,
        "k8s_config":{
            "workers": [],
            "service_cluster_ip_range":"172.19.0.0/16",
            "network_cidr":"172.20.0.0/16",
            "fqdn":"",
            "masters":[
                {
                "cpu":MasterCPU,
                "memory_mib":MasterMem,
                "image":image,
                "disk_mib":MasterDisk
                }
            ],
            "os_flavor":osflavor,
            "network_subnet_len":24,
            "version":'v'+version
        }
        ,"cluster_ref":clusteruuid,
        "logging_config":
            {
            "enable_app_logging":False},
            "storage_class_config":
                {
                    "metadata":
                        {
                            "name":"default-storageclass"},
                    "spec":
                        {
                            "cluster_ref":clusteruuid,
                            "user":PEUsername,
                            "password":PEPassword,
                            "storage_container":container,
                            "file_system":FS,
                            "flash_mode":False
                        }
                },
            "etcd_config":
                {
                    "num_instances":etcdnumber,
                    "name":ClusterK8SName,
                    "resource_config":
                        {
                            "cpu":etcdCPU,
                            "memory_mib":etcdmem,
                            "image":image,
                            "disk_mib":etcdDisk
                        }
                }
    }

    WorkerNumber, WorkerMem, WorkerDisk, WorkerCPU = Workerconfig()

    for _ in range(WorkerNumber):
        data["k8s_config"]["workers"].append(
            {"cpu": WorkerCPU, "memory_mib": WorkerMem, "image": image, "disk_mib": WorkerDisk})

    payload = json.dumps(data)
    payload = json.loads(payload)
    return payload


data = buildpayload()

headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}

r = requests.post(Karbonurl, auth=(PCusername, PCpassword), verify=False, data=json.dumps(data), headers=headers,
                  cookies=cookies)

output = r.json()

print(output)
