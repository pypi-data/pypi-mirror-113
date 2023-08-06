from localstack.utils.aws import aws_models
tXaou=super
tXaoF=None
tXaow=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  tXaou(LambdaLayer,self).__init__(arn)
  self.cwd=tXaoF
  self.runtime=''
  self.handler=''
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.tXaow.split(':')[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,tXaow,env=tXaoF):
  tXaou(RDSDatabase,self).__init__(tXaow,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,tXaow,env=tXaoF):
  tXaou(RDSCluster,self).__init__(tXaow,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,tXaow,env=tXaoF):
  tXaou(AppSyncAPI,self).__init__(tXaow,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,tXaow,env=tXaoF):
  tXaou(AmplifyApp,self).__init__(tXaow,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,tXaow,env=tXaoF):
  tXaou(ElastiCacheCluster,self).__init__(tXaow,env=env)
class TransferServer(BaseComponent):
 def __init__(self,tXaow,env=tXaoF):
  tXaou(TransferServer,self).__init__(tXaow,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,tXaow,env=tXaoF):
  tXaou(CloudFrontDistribution,self).__init__(tXaow,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,tXaow,env=tXaoF):
  tXaou(CodeCommitRepository,self).__init__(tXaow,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
