from tree_sitter_languages import get_language

# 测试常见语言
languages = ["python", "javascript", "json", "yaml", "c", "cpp", "java", "go"]
for lang in languages:
    try:
        print(f"{lang}: {get_language(lang)}")
    except Exception as e:
        print(f"{lang}: {e}")