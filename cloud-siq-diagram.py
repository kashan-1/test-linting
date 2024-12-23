import ssl 
from urllib.request import urlretrieve
from diagrams import Diagram, Cluster, Edge, Node
from diagrams.onprem.client import Users
from diagrams.custom import Custom
from diagrams.aws.analytics import ManagedStreamingForKafka
from diagrams.aws.analytics import EMR
from diagrams.aws.compute import EC2 , EC2Instances
from diagrams.aws.database import Dynamodb, DDB
from diagrams.aws.storage import SimpleStorageServiceS3, S3
from diagrams.aws.network import ElbApplicationLoadBalancer, ALB
from diagrams.aws.network import CloudFront, CF
from diagrams.aws.network import Route53
from diagrams.aws.compute import ECS




graph_attr = {
    "splines": "spline",
    "fontsize": "20",
    
}

node_attr = {
    "fontsize": "15",
    "fontcolor": "black",
    "width": "1.0",
    "height": "1.0",
    "labelloc": "b",  # Place label at the bottom
    "fixedsize": "true",
}

ssl._create_default_https_context = ssl._create_unverified_context

group_url = "https://www.freeiconspng.com/download/35905"
group_icon = "35905.png"
urlretrieve(group_url, group_icon)


# _url = "https://iconduck.com/icons/109308/user-group"
# _icon = "_logo.svg"
# urlretrieve(_url, _icon)

sales_sheet_url = "https://www.freeiconspng.com/download/24173"
sales_sheet_icon = "24173.png"
urlretrieve(sales_sheet_url, sales_sheet_icon)

csp_hd_app_url = "https://www.freeiconspng.com/download/2363"
csp_hd_app_icon = "2363.png"
urlretrieve(csp_hd_app_url, csp_hd_app_icon)


mobile_app_url = "https://www.freeiconspng.com/download/2379"
mobile_app_icon = "2379.png"
urlretrieve(mobile_app_url, mobile_app_icon)

customer_service_url = "https://www.freeiconspng.com/download/1026"
customer_service_icon = "1026.png"
urlretrieve(customer_service_url, customer_service_icon)


bed_url = "https://www.freeiconspng.com/download/35985"
bed_icon = "35985.png"
urlretrieve(bed_url, bed_icon)



