from localstack.utils.aws import aws_models
yTiXF=super
yTiXg=None
yTiXv=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  yTiXF(LambdaLayer,self).__init__(arn)
  self.cwd=yTiXg
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.yTiXv.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,yTiXv,env=yTiXg):
  yTiXF(RDSDatabase,self).__init__(yTiXv,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,yTiXv,env=yTiXg):
  yTiXF(RDSCluster,self).__init__(yTiXv,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,yTiXv,env=yTiXg):
  yTiXF(AppSyncAPI,self).__init__(yTiXv,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,yTiXv,env=yTiXg):
  yTiXF(AmplifyApp,self).__init__(yTiXv,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,yTiXv,env=yTiXg):
  yTiXF(ElastiCacheCluster,self).__init__(yTiXv,env=env)
class TransferServer(BaseComponent):
 def __init__(self,yTiXv,env=yTiXg):
  yTiXF(TransferServer,self).__init__(yTiXv,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,yTiXv,env=yTiXg):
  yTiXF(CloudFrontDistribution,self).__init__(yTiXv,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,yTiXv,env=yTiXg):
  yTiXF(CodeCommitRepository,self).__init__(yTiXv,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
