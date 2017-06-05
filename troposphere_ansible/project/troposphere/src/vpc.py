from troposphere import Ref, Template, Tags, Join, Parameter
from troposphere.ec2 import VPC, Subnet, NetworkAcl, NetworkAclEntry, InternetGateway, \
VPCGatewayAttachment, RouteTable, Route, SubnetRouteTableAssociation, SubnetNetworkAclAssociation

t = Template()

stackname_param = t.add_parameter(Parameter(
    "stackname",
    Description="Environment Name (default: StackNameNotDefined)",
    Type="String",
    Default="Dev",
))

t.add_description("Stack creating a VPC")

vpc = t.add_resource(VPC(
  "VPC",
  CidrBlock="172.21.0.0/16",
  InstanceTenancy="default",
  EnableDnsSupport=True,
  EnableDnsHostnames=False,
  Tags=Tags(
    Name=Ref("AWS::StackName")
  )
))

# internet gateway
internetGateway = t.add_resource(InternetGateway(
  "InternetGateway",
  Tags=Tags(
    Name=Join("", [Ref("AWS::StackName"), "-gateway"]),
  ),
))

gatewayAttachment = t.add_resource(VPCGatewayAttachment(
  "InternetGatewayAttachment",
  InternetGatewayId=Ref(internetGateway),
  VpcId=Ref(vpc)
))

# public routing table
publicRouteTable = t.add_resource(RouteTable(
  "PublicRouteTable",
  VpcId=Ref(vpc),
  Tags=Tags(
   Name=Join("-", [Ref("AWS::StackName"), "public-rt"]),
  ),
))

privateRouteTable = t.add_resource(RouteTable(
  "PrivateRouteTable",
  VpcId=Ref(vpc),
  Tags=Tags(
    Name=Join("-", [Ref("AWS::StackName"), "private-rt"]),
  ),
))

internetRoute = t.add_resource(Route(
  "RouteToInternet",
  DestinationCidrBlock="0.0.0.0/0",
  GatewayId=Ref(internetGateway),
  RouteTableId=Ref(publicRouteTable),
  DependsOn=gatewayAttachment.title
))

# private subnetworks
subnetPrivateA = t.add_resource(Subnet(
  "StackPrivateSubnetA",
  AvailabilityZone=Join("", [Ref("AWS::Region"), "a"]),
  CidrBlock="172.21.1.0/24",
  MapPublicIpOnLaunch=False,
  Tags=Tags(
    Name=Join("", [Ref("AWS::StackName"), " private subnet A"]),
  ),
  VpcId=Ref(vpc)
))

t.add_resource(SubnetRouteTableAssociation(
  "PrivateSubnetARouteTable",
  RouteTableId=Ref(privateRouteTable),
  SubnetId=Ref(subnetPrivateA)
))

subnetPrivateB = t.add_resource(Subnet(
  "StackPrivateSubnetB",
  AvailabilityZone=Join("", [Ref("AWS::Region"), "b"]),
  CidrBlock="172.21.2.0/24",
  MapPublicIpOnLaunch=False,
  Tags=Tags(
    Name=Join("", [Ref("AWS::StackName"), " private subnet B"]),
  ),
  VpcId=Ref(vpc)
))

t.add_resource(SubnetRouteTableAssociation(
  "PrivateSubnetBRouteTable",
  RouteTableId=Ref(privateRouteTable),
  SubnetId=Ref(subnetPrivateB)
))

subnetPrivateC = t.add_resource(Subnet(
  "StackPrivateSubnetC",
  AvailabilityZone=Join("", [Ref("AWS::Region"), "c"]),
  CidrBlock="172.21.3.0/24",
  MapPublicIpOnLaunch=False,
  Tags=Tags(
    Name=Join("", [Ref("AWS::StackName"), " private subnet C"]),
  ),
  VpcId=Ref(vpc)
))

t.add_resource(SubnetRouteTableAssociation(
  "PrivateSubnetCRouteTable",
  RouteTableId=Ref(privateRouteTable),
  SubnetId=Ref(subnetPrivateC)
))

# public subnetworks
subnetPublicA = t.add_resource(Subnet(
  "StackPublicSubnetA",
  AvailabilityZone=Join("", [Ref("AWS::Region"), "a"]),
  CidrBlock="172.21.128.0/24",
  MapPublicIpOnLaunch=True,
  Tags=Tags(
    Name=Join("", [Ref("AWS::StackName"), " public subnet A"]),
  ),
  VpcId=Ref(vpc),
))

t.add_resource(SubnetRouteTableAssociation(
  "PublicSubnetARouteTable",
  RouteTableId=Ref(publicRouteTable),
  SubnetId=Ref(subnetPublicA)
))

subnetPublicB = t.add_resource(Subnet(
  "StackPublicSubnetB",
  AvailabilityZone=Join("", [Ref("AWS::Region"), "b"]),
  CidrBlock="172.21.129.0/24",
  MapPublicIpOnLaunch=True,
  Tags=Tags(
    Name=Join("", [Ref("AWS::StackName"), " public subnet B"]),
  ),
  VpcId=Ref(vpc),
))

t.add_resource(SubnetRouteTableAssociation(
  "PublicSubnetBRouteTable",
  RouteTableId=Ref(publicRouteTable),
  SubnetId=Ref(subnetPublicB)
))

subnetPublicC = t.add_resource(Subnet(
  "StackPublicSubnetC",
  AvailabilityZone=Join("", [Ref("AWS::Region"), "c"]),
  CidrBlock="172.21.130.0/24",
  MapPublicIpOnLaunch=True,
  Tags=Tags(
    Name=Join("", [Ref("AWS::StackName"), " public subnet C"]),
  ),
  VpcId=Ref(vpc)
))

t.add_resource(SubnetRouteTableAssociation(
  "PublicSubnetCRouteTable",
  RouteTableId=Ref(publicRouteTable),
  SubnetId=Ref(subnetPublicC)
))

# network ACL for private subnets
privateNetworkAcl = t.add_resource(NetworkAcl(
  "PrivateNetworkAcl",
  VpcId=Ref(vpc),
  Tags=Tags(
    Name=Join("", [Ref("AWS::StackName"), "-private-nacl"]),
  ),
))

t.add_resource(SubnetNetworkAclAssociation(
  "PrivateNetworkAAclAss",
  SubnetId=Ref(subnetPrivateA),
  NetworkAclId=Ref(privateNetworkAcl)
))

t.add_resource(SubnetNetworkAclAssociation(
  "PrivateNetworkBAclAss",
  SubnetId=Ref(subnetPrivateB),
  NetworkAclId=Ref(privateNetworkAcl)
))

t.add_resource(SubnetNetworkAclAssociation(
  "PrivateNetworkCAclAss",
  SubnetId=Ref(subnetPrivateC),
  NetworkAclId=Ref(privateNetworkAcl)
))

t.add_resource(NetworkAclEntry(
  "PrivateNetworkAclEntryIngress",
  CidrBlock="172.21.0.0/16",
  Egress=False,
  NetworkAclId=Ref(privateNetworkAcl),
  Protocol=-1,
  RuleAction="allow",
  RuleNumber=200
))

t.add_resource(NetworkAclEntry(
  "PrivateNetworkAclEntryEgress",
  CidrBlock="172.21.0.0/16",
  Egress=True,
  NetworkAclId=Ref(privateNetworkAcl),
  Protocol=-1,
  RuleAction="allow",
  RuleNumber=200
))

if __name__ == "__main__":
    with open('../../ansible/roles/vpc/files/vpc.json', 'w') as f:
        f.write(str(t.to_json()))
