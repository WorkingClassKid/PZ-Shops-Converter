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
        lines = f.readlines()

    output_lines = []
    pending_comments = []
    buffer = ""

    for line in lines:
        stripped = line.strip()

        # --- 1) Commentaires avant un bloc ---
        if stripped.startswith("--"):
            pending_comments.append(line.rstrip("\n"))
            continue

        # --- 2) Détection des commentaires inline ---
        inline_comment = None
        if "--" in line:
            parts = line.split("--", 1)
            line = parts[0] + "\n"
            inline_comment = "--" + parts[1].rstrip("\n")

        buffer += line

        # --- 3) Détection d'un bloc complet ---
        match = pattern.search(buffer)
        if match:
            item_id = match.group(1).strip()
            block = match.group(2).strip()

            # Nettoyage du bloc
            raw_lines = [l.strip() for l in block.split(",") if l.strip()]
            lines_clean = [l for l in raw_lines if not l.startswith("priceBroken")]

            formatted_block = ",\n    ".join(f"{l}," for l in lines_clean)

            # Injecter les commentaires avant le bloc
            if pending_comments:
                output_lines.extend(pending_comments)
                pending_comments = []

            # Construire l'entrée convertie
            new_entry = (
                f'Shop.RegisterSellItem("{item_id}", {{\n'
                f'    {formatted_block}\n'
                f'}})'
            )

            # Ajouter le commentaire inline s'il existe
            if inline_comment:
                new_entry += f"  {inline_comment}"

            output_lines.append(new_entry + "\n")

            buffer = ""  # reset pour le prochain bloc

    # Écriture finale
    with open(output_path, "w", encoding="utf-8") as f:
        f.write("\n".join(output_lines))


def main():
    if len(sys.argv) != 3:
        print("Usage: python3 convert_forsell.py input.lua output.lua")
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]

    convert_file(input_path, output_path)
    print(f"Conversion terminée → {output_path}")


if __name__ == "__main__":
    main()

