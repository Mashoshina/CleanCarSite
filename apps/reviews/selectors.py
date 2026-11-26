from .models import Review


def list_reviews(limit=None):
    """Вернуть отзывы от новых к старым; limit ограничивает их количество."""
    reviews = Review.objects.order_by("-id")

    if limit is not None:
        reviews = reviews[:limit]

    return reviews