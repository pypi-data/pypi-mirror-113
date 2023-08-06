from localstack.utils.aws import aws_models
tWJuj=super
tWJuS=None
tWJup=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  tWJuj(LambdaLayer,self).__init__(arn)
  self.cwd=tWJuS
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.tWJup.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,tWJup,env=tWJuS):
  tWJuj(RDSDatabase,self).__init__(tWJup,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,tWJup,env=tWJuS):
  tWJuj(RDSCluster,self).__init__(tWJup,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,tWJup,env=tWJuS):
  tWJuj(AppSyncAPI,self).__init__(tWJup,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,tWJup,env=tWJuS):
  tWJuj(AmplifyApp,self).__init__(tWJup,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,tWJup,env=tWJuS):
  tWJuj(ElastiCacheCluster,self).__init__(tWJup,env=env)
class TransferServer(BaseComponent):
 def __init__(self,tWJup,env=tWJuS):
  tWJuj(TransferServer,self).__init__(tWJup,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,tWJup,env=tWJuS):
  tWJuj(CloudFrontDistribution,self).__init__(tWJup,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,tWJup,env=tWJuS):
  tWJuj(CodeCommitRepository,self).__init__(tWJup,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
