#!/usr/bin/env python3
"""Build a 16:9 policy deck: A Documented Pakistan."""

from pptx import Presentation
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.oxml.ns import qn
from pptx.util import Inches, Pt
from lxml import etree

# 16:9
W, H = Inches(13.333), Inches(7.5)

FOREST = RGBColor(0x0B, 0x3D, 0x2E)
DEEP = RGBColor(0x07, 0x1C, 0x16)
PINE = RGBColor(0x12, 0x35, 0x28)
GOLD = RGBColor(0xC9, 0xA2, 0x27)
GOLD_SOFT = RGBColor(0xE8, 0xD4, 0x8B)
CREAM = RGBColor(0xF6, 0xF1, 0xE6)
WHITE = RGBColor(0xFF, 0xFD, 0xF8)
INK = RGBColor(0x14, 0x20, 0x1B)
MUTED = RGBColor(0x5C, 0x6B, 0x64)
DANGER = RGBColor(0x3A, 0x15, 0x15)
DANGER_SOFT = RGBColor(0x9B, 0x2C, 0x2C)
CARD = RGBColor(0xFF, 0xFF, 0xFF)
CARD_DARK = RGBColor(0x0F, 0x2A, 0x22)


def set_run(run, size, bold=False, color=INK, font="Calibri", italic=False):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    run.font.name = font
    rPr = run._r.get_or_add_rPr()
    # East Asian / latin fallback
    for tag in ("latin", "ea", "cs"):
        el = rPr.find(qn(f"a:{tag}"))
        if el is None:
            el = etree.SubElement(rPr, qn(f"a:{tag}"))
        el.set("typeface", font)


def add_text(box, text, size=18, bold=False, color=INK, font="Calibri", align=PP_ALIGN.LEFT, italic=False):
    tf = box.text_frame
    tf.clear()
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    set_run(run, size, bold, color, font, italic)
    return tf


def add_para(tf, text, size=16, bold=False, color=INK, font="Calibri", space_before=6, space_after=0, italic=False):
    p = tf.add_paragraph()
    p.space_before = Pt(space_before)
    p.space_after = Pt(space_after)
    run = p.add_run()
    run.text = text
    set_run(run, size, bold, color, font, italic)
    return p


def fill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def rect(slide, l, t, w, h, color):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, l, t, w, h)
    fill(s, color)
    return s


def round_rect(slide, l, t, w, h, color):
    s = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, l, t, w, h)
    fill(s, color)
    # less rounded
    try:
        s.adjustments[0] = 0.08
    except Exception:
        pass
    return s


def gold_bar(slide, l, t, w=Inches(0.7), h=Inches(0.05)):
    return rect(slide, l, t, w, h, GOLD)


def footer(slide, left, right, dark=False):
    color = RGBColor(0xA8, 0xB5, 0xAE) if dark else MUTED
    box = slide.shapes.add_textbox(Inches(0.55), Inches(7.12), Inches(8.5), Inches(0.28))
    add_text(box, left, 10, False, color)
    box2 = slide.shapes.add_textbox(Inches(9.2), Inches(7.12), Inches(3.55), Inches(0.28))
    add_text(box2, right, 10, False, color, align=PP_ALIGN.RIGHT)


def kicker(slide, text, l=Inches(0.55), t=Inches(0.32), dark=False):
    box = slide.shapes.add_textbox(l, t, Inches(12.2), Inches(0.32))
    add_text(box, text.upper(), 11, True, GOLD_SOFT if dark else GOLD)


def heading(slide, text, l=Inches(0.55), t=Inches(0.62), w=Inches(12.2), h=Inches(1.1), size=32, color=INK, font="Georgia"):
    box = slide.shapes.add_textbox(l, t, w, h)
    add_text(box, text, size, True, color, font)
    return box


def bullets(slide, items, l, t, w, h, size=15, color=INK, dark=False):
    box = slide.shapes.add_textbox(l, t, w, h)
    tf = box.text_frame
    tf.word_wrap = True
    tf.clear()
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.level = 0
        p.space_after = Pt(8)
        run = p.add_run()
        run.text = "•  " + item
        set_run(run, size, False, color)
    return box


def card(slide, l, t, w, h, dark=False):
    return round_rect(slide, l, t, w, h, CARD_DARK if dark else WHITE)


