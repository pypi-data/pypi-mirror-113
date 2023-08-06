from localstack.utils.aws import aws_models
xoGfD=super
xoGfz=None
xoGfH=id
class LambdaLayer(aws_models.LambdaFunction):
 def __init__(self,arn):
  xoGfD(LambdaLayer,self).__init__(arn)
  self.cwd=xoGfz
  self.runtime=""
  self.handler=""
  self.envvars={}
  self.versions={}
class BaseComponent(aws_models.Component):
 def name(self):
  return self.xoGfH.split(":")[-1]
class RDSDatabase(BaseComponent):
 def __init__(self,xoGfH,env=xoGfz):
  xoGfD(RDSDatabase,self).__init__(xoGfH,env=env)
class RDSCluster(BaseComponent):
 def __init__(self,xoGfH,env=xoGfz):
  xoGfD(RDSCluster,self).__init__(xoGfH,env=env)
class AppSyncAPI(BaseComponent):
 def __init__(self,xoGfH,env=xoGfz):
  xoGfD(AppSyncAPI,self).__init__(xoGfH,env=env)
class AmplifyApp(BaseComponent):
 def __init__(self,xoGfH,env=xoGfz):
  xoGfD(AmplifyApp,self).__init__(xoGfH,env=env)
class ElastiCacheCluster(BaseComponent):
 def __init__(self,xoGfH,env=xoGfz):
  xoGfD(ElastiCacheCluster,self).__init__(xoGfH,env=env)
class TransferServer(BaseComponent):
 def __init__(self,xoGfH,env=xoGfz):
  xoGfD(TransferServer,self).__init__(xoGfH,env=env)
class CloudFrontDistribution(BaseComponent):
 def __init__(self,xoGfH,env=xoGfz):
  xoGfD(CloudFrontDistribution,self).__init__(xoGfH,env=env)
class CodeCommitRepository(BaseComponent):
 def __init__(self,xoGfH,env=xoGfz):
  xoGfD(CodeCommitRepository,self).__init__(xoGfH,env=env)
# Created by pyminifier (https://github.com/liftoff/pyminifier)
