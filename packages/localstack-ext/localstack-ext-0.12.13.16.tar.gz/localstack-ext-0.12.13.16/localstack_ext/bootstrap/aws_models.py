from localstack.utils.aws import aws_models
gPTHL=super
gPTHv=None
gPTHx=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  gPTHL(LambdaLayer,self).__init__(arn)
  self.cwd=gPTHv
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.gPTHx.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,gPTHx,env=gPTHv):
  gPTHL(RDSDatabase,self).__init__(gPTHx,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,gPTHx,env=gPTHv):
  gPTHL(RDSCluster,self).__init__(gPTHx,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,gPTHx,env=gPTHv):
  gPTHL(AppSyncAPI,self).__init__(gPTHx,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,gPTHx,env=gPTHv):
  gPTHL(AmplifyApp,self).__init__(gPTHx,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,gPTHx,env=gPTHv):
  gPTHL(ElastiCacheCluster,self).__init__(gPTHx,env=env)
class TransferServer(BaseComponent):
 def __init__(self,gPTHx,env=gPTHv):
  gPTHL(TransferServer,self).__init__(gPTHx,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,gPTHx,env=gPTHv):
  gPTHL(CloudFrontDistribution,self).__init__(gPTHx,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,gPTHx,env=gPTHv):
  gPTHL(CodeCommitRepository,self).__init__(gPTHx,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
