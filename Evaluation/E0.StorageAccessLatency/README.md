lambda 访问 ElasticCache 与访问S3不同，不需要提供AWS_ACCESS_KEY_ID和AWS_SECRET_KEY_ID。
但是需要确保lambda函数的role具有AWSLambdaVPCAccessExecutionRole的权限 ，要保证lambda和要访问的ElasticCache 的VPC、子网以及安全组能够保持一致。
具体操作可以参照[此教程](https://link.zhihu.com/?target=https%3A//docs.aws.amazon.com/AmazonElastiCache/latest/mem-ug/Lambda.html)。

此外Lambda的内存配置对于性能的影响非常大，目前的测试数据都是以1024MB的内存配置为基准的。