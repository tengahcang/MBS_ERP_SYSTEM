from django.utils.deprecation import MiddlewareMixin

class NoCacheMiddleware(MiddlewareMixin):
    def process_response(self, request, response):
        # Cek jika user sedang mengakses halaman admin
        if request.path.startswith('/admin/'):
            # Paksa browser untuk tidak menyimpan cache sama sekali
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate, max-age=0'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response