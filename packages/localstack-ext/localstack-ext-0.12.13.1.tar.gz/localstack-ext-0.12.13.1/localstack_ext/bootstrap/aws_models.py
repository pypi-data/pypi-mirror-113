from localstack.utils.aws import aws_models
NTLbn=super
NTLbY=None
NTLbJ=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  NTLbn(LambdaLayer,self).__init__(arn)
  self.cwd=NTLbY
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.NTLbJ.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,NTLbJ,env=NTLbY):
  NTLbn(RDSDatabase,self).__init__(NTLbJ,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,NTLbJ,env=NTLbY):
  NTLbn(RDSCluster,self).__init__(NTLbJ,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,NTLbJ,env=NTLbY):
  NTLbn(AppSyncAPI,self).__init__(NTLbJ,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,NTLbJ,env=NTLbY):
  NTLbn(AmplifyApp,self).__init__(NTLbJ,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,NTLbJ,env=NTLbY):
  NTLbn(ElastiCacheCluster,self).__init__(NTLbJ,env=env)
class TransferServer(BaseComponent):
 def __init__(self,NTLbJ,env=NTLbY):
  NTLbn(TransferServer,self).__init__(NTLbJ,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,NTLbJ,env=NTLbY):
  NTLbn(CloudFrontDistribution,self).__init__(NTLbJ,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,NTLbJ,env=NTLbY):
  NTLbn(CodeCommitRepository,self).__init__(NTLbJ,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
