from django.contrib import admin
from .models import City

# Register the city model with the Django admin interface
@admin.register(City)
class cityAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the 'name' field in the list view
    search_fields = ('name',)  # Allow searching by the city name
    list_filter = ('name',)  # Optional: Filter citys by their name (in this case, it would be the same as the search)

