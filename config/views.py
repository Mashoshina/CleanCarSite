from django.http import HttpResponse


def home(request):
    return HttpResponse(
        """
        <!doctype html>
        <html lang="ru">
          <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <title>CleanCar — Django работает</title>
          </head>
          <body>
            <h1>CleanCar</h1>
            <p>Django backend работает корректно.</p>
          </body>
        </html>
        """,
        content_type="text/html; charset=utf-8",
    )