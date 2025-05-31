from rest_framework.views import APIView


class ProfileDetailView(APIView):
    def get(self, request, profile_id):
        pass

    def patch(self, request, profile_id):
        pass


class ProfileBusinessView(APIView):
    def get(self, request):
        pass


class ProfileCustomerView(APIView):
    def get(self, request):
        pass
