"""Turn the raw CMT screenshots in ../raw into annotated figures in ..
Run:  python figures/cmt/src/build_figures.py
Personal names/e-mails in the screenshots are replaced by neutral placeholders.
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shotkit import (Fig, load, vstack, hstack, replace_text, erase,
                     ORANGE, RED, RED_PALE, GREY)

NAV = (51, 51, 51)

# ---------------------------------------------------------------- authors
def author_console():
    im = load("author_console_choose_Section.png").crop((0, 0, 880, 600))
    f = Fig(im, margin=(18, 18, 365, 18))
    f.box((14, 93, 226, 128))
    f.label(250, 111, "Click  + Create new submission…", n=1)
    f.box((15, 136, 863, 161), pad=2)
    b = f.label(905, 148, "Choose your minisymposium.\nThe track decides who\nreviews your abstract.", n=2)
    f.line([(b[0], 148), (866, 148)])
    b = f.label(905, 398, "Tip: tracks are sorted\nalphabetically, so S10–S18\nappear before S2–S9.", color=GREY,
                fill=(243, 245, 248))
    f.line([(b[0], 398), (866, 398)], color=GREY)
    f.save("author-console.png")


def title_abstract():
    im = load("title_and_abstract.png").crop((0, 0, 730, 538))
    erase(im, (628, 460, 698, 503), bg=(255, 255, 255))           # browser-extension icons
    replace_text(im, (212, 203, 700, 229), "Meshfree modelling of large-deformation contact (example)",
                 size=16, bg=(255, 255, 255), dx=7)
    abstract = "Paste your abstract here as plain text, e.g. u_h, E = 200 GPa."
    replace_text(im, (212, 262, 700, 285), abstract, size=16, bg=(255, 255, 255), dx=7)
    replace_text(im, (204, 509, 420, 527), f"{2000 - len(abstract)} characters left",
                 size=12, color=(102, 102, 102), bg=(255, 255, 255), dx=2)
    f = Fig(im, margin=(18, 18, 330, 18))
    f.box((24, 112, 585, 134), pad=3)
    b = f.label(760, 123, "Check that this is the\nright minisymposium", n=1)
    f.line([(b[0], 123), (589, 123)])
    f.box((206, 197, 705, 234), pad=2)
    b = f.label(760, 216, "Title of your talk", n=2)
    f.line([(b[0], 216), (709, 216)])
    f.box((206, 255, 705, 527), pad=2)
    b = f.label(760, 390, "Abstract as plain text,\nmax. 2,000 characters\n(counter below the box)", n=3)
    f.line([(b[0], 390), (709, 390)])
    f.save("title-abstract.png")


def authors():
    im = load("authors.png")
    bg = (247, 252, 255)
    replace_text(im, (182, 124, 590, 147), "your.name@university.ac.uk", size=16, bg=bg, dx=3)
    replace_text(im, (606, 124, 830, 147), "Firstname", size=16, bg=bg, dx=4)
    replace_text(im, (842, 124, 1010, 147), "Lastname", size=16, bg=bg, dx=4)
    f = Fig(im, margin=(18, 18, 18, 78))
    f.box((40, 118, 172, 156), pad=1)
    f.badge(40, 118, 1)
    f.box((35, 174, 1586, 258), pad=3)
    f.badge(35, 174, 2)
    f.box((1568, 120, 1642, 152), pad=1)
    f.badge(1642, 120, 3)
    y = 278 + 46
    b1 = f.label(20, y, "You are the Primary Contact\n(corresponding author)", n=1)
    b2 = f.label(560, y, "Co-author: e-mail of their CMT account, name,\norganisation and country, then  + Add", n=2)
    b3 = f.label(1642, y, "Remove (×) or\nreorder (↑↓) authors", n=3, anchor="r")
    f.line([(106, b1[1]), (106, 160)])
    f.line([(800, b2[1]), (800, 262)])
    f.line([(1605, b3[1]), (1605, 156)])
    f.save("authors.png")


def files_submit():
    files = load("drop_files.png")
    sub = load("click_submit.png").crop((0, 0, files.width, 87))
    gap = Fig  # noqa (keeps linters quiet)
    im = vstack([files, sub], gap=34)
    f = Fig(im, margin=(18, 18, 18, 18))
    f.d.text(f.P(820, 218 + 17), "⋮  other sections of the form, if shown  ⋮",
             font=__import__("shotkit").font("ann", 13), fill=GREY, anchor="mm")
    f.box((5, 41, 523, 60), pad=2)
    f.label(40, 120, "1 to 3 files · max. 10 MB\nPDF, DOC or DOCX", n=1)
    f.line([(160, 98), (160, 64)])
    f.box((723, 141, 901, 172), pad=3)
    b = f.label(960, 140, "Drag and drop the file,\nor Upload from Computer", n=2)
    f.line([(b[0], 140), (906, 150)])
    y0 = 218 + 34
    f.box((236, y0 + 18, 311, y0 + 55), pad=3)
    f.label(462, y0 + 34, "Click Submit – the form and your\nfiles are saved only now", n=3)
    f.line([(462, y0 + 50), (446, y0 + 72), (273, y0 + 72), (273, y0 + 61)])
    f.save("files-submit.png")


# ---------------------------------------------------------------- track chairs
def track_nav():
    im = load("choose_users_then_reviewers.png").crop((0, 0, 1275, 296))
    erase(im, (343, 98, 870, 138), bg=(255, 255, 255))          # tooltip text behind menu
    f = Fig(im, margin=(18, 76, 18, 18))
    f.box((998, 47, 1264, 79), pad=1)
    b = f.label(1264, -40, "Select Your Role: Track Chair", n=1, anchor="r")
    f.line([(1131, b[3]), (1131, 44)])
    f.box((362, 47, 970, 79), pad=1)
    b = f.label(420, -40, "The minisymposium (track) you manage", n=2)
    f.line([(600, b[3]), (600, 44)])
    f.box((143, 3, 229, 43), pad=0)
    f.box((145, 101, 341, 133), pad=1)
    f.label(372, 117, "Users  ›  Reviewers  opens Manage Reviewers", n=3)
    f.save("track-chair-nav.png")


def actions_invite():
    raw = load("choose_actions_invite.png")
    left, right = raw.crop((0, 90, 320, 383)), raw.crop((1400, 90, 1654, 383))
    im = hstack([left, right], gap=40)
    X = lambda x: x - 1400 + 360
    f = Fig(im, margin=(18, 18, 360, 18))
    f.break_mark(340, 4, 289)
    f.box((X(1547), 62, X(1628), 96), pad=2)
    f.box((X(1463), 104, X(1626), 196), pad=2)
    lx = X(1654) + 34
    b = f.label(lx, 26, "Open Actions", n=1)
    f.line([(lx, 26), (X(1632), 72)])
    b = f.label(lx, 92, "Invite: one reviewer at a time", n=2)
    f.line([(lx, 92), (X(1630), 119)])
    b = f.label(lx, 152, "Invite (Bulk): upload a list", n=3)
    f.line([(lx, 152), (X(1630), 150)])
    b = f.label(lx, 220, "Manage Invites: see replies,\nsend reminders", n=4)
    f.line([(lx, 220), (X(1630), 180)])
    f.save("actions-invite.png")


def invite_search():
    raw = load("search_reviewer_with_email.png")
    replace_text(raw, (36, 292, 231, 319), "a.reviewer@uni.ac.uk", size=16, color=(85, 85, 85),
                 bg=(255, 255, 255), dx=6)
    replace_text(raw, (34, 398, 600, 423), "A. Reviewer", size=16, color=(51, 51, 51), dx=4)
    im = vstack([raw.crop((0, 95, 1000, 180)), raw.crop((0, 278, 1000, 522))])
    Y = lambda y: y - 193
    f = Fig(im, margin=(18, 18, 345, 18))
    f.box((30, Y(287), 330, Y(324)), pad=2)
    f.label(352, Y(305), "Type the reviewer’s e-mail, then Search", n=1)
    f.box((30, Y(391), 999, Y(431)), pad=1)
    b = f.label(1030, Y(411), "Existing CMT user found.\nNot found? Enter first name,\nlast name and organisation.", n=2)
    f.line([(b[0], Y(411)), (1003, Y(411))])
    f.box((472, Y(472), 530, Y(508)), pad=3)
    f.label(556, Y(490), "Next: write the invitation", n=3)
    f.save("invite-search.png")


def dashed(f, x0, x1, y, color=ORANGE):
    x = x0
    while x < x1:
        f.line([(x, y), (min(x + 10, x1), y)], color=color, width=2, dot=False)
        x += 18


def invite_compose():
    im = load("invite_reviewer_compose_email.png").crop((0, 0, 1200, 798))
    replace_text(im, (199, 104, 760, 127), "Track Chair Name <track.chair@university.ac.uk>",
                 size=16, bg=(255, 255, 255), dx=2)
    replace_text(im, (199, 158, 760, 181), "A. Reviewer <a.reviewer@uni.ac.uk>",
                 size=16, bg=(255, 255, 255), dx=2)
    f = Fig(im, margin=(18, 18, 18, 18))
    dashed(f, 214, 700, 356)
    f.label(745, 352, "Add your own paragraph here:\nminisymposium, number of\nabstracts and review period", n=1)
    f.line([(745, 352), (704, 356)])
    f.box((209, 369, 522, 462), color=RED, pad=3, fill=None)
    f.label(745, 428, "Do not edit or delete\nthe accept/decline links", n=2, color=RED, fill=RED_PALE)
    f.line([(745, 428), (528, 418)], color=RED)
    f.box((210, 584, 292, 606), pad=3)
    f.label(745, 595, "Sign with your name\ninstead of “CMT team”", n=3)
    f.line([(745, 595), (298, 595)])
    f.box((464, 754, 547, 791), pad=3)
    f.label(572, 772, "Preview, then Send", n=4)
    f.save("invite-compose.png")


def bulk_invite():
    im = load("bulk_invite_reviewer.png")
    f = Fig(im, margin=(18, 18, 18, 18))
    f.box((22, 272, 1632, 312), pad=3)
    b = f.label(700, 354, "One reviewer per line: these five fields in this order,\n"
                          "separated by tabs (leave Middle Initial empty if none)", n=1)
    f.line([(900, b[1]), (900, 317)])
    f.box((20, 330, 236, 351), pad=2)
    f.box((22, 409, 155, 440), pad=3)
    f.label(182, 425, "Save as UTF-8 text (.txt), then Upload user list", n=2)
    f.box((465, 480, 523, 517), pad=3)
    f.label(548, 498, "Check the list → Next → edit e-mail → Preview → Send", n=3)
    f.save("bulk-invite.png")


if __name__ == "__main__":
    author_console(); title_abstract(); authors(); files_submit()
    track_nav(); actions_invite(); invite_search(); invite_compose(); bulk_invite()
    print("all figures built")
