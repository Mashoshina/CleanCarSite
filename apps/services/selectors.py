from .models import Service


def list_services(service_type=None):
    """Вернуть услуги, при необходимости отфильтрованные по типу."""
    services = Service.objects.all()

    if service_type:
        services = services.filter(service_type=service_type)

    return services.order_by("vehicle_type", "name")