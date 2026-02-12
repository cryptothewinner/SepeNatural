from typing import List, Dict, Any
from ..models.domain import Product, Ingredient

class SepenaturalMapper:
    @staticmethod
    def map_to_product(raw_data: Dict[str, Any]) -> Product:
        """
        Maps raw input from scraper SQLite to standard Product model.
        """
        ingredients = []
        for ing in raw_data.get('ingredients', []):
            ingredients.append(Ingredient(
                name=ing.get('ingredient_name', 'Bilinmeyen'),
                amount=ing.get('amount'),
                unit=ing.get('unit'),
                percentage=ing.get('percentage'),
                raw_text=ing.get('raw_text')
            ))

        return Product(
            sku=raw_data.get('sku', 'N/A'),
            name=raw_data.get('name', 'Adsız Ürün'),
            barcode=raw_data.get('barcode'),
            price=raw_data.get('price'),
            currency=raw_data.get('currency', 'TRY'),
            categories=raw_data.get('categories', []),
            attributes=raw_data.get('attributes', {}),
            ingredients=ingredients,
            usage_text=raw_data.get('usage_text'),
            warnings_text=raw_data.get('warnings_text'),
            storage_text=raw_data.get('storage_text'),
            description_html=raw_data.get('description_html'),
            url=raw_data.get('url'),
            source="scraper"
        )

    @classmethod
    def map_list(cls, raw_list: List[Dict]) -> List[Product]:
        return [cls.map_to_product(item) for item in raw_list]
