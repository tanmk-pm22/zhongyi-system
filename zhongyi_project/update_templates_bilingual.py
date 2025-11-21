"""
Batch update templates to use bilingual format: 中文 | English
"""
import os
import re

# Define translation mappings
TRANSLATIONS = {
    # Common terms
    r'{% trans "View" %}': '查看 | View',
    r'{% trans "Edit" %}': '编辑 | Edit',
    r'{% trans "Delete" %}': '删除 | Delete',
    r'{% trans "Save" %}': '保存 | Save',
    r'{% trans "Cancel" %}': '取消 | Cancel',
    r'{% trans "Back" %}': '返回 | Back',
    r'{% trans "New Record" %}': '新建记录 | New Record',
    r'{% trans "First" %}': '首页 | First',
    r'{% trans "Previous" %}': '上一页 | Previous',
    r'{% trans "Next" %}': '下一页 | Next',
    r'{% trans "Last" %}': '末页 | Last',
    r'{% trans "No results found" %}': '未找到结果 | No results found',
    r'{% trans "Showing" %}': '显示 | Showing',
    r'{% trans "to" %}': '至 | to',
    r'{% trans "of" %}': '共 | of',
    r'{% trans "entries" %}': '条记录 | entries',

    # Status terms
    r'{% trans "Active" %}': '活跃 | Active',
    r'{% trans "Inactive" %}': '非活跃 | Inactive',
    r'{% trans "Status" %}': '状态 | Status',
    r'{% trans "Created" %}': '创建时间 | Created',
    r'{% trans "Updated" %}': '更新时间 | Updated',

    # Confirmation messages
    r'{% trans "Are you sure" %}': '您确定吗 | Are you sure',
    r'{% trans "This action cannot be undone" %}': '此操作不可撤销 | This action cannot be undone',
    r'{% trans "Confirm" %}': '确认 | Confirm',
    r'{% trans "Yes" %}': '是 | Yes',
    r'{% trans "No" %}': '否 | No',
}

def update_template_file(filepath):
    """Update a single template file with bilingual format."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        changes_made = 0

        # Apply all translations
        for pattern, replacement in TRANSLATIONS.items():
            if pattern in content:
                content = content.replace(pattern, replacement)
                changes_made += 1

        # Only write if changes were made
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            return changes_made

        return 0

    except Exception as e:
        print(f"Error processing {filepath}: {e}")
        return 0

def main():
    """Process all template files in the templates directory."""
    base_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(base_dir, 'templates')

    total_files = 0
    total_changes = 0

    # Walk through all template files
    for root, dirs, files in os.walk(templates_dir):
        for file in files:
            if file.endswith('.html'):
                filepath = os.path.join(root, file)
                changes = update_template_file(filepath)
                if changes > 0:
                    total_files += 1
                    total_changes += changes
                    relative_path = os.path.relpath(filepath, base_dir)
                    print(f"Updated: {relative_path} ({changes} changes)")

    print(f"\nTotal: {total_files} files updated with {total_changes} changes")

if __name__ == '__main__':
    main()
