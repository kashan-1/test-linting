import ssl
from urllib.request import urlretrieve
from diagrams import Diagram, Cluster, Edge, Node
from diagrams.aws.compute import EC2
from diagrams.aws.network import TransitGateway
from diagrams.aws.network import ClientVpn
from diagrams.generic.network import Switch
from diagrams.onprem.client import Users
from diagrams.aws.network import VPC
from diagrams.aws.security import IdentityAndAccessManagementIamAWSStsAlternate
from diagrams.aws.security import (
    IdentityAndAccessManagementIamTemporarySecurityCredential,
)
from diagrams.custom import Custom
from diagrams.aws.analytics import ManagedStreamingForKafka
from diagrams.aws.compute import EC2
from diagrams.aws.compute import Fargate
from diagrams.aws.integration import SimpleQueueServiceSqs, SQS
from diagrams.aws.database import Dynamodb, DDB
from diagrams.aws.storage import SimpleStorageServiceS3, S3
from diagrams.generic.device import Mobile
from diagrams.aws.security import WAF
from diagrams.aws.mobile import APIGateway
from diagrams.aws.security import Cognito
from diagrams.programming.language import Bash
from diagrams.aws.database import Aurora
from diagrams.aws.network import ElbApplicationLoadBalancer, ALB
from diagrams.aws.network import NATGateway
from diagrams.aws.network import Endpoint
from diagrams.aws.network import CloudFront, CF
from diagrams.aws.analytics import DataLakeResource
from diagrams.aws.security import KeyManagementService, KMS
from diagrams.aws.security import SecretsManager
from diagrams.saas.logging import Datadog, DataDog
from diagrams.azure.identity import ADIdentityProtection
from diagrams.saas.identity import Okta


graph_attr = {
    "fontname": "Verdana",
    "labelloc": "t",
    "fontsize": "50",
    "layout": "dot",
    "compound": "true",
    # "splines": "spline"
}

cluster_attr = {
    "fontname": "Verdana",
    "fontsize": "25",
    "labelloc": "b",
}

node_attr = {
    "fontname": "Verdana",
}

edge_attr = {
    # "minlen": "3.0",
    # "penwidth":"4.0",
    # "concentrate": "true"
}

ssl._create_default_https_context = ssl._create_unverified_context

# Download an image to be used into a Custom Node class
okta_url = "https://upload.wikimedia.org/wikipedia/commons/5/5c/Okta_logo.svg"
okta_icon = "Okta_logo.svg"
urlretrieve(okta_url, okta_icon)

device_browser_url = (
    "http://media.bizj.us/view/img/1217421/screen-shot-2013-10-16-at-124757-pm.png"
)
device_browser_icon = "screen-shot-2013-10-16-at-124757-pm.png"
urlretrieve(device_browser_url, device_browser_icon)

cloud_api_url = "https://cdn.vectorstock.com/i/1000x1000/75/49/cloud-api-software-integration-icon-vector-23527549.webp"
cloud_api_icon = "cloud-api-software-integration-icon-vector-23527549.webp"
urlretrieve(cloud_api_url, cloud_api_icon)

databricks_url = (
    "https://upload.wikimedia.org/wikipedia/commons/6/63/Databricks_Logo.png"
)
databricks_icon = "Databricks_Logo.png"
urlretrieve(databricks_url, databricks_icon)

sumologic_url = "https://files.readme.io/9d59b0f-SumoLogic_Logo_SumoBlue_RGB-1.gif"
sumologic_icon = "9d59b0f-SumoLogic_Logo_SumoBlue_RGB-1.gif"
urlretrieve(sumologic_url, sumologic_icon)

pagerduty_url = "https://www.drupal.org/files/styles/grid-4-2x/public/pagerduty.png"
pagerduty_icon = "pagerduty.png"
urlretrieve(pagerduty_url, pagerduty_icon)

chargebee_url = (
    "https://upload.wikimedia.org/wikipedia/commons/0/01/Chargebee-logotype.png"
)
chargebee_icon = "Chargebee-logotype.png"
urlretrieve(chargebee_url, chargebee_icon)

adyen_url = "https://upload.wikimedia.org/wikipedia/commons/9/9f/Adyen_Logo.png"
adyen_icon = "Adyen_Logo.png"
urlretrieve(adyen_url, adyen_icon)


