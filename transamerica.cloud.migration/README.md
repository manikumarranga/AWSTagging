Using AWS API to update tags is cumbersome, complex and time consuming to implement because the methods are different for each service. The following examples demonstrate this challenge:

Example 1: Update S3 bucket tag

    response = client.put_bucket_tagging(
        Bucket='string',
	Tagging={
	    'TagSet': [
	        {
	            'Key': 'string',
	            'Value': 'string'
	        },
	    ]
        }
    )

Example 1: Update Glacier tag

    response = client.add_tags_to_vault(
        vaultName='string',
        Tags={
            'string': 'string'
	}
    )

The Solution: the API provided in this branch provides an abstraction layer that makes is easier to manage AWS tags.

Example 1: Update S3 tag

    UpdateTag('s3', ResourceId, TagName, TagValue)

Example 2: Update Glacier tag

    UpdateTag('glacier', ResourceId, TagName, TagValue)
