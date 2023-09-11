# from rest_framework.pagination import PageNumberPagination

# class CustomPagination(PageNumberPagination):
#     def get_paginated_response(self, data):
#         return {
#             'custom_metadata': {
#                 'count': self.page.paginator.count,
#                 'next': self.get_next_link(),
#                 'previous': self.get_previous_link(),
#             },
#             'custom_results': data,
#         }