import awscli
response=ListTagsLogGroup
	{
		"logGroupName":"/aws/lambda/test_start"
	}
print(response)
