from django.db import models

# Create your models here.

class Quotation(models.Model):
    project = models.ForeignKey("projects.Project", on_delete=models.CASCADE, related_name="quotations")
    quote_number = models.CharField(max_length=50, unique=True)
    subject = models.CharField(max_length=200)
    date = models.DateField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)

    status = models.CharField(
        max_length=50,
        choices=[
            ('draft', 'Draft'),
            ('sent', 'Sent'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ],
        default='draft'
    )

    notes = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Quotation {self.quote_number}"
    
class QuotationItem(models.Model):
    quotation = models.ForeignKey(Quotation, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey("products.Product", on_delete=models.SET_NULL, null=True, blank=True)
    description = models.CharField(max_length=255)
    quantity = models.IntegerField(default=1)
    price = models.DecimalField(max_digits=15, decimal_places=2)

    def subtotal(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.description} ({self.quotation.quote_number})"
