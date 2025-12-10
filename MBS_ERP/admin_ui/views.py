from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# TAMBAHAN: Sesuaikan 'core' dengan nama app tempat Anda menyimpan model Product
from core.models import Product
from django.db.models import Q

# --- 1. Fungsi Bantuan (Simpan Menu Disini) ---
def get_side_menu():
    """
    Fungsi ini menyimpan data menu agar bisa dipanggil oleh semua View.
    Jadi tidak perlu nulis ulang menu_list di setiap fungsi.
    """
    return [
        {
            "category": "Authentication",
            "items": [
                {
                    "name": "Users",
                    "icon": "fa-users",
                    "url_name": "admin_ui:user_list",
                    "description": "Kelola data sales dan staff"
                },
                {
                    "name": "Groups",
                    "icon": "fa-layer-group",
                    "url_name": "admin_ui:dashboard", # Arahkan ke dashboard dulu sbg placeholder
                    "description": "Kelola hak akses role"
                }
            ]
        },
        {
            "category": "Core Business",
            "items": [
                {
                    "name": "Products",
                    "icon": "fa-box",
             
                    "url_name": "admin_ui:product_list", 
                    "description": "Daftar barang jualan"
                },
                {
                    "name": "Vendors",
                    "icon": "fa-truck",
                    "url_name": "admin_ui:dashboard",
                    "description": "Data supplier"
                }
            ]
        }
    ]

# --- 2. View Dashboard ---
@login_required(login_url='/login/')
def dashboard(request):
    context = {
        "menu_list": get_side_menu(), # Panggil fungsi menu tadi
        "total_users": User.objects.count(),
        "page_title": "Sales Dashboard"
    }
    return render(request, "dashboard/dashboard.html", context)

# --- 3. View User List ---
@login_required(login_url='/login/')
def user_list(request):
    users = User.objects.all()
    
    context = {
        "menu_list": get_side_menu(), # <--- INI KUNCINYA (Jangan Lupa Tambahkan Ini)
        "users": users,
        "page_title": "Users Management"
    }
    
    return render(request, "dashboard/user_list.html", context)


# --- 4. View Product List (BARU) ---
@login_required(login_url='/login/')
def product_list(request):
    """
    Menampilkan daftar produk dengan Fitur Search.
    """
    # 1. Ambil data dasar
    products = Product.objects.select_related('brand', 'category').all().order_by('-id')
    
    # 2. Cek apakah ada request pencarian (parameter 'q')
    query = request.GET.get('q')
    
    if query:
        # Lakukan filter: Cari di Nama Produk ATAU Product Code
        # icontains = Case Insensitive (Huruf besar/kecil dianggap sama)
        products = products.filter(
            Q(name__icontains=query) | 
            Q(product_code__icontains=query)
        )
    
    context = {
        "menu_list": get_side_menu(),
        "products": products,
        "page_title": "Product Catalog"
    }
    
    return render(request, "dashboard/product_list.html", context)