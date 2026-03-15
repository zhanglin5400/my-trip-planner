import re
import sys

file_path = '/usr/local/lib/python3.11/site-packages/mcp/client/stdio/__init__.py'

try:
    with open(file_path, 'r') as f:
        content = f.read()

    if 'fixed_line = line.replace' not in content:
        # 在原来的 message = ... 行之前插入 fixed_line 替换
        new_content = re.sub(
            r'(message = types\.JSONRPCMessage\.model_validate_json\(line\))',
            r'        fixed_line = line.replace("\'", "\"")\n        \1',
            content
        )
        with open(file_path, 'w') as f:
            f.write(new_content)
        print("✅ MCP client JSON parsing fix applied.")
    else:
        print("✅ MCP client already fixed.")
except Exception as e:
    print(f"❌ Error applying fix: {e}")
    sys.exit(1)