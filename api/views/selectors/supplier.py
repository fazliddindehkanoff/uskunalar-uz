from api.models.product import Supplier


def get_supplier_data(supplier: Supplier) -> dict:
    return {
        "company_name": supplier.company_name,
        "experience": supplier.experience,
        "cooperational_status": supplier.get_cooperational_status_display(),
        "country": supplier.country,
    }
