from app.ingestion.manager import process_file

# Test any file you want
test_file_path = "tests/test_files/Synopsis_Miscro-dopler_(1)[1].docx"  # or your .docx or .png
user_id = "debug_user"

result = process_file(test_file_path, user_id=user_id)

print("\n==== METADATA ====")
print(result["metadata"])

print("\n==== FILE SIZE ====")
print(result["file_size"])

print("\n==== TEXT WITH CITATIONS (first 10 paragraphs) ====")
for item in result["text_with_citations"][:20]:
    print(f"[Page {item['page']}, Paragraph {item['paragraph']}] {item['text']}")
