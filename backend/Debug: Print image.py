# Debug: Print image information for each item
print("Image debug information:")
for i, item in enumerate(selected_items):
    print(f"Item {i+1}: {item['name']}")
    print(f"  Has 'images' key: {'Yes' if 'images' in item else 'No'}")
    if 'images' in item:
        print(f"  Images value type: {type(item['images'])}")
        print(f"  Images value: {str(item['images'])[:100]}")  # Show first 100 chars

for item in selected_items:
    # Check if the item has images key
    if 'images' in item and item['images']:
        try:
            # Get the image URL - handle different possible formats
            image_url = None
            
            if isinstance(item['images'], str):
                # Direct URL string
                image_url = item['images']
            elif isinstance(item['images'], list) and len(item['images']) > 0:
                # List of URLs - take the first one
                image_url = item['images'][0]
            elif isinstance(item['images'], dict) and len(item['images']) > 0:
                # Dictionary of URLs - take the first value
                image_url = list(item['images'].values())[0]
            
            # If it's a relative URL, convert to absolute (example)
            if image_url and image_url.startswith('/'):
                # This is just an example - update with your actual domain
                image_url = f"https://yourdomain.com{image_url}"
            
            # Print the processed URL for debugging
            print(f"Processed image URL for {item['name']}: {image_url}")
            
            if image_url:
                # Create HTML for the image with caption
                item_price = f"S${item['normalized_price']:.2f}" if item['normalized_price'] is not None else "N/A"
                
                # Add a discount badge if available
                discount_badge = ""
                if item.get('has_bulk_discount', False):
                    discount_badge = """
                    <div style='position: absolute; top: 5px; right: 5px; background-color: #FF9800; color: white; padding: 5px; border-radius: 4px; font-size: 0.8em;'>
                        BULK DISCOUNT
                    </div>
                    """
                
                html_content += f"""
                <div style='border: 1px solid #ddd; border-radius: 8px; padding: 10px; max-width: 250px; position: relative;'>
                    {discount_badge}
                    <img src="{image_url}" alt="{item['name']}" style='width: 100%; max-height: 200px; object-fit: contain;'>
                    <p style='margin-top: 8px; font-weight: bold;'>{item['name']}</p>
                    <p>{item_price}</p>
                """
                
                # Add discount info if available
                if item.get('formatted_discount', ''):
                    html_content += f"""<p style='color: #FF9800; font-weight: bold;'>{item.get('formatted_discount', '')}</p>
                """
                
                html_content += "</div>"
                count += 1
        except Exception as e:
            print(f"Error processing image for {item['name']}: {str(e)}")
