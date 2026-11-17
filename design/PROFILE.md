# Organization profile design

## Acceptance criteria

- Replace the table-heavy profile with an editorial composition, preserving official identity assets and public destinations.
- Use GitHub-supported HTML (`picture`, `source`, `img`, `a`, headings, and `details`); no scripts, inline CSS, or remote badge services.
- Keep the profile usable at 390 px and desktop widths in both GitHub themes, with meaningful image alternatives and native text/link fallbacks.
- Keep raster artwork unchanged. SVG layouts may surround approved artwork, but must not redraw the mark or mascot.
- Validate HTML rendering through GitHub, local asset references, SVG parsing, links, mobile layout, and visual screenshots before merging.

## References and rationale

- [Microsoft](https://github.com/microsoft/.github/blob/main/profile/README.md): distinctive cover art, concise participation paths.
- [Home Assistant](https://github.com/home-assistant/.github/blob/master/profile/README.md): a clear mission, community focus, and a short entry-point list.
- [Charm](https://github.com/charmbracelet): strong personality and a coherent project vocabulary.

These are structural references, not copied layouts or artwork. Our visual direction uses the official violet, emerald, lavender, and navy palette, paths that connect people, editorial numbering, and Ukuku.

## Asset provenance

- The official mark and Ukuku are unchanged copies of approved artwork from the community website.
- Original banner and mascot assets remain available in `profile/assets/`.
- New SVG compositions are generated from editable code. Letterforms use the website's Epilogue typeface, licensed under the SIL Open Font License; outlines avoid platform font substitution.
- Native HTML preserves the community description, topic vocabulary, participation links, and Spanish entry point. Every linked illustration has a descriptive alternative.

## Maintenance

Install `design/requirements.txt` in a Python virtual environment, then run `python scripts/render-profile.py` and `python scripts/verify-profile.py`. The generator resolves paths relative to the repository and embeds the exact approved raster bytes. Do not edit generated paths by hand.

The `picture` elements use separate mobile compositions. Cards have an intrinsic display width of 400 px and wrap naturally, without layout tables. Illustrations use their own accessible brand surfaces in either GitHub theme. They are static by design and make no motion or API requests. Keep the original assets for provenance.

Do not rely on a successful parse as visual proof: inspect the branch README on GitHub at 390 px and desktop widths before merging. Screenshots are local QA artifacts and must not be committed.
