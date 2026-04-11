import os

from markdown import extract_title
from markdown_to_html import markdown_to_html_node


def generate_page(from_path, template_path, dest_path):
    # Print "Generating page: {from_path} to {dest_path} using template {template_path}"
    print(f"Generating page: {from_path} to {dest_path} using template {template_path}")

    # Read markdown from from_path
    with open(from_path, 'r') as f:
        markdown = f.read()

        # Read template from template_path
        with open(template_path, 'r') as t:
            template = t.read()

            # Convert markdown to html
            html = markdown_to_html_node(markdown).to_html()

            # Extract title from markdown using extract_title and replace {{ Title }} in template with the extracted title
            title = extract_title(markdown)
            template = template.replace('{{ Title }}', title)

            # Insert html into template, replacing {{ Content }}
            final_html = template.replace('{{ Content }}', html)

            # Write final_html to dest_path
            with open(dest_path, 'w') as d:
                d.write(final_html)

def generate_pages_recursively(dir_path_content, template_path, dest_dir_path):
    # For each markdown file in dir_path_content and subdirectories, generate a page in dest_dir_path with the same directory structure, using template_path
    for root, dirs, files in os.walk(dir_path_content):
        for filename in files:
            if filename.endswith('.md'):
                from_path = os.path.join(root, filename)
                dest_path = os.path.join(dest_dir_path, os.path.relpath(from_path, dir_path_content).replace('.md', '.html'))

                # Create any necessary directories in dest_dir_path
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                generate_page(from_path, template_path, dest_path)