with Diagram(
    "Digital Services Platform (Subscription) Network Architecture",
    show=False,
    graph_attr=graph_attr,
    edge_attr=edge_attr,
    node_attr=node_attr,
    direction="TB",
):
    # with Diagram("Subscription Infrastructure", show=False, direction="LR"):
    # with Diagram("Digital Services Platform", show=False, direction="TB") as diag:
    with Cluster("Users", graph_attr=cluster_attr):
        users = Users("Users")

    with Cluster(
        "",
    ):
        # okta = Custom("", okta_icon)
        okta = Okta()

    with Cluster("VPC:siq-sso", graph_attr=cluster_attr):
        sts = IdentityAndAccessManagementIamAWSStsAlternate("STS")
        iam = IdentityAndAccessManagementIamTemporarySecurityCredential("IAM")

        aws_client_vpn = ClientVpn("AWS Client VPN")
        transit_gateway = TransitGateway("AWS Transit Gateway")

        users >> aws_client_vpn >> transit_gateway
        aws_client_vpn >> Edge(xlabel="user auth") << okta

        users >> okta
        okta >> Edge(color="darkgreen") << sts
        sts >> Edge(color="darkgreen") << iam

    with Cluster("Client Device", graph_attr=cluster_attr):
        hf_mobile = Mobile("HF Mobile App")
        device_browser = Custom("SIQ Web App", device_browser_icon)
        sn_mobile = Mobile("SN Mobile App")
        (
            sn_mobile
            >> Edge(xlabel="deep link")
            >> device_browser
            << Edge(xlabel="deep link")
            << hf_mobile
        )
        sn_mobile >> Edge(color="darkgreen", xlabel="deep link") << hf_mobile
        # sqs - Edge(color="brown", style="dotted") - dynamodb - Edge(color="brown", style="dotted") - s3

    with Cluster("VPC:siq-<env>-shared-infra", graph_attr=cluster_attr):
        # vpc = VPC("Shared Infra VPC")
        msk_vpc_endpoint1 = Endpoint("MSK VPC Endpoint")
        # msk_vpc_endpoint2 = Endpoint("MSK VPC Endpoint 2")
        with Cluster("Message Queue"):
            sqs = SQS("SQS")
        with Cluster("Configuration"):
            dynamodb = DDB("Dynamo DB")
        with Cluster("Data Lake"):
            s3 = S3("S3 Buckets")
        # sqs - Edge(color="brown", style="dotted") - dynamodb - Edge(color="brown", style="dotted") - s3
        msk = ManagedStreamingForKafka("SBI-MSK")
        jumphost = EC2("SSH Jumphost")
        kafkamanager = EC2("Kafka Manager")
        # fargate = Fargate("Kafka Consumers")

        # Step 2
        # transit_gateway >> vpc
        # vpc >> msk
        jumphost >> msk
        kafkamanager >> msk
        # msk << Edge(xlabel="Kafka consumers" ) << fargate
        msk_vpc_endpoint1 >> msk
        # msk_vpc_endpoint2 >> msk
        (
            transit_gateway
            >> Edge(
                color="black",
                ltail="cluster_VPC:siq-sso",
                lhead="cluster_VPC:siq-<env>-shared-infra",
            )
            >> msk_vpc_endpoint1
        )

    with Cluster("VPC:zepp", graph_attr=cluster_attr):
        rollup_service = Fargate("Rollup\nService")
        aggregate_service = Fargate("Aggregate\nService")
        edp_kafka_consumer = Fargate("EDP\nKafka Consumer")
        wellness_insight_consumer = Fargate("Wellness\nInsight Consumer")
        wellness_aggregate_service = Fargate("Wellness\nAggregate Service")
        cloudfront_webui = CF("CloudFront Web UI")
        webui_contents = S3("Web UI Contents")
        rollup_service >> Edge(xlabel="Publish") >> msk_vpc_endpoint1
        aggregate_service >> Edge(xlabel="Consume") >> msk_vpc_endpoint1
        edp_kafka_consumer >> Edge(xlabel="Consume") >> msk_vpc_endpoint1
        wellness_insight_consumer >> Edge(xlabel="Consume") >> msk_vpc_endpoint1
        device_browser >> Edge(xlabel="HTTPS TLSv1.2+") >> cloudfront_webui
        cloudfront_webui >> webui_contents

    with Cluster("VPC:siq-dp", graph_attr=cluster_attr):
        datalake = DataLakeResource("Datalake")
        with Cluster("SDP Service VPC"):
            tools = Bash("Int tools")
            # sdp_service_vpc = VPC("")
        with Cluster("SDP Databricks VPC"):
            databricks = Custom("", databricks_icon)
            # sdp_datalake_vpc = VPC("")
        # sdp_service_vpc >> tools
        # sdp_datalake_vpc >> databricks
        # sdp_service_vpc >> msk_vpc_endpoint2
        # sdp_datalake_vpc >> msk_vpc_endpoint2
        (
            databricks
            >> Edge(
                color="black",
                minlen="4",
                ltail="cluster_VPC:siq-dp",
                lhead="cluster_VPC:siq-<env>-shared-infra",
            )
            >> msk_vpc_endpoint1
        )

    with Cluster("VPC:siq-ecim", graph_attr=cluster_attr):
        waf = WAF("WAF")
        api_gateway = APIGateway("API Gateway")
        cognito_user_pool = Cognito("Cognito User Pool")
        waf >> api_gateway >> cognito_user_pool
        sn_mobile >> Edge(xlabel="Cognito\nAuthentication") >> waf
        hf_mobile >> Edge(xlabel="Cognito\nAuthentication") >> waf

    with Cluster("Harpers Ferry", graph_attr=cluster_attr):
        hf_cloud_apis = Custom("", cloud_api_icon)
        hf_mobile >> Edge(xlabel="Cognito\nAuthentication") >> hf_cloud_apis

    with Cluster("VPC:siq-dsp", graph_attr=cluster_attr):
        with Cluster("Private Subnet"):
            ec2_jumphost = EC2("Jump Host")
            internal_tools = Bash("Int tools")
            ec2_jumphost - Edge(color="brown", style="dotted") - internal_tools

        with Cluster("Backend Subnet"):
            aurora_db = Aurora("Amazon Aurora")
        with Cluster("Service Subnet"):
            subscription_mgmt_be_api = Fargate("Subscription\nManagement BE API")
            subscription_mgmt_content_be_api = Fargate("Subscription\nContent BE API")
            chargebee_kafka_event_producer = Fargate("ChargeBee\nKafka Event Producer")
            wellness_score_kafka_consumer = Fargate("Wellness Score\nKafka Consumer")
            subscription_mgmt_be_alb = ALB("Int ALB")
            subscription_mgmt_content_be_alb = ALB("Int ALB")
            chargebee_kafka_event_producer_be_alb = ALB("Int ALB")
            subscription_mgmt_fe_api = Fargate("Subscription\nManagement FE API")
            subscription_mgmt_content_fe_api = Fargate("Subscription\nContent FE API")
            chargebee_kafka_event_fe_api = Fargate("ChargeBee Kafka\nEvent FE API")
        with Cluster("Public Subnet"):
            # public_subnet_nat_gateway = NATGateway("NAT")
            subscription_mgmt_ext_alb = ALB("Ext ALB")
            subscription_mgmt_content_ext_alb = ALB("Ext ALB")
            chargebee_kafka_event_producer_ext_alb = ALB("Ext ALB")
            subscription_mgmt_ext_waf = WAF("WAF")
            subscription_mgmt_content_ext_waf = WAF("WAF")
            chargebee_kafka_event_producer_ext_waf = WAF("WAF")

            # connections
            hf_mobile >> Edge(xlabel="Get Sleeper Info") >> subscription_mgmt_ext_waf
            sn_mobile >> subscription_mgmt_content_ext_waf
            (
                subscription_mgmt_ext_waf
                >> Edge(xlabel="HTTP TLSv1.2+")
                >> subscription_mgmt_ext_alb
            )
            (
                subscription_mgmt_content_ext_waf
                >> Edge(xlabel="HTTP TLSv1.2+")
                >> subscription_mgmt_content_ext_alb
            )
            subscription_mgmt_ext_alb >> subscription_mgmt_fe_api
            subscription_mgmt_content_ext_alb >> subscription_mgmt_content_fe_api
            (
                subscription_mgmt_fe_api
                >> Edge(xlabel="HTTP TLSv1.3")
                >> subscription_mgmt_be_alb
            )
            (
                subscription_mgmt_content_fe_api
                >> Edge(xlabel="HTTP TLSv1.3")
                >> subscription_mgmt_content_be_alb
            )
            subscription_mgmt_be_alb >> subscription_mgmt_be_api
            subscription_mgmt_content_be_alb >> subscription_mgmt_content_be_api
            subscription_mgmt_be_api >> Edge(xlabel="RW") >> aurora_db
            subscription_mgmt_content_be_api >> Edge(xlabel="R") >> aurora_db
            wellness_score_kafka_consumer >> Edge(xlabel="W") >> aurora_db
            (
                chargebee_kafka_event_producer_ext_waf
                >> chargebee_kafka_event_producer_ext_alb
                >> chargebee_kafka_event_fe_api
                >> Edge(xlabel="HTTP TLSv1.3")
                >> chargebee_kafka_event_producer_be_alb
                >> chargebee_kafka_event_producer
                >> Edge(xlabel="RW")
                >> aurora_db
            )
            ec2_jumphost >> aurora_db
            wellness_score_kafka_consumer << Edge(xlabel="Consume") << msk_vpc_endpoint1
            (
                chargebee_kafka_event_producer
                >> Edge(xlabel="Publish")
                >> msk_vpc_endpoint1
            )
            subscription_mgmt_fe_api >> hf_cloud_apis
            hf_cloud_apis >> subscription_mgmt_ext_waf

    with Cluster("VPC:siq-secrets", graph_attr=cluster_attr):
        aws_kms = KMS("AWS KMS")
        secrets_manager = SecretsManager("AWS Secrets Manager")
        (
            aws_kms
            << secrets_manager
            << Edge(
                label="Use Least\nPrevilage Access",
                color="black",
                minlen="1",
                ltail="cluster_VPC:siq-secrets",
                lhead="cluster_VPC:siq-dsp",
            )
            << subscription_mgmt_content_fe_api
        )
        webui_contents >> Edge(color="white", minlen="3") >> msk_vpc_endpoint1
        transit_gateway >> Edge(color="white", minlen="2") >> msk_vpc_endpoint1
        # secrets_manager >> Edge(minlen="3") >> public_subnet_nat_gateway

    with Cluster("Managed Services:Monitoring", graph_attr=cluster_attr):
        sumologic = Custom("", sumologic_icon)
        datadog = DataDog()
        pagerduty = Custom("", pagerduty_icon)
        sumologic >> Edge(color="brown", style="dotted") >> pagerduty
        datadog >> Edge(color="brown", style="dotted") >> pagerduty
        (
            databricks
            >> Edge(
                color="black",
                style="dotted",
                minlen="4",
                ltail="cluster_VPC:siq-dp",
                lhead="cluster_Managed Services:Monitoring",
            )
            >> pagerduty
        )
        (
            secrets_manager
            >> Edge(
                color="black",
                style="dotted",
                minlen="4",
                ltail="cluster_VPC:siq-secrets",
                lhead="cluster_Managed Services:Monitoring",
            )
            >> pagerduty
        )
        (
            cognito_user_pool
            >> Edge(
                color="black",
                style="dotted",
                minlen="4",
                ltail="cluster_VPC:siq-ecim",
                lhead="cluster_Managed Services:Monitoring",
            )
            >> pagerduty
        )
        (
            msk_vpc_endpoint1
            >> Edge(
                color="black",
                style="dotted",
                minlen="4",
                ltail="cluster_VPC:siq-<env>-shared-infra",
                lhead="cluster_Managed Services:Monitoring",
            )
            >> pagerduty
        )
        (
            aurora_db
            >> Edge(
                color="black",
                style="dotted",
                minlen="4",
                ltail="cluster_VPC:siq-dsp",
                lhead="cluster_Managed Services:Monitoring",
            )
            >> pagerduty
        )
        (
            webui_contents
            >> Edge(
                color="black",
                style="dotted",
                minlen="4",
                ltail="cluster_VPC:zepp",
                lhead="cluster_Managed Services:Monitoring",
            )
            >> pagerduty
        )

    with Cluster("VPC:Chargebee", graph_attr=cluster_attr):
        chargebee = Custom("", chargebee_icon)
        chargebee_offerings = (
            Node(
                "Product Catalog\nPlans\nPayment Gateway\nWebhooks\nAPI Keys\nCustomers\nSubscriptions\nFinancial Reports",
                shape="rectangle",
                height="3",
                width="2.8",
                fontsize="20",
            ),
        )
        chargebee_roles_and_perms = Node(
            "Roles and Permissions",
            shape="rectangle",
            height="0.5",
            width="3.2",
            fontsize="20",
        )
        # chargebee_roles_and_perms >> Edge(color="black", minlen="4", ltail="cluster_VPC:siq-dp", lhead="cluster_VPC:Chargebee") >> msk_vpc_endpoint1
        chargebee_offerings << subscription_mgmt_be_api
        chargebee_offerings >> hf_cloud_apis
        chargebee_offerings >> chargebee_kafka_event_producer_ext_waf

    with Cluster("Adyen Payment Gateway", graph_attr=cluster_attr):
        adyen_payment_gateway = Custom("", adyen_icon)
        (
            chargebee
            >> Edge(
                color="black",
                ltail="cluster_VPC:Chargebee",
                lhead="cluster_Ayden Payment Gateway",
            )
            >> adyen_payment_gateway
        )

    with Cluster("SN/HF Support Users", graph_attr=cluster_attr):
        sn_hf_support_users = Users("SN and HF\nSupport Users")

    with Cluster("Azure AD", graph_attr=cluster_attr):
        azure_ad_identify_protection = ADIdentityProtection(
            "Azure AD\nIdentity Protection"
        )
        (
            sn_hf_support_users
            >> Edge(xlabel="SSO + MFA\nEnabled", labelloc="c")
            >> azure_ad_identify_protection
            >> Edge(xlabel="Platform\nManagement")
            >> chargebee_roles_and_perms
        )
