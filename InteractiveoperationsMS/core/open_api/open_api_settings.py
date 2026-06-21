from drf_spectacular.extensions import OpenApiAuthenticationExtension, OpenApiSerializerExtension
from drf_spectacular.generators import SchemaGenerator
from drf_spectacular.utils import extend_schema
from drf_spectacular.views import SpectacularAPIView


class OAuth2BearerAuthenticationScheme(OpenApiAuthenticationExtension):
    target_class = "core.authentication.OAuth2BearerAuthentication"
    name = ['UserBearerAuth', 'AdminBearerAuth', 'UniversityBearerAuth', 'IndustryBearerAuth', 'BusinessBearerAuth']

    def get_security_definition(self, auto_schema):
        return {}


# def check_authorize_required_path(persmission_classes: list[Any]):
#     print(persmission_classes)
#     for permission in persmission_classes:
#         if isinstance(permission, AllowAny):
#             return False
#     return True
#     return (
#         any(
#             not isinstance(permission, AllowAny)
#             # and isinstance(permission, BasePermission)
#         )
#     )


def custom_openapi_security_schemes(result, generator: SchemaGenerator, request, public):
    result["components"]["securitySchemes"] = {
        "UserBearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token for User endpoints",
        },
        "AdminBearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token for Admin endpoints",
        },
        "UniversityBearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token for University endpoints",
        },
        "IndustryBearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token for Industry endpoints",
        },
        "BusinessBearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
            "description": "JWT token for Business endpoints",
        },
    }
    path_to_view = {path: view_func for path, _, _, view_func in generator.endpoints}
    for path, path_item in result["paths"].items():
        for method_key, method in path_item.items():
            view_func = path_to_view.get(path)
            permission_classes = getattr(view_func.view_class, "permission_classes", [])
            if permission_classes:
                tags = method.get("tags", [])
                # if any(tag.startswith("Admin")or tag.startswith("Common")or tag.startswith("Backend")for tag in tags):
                if any(tag.startswith("Admin") or tag.startswith("Backend") for tag in tags):
                    method["security"] = [{"AdminBearerAuth": []}]
                elif any(tag.startswith("User") for tag in tags):
                    method["security"] = [{"UserBearerAuth": []}]
                elif any(tag.startswith("University") for tag in tags):
                    method["security"] = [{"UniversityBearerAuth": []}]
                elif any(tag.startswith("Industry") for tag in tags):
                    method["security"] = [{"IndustryBearerAuth": []}]
                elif any(tag.startswith("Business") for tag in tags):
                    method["security"] = [{"BusinessBearerAuth": []}]
                elif any(tag.startswith("All Actor") for tag in tags):
                    method["security"] = [{"UserBearerAuth": []}, {"AdminBearerAuth": []}, {"UniversityBearerAuth": []},
                                          {"IndustryBearerAuth": []}, {"BusinessBearerAuth": []}]
                elif any(tag.startswith("SRV/User") for tag in tags):
                    method["security"] = [{"UserBearerAuth": []}, {"UniversityBearerAuth": []},
                                          {"IndustryBearerAuth": []}, {"BusinessBearerAuth": []}]
                elif any(tag.startswith("SRV/Admin") for tag in tags):
                    method["security"] = [{"AdminBearerAuth": []}, {"UniversityBearerAuth": []},
                                          {"IndustryBearerAuth": []}, {"BusinessBearerAuth": []}]

                else:
                    method["security"] = None
            else:
                method["security"] = None

    return result


@extend_schema(exclude=True)
class SchemaView(SpectacularAPIView):
    pass