def blank(prs, dark=False):
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    rect(slide, 0, 0, W, H, DEEP if dark else CREAM)
    if not dark:
        rect(slide, 0, 0, W, Inches(0.08), FOREST)
        rect(slide, 0, Inches(7.42), W, Inches(0.08), GOLD)
    else:
        rect(slide, 0, Inches(7.42), W, Inches(0.08), GOLD)
    return slide


def build():
    prs = Presentation()
    prs.slide_width = W
    prs.slide_height = H

    # 1 Cover
    s = blank(prs, dark=True)
    kicker(s, "Pakistan Policy Briefing  ·  Civic  ·  Fiscal  ·  Reform", dark=True)
    gold_bar(s, Inches(0.55), Inches(1.55))
    heading(s, "A Documented Pakistan", Inches(0.55), Inches(1.75), Inches(12), Inches(1.4), 48, CREAM, "Georgia")
    box = s.shapes.add_textbox(Inches(0.55), Inches(3.35), Inches(11.2), Inches(1.6))
    add_text(
        box,
        "Tax compliance, a wider tax net, and a fairer economy: what it is, how we achieve it, who benefits, who is punished if the law is applied, and the problems we already live with by not doing it.",
        20,
        False,
        GOLD_SOFT,
    )
    footer(s, "Policy presentation  ·  For classroom / civic briefing use", "01 / 13", True)

    # 2 Argument
    s = blank(prs)
    kicker(s, "01  —  The argument")
    heading(s, "Pakistan does not have a revenue problem first.\nIt has a documentation problem.", size=28)
    gold_bar(s, Inches(0.55), Inches(1.85))
    box = s.shapes.add_textbox(Inches(0.55), Inches(2.1), Inches(6.3), Inches(1.4))
    add_text(
        box,
        "A documented economy means sales, salaries, property, imports and bank flows are visible to the state — so tax can be collected fairly, credit can be given honestly, and policy can be based on facts rather than guesses.",
        16,
        False,
        MUTED,
    )
    bullets(
        s,
        [
            "The salaried class and a thin layer of companies already pay.",
            "A large share of retail, real estate, agriculture wealth and cash trade does not.",
            "Governments then raise rates on the visible few, which pushes more activity underground.",
        ],
        Inches(0.55),
        Inches(3.55),
        Inches(6.3),
        Inches(2.6),
        16,
    )
    card(s, Inches(7.15), Inches(2.1), Inches(5.55), Inches(4.55))
    box = s.shapes.add_textbox(Inches(7.4), Inches(2.28), Inches(5.1), Inches(0.35))
    add_text(box, "THIS BRIEFING ANSWERS FOUR QUESTIONS", 11, True, GOLD)
    bullets(
        s,
        [
            "How can Pakistan actually achieve documentation?",
            "What are the benefits if we do?",
            "What punishment applies if a person does not comply — and if the law is enforced?",
            "What problems are we already facing by not doing this?",
        ],
        Inches(7.4),
        Inches(2.7),
        Inches(5.1),
        Inches(3.0),
        15,
    )
    box = s.shapes.add_textbox(Inches(7.4), Inches(5.7), Inches(5.1), Inches(0.7))
    add_text(box, "Slide 07 puts all four answers on one page — the complete Pakistan picture.", 13, False, MUTED, italic=True)
    footer(s, "A Documented Pakistan", "02 / 13")

    # 3 Numbers
    s = blank(prs)
    kicker(s, "02  —  The gap")
    heading(s, "The documentation gap, in numbers", size=30, h=Inches(0.7))
    gold_bar(s, Inches(0.55), Inches(1.4))
    stats = [
        ("POPULATION", "~240m", "People living in the economy that must be financed."),
        ("WORKFORCE", "~85m", "People earning. Most are outside the income-tax net."),
        ("ACTIVE RETURN FILERS", "~2.5m", "Roughly 3 in 100 workers file a meaningful return."),
        ("INFORMAL ECONOMY", "35–40%", "Share of GDP outside proper books, POS and returns."),
    ]
    for i, (lab, num, desc) in enumerate(stats):
        x = Inches(0.55) + i * Inches(3.15)
        card(s, x, Inches(1.7), Inches(3.0), Inches(2.45))
        b = s.shapes.add_textbox(x + Inches(0.18), Inches(1.85), Inches(2.65), Inches(0.3))
        add_text(b, lab, 11, True, GOLD)
        b = s.shapes.add_textbox(x + Inches(0.18), Inches(2.15), Inches(2.65), Inches(0.7))
        add_text(b, num, 32, True, FOREST, "Georgia")
        b = s.shapes.add_textbox(x + Inches(0.18), Inches(2.9), Inches(2.65), Inches(1.0))
        add_text(b, desc, 13, False, MUTED)
    stats2 = [
        ("FBR COLLECTION FY2026", "Rs 13.01 tr", "Record collection — still a narrow base, not a broad one."),
        ("FBR TAX-TO-GDP FY2026", "10.3%", "Developing peers often sit in the mid-teens; OECD around one-third of GDP."),
        ("REGISTERED FILERS (JUN 2025)", "7.2m", "Registration rose. Active, honest filing did not rise at the same pace."),
    ]
    for i, (lab, num, desc) in enumerate(stats2):
        x = Inches(0.55) + i * Inches(4.2)
        card(s, x, Inches(4.35), Inches(4.0), Inches(2.35))
        b = s.shapes.add_textbox(x + Inches(0.2), Inches(4.5), Inches(3.6), Inches(0.28))
        add_text(b, lab, 11, True, GOLD)
        b = s.shapes.add_textbox(x + Inches(0.2), Inches(4.8), Inches(3.6), Inches(0.55))
        add_text(b, num, 26, True, FOREST, "Georgia")
        b = s.shapes.add_textbox(x + Inches(0.2), Inches(5.4), Inches(3.6), Inches(1.05))
        add_text(b, desc, 13, False, MUTED)
    footer(s, "Sources: Finance Division Jul 2026 · FBR 2025 · The News FY27 analysis", "03 / 13")

    # 4 Definition
    s = blank(prs)
    kicker(s, "03  —  Definition")
    heading(s, "What “doing this” actually means", size=30, h=Inches(0.7))
    gold_bar(s, Inches(0.55), Inches(1.4))
    defs = [
        ("01  ·  CITIZEN", "File, declare, stay on the ATL", "Every person with taxable income files an income-tax return on time, stays on the Active Taxpayer List, and can explain large purchases from declared wealth."),
        ("02  ·  BUSINESS", "Books, invoices, banked sales", "Shops and firms issue invoices, keep purchase and sales records, use bank or digital payment where required, and — if notified — connect POS / e-invoicing to FBR."),
        ("03  ·  STATE", "Simple rules, equal enforcement", "The state makes compliance cheaper than hiding, stops harassing honest filers, and uses data (utilities, property, imports, banking) instead of raids as the default tool."),
    ]
    for i, (tag, title, body) in enumerate(defs):
        x = Inches(0.55) + i * Inches(4.2)
        card(s, x, Inches(1.7), Inches(4.0), Inches(3.7))
        b = s.shapes.add_textbox(x + Inches(0.22), Inches(1.9), Inches(3.55), Inches(0.3))
        add_text(b, tag, 11, True, GOLD)
        b = s.shapes.add_textbox(x + Inches(0.22), Inches(2.3), Inches(3.55), Inches(0.9))
        add_text(b, title, 20, True, INK, "Georgia")
        b = s.shapes.add_textbox(x + Inches(0.22), Inches(3.3), Inches(3.55), Inches(1.85))
        add_text(b, body, 15, False, MUTED)
    b = s.shapes.add_textbox(Inches(0.55), Inches(5.6), Inches(12.2), Inches(1.1))
    add_text(
        b,
        "Documentation is not “more tax on the same people.” It is bringing hidden turnover into the light so rates on the documented minority can eventually come down.",
        18,
        False,
        INK,
        "Georgia",
    )
    footer(s, "A Documented Pakistan", "04 / 13")

    # 5 How
    s = blank(prs)
    kicker(s, "04  —  How we achieve this")
    heading(s, "How Pakistan can achieve a documented economy", size=28, h=Inches(0.7))
    gold_bar(s, Inches(0.55), Inches(1.4))
    steps = [
        ("01", "Make filing easy", "IRIS, mobile apps, Urdu/regional forms, facilitation centres. Fixed Tax Asaan Scheme (1% of turnover, min Rs 25,000, sales up to Rs 200m) is built for this."),
        ("02", "Reward the filer", "Lowest withholding, refunds, bank accounts, property and vehicle access, government contracts and cheaper credit must belong to people on the ATL."),
        ("03", "See the transaction", "POS and e-invoicing for large retail and notified sectors; NADRA / land / customs / bank data matched to returns so lifestyle and income cannot stay strangers."),
        ("04", "Protect the honest", "No random shop raids on scheme participants, association-based disputes, and a real end to “audit as harassment.” Fear is why Tajir Dost failed."),
        ("05", "Enforce the big leaks", "Apply penalties, Section 114C high-value blocks, and sealing powers on persistent non-filers and fake invoicing — not on the smallest compliant trader."),
    ]
    for i, (n, title, body) in enumerate(steps):
        x = Inches(0.4) + i * Inches(2.56)
        r = round_rect(s, x, Inches(1.7), Inches(2.44), Inches(4.85), WHITE)
        rect(s, x, Inches(1.7), Inches(2.44), Inches(0.08), GOLD)
        b = s.shapes.add_textbox(x + Inches(0.12), Inches(1.95), Inches(2.2), Inches(0.45))
        add_text(b, n, 26, True, GOLD, "Georgia")
        b = s.shapes.add_textbox(x + Inches(0.12), Inches(2.45), Inches(2.2), Inches(0.85))
        add_text(b, title, 16, True, INK, "Georgia")
        b = s.shapes.add_textbox(x + Inches(0.12), Inches(3.35), Inches(2.2), Inches(2.95))
        add_text(b, body, 12, False, MUTED)
    footer(s, "Path: simplify → reward → digitise → protect → punish the leak, not the compliant", "05 / 13")

    # 6 Benefits
    s = blank(prs)
    kicker(s, "05  —  Benefits")
    heading(s, "Benefits if Pakistan actually does this", size=30, h=Inches(0.7))
    gold_bar(s, Inches(0.55), Inches(1.4))
    card(s, Inches(0.55), Inches(1.7), Inches(6.0), Inches(4.9))
    b = s.shapes.add_textbox(Inches(0.8), Inches(1.9), Inches(5.5), Inches(0.3))
    add_text(b, "FOR THE COUNTRY", 12, True, GOLD)
    bullets(
        s,
        [
            "More revenue without crushing the same 2.5 million people — a wider base funds schools, hospitals, water and defence.",
            "Lower fiscal deficit and less debt interest. FY2026 showed what a primary surplus can do; a broader base makes it lasting.",
            "Subsidies can be targeted instead of sprayed — including on power.",
            "Better policy: you cannot plan industry, exports or cities if half of GDP is a rumour.",
        ],
        Inches(0.8),
        Inches(2.35),
        Inches(5.5),
        Inches(4.0),
        15,
    )
    card(s, Inches(6.8), Inches(1.7), Inches(6.0), Inches(4.9))
    b = s.shapes.add_textbox(Inches(7.05), Inches(1.9), Inches(5.5), Inches(0.3))
    add_text(b, "FOR THE CITIZEN AND THE HONEST BUSINESS", 12, True, GOLD)
    bullets(
        s,
        [
            "ATL / filer status: lowest withholding on property, cars, bank profit, dividends; refund of extra tax; normal bank accounts.",
            "Documented sales are the passport to bank loans, export certification and government tenders.",
            "Fair competition: the shop that issues invoices stops losing to the shop that hides turnover.",
            "Dignity: a return is proof of contribution — and proof of income for a visa, a plot, or a court.",
        ],
        Inches(7.05),
        Inches(2.35),
        Inches(5.5),
        Inches(4.0),
        15,
    )
    footer(s, "A Documented Pakistan", "06 / 13")

    # 7 COMPLETE SLIDE
    s = blank(prs, dark=True)
    kicker(s, "06  —  Complete Pakistan picture", dark=True)
    heading(s, "How we achieve this in Pakistan — benefits, punishments, and the cost of not doing it", size=22, h=Inches(0.7), color=CREAM)
    b = s.shapes.add_textbox(Inches(0.55), Inches(1.28), Inches(12.2), Inches(0.3))
    add_text(b, "One slide. Four answers. This is the civic choice in front of the country.", 13, False, GOLD_SOFT)

    panels = [
        (FOREST, "A  ·  HOW WE ACHIEVE IT", [
            "Every earner files; traders join Asaan Tax (1% turnover, min Rs 25,000) or the regular return.",
            "Large retail / notified sectors live on FBR e-invoices and POS — no sale off-system.",
            "Banks, land records, NADRA, customs and utilities talk to IRIS so lifestyle matches income.",
            "The state cuts harassment, keeps rates predictable, and spends visibly so people see a return on tax.",
            "Provinces document urban property and agricultural wealth instead of leaving the salaried class alone in the net.",
        ]),
        (PINE, "B  ·  BENEFITS IF WE DO IT", [
            "Wider tax base → room to lower rates on those already paying.",
            "ATL benefits: cheaper withholding, refunds, cars, plots, bank accounts, tenders.",
            "Banks can lend against real books; investment and jobs follow documentation.",
            "State can fund education, health, water and climate without repeating debt crises.",
            "Informal 35–40% of GDP slowly becomes countable, taxable and financeable.",
        ]),
        (DANGER, "C  ·  PUNISHMENT IF ONE DOES NOT APPLY / IF THE LAW IS APPLIED", [
            "Non-filer: 2–4× withholding on banks, property, cars, dividends; no ordinary new bank account; no refund.",
            "Late filer: daily default penalty + ATL surcharge (individuals Rs 25,000 in 2026-27).",
            "Concealment / false particulars: penalty raised to Rs 1 million (Finance Bill 2026) plus tax evaded.",
            "No records on audit: Rs 100,000 / 200,000 / 300,000. Failure to withhold: Rs 500,000; company officers personally Rs 500,000.",
            "Section 114C (gazette pending): blocks cars over Rs 7m, homes over Rs 50m, commercial property over Rs 100m, securities over Rs 50m/year, cash out over Rs 100m/year unless resources are declared at 130% of the deal. Persistent default: fines and power to seal premises.",
        ]),
        (RGBColor(0x2A, 0x24, 0x10), "D  ·  PROBLEMS WE FACE BY NOT DOING THIS", [
            "The documented minority is over-taxed; the undocumented majority is invisible — a justice failure, not only a fiscal one.",
            "Every budget becomes an IMF negotiation because the base is too small for the state’s bills.",
            "Cash, smuggling and benami property hide crime, terror finance and elite tax evasion in the same fog.",
            "Honest businesses cannot compete; talent leaves; investment stays short-term and speculative.",
            "No data means bad schools, leaking power, unplanned cities, and subsidies that never reach the poor.",
        ]),
    ]
    coords = [
        (Inches(0.4), Inches(1.65)),
        (Inches(6.75), Inches(1.65)),
        (Inches(0.4), Inches(4.2)),
        (Inches(6.75), Inches(4.2)),
    ]
    for (color, title, items), (x, y) in zip(panels, coords):
        round_rect(s, x, y, Inches(6.15), Inches(2.45), color)
        b = s.shapes.add_textbox(x + Inches(0.18), y + Inches(0.08), Inches(5.8), Inches(0.32))
        add_text(b, title, 10, True, GOLD_SOFT)
        bullets(s, items, x + Inches(0.12), y + Inches(0.38), Inches(5.9), Inches(2.0), 11, CREAM)
    footer(s, "The complete civic slide  ·  Apply · Benefit · Or pay the penalty", "07 / 13", True)

    # 8 Punishment table-like
    s = blank(prs)
    kicker(s, "07  —  Punishment if applied")
    heading(s, "What the law does to you if you do not apply", size=28, h=Inches(0.65))
    gold_bar(s, Inches(0.55), Inches(1.35))
    rows = [
        ("If you…", "Status", "What hits you", True),
        ("File on time and stay truthful", "Active filer (ATL)", "Lowest withholding; refunds allowed; full economic access; still must keep books.", False),
        ("File after the deadline", "Late filer", "Daily penalty (Finance Bill 2026 proposed sharp increases, including Rs 2,000/day in some sales-tax cases). ATL surcharge to return to the list (Rs 25,000 for individuals, 2026-27).", False),
        ("Never file", "Non-filer", "2–4× withholding on almost every documented transaction. New bank accounts largely blocked. No refund. Highest friction on property and vehicles.", False),
        ("Hide income or file false details", "Evader", "Penalty up to Rs 1,000,000 plus the tax evaded. Repeat behaviour can go higher. Criminal provisions remain available for tax fraud.", False),
        ("Ignore audit notices / don’t withhold", "Defaulter", "Record penalties Rs 100k–300k; withholding failure Rs 500,000; company principals personally Rs 500,000. Premises can be sealed after continued default.", False),
        ("Large lifestyle, no declared wealth", "Ineligible (s.114C)", "Once notified: cannot book a car above Rs 7m, a house above Rs 50m FMV, commercial property above Rs 100m, heavy securities, or pull Rs 100m+ cash in a year without 130% declared resources.", False),
    ]
    y = Inches(1.55)
    col_w = [Inches(3.15), Inches(2.4), Inches(6.65)]
    for i, (a, btxt, c, header) in enumerate(rows):
        hrow = Inches(0.68) if not header else Inches(0.38)
        bg = FOREST if header else (WHITE if i % 2 == 0 else RGBColor(0xEE, 0xE6, 0xD6))
        x = Inches(0.55)
        for w, txt in zip(col_w, (a, btxt, c)):
            r = rect(s, x, y, w, hrow, bg)
            tb = s.shapes.add_textbox(x + Inches(0.08), y + Inches(0.04), w - Inches(0.12), hrow - Inches(0.06))
            add_text(tb, txt, 10 if header else 11, True if header or (w == col_w[1] and not header) else False, CREAM if header else INK)
            x += w
        y += hrow
    b = s.shapes.add_textbox(Inches(0.55), Inches(6.55), Inches(12.2), Inches(0.5))
    add_text(
        b,
        "Note: Section 114C is in the Income Tax Ordinance (Finance Act 2025) but, as of August 2026 reporting, the federal gazette date and operational rules were still pending. Withholding and ATL disadvantages already apply.",
        11,
        False,
        MUTED,
        italic=True,
    )
    footer(s, "Finance Bill 2026  ·  Income Tax Ordinance 2001  ·  FBR ATL rules", "08 / 13")

    # 9 Problems
    s = blank(prs, dark=True)
    kicker(s, "08  —  Cost of not doing this", dark=True)
    heading(s, "Problems we are already facing by not doing this", size=28, h=Inches(0.7), color=CREAM)
    gold_bar(s, Inches(0.55), Inches(1.4))
    probs = [
        ("01", "A state that cannot pay for itself", "Interest on old debt eats the budget. Development is residual. We borrow to run the government because too few people are on the books."),
        ("02", "The salaried class as a hostage", "Tax is deducted from the salary slip before the employee sees it. Retail, wholesale, real-estate flipping and cash professions often pay nothing comparable."),
        ("03", "Fake competition", "A documented factory paying payroll, GST and industrial power cannot beat a cash competitor. Industry thins out. Jobs that should exist never appear."),
        ("04", "Black money has a home", "Undocumented plots, cash and under-invoiced imports are where corruption, smuggling and tax evasion hide. Without trails, courts and banks are guessing."),
        ("05", "No credit, no scale", "Banks will not lend against a notebook in a drawer. Firms stay small, families stay informal, and the country stays a trading economy instead of a producing one."),
        ("06", "Trust collapse", "Citizens ask why they should pay if the elite does not. The state asks why it should improve service if nobody pays. Both are waiting. Both are wrong to wait."),
    ]
    for i, (n, title, body) in enumerate(probs):
        r, c = divmod(i, 3)
        x = Inches(0.45) + c * Inches(4.25)
        y = Inches(1.65) + r * Inches(2.55)
        card(s, x, y, Inches(4.1), Inches(2.4), dark=True)
        b = s.shapes.add_textbox(x + Inches(0.2), y + Inches(0.12), Inches(3.7), Inches(0.45))
        add_text(b, n, 22, True, GOLD, "Georgia")
        b = s.shapes.add_textbox(x + Inches(0.2), y + Inches(0.55), Inches(3.7), Inches(0.55))
        add_text(b, title, 15, True, CREAM, "Georgia")
        b = s.shapes.add_textbox(x + Inches(0.2), y + Inches(1.15), Inches(3.7), Inches(1.1))
        add_text(b, body, 12, False, GOLD_SOFT)
    footer(s, "Not doing documentation is not neutral. It is a daily policy choice with victims.", "09 / 13", True)

    # 10 Fairness
    s = blank(prs)
    kicker(s, "09  —  Fairness")
    heading(s, "Who pays today — and who should", size=30, h=Inches(0.7))
    gold_bar(s, Inches(0.55), Inches(1.4))
    card(s, Inches(0.55), Inches(1.7), Inches(6.0), Inches(4.35))
    b = s.shapes.add_textbox(Inches(0.8), Inches(1.88), Inches(5.5), Inches(0.28))
    add_text(b, "OVER-DOCUMENTED", 12, True, GOLD)
    b = s.shapes.add_textbox(Inches(0.8), Inches(2.2), Inches(5.5), Inches(0.7))
    add_text(b, "Salaried employees, large companies, importers at the port, formal banks", 16, True, INK, "Georgia")
    bullets(
        s,
        [
            "Cannot hide: withholding is automatic.",
            "Face audits, payroll tax, sales tax and rising rates whenever the deficit yawns.",
            "This is why “tax culture” speeches sound empty to a teacher or a software employee.",
        ],
        Inches(0.8),
        Inches(3.05),
        Inches(5.5),
        Inches(2.6),
        15,
    )
    card(s, Inches(6.8), Inches(1.7), Inches(6.0), Inches(4.35))
    b = s.shapes.add_textbox(Inches(7.05), Inches(1.88), Inches(5.5), Inches(0.28))
    add_text(b, "UNDER-DOCUMENTED", 12, True, GOLD)
    b = s.shapes.add_textbox(Inches(7.05), Inches(2.2), Inches(5.5), Inches(0.7))
    add_text(b, "Cash retail, parts of wholesale, speculators, some cash professions, much real-estate gain", 16, True, INK, "Georgia")
    bullets(
        s,
        [
            "About 4.2–4.4 million traders are the Asaan Tax target — most still outside a serious return.",
            "High-value cars and houses are often bought without income that matches the price.",
            "Agriculture income is provincial; urban agri-wealth and lifestyle often escape both federation and province.",
        ],
        Inches(7.05),
        Inches(3.05),
        Inches(5.5),
        Inches(2.6),
        15,
    )
    b = s.shapes.add_textbox(Inches(0.55), Inches(6.2), Inches(12.2), Inches(0.7))
    add_text(
        b,
        "A just policy does not hunt the easy target. It documents the large leak, simplifies the small trader, and then lowers rates for everyone who stayed honest.",
        16,
        False,
        INK,
        "Georgia",
    )
    footer(s, "A Documented Pakistan", "10 / 13")

    # 11 Path
    s = blank(prs)
    kicker(s, "10  —  Practical path")
    heading(s, "A 12-month path that can actually work", size=30, h=Inches(0.7))
    gold_bar(s, Inches(0.55), Inches(1.4))
    cols = [
        ("CITIZENS", "File this year. Stay on ATL.", [
            "Create an IRIS account / FBR app login.",
            "File even if income is modest — filer status is an asset.",
            "Keep bank trails for rent, fees and large buys.",
            "Do not “save” tax by staying a non-filer: extra withholding is usually larger than the tax due.",
        ]),
        ("TRADERS & SMEs", "Pick the simple door, then grow.", [
            "If turnover ≤ Rs 200m: Fixed Tax Asaan Scheme — 1% of sales, minimum Rs 25,000, no routine POS/audit.",
            "Keep a basic sales and purchase book. Under-declaring now is a future raid.",
            "If you scale past the scheme, integrate e-invoicing before FBR forces it.",
        ]),
        ("THE STATE", "Stop repeating Tajir Dost.", [
            "Honour the no-harassment promise on scheme shops.",
            "Notify Section 114C with clear rules — then apply it to luxury leaks, not kiryana stores.",
            "Publish where the extra rupee goes: schools, water, local hospitals.",
            "Match property, cars and electricity with returns. Quiet data beats noisy raids.",
        ]),
    ]
    for i, (tag, title, items) in enumerate(cols):
        x = Inches(0.45) + i * Inches(4.25)
        card(s, x, Inches(1.7), Inches(4.1), Inches(4.9))
        b = s.shapes.add_textbox(x + Inches(0.22), Inches(1.9), Inches(3.65), Inches(0.28))
        add_text(b, tag, 12, True, GOLD)
        b = s.shapes.add_textbox(x + Inches(0.22), Inches(2.25), Inches(3.65), Inches(0.7))
        add_text(b, title, 18, True, INK, "Georgia")
        bullets(s, items, x + Inches(0.18), Inches(3.05), Inches(3.75), Inches(3.3), 14)
    footer(s, "A Documented Pakistan", "11 / 13")

    # 12 Do vs don't
    s = prs.slides.add_slide(prs.slide_layouts[6])
    rect(s, 0, 0, Inches(6.666), H, PINE)
    rect(s, Inches(6.666), 0, Inches(6.667), H, DANGER)
    b = s.shapes.add_textbox(Inches(0.5), Inches(0.45), Inches(5.7), Inches(0.3))
    add_text(b, "IF WE DO THIS", 12, True, GOLD_SOFT)
    b = s.shapes.add_textbox(Inches(0.5), Inches(0.85), Inches(5.7), Inches(1.1))
    add_text(b, "A country that can see itself", 28, True, CREAM, "Georgia")
    bullets(
        s,
        [
            "Tax base expands; rates on the salaried can be discussed downward in good faith.",
            "IMF programmes become shorter because the numbers add up.",
            "Banks finance factories, not only plots.",
            "Luxury that cannot be explained is blocked at the registration desk.",
            "A teacher and a trader stand in the same civic line: both documented, both served.",
        ],
        Inches(0.5),
        Inches(2.2),
        Inches(5.7),
        Inches(4.5),
        16,
        CREAM,
    )
    b = s.shapes.add_textbox(Inches(7.15), Inches(0.45), Inches(5.7), Inches(0.3))
    add_text(b, "IF WE DO NOT", 12, True, GOLD_SOFT)
    b = s.shapes.add_textbox(Inches(7.15), Inches(0.85), Inches(5.7), Inches(1.1))
    add_text(b, "The same cycle, more expensive", 28, True, CREAM, "Georgia")
    bullets(
        s,
        [
            "Another budget of higher penalties on the same trapped base.",
            "Capital and talent leave; remaining businesses stay informal on purpose.",
            "Debt interest remains the largest “development” line.",
            "Smog, water, schools and hospitals stay underfunded while cash houses rise.",
            "The next generation inherits a state that still cannot count its own economy.",
        ],
        Inches(7.15),
        Inches(2.2),
        Inches(5.7),
        Inches(4.5),
        16,
        CREAM,
    )

    # 13 Close
    s = blank(prs, dark=True)
    kicker(s, "Close", dark=True)
    gold_bar(s, Inches(0.55), Inches(1.15))
    b = s.shapes.add_textbox(Inches(0.55), Inches(1.4), Inches(12.2), Inches(1.8))
    add_text(
        b,
        "Documentation is not a tax. It is the decision that Pakistan will stop guessing — and stop punishing only the people it can already see.",
        28,
        True,
        CREAM,
        "Georgia",
    )
    notes = [
        ("REMEMBER", "~2.5 million active filers cannot finance 240 million lives. Broaden the base, then lower the rate."),
        ("APPLY", "File. Join Asaan Tax if you trade small. Keep books. The penalty for staying invisible is already more expensive than the tax."),
        ("DEMAND", "Enforcement on the big leak, protection for the honest, and public proof that the rupee built a school, not a scandal."),
    ]
    for i, (tag, body) in enumerate(notes):
        x = Inches(0.55) + i * Inches(4.2)
        b = s.shapes.add_textbox(x, Inches(3.5), Inches(3.95), Inches(0.3))
        add_text(b, tag, 12, True, GOLD)
        b = s.shapes.add_textbox(x, Inches(3.9), Inches(3.95), Inches(1.5))
        add_text(b, body, 15, False, CREAM)
    b = s.shapes.add_textbox(Inches(0.55), Inches(5.6), Inches(12.2), Inches(1.35))
    add_text(
        b,
        "Figures and legal notes: Finance Division Monthly Economic Update (July 2026); FBR collection and filer briefings (FY2025–FY2026); The News Budget FY27 analysis; Dawn and PKRevenue on Finance Bill 2026 penalties; Income Tax Ordinance s.114C (Finance Act 2025); Fixed Tax Asaan Scheme (June 2026). Penalty amounts and notification dates can change — verify on FBR / gazette before relying for compliance.",
        11,
        False,
        RGBColor(0x8A, 0x9A, 0x93),
    )
    footer(s, "A Documented Pakistan", "13 / 13  ·  End of briefing", True)

    out = "/workspace/presentation/Pakistan_Documented_Economy.pptx"
    prs.save(out)
    print("Wrote", out)


if __name__ == "__main__":
    build()
