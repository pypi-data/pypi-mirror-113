from localstack.utils.aws import aws_models
nBigX=super
nBigM=None
nBigj=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  nBigX(LambdaLayer,self).__init__(arn)
  self.cwd=nBigM
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.nBigj.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,nBigj,env=nBigM):
  nBigX(RDSDatabase,self).__init__(nBigj,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,nBigj,env=nBigM):
  nBigX(RDSCluster,self).__init__(nBigj,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,nBigj,env=nBigM):
  nBigX(AppSyncAPI,self).__init__(nBigj,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,nBigj,env=nBigM):
  nBigX(AmplifyApp,self).__init__(nBigj,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,nBigj,env=nBigM):
  nBigX(ElastiCacheCluster,self).__init__(nBigj,env=env)
class TransferServer(BaseComponent):
 def __init__(self,nBigj,env=nBigM):
  nBigX(TransferServer,self).__init__(nBigj,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,nBigj,env=nBigM):
  nBigX(CloudFrontDistribution,self).__init__(nBigj,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,nBigj,env=nBigM):
  nBigX(CodeCommitRepository,self).__init__(nBigj,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
