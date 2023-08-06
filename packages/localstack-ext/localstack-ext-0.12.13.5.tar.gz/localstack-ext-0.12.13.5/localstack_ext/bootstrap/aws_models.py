from localstack.utils.aws import aws_models
NtBYT=super
NtBYW=None
NtBYD=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  NtBYT(LambdaLayer,self).__init__(arn)
  self.cwd=NtBYW
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.NtBYD.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,NtBYD,env=NtBYW):
  NtBYT(RDSDatabase,self).__init__(NtBYD,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,NtBYD,env=NtBYW):
  NtBYT(RDSCluster,self).__init__(NtBYD,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,NtBYD,env=NtBYW):
  NtBYT(AppSyncAPI,self).__init__(NtBYD,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,NtBYD,env=NtBYW):
  NtBYT(AmplifyApp,self).__init__(NtBYD,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,NtBYD,env=NtBYW):
  NtBYT(ElastiCacheCluster,self).__init__(NtBYD,env=env)
class TransferServer(BaseComponent):
 def __init__(self,NtBYD,env=NtBYW):
  NtBYT(TransferServer,self).__init__(NtBYD,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,NtBYD,env=NtBYW):
  NtBYT(CloudFrontDistribution,self).__init__(NtBYD,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,NtBYD,env=NtBYW):
  NtBYT(CodeCommitRepository,self).__init__(NtBYD,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
