from product_finder import category_writer, get_products

CATEGORIES = [
    "Wine",
    "Spirits",
    "Beer%20%26%20Cider",
    "Coolers",
#     "Traditional%20Coolers",
#     "Accessories%20And%20Non-Alcohol%20Items",
#     "Cocktails",
#     "Hard Seltzers",
#     "Teas",
]


category_writer(CATEGORIES, get_products)