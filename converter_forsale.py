#!/usr/bin/env python3
import re
import sys

# Regex pour capturer l'ID et le contenu du bloc
pattern = re.compile(
    r'\["([^"]+)"\]\s*=\s*\{([^}]*)\}',
    re.DOTALL
)

def convert_file(input_path, output_path):
    with open(input_path, "r", encoding="utf-8") as f:
        content = f.read()

    output_lines = []

    for match in pattern.finditer(content):
        item_id = match.group(1).strip()
        block = match.group(2).strip()

        # Découper les lignes et filtrer priceBroken
        raw_lines = [l.strip() for l in block.split(",") if l.strip()]
        lines = [l for l in raw_lines if not l.startswith("priceBroken")]

        # Ajouter une virgule à chaque ligne
        formatted_block = ",\n    ".join(f"{l}," for l in lines)

        new_entry = (
            f'Shop.RegisterSellItem("{item_id}", {{\n'
            f'    {formatted_block}\n'
            f'}})\n'
        )

        output_lines.append(new_entry)

    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 convert_sell.py input.lua output.lua")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    convert_file(input_path, output_path)
    print(f"Conversion terminée → {output_path}")


if __name__ == "__main__":
    main()

