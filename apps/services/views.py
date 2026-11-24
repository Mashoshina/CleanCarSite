from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Service
from .selectors import list_services
from .serializers import ServiceSerializer


class ServiceListView(APIView):
    """Список услуг; можно фильтровать по типу обслуживания."""

    def get(self, request):
        service_type = request.query_params.get("type")

        allowed_types = {
            Service.ServiceType.SELF_SERVICE,
            Service.ServiceType.STAFF_SERVICE,
        }

        if service_type and service_type not in allowed_types:
            return Response(
                {
                    "type": (
                        "Допустимые значения: "
                        "self_service или staff_service."
                    )
                },
                status=400,
            )

        services = list_services(service_type=service_type)
        return Response(ServiceSerializer(services, many=True).data)