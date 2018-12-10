"""This module provides classes and functions to update tags for AWS services"""
import boto3
from botocore.exceptions import ClientError

class TagNotSupportedError(Exception):
    """An exception class which can be raised when tagging not supported"""

    def __init__(self, Service):
        super().__init__('Tagging not supported for service ' + Service)



class AwsTag:
    """Update tags for supported AWS services"""

    __Services__ = ['ec2', 's3', 'lambda', 'logs', 'rds', 'es', 'emr', 'dynamodb', 'firehose', \
                     'glacier', 'kms', 'apigateway', 'kinesis', 'cloudtrail', 'sqs', 'secretsmanager', \
		     'cloudfront', 'efs', 'sagemaker', 'redshift', 'elasticache', 'workspaces', \
		     'ds', 'dax', 'route53', 'directconnect' \
                    ]

    def __init__(self, Service=None):
        """Constructor"""

        self.Service = Service
        if self.Service not in AwsTag.__Services__:
            raise TagNotSupportedError(str(self.Service))

    def GetServicesCount(self):
        """Return number of supported services"""

        return len(AwsTag.__Services__)

    def TagResource(self, ResourceId, TagName, TagValue):
        """Update tags using boto3 method tag_resource()"""

        Client = boto3.client(self.Service)

        if self.Service == 'lambda':
            response = Client.tag_resource (
                Resource = ResourceId,
		Tags =  {
                    TagName: TagValue
                }
	    )
        elif self.Service == 'dax':
            response = Client.tag_resource (
                ResourceName = ResourceId,
		Tags = [
		    {
                        'Key': TagName,
			'Value': TagValue
		    }
		]
	    )
        elif self.Service == 'directconnect':
            response = Client.tag_resource (
                resourceArn = ResourceId,
		Tags = [
		    {
                        'key': TagName,
			'value': TagValue
		    }
		]
	    )
        elif self.Service == 'dynamodb':
            response = Client.tag_resource (
                ResourceArn = ResourceId,
		Tags = [
		    {
                        'Key': TagName,
			'Value': TagValue
		    }
		]
	    )
        elif self.Service == 'kms':
            response = Client.tag_resource (
                KeyId = ResourceId,
		Tags = [
		    {
                        'TagKey': TagName,
			'TagValue': TagValue
		    }
		]
	    )
        elif self.Service == 'apigateway':
            response = Client.tag_resource (
                resourceArn = ResourceId,
		tags = [
		    {
			TagName: TagValue
		    }
		]
	    )
        elif self.Service == 'secretsmanager':
            response = Client.tag_resource (
                SecretId = ResourceId,
		Tags = [
		    {
			'Key': TagName,
			'Value': TagValue
		    }
		]
	    )
        elif self.Service == 'cloudfront':
            response = Client.tag_resource (
                Resource = ResourceId,
		Tags = {
                    'Items': [
		        {
			    'Key': TagName,
			    'Value': TagValue
		        }
                    ]
		}
	    )
        else:
            raise TagNotSupportedError(str(self.Service))

        return True

    def AddTagsToResource(self, ResourceId, TagName, TagValue):
        """Update tags using boto3 method add_tags_to_resource()"""

        Client = boto3.client(self.Service)

        if self.Service == 'rds':
            response = Client.add_tags_to_resource (
                ResourceName = ResourceId,
                Tags = [
                    {
                        'Key': TagName,
                        'Value': TagValue
		    }
		]
	    )
        elif self.Service == 'elasticache':
            response = Client.add_tags_to_resource (
                ResourceName = ResourceId,
                Tags = [
                    {
                        'Key': TagName,
                        'Value': TagValue
		    }
		]
	    )
        elif self.Service == 'ds':
            response = Client.add_tags_to_resource (
                ResourceId = ResourceId,
                Tags = [
                    {
                        'Key': TagName,
                        'Value': TagValue
		    }
		]
	    )
        else:
            raise TagNotSupportedError(str(self.Service))

        return True

    def AddTags(self, ResourceId, TagName, TagValue):
        """Update tags using boto3 method add_tags()"""

        Client = boto3.client(self.Service)

        if self.Service == 'es':
            response = Client.add_tags (
                ARN = ResourceId,
                TagList = [
		    {
                        'Key': TagName,
                        'Value': TagValue
		    }
                ]
	    )
        elif self.Service == 'emr':
            response = Client.add_tags (
                ResourceId = ResourceId,
                Tags = [
		    {
                        'Key': TagName,
                        'Value': TagValue
		    }
                ]
	    )
        elif self.Service == 'cloudtrail':
            response = Client.add_tags (
                ResourceId = ResourceId,
                TagsList = [
		    {
                        'Key': TagName,
                        'Value': TagValue
		    }
                ]
	    )
        elif self.Service == 'sagemaker':
            response = Client.add_tags (
                ResourceArn = ResourceId,
                Tags = [
		    {
                        'Key': TagName,
                        'Value': TagValue
		    }
                ]
	    )
        elif self.Service == 'datapipeline':
            response = Client.add_tags (
                pipelineId = ResourceId,
                tags = [
		    {
                        'Key': TagName,
                        'Value': TagValue
		    }
                ]
	    )
        else:
            raise TagNotSupportedError(str(self.Service))

        return True

    def CreateTags(self, ResourceId, TagName, TagValue):
        """Update tags using boto3 method create_tags()"""

        Client = boto3.client(self.Service)

        if self.Service == 'ec2':
            response = Client.create_tags(
                Resources = [
		    ResourceId
		],
		Tags = [
                    {
		        'Key': TagName,
		        'Value': TagValue
                    }
		]
	    )
        elif self.Service == 'efs':
            response = Client.create_tags(
                FileSystemId = ResourceId,
		Tags = [
                    {
		        'Key': TagName,
		        'Value': TagValue
                    }
		]
	    )
        elif self.Service == 'redshift':
            response = Client.create_tags(
                ResourceName = ResourceId,
		Tags = [
                    {
		        'Key': TagName,
		        'Value': TagValue
                    }
		]
	    )
        elif self.Service == 'workspaces':
            response = Client.create_tags(
                ResourceId = ResourceId,
		Tags = [
                    {
		        'Key': TagName,
		        'Value': TagValue
                    }
		]
	    )
        else:
            raise TagNotSupportedError(str(self.Service))

        return True

    def UpdateS3Tag(self, ResourceId, TagName, TagValue):
        """Update s3 service tag"""
        Client = boto3.client('s3')

        response = Client.get_bucket_tagging (
            Bucket = ResourceId
	)
        Tags = response['TagSet']

        ### if tag exists, replace tag value; otherwise, append tag
        if self.IsTagExists(ResourceId, TagName):
            for Tag in Tags:
                if Tag['Key'] == TagName:
                    Tag['Value'] = TagValue
        else:
            Tags.append (
                {
                    'Key': TagName,
                    'Value': TagValue
                }
            )
           

        response = Client.put_bucket_tagging (
            Bucket = ResourceId,
            Tagging = {
                'TagSet': Tags
	    }
        )

        return True

    def UpdateLogsTag(self, ResourceId, TagName, TagValue):
        """Update cloudwatch logs service tag"""
        Client = boto3.client('logs')

        ### get LogGroupName from ResourceId
        LogGroupName = ResourceId.split(':')[-1]
	    
        response = Client.tag_log_group(
            logGroupName = LogGroupName,
            tags = {
	        TagName: TagValue
            }
	)

        return True

    def UpdateGlacierTag(self, ResourceId, TagName, TagValue):
        """Update glacier service tag"""
        Client = boto3.client('glacier')

        Vault = ResourceId.split(':')[-1].split('/')[-1]

        response = Client.add_tags_to_vault(
            vaultName = Vault,
            Tags = {
	            TagName: TagValue
            }
	)

        return True

    def UpdateKinesisTag(self, ResourceId, TagName, TagValue):
        """Update kinesis service tag"""
        Client = boto3.client('kinesis')

        StreamName = ResourceId.split(':')[-1].split('/')[-1]

        response = Client.add_tags_to_stream(
            StreamName = StreamName,
            Tags = {
	            TagName: TagValue
            }
	)

        return True

    def UpdateSqsTag(self, ResourceId, TagName, TagValue):
        """Update sqs service tag"""
        Client = boto3.client('sqs')

        response = Client.tag_queue(
            QueueUrl = ResourceId,
            Tags = [
                {
	            TagName: TagValue
                }
	    ]
	)

        return True

    def UpdateRoute53Tag(self, ResourceId, TagName, TagValue):
        """Update route53 service tag"""

        Client = boto3.client('route53')

        response = Client.change_tags_for_resource ( 
            ResourceType = 'hostedzone',
            ResourceId = ResourceId,
            AddTags = [
	        {
		    'Key': TagName,
		    'Value': TagValue
		}
	    ]
	)

        return True

    def UpdateFirehoseTag(self, ResourceId, TagName, TagValue):
        """Update firehose service tag"""

        Client = boto3.client('firehose')

        StreamName = ResourceId.split(':')[-1].split('/')[-1]

        response = Client.tag_delivery_stream(
	    DeliveryStreamName = StreamName,
	    Tags = [
	        {
		    'Key': TagName,
		    'Value': TagValue
		}
	    ]
	)

        return True

    def UpdateTag(self, ResourceId, TagName, TagValue):
        """Calls other methods to update tags"""

        try:
            if self.Service == 'ec2':
                response = self.CreateTags(ResourceId, TagName, TagValue)
            elif self.Service == 's3':
                response = self.UpdateS3Tag(ResourceId, TagName, TagValue)
            elif self.Service == 'lambda':
                response = self.TagResource(ResourceId, TagName, TagValue)
            elif self.Service == 'logs':
                response = self.UpdateLogsTag(ResourceId, TagName, TagValue)
            elif self.Service == 'rds':
                response = self.AddTagsToResource(ResourceId, TagName, TagValue)
            elif self.Service == 'es':
                response = self.AddTags(ResourceId, TagName, TagValue)
            elif self.Service == 'emr':
                response = self.AddTags(ResourceId, TagName, TagValue)
            elif self.Service == 'dynamodb':
                response = self.TagResource(ResourceId, TagName, TagValue)
            elif self.Service == 'firehose':
                response = self.UpdateFirehoseTag(ResourceId, TagName, TagValue)
            elif self.Service == 'glacier':
                response = self.UpdateGlacierTag(ResourceId, TagName, TagValue)
            elif self.Service == 'kms':
                response = self.TagResource(ResourceId, TagName, TagValue)
            elif self.Service == 'apigateway':
                response = self.TagResource(ResourceId, TagName, TagValue)
            elif self.Service == 'kinesis':
                response = self.UpdateKinesisTag(ResourceId, TagName, TagValue)
            elif self.Service == 'cloudtrail':
                response = self.AddTags(ResourceId, TagName, TagValue)
            elif self.Service == 'sqs':
                response = self.UpdateSqsTag(ResourceId, TagName, TagValue)
            elif self.Service == 'secretsmanager':
                response = self.TagResource(ResourceId, TagName, TagValue)
            elif self.Service == 'cloudfront':
                response = self.TagResource(ResourceId, TagName, TagValue)
            elif self.Service == 'efs':
                response = self.CreateTags(ResourceId, TagName, TagValue)
            elif self.Service == 'sagemaker':
                response = self.AddTags(ResourceId, TagName, TagValue)
            elif self.Service == 'redshift':
                response = self.CreateTags(ResourceId, TagName, TagValue)
            elif self.Service == 'elasticache':
                response = self.AddTagsToResource(ResourceId, TagName, TagValue)
            elif self.Service == 'workspaces':
                response = self.CreateTags(ResourceId, TagName, TagValue)
            elif self.Service == 'ds':
                response = self.AddTagsToResource(ResourceId, TagName, TagValue)
            elif self.Service == 'dax':
                response = self.TagResource(ResourceId, TagName, TagValue)
            elif self.Service == 'route53':
                response = self.UpdateRoute53Tag(ResourceId, TagName, TagValue)
            elif self.Service == 'directconnect':
                response = self.TagResource(ResourceId, TagName, TagValue)
            elif self.Service == 'datapipeline':
                response = self.AddTags(ResourceId, TagName, TagValue)
            else:
                raise TagNotSupportedError(self.Service)
        except Exception as e:
            raise e

        return True

    def DescribeTags(self, ResourceId):
        """Get tags using boto3 method describe_tags()"""

        Client = boto3.client(self.Service) 
        
        if self.Service == 'ec2':
            response = Client.describe_tags (
                Filters = [
	            {
                        'Name': 'resource-id',
	                'Values': [
	                    ResourceId
		        ]
		    }
	        ]
	    )
        elif self.Service == 'efs':
            response = Client.describe_tags (
                FileSystemId = ResourceId
	    )
        elif self.Service == 'redshift':
            response = Client.describe_tags (
                ResourceName = ResourceId
            )
        elif self.Service == 'workspaces':
            response = Client.describe_tags (
                ResourceId = ResourceId
            )
        elif self.Service == 'directconnect':
            response = Client.describe_tags (
                ResourceArn = [
                    ResourceId
		]
            )
        else:
            raise TagNotSupportedError(self.Service)

        return response


    def GetBucketTagging(self, ResourceId):
        """Get tags using boto3 method get_bucket_tagging()"""
   
        Client = boto3.client('s3') 

        response = Client.get_bucket_tagging (
            Bucket = ResourceId
	)

        return response


    def ListTags(self, ResourceId):
        """Get tags using boto3 method list_tags()"""
   
        Client = boto3.client(self.Service) 

        if self.Service == 's3':
            response = Client.list_tags (
                Bucket = ResourceId
	    )
        elif self.Service == 'es':
            response = Client.list_tags (
                ARN = ResourceId
	    )
        elif self.Service == 'cloudtrail':
            response = Client.list_tags (
                ResourceIdList = [
                    ResourceId
		]
	    )
        elif self.Service == 'sagemaker':
            response = Client.list_tags (
                ResourceArn = ResourceId
	    )
        elif self.Service == 'dax':
            response = Client.list_tags (
                ResourceName = ResourceId
	    )
        elif self.Service == 'lambda':
            response = Client.list_tags (
                Resource = ResourceId
	    )
        else:
            raise TagNotSupportedError(self.Service)
       
        return response

    def ListTagsLogGroup(self, ResourceId):
        """Get tags using boto3 method list_tags_log_group()"""
   
        Client = boto3.client('logs') 

        response = Client.list_tags_log_group (
            logGroupName = ResourceId
	)

        return response


    def ListTagsForResource(self, ResourceId):
        """Get tags using boto3 method list_tags_for_resource()"""

        Client = boto3.client(self.Service) 
        
        if self.Service == 's3':
            response = Client.list_tags_for_resource (
                ResourceName = ResourceId
	    )
        elif self.Service == 'cloudfront':
            response = Client.list_tags_for_resource (
                Resource = ResourceId
	    )
        elif self.Service == 'elasticache':
            response = Client.list_tags_for_resource (
                ResourceName = ResourceId
            )
        elif self.Service == 'ds':
            response = Client.list_tags_for_resource (
                ResourceId = ResourceId
            )
        elif self.Service == 'route53':
            response = Client.list_tags_for_resource (
                ResourceType = 'hostedzone',
                ResourceId = ResourceId
            )
        elif self.Service == 'rds':
            response = Client.list_tags_for_resource (
                ResourceName = ResourceId
            )
        else:
            raise TagNotSupportedError(self.Service)

        return response


    def ListTagsOfResource(self, ResourceId):
        """Get tags using boto3 method list_tags_of_resource()"""

        Client = boto3.client('dynamodb')
        
        response = Client.list_tags_of_resource (
            ResourceArn = ResourceId
	)

        return response


    def ListTagsForVault(self, ResourceId):
        """Get tags using boto3 method list_tags_for_vault()"""

        Client = boto3.client('glacier')

        Vault = ResourceId.split(':')[-1].split('/')[-1]
        
        response = Client.list_tags_for_vault (
            vaultName = Vault
	)

        return response


    def ListResourceTags(self, ResourceId):
        """Get tags using boto3 method list_resource_tags()"""

        Client = boto3.client('kms')
        
        response = Client.list_resource_tags (
            KeyId = ResourceId
	)

        return response


    def ListTagsForStream(self, ResourceId):
        """Get tags using boto3 method list_tags_for_stream()"""

        Client = boto3.client('kinesis')

        StreamName = ResourceId.split(':')[-1].split('/')[-1]
        
        response = Client.list_tags_for_stream (
            StreamName = StreamName
	)

        return response


    def ListQueueTags(self, ResourceId):
        """Get tags using boto3 method list_queue_tags()"""

        Client = boto3.client('sqs')
        
        response = Client.list_queue_tags (
            QueueUrl = ResourceId
	)

        return response

    def ListTagsForDeliveryStream(self, ResourceId):
        """Get tags using boto3 method list_tags_for_delivery_stream()"""

        Client = boto3.client('firehose')

        StreamName = ResourceId.split(':')[-1].split('/')[-1]
        
        response = Client.list_tags_for_delivery_stream (
            DeliveryStreamName = StreamName
	)

        return response


    def DescribeSecret(self, ResourceId):
        """Get tags using boto3 method describe_secret()"""

        Client = boto3.client('secretsmanager')
        
        response = Client.describe_secret (
            SecretId = ResourceId
	)

        return response


    def DescribeCluster(self, ResourceId):
        """Get tags using boto3 method describe_cluster()"""

        Client = boto3.client('emr')
        
        response = Client.describe_cluster (
            ClusterId = ResourceId
	)

        return response


    def DescribePipelines(self, ResourceId):
        """Get tags using boto3 method describe_pipelines()"""

        Client = boto3.client('datapipeline')
        
        response = Client.describe_cluster (
            pipelineIds = [
                ResourceId
            ]
	)

        return response

    def IsTagExists(self, ResourceId, TagName):
        """Calls other methods to check if tag exists"""

        try:
            if self.Service == 'ec2':
                response = self.DescribeTags(ResourceId)
                if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])):
                    return True
            elif self.Service == 's3':
                response = self.GetBucketTagging(ResourceId)
                if TagName in list(map(lambda x: x['Key'], [x for x in response['TagSet']])):
                    return True
            elif self.Service == 'lambda':
                response = self.ListTags(ResourceId)
                if TagName in [x for x in response['Tags']]:
                    return True
            elif self.Service == 'logs':
                response = self.ListTagsLogGroup(ResourceId)
                if TagName in [x for x in response['tags']]:
                    return True
            elif self.Service == 'rds':
                response = self.ListTagsForResource(ResourceId)
                if TagName in list(map(lambda x: x['Key'], [x for x in response['TagList']])):
                    return True
            elif self.Service == 'es':
                response = self.ListTags(ResourceId)
                if TagName in list(map(lambda x: x['Key'], [x for x in response['TagList']])):
                    return True
            elif self.Service == 'emr':
                response = self.DescribeCluster(ResourceId)
                if TagName in list(map(lambda x: x['Key'], [Tag for Tag in response['Cluster']['Tags']])):
                    return True
            elif self.Service == 'dynamodb':
                response = self.ListTagsOfResource(ResourceId)
                if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])):
                    return True
            elif self.Service == 'firehose':
                response = self.ListTagsForDeliveryStream(ResourceId)
                if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])):
                    return True
            elif self.Service == 'glacier':
                response = self.ListTagsForVault(ResourceId)
                if TagName in [x for x in response['Tags']]:
                    return True
            elif self.Service == 'kms':
                response = self.ListResourceTags(ResourceId)
                if TagName in list(map(lambda x: x['TagKey'], [x for x in response['Tags']])):
                    return True
            elif self.Service == 'apigateway':
                print('No api to list tags')
                return False
            elif self.Service == 'kinesis':
                response = self.ListTagsForStream(ResourceId)
                if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])):
                    return True
            elif self.Service == 'cloudtrail':
                response = self.ListTags(ResourceId)
                TagsList = map(lambda RTL: RTL['TagsList'], [RTL for RTL in response['ResourceTagList']])
                for Tags in TagsList:
                    for Tag in Tags:
                        if Tag['Key'] == 'Channel':
                            return True
            elif self.Service == 'sqs':
                response = self.ListTags(ResourceId)
                if TagName in [x for x in response['Tags']]:
                    return True
            elif self.Service == 'secretsmanager':
                response = self.DescribeSecret(ResourceId)
                if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])):
                    return True
            elif self.Service == 'cloudfront':
                response = self.ListTagsForResource(ResourceId)
                if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])):
                    return True
            elif self.Service == 'efs':
                response = self.DescribeTags(ResourceId)
                if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])):
                    return True
            elif self.Service == 'sagemaker':
                response = self.ListTags(ResourceId)
                if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])):
                    return True
            elif self.Service == 'redshift':
                response = self.DescribeTags(ResourceId)
                if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])):
                    return True
            elif self.Service == 'elasticache':
                response = self.ListTagsForResource(ResourceId)
                if TagName in list(map(lambda x: x['Key'], [x for x in response['TagList']])):
                    return True
            elif self.Service == 'workspaces':
                response = self.DescribeTags(ResourceId)
                if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])):
                    return True
            elif self.Service == 'ds':
                response = self.ListTagsForResource(ResourceId)
                if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])):
                    return True
            elif self.Service == 'dax':
                response = self.ListTags(ResourceId)
                if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])):
                    return True
            elif self.Service == 'route53':
                response = self.ListTagsForResource(ResourceId)
                if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])):
                    return True
            elif self.Service == 'directconnect':
                response = self.DescribeTags(ResourceId)
                if TagName in list(map(lambda x: x['Key'], [x for x in response['Tags']])):
                    return True
            elif self.Service == 'datapipeline':
                response = self.DescribePipelines(ResourceId)
                Tags = list(map(lambda x: x['tags'], [tags for tags in response['pipelineDescriptionList']]))
                for i in Tags:
                    for j in i:
                        if j['key'] == 'Channel':
                            return True
            else:
                raise TagNotSupportedError(self.Service)
        except Exception as e:
            raise e

        return False


def UpdateTag(Service, ResourceId, TagName, TagValue):
    """Update tag for services"""

    try:
        Tag = AwsTag(Service)
        Tag.UpdateTag(ResourceId, TagName, TagValue)
    except ClientError as c:
        raise Exception(type(c))
    except Exception as e:
        raise e

    return True


def IsTagExists(Service, ResourceId, TagName):
    """Check if tag name exists"""

    try:
        Tag = AwsTag(Service)
        if Tag.IsTagExists(ResourceId, TagName):
            return True
    except Exception as e:
        raise e

    return False

if __name__ == '__main__':
    Tag = AwsTag('ec2')
    print('I prefer to be a module; however, I can run some tests')
    ServicesExpected = 26
    print('TEST 1: check number of services is', ServicesExpected, 'or more', end='')
    assert Tag.GetServicesCount() >= ServicesExpected
    print('...OK')
