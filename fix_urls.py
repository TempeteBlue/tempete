import json
import re

# Read the search index
with open("static/search-index.json", "r", encoding="utf-8") as f:
    index = json.load(f)


def hugo_slugify(text):
    """Replicate Hugo's exact slugify behavior"""
    # Convert to lowercase
    text = text.lower()
    # Replace & with space (Hugo removes it or treats as word separator)
    text = text.replace("&", " ")
    # Replace spaces with hyphens (each space becomes a hyphen)
    text = re.sub(r"[\s]", "-", text)
    # Keep letters, numbers, accented chars, and dots
    # Remove other punctuation
    text = re.sub(r"[^a-z0-9àáâãäåæçèéêëìíîïðñòóôõöøùúûüýþÿ.\-]", "", text)
    # Strip hyphens from ends
    text = text.strip("-")
    return text


# Fix URLs for all manuels
for entry in index:
    if entry["section"] == "manuels" and "/options/" in entry["url"]:
        # Extract the folder name from the title
        title = entry["title"]
        # Generate proper slug
        proper_slug = hugo_slugify(title)

        # Extract category from current URL
        url_parts = entry["url"].split("/")
        if len(url_parts) >= 4:
            category = url_parts[2]  # e.g., 'options'
            # Build new URL
            new_url = f"/manuels/{category}/{proper_slug}/"

            if new_url != entry["url"]:
                print(f"Fixed: {entry['url']}")
                print(f"   -> {new_url}")
                entry["url"] = new_url

# Write back
with open("static/search-index.json", "w", encoding="utf-8") as f:
    json.dump(index, f, ensure_ascii=False, indent=2)

print("\nDone! URLs updated to match Hugo's format.")
