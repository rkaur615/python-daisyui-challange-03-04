import requests

# 1. API URL
data_url = "https://dam.flippenterprise.net/flyerkit/publication/7813184/products?display_type=all&locale=en&access_token=881f0b9feea3693a704952a69b2a037a"

# 2. Browser Headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

print("Fetching and fixing data...")

try:
    response = requests.get(data_url, headers=headers)
    all_products = response.json()
except Exception as e:
    print(f"Error: {e}")
    all_products = []

# 3. HTML Content Start
html_table = "<h1 class='text-4xl font-bold text-center mb-10 text-primary'>FreshCo Weekly Deals</h1>"
html_table += """
<div class="overflow-x-auto shadow-2xl rounded-2xl border border-base-300">
  <table class="table table-zebra w-full">
    <thead>
      <tr class="bg-primary text-primary-content text-lg text-center">
        <th>Product</th>
        <th>Name</th>
        <th>Price</th>
        <th>Actions</th>
      </tr>
    </thead>
    <tbody class="text-center">
"""

# 4. Loop through products
for item in all_products[:40]:
    # Extracting data with correct keys from Flipp API
    name = item.get('name', 'Product')
    # Use 'current_price' and handle if it's None
    price = item.get('current_price')
    if price is None or price == 0:
        price = "See Store"
    else:
        price = f"${price}"

    # Fix Image URL: Prioritize 'cutout_image_url' then 'image_url'
    img_url = item.get('cutout_image_url') or item.get('image_url') or ""
    
    # Ensure URL is absolute (Add https: if missing)
    if img_url.startswith('//'):
        img_url = "https:" + img_url
    elif not img_url.startswith('http') and img_url != "":
        img_url = "https:" + img_url # Some links are just the path
    
    if not img_url:
        img_url = "https://via.placeholder.com/50?text=No+Img"

    # 5. Row Generation
    html_table += f"""
      <tr class="hover">
        <td class="flex justify-center">
          <div class="avatar">
            <div class="mask mask-squircle w-14 h-14 bg-white shadow-sm">
              <img src="{img_url}" alt="{name}" onerror="this.src='https://via.placeholder.com/50?text=Error'"/>
            </div>
          </div>
        </td>
        <td class="font-bold text-base">{name}</td>
        <td class="text-secondary font-mono text-xl font-bold">{price}</td>
        <td>
          <div class="flex justify-center gap-2">
            <button class="btn btn-square btn-success btn-sm text-white font-bold">Edit</button>
            <button class="btn btn-square btn-error btn-sm text-white font-bold">Delete</button>
          </div>
        </td>
      </tr>
    """

html_table += "</tbody></table></div>"

# 6. Injection into index.html
try:
    with open("index.html", "r", encoding="utf-8") as f:
        content = f.read()

    # This part replaces the OLD table with the NEW one
    # If your file already has a table, it will look for the <body> tag and put it inside
    import re
    # Find everything between <body> and </body> and replace it
    new_html = re.sub(r'<body.*?>.*?</body>', f'<body class="p-10 bg-base-100 font-sans">{html_table}</body>', content, flags=re.DOTALL)

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(new_html)

    print("--- SUCCESS! ---")
    print("All images and prices should be visible now. Refresh your browser.")

except Exception as e:
    print(f"Error saving file: {e}")
