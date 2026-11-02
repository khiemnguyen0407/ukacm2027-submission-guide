# UKACM 2027 – Abstract submission and review guide (Quarto)

- `ukacm2027-submission-guide.qmd` – source (renders to HTML and PDF).
- `figures/cmt/*.png` – annotated CMT screenshots used by the guide.
- `figures/cmt/raw/` – your original screenshots (unchanged).
- `figures/cmt/src/` – script that turns raw screenshots into the annotated figures:
  `python figures/cmt/src/build_figures.py` (needs Pillow; Liberation Sans and DejaVu Sans fonts).

Render:  `quarto render ukacm2027-submission-guide.qmd`  (or `--to pdf` / `--to html`).
Edit dates, e-mail, file limits etc. in the `ukacm:` block at the top of the .qmd.
Names and e-mail addresses in the screenshots were replaced by placeholders before publication.
