from rest_framework.pagination import PageNumberPagination

class CustomPagination(PageNumberPagination):
    """
    Custom pagination class for API responses.

    Attributes:
        - page_size (int): Default number of items per page (6).
        - page_size_query_param (str): Allows client to set custom page size via query parameter.
        - max_page_size (int): Maximum allowed number of items per page (100).
    """
    page_size = 6
    page_size_query_param = "page_size"
    max_page_size = 100