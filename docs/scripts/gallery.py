import pathlib


def generate_gallery_markdown(image_dir, output_file, subdirs):
    """
    Generates a Markdown gallery of images from specified subdirectories.
    Each image is clickable and redirects to its corresponding markdown file.

    Args:
        image_dir (str or pathlib.Path): Path to the base directory containing image subdirectories.
        output_file (str or pathlib.Path): Path to the output Markdown file.
        subdirs (list of str): List of specific subdirectories to include in the gallery.
    """
    image_extensions = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tiff"}

    image_dir = pathlib.Path(image_dir)
    output_file = pathlib.Path(output_file)

    if not image_dir.is_dir():
        raise NotADirectoryError(
            f"The specified image directory does not exist: {image_dir}"
        )

    output_file.parent.mkdir(parents=True, exist_ok=True)

    markdown_lines = ["# Gallery\n"]

    for subdir in subdirs:
        subdir_path = image_dir / subdir
        if not subdir_path.is_dir():
            print(
                f"Warning: Subdirectory does not exist and will be skipped: {subdir_path}"
            )
            continue

        image_files = sorted(
            [
                file
                for file in subdir_path.iterdir()
                if file.suffix.lower() in image_extensions and file.is_file()
            ]
        )

        if not image_files:
            print(f"Warning: No image files found in subdirectory: {subdir_path}")
            continue

        subdir_md = f"{subdir}.md"
        subdir_md_path = pathlib.Path(output_file.parent) / "tuto" / subdir_md

        if not subdir_md_path.is_file():
            print(
                f"Warning: Markdown file does not exist for subdirectory '{subdir}': {subdir_md_path}"
            )
            link_target = "#"
        else:
            try:
                link_target = subdir_md_path.relative_to(output_file.parent)
            except ValueError:
                link_target = subdir_md_path.resolve()

        markdown_lines.append(f"## {subdir.capitalize()}\n")

        for image in image_files:
            try:
                relative_image_path = image.relative_to(output_file.parent)
            except ValueError:
                relative_image_path = image.resolve()

            markdown_line = f"[![{image.stem}]({relative_image_path})]({link_target})"
            markdown_lines.append(markdown_line)
            markdown_lines.append("\n")
            markdown_lines.append("<br>")

        markdown_lines.append("\n")

    markdown_content = "\n".join(markdown_lines)

    with output_file.open("w", encoding="utf-8") as md_file:
        md_file.write(markdown_content)

    print(f"\n\n  Gallery generated successfully at {output_file}")


if __name__ == "__main__":
    IMAGE_DIR = "docs/img/"
    OUTPUT_FILE = "docs/gallery.md"
    SUBDIRECTORIES = ["basic-styling", "boxstyle", "combine-charts", "negative-values"]
    generate_gallery_markdown(IMAGE_DIR, OUTPUT_FILE, SUBDIRECTORIES)
