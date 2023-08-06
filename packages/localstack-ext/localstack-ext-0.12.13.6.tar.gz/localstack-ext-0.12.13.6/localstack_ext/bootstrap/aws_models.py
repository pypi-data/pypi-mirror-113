from localstack.utils.aws import aws_models
sAEwq=super
sAEwx=None
sAEwo=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  sAEwq(LambdaLayer,self).__init__(arn)
  self.cwd=sAEwx
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.sAEwo.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,sAEwo,env=sAEwx):
  sAEwq(RDSDatabase,self).__init__(sAEwo,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,sAEwo,env=sAEwx):
  sAEwq(RDSCluster,self).__init__(sAEwo,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,sAEwo,env=sAEwx):
  sAEwq(AppSyncAPI,self).__init__(sAEwo,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,sAEwo,env=sAEwx):
  sAEwq(AmplifyApp,self).__init__(sAEwo,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,sAEwo,env=sAEwx):
  sAEwq(ElastiCacheCluster,self).__init__(sAEwo,env=env)
class TransferServer(BaseComponent):
 def __init__(self,sAEwo,env=sAEwx):
  sAEwq(TransferServer,self).__init__(sAEwo,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,sAEwo,env=sAEwx):
  sAEwq(CloudFrontDistribution,self).__init__(sAEwo,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,sAEwo,env=sAEwx):
  sAEwq(CodeCommitRepository,self).__init__(sAEwo,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
