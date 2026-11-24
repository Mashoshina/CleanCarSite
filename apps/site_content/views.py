from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AboutUsSection
from .serializers import AboutUsSectionSerializer


class AboutUsView(APIView):
    def get(self, request):
        section = (
            AboutUsSection.objects.filter(is_published=True)
            .prefetch_related("bullets", "features")
            .first()
        )

        if section is None:
            return Response(
                {"detail": "Раздел «О нас» пока не опубликован."},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(AboutUsSectionSerializer(section).data)