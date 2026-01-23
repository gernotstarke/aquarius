import json
import os

def format_python_test_name_to_description(nodeid):
    """
    Formats a pytest nodeid into a human-readable description.
    Example: "tests/api/test_verein.py::test_create_verein" -> "API Verein: Create Verein"
    """
    parts = nodeid.split('::')
    test_function_name = parts[-1]
    
    # Remove 'test_' prefix, replace underscores with spaces, capitalize first letter
    description = test_function_name.replace('test_', '').replace('_', ' ').capitalize()
    
    # Optional: Add module context if desired, similar to frontend
    if len(parts) > 1:
        module_path = parts[0].replace('tests/', '').replace('.py', '')
        module_name_parts = module_path.split('/')
        if len(module_name_parts) > 1:
            module_context = ' '.join(p.capitalize() for p in module_name_parts)
            description = f"{module_context}: {description}"
        else:
            description = f"{module_name_parts[0].capitalize()}: {description}"

    return description


def compile_test_results(backend_report_path, frontend_report_path, output_path):
    all_test_results = []

    # Process backend (pytest) report
    if os.path.exists(backend_report_path):
        with open(backend_report_path, 'r') as f:
            backend_data = json.load(f)
        
        for test in backend_data.get('tests', []):
            # Exclude skipped tests with specific longrepr indicating unimplemented business rules
            if test['outcome'] == 'skipped' and test.get('setup', {}).get('longrepr') and \
               'Skipped: Business rule not yet implemented' in test['setup']['longrepr']:
                continue

            # Attempt to get docstring, fallback to formatted name
            # pytest-json-report doesn't directly expose docstrings in a dedicated field for all tests.
            # For simplicity, derive description from nodeid for now.
            # Further enhancement would involve parsing Python source code for docstrings.
            description = format_python_test_name_to_description(test['nodeid'])

            all_test_results.append({
                'description': description,
                'technical_name': test['nodeid'],
                'result': test['outcome']
            })
    
    # Process frontend (vitest) report
    if os.path.exists(frontend_report_path):
        with open(frontend_report_path, 'r') as f:
            # Vitest output sometimes contains console logs before the actual JSON.
            # Find the first '{' to start parsing JSON.
            content = f.read()
            json_start = content.find('{')
            if json_start != -1:
                frontend_data = json.loads(content[json_start:])
            else:
                frontend_data = {}

        for test_file in frontend_data.get('testResults', []):
            # Skip playwright e2e tests
            if "e2e" in test_file['name'].lower():
                continue

            # Extract the module context for a more specific description
            file_name = os.path.basename(test_file['name'])
            module_context = file_name.replace('.test.ts', '').replace('.test.tsx', '')
            module_context = ' '.join(word.capitalize() for word in module_context.split('.'))

            # Look for a comment in the describe block for a more specific description
            describe_comment = None
            if hasattr(test_file, 'assertionResults') and len(test_file['assertionResults']) > 0:
                 # This is a placeholder logic, actual extraction would require parsing the JS/TS file
                 # For now, rely on module_context + test title
                pass


            for assertion in test_file.get('assertionResults', []):
                # Ancestor titles can give context for description
                full_description_parts = assertion['ancestorTitles'] + [assertion['title']]
                
                # Use the describe block comment if available, otherwise construct from titles
                if describe_comment and assertion['ancestorTitles'] and describe_comment in assertion['ancestorTitles'][0]:
                    short_description = describe_comment.replace('//', '').strip()
                else:
                    short_description = " ".join(full_description_parts).replace('Input Component', 'Input').replace('API Service', 'API')
                    short_description = short_description.replace('::', ': ').replace('/', ' ').replace(' _ ', ' ').strip()
                    short_description = short_description.capitalize()

                all_test_results.append({
                    'description': short_description,
                    'technical_name': assertion['fullName'],
                    'result': assertion['status']
                })

    # Ensure output directory exists
    output_dir = os.path.dirname(output_path)
    os.makedirs(output_dir, exist_ok=True)

    with open(output_path, 'w') as f:
        json.dump(all_test_results, f, indent=2)

if __name__ == '__main__':
    backend_report = 'docs/build/test-results/backend.json'
    frontend_report = 'docs/build/test-results/frontend.json'
    output_json = 'docs/_data/test_results.json'
    compile_test_results(backend_report, frontend_report, output_json)
