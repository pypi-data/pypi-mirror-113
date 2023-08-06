from localstack.utils.aws import aws_models
hnWYq=super
hnWYw=None
hnWYo=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  hnWYq(LambdaLayer,self).__init__(arn)
  self.cwd=hnWYw
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.hnWYo.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,hnWYo,env=hnWYw):
  hnWYq(RDSDatabase,self).__init__(hnWYo,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,hnWYo,env=hnWYw):
  hnWYq(RDSCluster,self).__init__(hnWYo,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,hnWYo,env=hnWYw):
  hnWYq(AppSyncAPI,self).__init__(hnWYo,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,hnWYo,env=hnWYw):
  hnWYq(AmplifyApp,self).__init__(hnWYo,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,hnWYo,env=hnWYw):
  hnWYq(ElastiCacheCluster,self).__init__(hnWYo,env=env)
class TransferServer(BaseComponent):
 def __init__(self,hnWYo,env=hnWYw):
  hnWYq(TransferServer,self).__init__(hnWYo,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,hnWYo,env=hnWYw):
  hnWYq(CloudFrontDistribution,self).__init__(hnWYo,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,hnWYo,env=hnWYw):
  hnWYq(CodeCommitRepository,self).__init__(hnWYo,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
