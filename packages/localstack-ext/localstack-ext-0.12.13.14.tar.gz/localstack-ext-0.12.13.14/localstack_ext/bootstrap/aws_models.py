from localstack.utils.aws import aws_models
TtEVL=super
TtEVH=None
TtEVf=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  TtEVL(LambdaLayer,self).__init__(arn)
  self.cwd=TtEVH
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.TtEVf.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,TtEVf,env=TtEVH):
  TtEVL(RDSDatabase,self).__init__(TtEVf,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,TtEVf,env=TtEVH):
  TtEVL(RDSCluster,self).__init__(TtEVf,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,TtEVf,env=TtEVH):
  TtEVL(AppSyncAPI,self).__init__(TtEVf,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,TtEVf,env=TtEVH):
  TtEVL(AmplifyApp,self).__init__(TtEVf,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,TtEVf,env=TtEVH):
  TtEVL(ElastiCacheCluster,self).__init__(TtEVf,env=env)
class TransferServer(BaseComponent):
 def __init__(self,TtEVf,env=TtEVH):
  TtEVL(TransferServer,self).__init__(TtEVf,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,TtEVf,env=TtEVH):
  TtEVL(CloudFrontDistribution,self).__init__(TtEVf,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,TtEVf,env=TtEVH):
  TtEVL(CodeCommitRepository,self).__init__(TtEVf,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
