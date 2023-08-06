from localstack.utils.aws import aws_models
KnSAv=super
KnSAz=None
KnSAx=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  KnSAv(LambdaLayer,self).__init__(arn)
  self.cwd=KnSAz
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.KnSAx.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,KnSAx,env=KnSAz):
  KnSAv(RDSDatabase,self).__init__(KnSAx,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,KnSAx,env=KnSAz):
  KnSAv(RDSCluster,self).__init__(KnSAx,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,KnSAx,env=KnSAz):
  KnSAv(AppSyncAPI,self).__init__(KnSAx,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,KnSAx,env=KnSAz):
  KnSAv(AmplifyApp,self).__init__(KnSAx,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,KnSAx,env=KnSAz):
  KnSAv(ElastiCacheCluster,self).__init__(KnSAx,env=env)
class TransferServer(BaseComponent):
 def __init__(self,KnSAx,env=KnSAz):
  KnSAv(TransferServer,self).__init__(KnSAx,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,KnSAx,env=KnSAz):
  KnSAv(CloudFrontDistribution,self).__init__(KnSAx,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,KnSAx,env=KnSAz):
  KnSAv(CodeCommitRepository,self).__init__(KnSAx,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
