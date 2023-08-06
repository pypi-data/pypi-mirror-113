from localstack.utils.aws import aws_models
GaNeD=super
GaNem=None
GaNep=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  GaNeD(LambdaLayer,self).__init__(arn)
  self.cwd=GaNem
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.GaNep.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,GaNep,env=GaNem):
  GaNeD(RDSDatabase,self).__init__(GaNep,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,GaNep,env=GaNem):
  GaNeD(RDSCluster,self).__init__(GaNep,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,GaNep,env=GaNem):
  GaNeD(AppSyncAPI,self).__init__(GaNep,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,GaNep,env=GaNem):
  GaNeD(AmplifyApp,self).__init__(GaNep,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,GaNep,env=GaNem):
  GaNeD(ElastiCacheCluster,self).__init__(GaNep,env=env)
class TransferServer(BaseComponent):
 def __init__(self,GaNep,env=GaNem):
  GaNeD(TransferServer,self).__init__(GaNep,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,GaNep,env=GaNem):
  GaNeD(CloudFrontDistribution,self).__init__(GaNep,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,GaNep,env=GaNem):
  GaNeD(CodeCommitRepository,self).__init__(GaNep,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
