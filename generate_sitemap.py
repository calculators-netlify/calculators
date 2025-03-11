import json
import os
from datetime import datetime

def generate_sitemap():
    # Base URL of the website
    base_url = "https://free-calculators.netlify.app"
    
    # Load calculator data
    with open('calculators.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Start XML content
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
    <!-- Homepage -->
    <url>
        <loc>{}</loc>
        <changefreq>weekly</changefreq>
        <priority>1.0</priority>
    </url>
    
    <!-- Categories Page -->
    <url>
        <loc>{}/categories</loc>
        <changefreq>weekly</changefreq>
        <priority>0.9</priority>
    </url>
""".format(base_url, base_url)

    # Add categories
    for category in data['categories']:
        category_url = f"{base_url}/{category['url'].lstrip('/')}"
        xml_content += f"""
    <url>
        <loc>{category_url}</loc>
        <changefreq>weekly</changefreq>
        <priority>0.8</priority>
    </url>"""

        # Add calculators for each category
        if 'calculators' in category:
            for calc in category['calculators']:
                # Handle variations
                if 'variations' in calc:
                    for var in calc['variations']:
                        calc_url = f"{base_url}/{var['url'].lstrip('/')}"
                        xml_content += f"""
    <url>
        <loc>{calc_url}</loc>
        <changefreq>weekly</changefreq>
        <priority>0.7</priority>
    </url>"""

                # Handle template-based calculators
                if 'template' in calc:
                    template = calc['template']
                    for i in range(template['range']['start'], template['range']['end'] + 1):
                        # Determine priority based on week number
                        priority = "0.7" if i <= 2 else "0.6" if i <= 16 else "0.5" if i <= 20 else "0.4"
                        calc_url = f"{base_url}/date/{i}-weeks-from-today.html"
                        xml_content += f"""
    <url>
        <loc>{calc_url}</loc>
        <changefreq>weekly</changefreq>
        <priority>{priority}</priority>
    </url>"""

    # Close XML
    xml_content += "\n</urlset>"

    # Write to file
    with open('sitemap.xml', 'w', encoding='utf-8') as f:
        f.write(xml_content)

if __name__ == "__main__":
    generate_sitemap() 