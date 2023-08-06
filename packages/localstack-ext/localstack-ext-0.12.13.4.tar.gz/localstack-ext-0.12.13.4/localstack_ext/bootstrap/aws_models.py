from localstack.utils.aws import aws_models
kOsde=super
kOsdm=None
kOsdS=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  kOsde(LambdaLayer,self).__init__(arn)
  self.cwd=kOsdm
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.kOsdS.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,kOsdS,env=kOsdm):
  kOsde(RDSDatabase,self).__init__(kOsdS,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,kOsdS,env=kOsdm):
  kOsde(RDSCluster,self).__init__(kOsdS,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,kOsdS,env=kOsdm):
  kOsde(AppSyncAPI,self).__init__(kOsdS,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,kOsdS,env=kOsdm):
  kOsde(AmplifyApp,self).__init__(kOsdS,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,kOsdS,env=kOsdm):
  kOsde(ElastiCacheCluster,self).__init__(kOsdS,env=env)
class TransferServer(BaseComponent):
 def __init__(self,kOsdS,env=kOsdm):
  kOsde(TransferServer,self).__init__(kOsdS,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,kOsdS,env=kOsdm):
  kOsde(CloudFrontDistribution,self).__init__(kOsdS,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,kOsdS,env=kOsdm):
  kOsde(CodeCommitRepository,self).__init__(kOsdS,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
