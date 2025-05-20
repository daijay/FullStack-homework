#from ninja import NinjaAPI
from ninja import Swagger
from ninja_extra import NinjaExtraAPI

api = NinjaExtraAPI(title="Hire Platform API",
    description="API for the Hire Platform",
    urls_namespace="hireplatform",
    docs=Swagger(settings={"persistAuthorization": True})
    )

api.add_router(prefix='', router='hire.api.router', tags=['hireplatform'])
api.add_router(prefix='', router='user.api.router', tags=['Users'])
