from localstack.utils.aws import aws_models
mWlya=super
mWlyV=None
mWlyg=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  mWlya(LambdaLayer,self).__init__(arn)
  self.cwd=mWlyV
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.mWlyg.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,mWlyg,env=mWlyV):
  mWlya(RDSDatabase,self).__init__(mWlyg,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,mWlyg,env=mWlyV):
  mWlya(RDSCluster,self).__init__(mWlyg,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,mWlyg,env=mWlyV):
  mWlya(AppSyncAPI,self).__init__(mWlyg,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,mWlyg,env=mWlyV):
  mWlya(AmplifyApp,self).__init__(mWlyg,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,mWlyg,env=mWlyV):
  mWlya(ElastiCacheCluster,self).__init__(mWlyg,env=env)
class TransferServer(BaseComponent):
 def __init__(self,mWlyg,env=mWlyV):
  mWlya(TransferServer,self).__init__(mWlyg,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,mWlyg,env=mWlyV):
  mWlya(CloudFrontDistribution,self).__init__(mWlyg,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,mWlyg,env=mWlyV):
  mWlya(CodeCommitRepository,self).__init__(mWlyg,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
