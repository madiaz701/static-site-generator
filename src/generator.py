
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