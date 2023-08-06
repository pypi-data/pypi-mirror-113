from localstack.utils.aws import aws_models
YpTjX=super
YpTjS=None
YpTjI=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  YpTjX(LambdaLayer,self).__init__(arn)
  self.cwd=YpTjS
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.YpTjI.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,YpTjI,env=YpTjS):
  YpTjX(RDSDatabase,self).__init__(YpTjI,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,YpTjI,env=YpTjS):
  YpTjX(RDSCluster,self).__init__(YpTjI,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,YpTjI,env=YpTjS):
  YpTjX(AppSyncAPI,self).__init__(YpTjI,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,YpTjI,env=YpTjS):
  YpTjX(AmplifyApp,self).__init__(YpTjI,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,YpTjI,env=YpTjS):
  YpTjX(ElastiCacheCluster,self).__init__(YpTjI,env=env)
class TransferServer(BaseComponent):
 def __init__(self,YpTjI,env=YpTjS):
  YpTjX(TransferServer,self).__init__(YpTjI,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,YpTjI,env=YpTjS):
  YpTjX(CloudFrontDistribution,self).__init__(YpTjI,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,YpTjI,env=YpTjS):
  YpTjX(CodeCommitRepository,self).__init__(YpTjI,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