with Diagram("SIQ Architecture-Infrastructure View", show=False, graph_attr=graph_attr, node_attr=node_attr, direction="TB"):
    
     with Cluster("",graph_attr={"bgcolor": "transparent","penwidth": "0"}):
        # Reordered icons with spacing
        users_tech = Users("SIQ Tech\nOperations Team")
        spacer1 = Node(label="", shape="none", width="0.5", height="0.5")  # Spacer node
        users_biz = Users("SIQ Business\nOperation Team")
        spacer3 = Node(label="", shape="none", width="0.5", height="0.5")  # Spacer node
        sales_sheet = Custom("Sales Order\nSystem (Fusion)\nIntegration", sales_sheet_icon)
        spacer4 = Node(label="", shape="none", width="0.5", height="0.5")  # Spacer node
        mobile_app = Custom("CSP HD App", mobile_app_icon)
        spacer5 = Node(label="", shape="none", width="0.5", height="0.5")  # Spacer node
        customer_service = Custom("Customer Service", customer_service_icon)
        spacer6 = Node(label="", shape="none", width="0.5", height="0.5")
        csp_hd_app = Custom("Consumer Web & Mobile App", csp_hd_app_icon)
        spacer6 = Node(label="", shape="none", width="0.5", height="0.5")
        bed = Custom("Pumps", bed_icon)
        
     spacer_between_clusters = Node(label="", shape="none", width="0.5", height="0.5")

     with Cluster("",graph_attr={"bgcolor": "transparent","penwidth": "0"}):

        bucket_1 = S3("\nBucket")
        side_lb = ElbApplicationLoadBalancer("Elastic\nLoad Balancer")
        EC2_instance_1 = EC2("Instance")
        bed >> Edge(label="", style="", color="black", constraint="false") >> bucket_1
        bed >> Edge(label="", style="", color="black", constraint="false") >> side_lb
        bucket_1 >> Edge(style="invis") >> side_lb
        side_lb >> Edge(label="", style="", color="black") >> EC2_instance_1
  

     with Cluster("", graph_attr={"bgcolor": "transparent", "penwidth": "0"}, direction="TB"):
        
        # domain1 = Custom("boson.bmblabs.com", "259338_compute_copy_hosted_networking_route_icon.png")
        domain1 = Route53("boson.bmblabs.com")
        domain2 = Route53("<stack>-dg")
        domain3 = Route53("<stack>-ui")
        domain4 = Route53("<stack>-api")
        domain5 = Route53("<stack>-csp")
        domain6 = Route53("<stack>-csp-api")
        domain7 = Route53("<stack>-hd-api")
        domain8 = Route53("<stack>-order-api")
        domain9 = Route53("<stack>-ops")
        domain10 = Route53("<stack>-oc")
        domain11 = Route53("<stack>-ssh")
        # Connections within the third cluster
        bed >> Edge(label="Device\nAdmin", style="", color="black", labeljust="c") >> domain1
        bed >> Edge(label="Device\nGateway", style="", color="black" ,labeljust="c") >> domain2
        csp_hd_app >> Edge(label="User\nInterface", style="", color="black", labeljust="c") >> domain3
        csp_hd_app >> Edge(label="Frontend\n REST API", style="", color="black", labeljust="c") >> domain4
        customer_service >> Edge(label="Static\nPages", style="", color="black", labeljust="c") >> domain5
        customer_service >> Edge(label="REST API", style="", color="black", labeljust="c") >> domain6
        mobile_app >> Edge(label="", style="", color="black", labeljust="c") >> domain7
        sales_sheet >> Edge(label="", style="", color="black", labeljust="c") >> domain8
        users_biz >> Edge(label="Products\nOps Portal", style="", color="black", labeljust="c") >> domain9
        users_biz >> Edge(label="Ops center", style="", color="black", labeljust="c") >> domain10
        users_tech >> Edge(label="SSh/Tunnel", style="", color="black", labeljust="c") >> domain11


        with Cluster("Public IP Subnet", graph_attr={"bgcolor": "transparent", "penwidth": "1"}):
            spacer10 = Node(label="", shape="none", height="0.2")
            with Cluster("Public Security Group", graph_attr={"bgcolor": "transparent","penwidth": "3" ,"style": "solid", "color": "black"}):

                ELB_1 = ElbApplicationLoadBalancer("Boson ELB")   
                ELB_2 = ElbApplicationLoadBalancer("DG ELB")
                cloudfront_1 = CloudFront("Web UI\n(CloudFront)")
                ELB_3 = ElbApplicationLoadBalancer("Application\nAPI ELB")
                cloudfront_2 = CloudFront("CSP UI\n(CloudFront)")
                ELB_4 = ElbApplicationLoadBalancer("Admin API\nELB")
                

                domain1 >> Edge(style="", color="black", labeljust="c") >> ELB_1
                domain2 >> Edge(style="", color="black", labeljust="c") >> ELB_2
                domain3 >> Edge(style="", color="black", labeljust="c") >> cloudfront_1
                domain4 >> Edge(style="", color="black", labeljust="c") >> ELB_3
                domain5 >> Edge(style="", color="black", labeljust="c") >> cloudfront_2
                domain6 >> Edge(style="", color="black", labeljust="c") >> ELB_4
                domain7 >> Edge(style="", color="black", labeljust="c") >> ELB_4
                domain8 >> Edge(style="", color="black", labeljust="c") >> ELB_4

            with Cluster("", graph_attr={"bgcolor": "transparent","penwidth": "0"}):
                spacer11 = Node(label="", shape="none", width="0.5", height="0.5")
                domain8 >> Edge(style="invis") >> spacer11

         
            with Cluster("Admin Security Group", graph_attr={"bgcolor": "transparent","penwidth": "3" ,"style": "solid", "color": "black"}):

                ELB_5 = ElbApplicationLoadBalancer("Operation\nELB")
                spacer12 = Node(label="", shape="none", width="0.5", height="0.5")
                ELB_6 = ElbApplicationLoadBalancer("OpsCenter\nELB")
                ELB_7 = ElbApplicationLoadBalancer("SSH ELB")


                domain9 >> Edge(style="", color="black", labeljust="c") >> ELB_5
                domain10 >> Edge(style="", color="black", labeljust="c") >> ELB_6
                domain11 >> Edge(style="", color="black", labeljust="c") >> ELB_7

        with Cluster("Private IP Subnet", graph_attr={"bgcolor": "transparent", "penwidth": "1"}):
                spacer13 = Node(label="", shape="none", height="0.2")
                # Boson VPC Cluster
                with Cluster("Boson VPC", graph_attr={"bgcolor": "transparent", "penwidth": "1", "style": "solid", "color": "black"}):
                    instances_1 = EC2Instances("Boson\nServers")
                    ELB_1 >> Edge(style="", color="black", labeljust="c") >> instances_1
                    spacer13 >> Edge(style="invis", constraint = "false")>>instances_1
                
                # Admin Security Group Cluster
                with Cluster("API Tier", graph_attr={"bgcolor": "transparent", "penwidth": "1", "style": "solid", "color": "black"}):
                    
                    instances_2 = EC2Instances("Device\nGateway\nServers\n(Netty)")
                    instances_3 = EC2Instances("Application\nAPI Servers\n(Tomcat7)")
                    
                    # ALB/ELBv2 Cluster with Target Groups
                    with Cluster("ALB/ELBv2", graph_attr={"bgcolor": "transparent", "penwidth": "3", "style": "dashed", "color": "black"}):
                        ELB_8 = ElbApplicationLoadBalancer("Target Group")   
                        ELB_9 = ElbApplicationLoadBalancer("Target Group")   
                        
                    instances_4 = EC2Instances("Admin\nAPI Servers\n(Tomcat7)")
                    instances_5 = EC2Instances("Backoffice\nPortal\n(Tomcat8)")
                    
                    # Adding edges between ELBs and instances
                    ELB_2 >> Edge(style="", color="black", labeljust="c") >> instances_2
                    ELB_3 >> Edge(style="", color="black", labeljust="c") >> instances_3
                    instances_3 >> Edge(label="", style="", color="black", constraint="false") >> ELB_8
                    instances_4 >> Edge(label="", style="", color="black", constraint="false") >> ELB_9
                    cloudfront_2 >> Edge(style="invis") >> ELB_8
                    cloudfront_2 >> Edge(style="invis") >> ELB_9
                    ELB_4 >> Edge(style="", color="black", labeljust="c") >> instances_4
                    ELB_5 >> Edge(style="", color="black", labeljust="c") >> instances_5
            
                with Cluster("Operation Tier", graph_attr={"bgcolor": "transparent", "penwidth": "1", "style": "solid", "color": "black"}):
                    instances_6 = EC2Instances("SSH\nBastion\nServers")
                    EC2_instance_2 = EC2("Mon/Utility")
                    instances_6 >> Edge(style="invis") >> EC2_instance_2
                    ELB_7 >> Edge(style="") >> instances_6


                with Cluster("Services Tier (ECS / Docker)", graph_attr={"bgcolor": "transparent", "penwidth": "1", "style": "solid", "color": "black"}):
                    spacer14 = Node(label="", shape="none", height="0.2")
                    ecs_1 = ECS("Batch\nServer")
                    ecs_2 = ECS("Rollup\nServer")
                    ecs_3 = ECS("DB\nManager")
                    ecs_4 = ECS("Application\nServices")
                    ecs_5 = ECS("Admin\nServices")

                    ELB_8 >> Edge(style="", color="black", labeljust="c") >> ecs_4
                    ELB_9 >> Edge(style="", color="black", labeljust="c") >> ecs_5
                    ecs_2 >> Edge(label="", style="", color="black", constraint="false") >> ecs_3
                    ecs_3 >> Edge(label="", style="", color="black", constraint="false") >> ecs_2
   
                with Cluster("Infrastructure Tier", graph_attr={"bgcolor": "transparent", "penwidth": "1", "style": "solid", "color": "black"}):

                    EC2_instance_3 = EC2("BamFS\n(NFS)")
                    # kafka_1 = Custom("Kafka","259349_app_copy_services_sqs_icon.png")
                    kafka_1 = ManagedStreamingForKafka("Kafka")
                    hazelcast_1 = Custom("Hazelcast\nCluster","259332_cluster_compute_copy_emr_hdfs_icon.png")
                    dynamodb_1 = DDB("DynamoDB\nConfiguration\nData")
                    db_master = Custom("SQL\nMAster","259321_copy_database_db_instance_rds_icon.png")
                    db_standby = Custom("SQL\nStandby","259319_copy_database_instance_rds_standby_icon.png")
                    
                    c_1 = Custom("C* (DSE)","259332_cluster_compute_copy_emr_hdfs_icon.png")
                    emr_1 = Custom("Daily Job\n(Spark)","259339_compute_copy_emr_networking_icon.png")
                    bucket_2 = S3("Archival /\nBackups /\n Device")
                    

                    ecs_1 >> Edge(style="", color="black", labeljust="c") >> EC2_instance_3
                    ecs_2 >> Edge(style="", color="black", labeljust="c") >> hazelcast_1
                    ecs_3 >> Edge(style="", color="black", labeljust="c") >> dynamodb_1
                    ecs_4 >> Edge(style="", color="black", labeljust="c") >> dynamodb_1
                    dynamodb_1 >> Edge(style="invis", constraint="false") >> db_standby
                    ecs_5 >> Edge(style="", color="black", labeljust="c") >> db_master
                    db_master >> Edge(style="", color="black") >> db_standby
                    db_standby >> Edge(style="", color="black") >> db_master
                    db_master >> Edge(style="", color="black", constraint="false") >> emr_1
                    c_1 >> Edge(style="", color="black" , constraint="false") >> emr_1
                    emr_1 >> Edge(style="", color="black") >> bucket_2
                    instances_2 >> Edge(style="", color="black") >> kafka_1
                    instances_6 >> Edge(style="", color="black") >> emr_1
                    ELB_6 >> Edge(style="", color="black") >> c_1
                   


                   

                # with Cluster("Infrastructure Tier", graph_attr={"bgcolor": "transparent", "penwidth": "1"}):
                   


                    






                    





         

         
            

        

    
        
        
   



    
    