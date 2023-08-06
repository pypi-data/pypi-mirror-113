from localstack.utils.aws import aws_models
YFSEf=super
YFSEe=None
YFSEl=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  YFSEf(LambdaLayer,self).__init__(arn)
  self.cwd=YFSEe
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.YFSEl.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,YFSEl,env=YFSEe):
  YFSEf(RDSDatabase,self).__init__(YFSEl,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,YFSEl,env=YFSEe):
  YFSEf(RDSCluster,self).__init__(YFSEl,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,YFSEl,env=YFSEe):
  YFSEf(AppSyncAPI,self).__init__(YFSEl,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,YFSEl,env=YFSEe):
  YFSEf(AmplifyApp,self).__init__(YFSEl,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,YFSEl,env=YFSEe):
  YFSEf(ElastiCacheCluster,self).__init__(YFSEl,env=env)
class TransferServer(BaseComponent):
 def __init__(self,YFSEl,env=YFSEe):
  YFSEf(TransferServer,self).__init__(YFSEl,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,YFSEl,env=YFSEe):
  YFSEf(CloudFrontDistribution,self).__init__(YFSEl,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,YFSEl,env=YFSEe):
  YFSEf(CodeCommitRepository,self).__init__(YFSEl,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
