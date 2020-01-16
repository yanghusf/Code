import shopify

# Replace the following with your shop URL
shop_url = "https://{API_KEY}:{PASSWORD}@{SHOP_NAME}.myshopify.com/admin"
shopify.ShopifyResource.set_site(shop_url)

# Create a new product
new_product = shopify.Product()
new_product.title = "Burton Custom Freestyle 151"
new_product.product_type = "Snowboard"
new_product.vendor = "Burton"
new_product.save()

# Update a product
new_product.title = "Burton Custom Freestyle 151 - Python Edition"
new_product.save()