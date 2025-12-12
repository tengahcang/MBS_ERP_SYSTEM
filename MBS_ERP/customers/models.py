from django.db import models

# Create your models here.

class Customer(models.Model):
    CUSTOMER_TYPES = (
        ('company', 'Company'),
        ('individual', 'Individual'),
    )
    
    BUSINESS_ENTITY_TYPES = (
        ('pt', 'PT'),
        ('cv', 'CV'),
        ('ud', 'UD'),
        ('firma', 'Firma'),
        ('koperasi', 'Koperasi'),
        ('yayasan', 'Yayasan'),
        ('instansi', 'Instansi Pemerintah'),
        ('lainnya', 'Lainnya'),
    )

    name = models.CharField(max_length=255)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPES, default='company')
    business_entity_type = models.CharField( max_length=50, choices=BUSINESS_ENTITY_TYPES, blank=True, null=True, help_text="Fill in only if the customer is a company" )
    address = models.TextField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    npwp = models.CharField(max_length=100, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.customer_type == "company" and self.business_entity_type:
            return f"{self.get_business_entity_type_display()} {self.name}"
        return self.name
    
class CustomerContactPerson(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="contacts")
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.customer.name})"