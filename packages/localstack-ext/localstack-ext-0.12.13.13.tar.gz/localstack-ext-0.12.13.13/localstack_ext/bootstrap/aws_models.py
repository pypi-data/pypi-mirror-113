from localstack.utils.aws import aws_models
vTczg=super
vTczQ=None
vTczG=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  vTczg(LambdaLayer,self).__init__(arn)
  self.cwd=vTczQ
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.vTczG.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,vTczG,env=vTczQ):
  vTczg(RDSDatabase,self).__init__(vTczG,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,vTczG,env=vTczQ):
  vTczg(RDSCluster,self).__init__(vTczG,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,vTczG,env=vTczQ):
  vTczg(AppSyncAPI,self).__init__(vTczG,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,vTczG,env=vTczQ):
  vTczg(AmplifyApp,self).__init__(vTczG,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,vTczG,env=vTczQ):
  vTczg(ElastiCacheCluster,self).__init__(vTczG,env=env)
class TransferServer(BaseComponent):
 def __init__(self,vTczG,env=vTczQ):
  vTczg(TransferServer,self).__init__(vTczG,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,vTczG,env=vTczQ):
  vTczg(CloudFrontDistribution,self).__init__(vTczG,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,vTczG,env=vTczQ):
  vTczg(CodeCommitRepository,self).__init__(vTczG,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
