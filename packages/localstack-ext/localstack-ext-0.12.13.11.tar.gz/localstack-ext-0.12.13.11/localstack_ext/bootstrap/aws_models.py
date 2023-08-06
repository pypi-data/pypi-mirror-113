from localstack.utils.aws import aws_models
ECmzL=super
ECmzf=None
ECmzR=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  ECmzL(LambdaLayer,self).__init__(arn)
  self.cwd=ECmzf
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.ECmzR.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,ECmzR,env=ECmzf):
  ECmzL(RDSDatabase,self).__init__(ECmzR,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,ECmzR,env=ECmzf):
  ECmzL(RDSCluster,self).__init__(ECmzR,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,ECmzR,env=ECmzf):
  ECmzL(AppSyncAPI,self).__init__(ECmzR,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,ECmzR,env=ECmzf):
  ECmzL(AmplifyApp,self).__init__(ECmzR,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,ECmzR,env=ECmzf):
  ECmzL(ElastiCacheCluster,self).__init__(ECmzR,env=env)
class TransferServer(BaseComponent):
 def __init__(self,ECmzR,env=ECmzf):
  ECmzL(TransferServer,self).__init__(ECmzR,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,ECmzR,env=ECmzf):
  ECmzL(CloudFrontDistribution,self).__init__(ECmzR,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,ECmzR,env=ECmzf):
  ECmzL(CodeCommitRepository,self).__init__(ECmzR,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
