"""Catalog of sheets and products with prices and links; prices are estimates.

Inputs: none. Outputs: none; read by settings.load() and passed to the model.
Implements spec 6.3 (Settings).
"""

# --- Sheets: (length, width, price €, link); prices are estimates until quoted ---
frame_sheet = (  # 37mm laminated pine, Strahan
    242,
    121.5,
    123.0,
    "https://www.strahanonlineshop.ie/products/2420-x-1215-x-37mm-lam-pine-board-furniture-grade",
)
thin_sheet = (  # 18mm laminated pine, Strahan
    244,
    122,
    69.68,
    "https://www.strahanonlineshop.ie/products/laminated-edged-glued-solid-pine-board-2240mm-1220mm?variant=54972301705553",
)
back_sheet = (  # 9mm V-groove MR MDF, Strahan, 50mm centres to order; price unquoted
    244,
    122,
    57.50,
    "https://www.strahanonlineshop.ie/products/moisture-mdf-medium-density-fibreboard-grooved?variant=54972282339665",
)

# --- Hardware and finish: (product, pack size, pack price €, link) ---
hinges = (
    "LOOTICH 110° soft-close inset",
    8,
    18.58,
    "https://www.amazon.ie/dp/B07S52MPYH",
)
knobs = ("owned", 1, 0.0, "")
long_screws = ("4 × 60mm countersunk, owned", 100, 0.0, "")
pocket_screws = (
    "Jyvex black M4 × 30mm pan head",
    100,
    7.79,
    "https://www.amazon.ie/dp/B0DG923ZSZ",
)
short_screws = ("4 × 30mm countersunk, owned", 100, 0.0, "")
washers = ("M4 flat, owned", 100, 0.0, "")
braces = (  # no screws included
    "Screwfix Essentials zinc 77 × 77mm",
    10,
    4.05,
    "https://www.screwfix.ie/p/essentials-corner-braces-zinc-plated-77mm-x-77mm-x-16-5mm-10-pack/12488",
)
brace_screws = ("15mm or shorter, owned", 100, 0.0, "")
dowels = (
    "Easyfix 8mm × 30mm",
    100,
    3.45,
    "https://www.screwfix.ie/p/easyfix-dowels-8mm-x-30mm-100-pack/282vn",
)
brackets = ("homemade", 1, 0.0, "")
varnish = (  # litres; TJ O'Mahony sale price
    "Ronseal Interior Varnish Antique Pine satin",
    0.75,
    21.91,
    "https://tjomahony.ie/rn-int-varnish-antique-pine-satin-750ml-7536837.html",
)
primer = (  # litres; B&Q
    "GoodHome grey multi-surface primer",
    0.75,
    20.0,
    "https://www.diy.ie/departments/goodhome-grey-multi-surface-wood-primer-undercoat-750ml/5036581057220_BQ.prd",
)
paint = (  # litres; B&Q
    "GoodHome Liberty black satin",
    0.75,
    20.0,
    "https://www.diy.ie/departments/goodhome-liberty-black-satin-interior-metal-wood-paint-750ml/5036581059460_BQ.prd",
)
roller = (  # sale price
    "Axus Blonde natural wool mini, 101mm",
    1,
    5.65,
    "https://tjomahony.ie/axus-blonde-100-natural-wool-mini-roller-kit-78axu-rkbln4.html",
)
sleeves = (  # sale price
    "Axus Blonde 101mm sleeves",
    10,
    9.72,
    "https://tjomahony.ie/axus-blonde-100-natural-wool-mini-sleeve-pack-of-10-4-101mm-78axu-rbln410.html",
)
brush = (
    "Screwfix 173FM synthetic, 3 inch",
    1,
    4.95,
    "https://www.screwfix.ie/p/synthetic-paint-brush-3-/173fm",
)
sponges = (
    "Bosch Expert 421VV, superfine/fine/medium",
    3,
    6.85,
    "https://www.screwfix.ie/p/bosch-expert-superfine-fine-medium-grit-multi-material-hand-sanding-sponges-97mm-x-67mm-3-pack/421vv",
)

# --- Tools: (product, pack size, price €, link); 0 when owned; prices paid ---
plunge_saw = (
    "Erbauer ERB1066PLG 185mm plunge saw with 2 rails",
    1,
    188.0,
    "https://www.screwfix.ie/p/erbauer-erb1066plg-185mm-electric-plunge-saw-with-2-x-rail-s-240v/676ah",
)
mitre_saw = (
    "MacAllister MCB1362MSW 210mm sliding mitre saw, owned",
    1,
    0.0,
    "https://www.diy.ie/departments/mac-allister-1500w-220-240v-210mm-corded-sliding-mitre-saw-mcb1362msw/5063022800107_BQ.prd",
)
guide_rails = ("guide rails, 4 (6 in all joined, about 2.6m used)", 1, 65.0, "")
pocket_jig = (
    "Gunpla 45pcs twin pocket hole jig kit",
    1,
    19.0,
    "https://www.amazon.ie/dp/B0BGWRQYNC",
)
drill = ("drill/driver, 8mm brad-point bit and depth stop, owned", 1, 0.0, "")
corner_clamps = (  # price unlisted (page unavailable); set what was paid
    "FengZeYing 4 aluminium 90° corner clamps, 77mm",
    1,
    0.0,
    "https://www.amazon.ie/dp/B0DF34CWXB",
)
clamps = ("clamps, a couple to prop a side on edge, owned", 1, 0.0, "")
t_square = (
    "Stanley T-square 565 × 1220mm",
    1,
    32.95,
    "https://www.screwfix.ie/p/stanley-t-square-22-1-4-x-48-565mm-x1220mm-/5826k",
)
tape_measure = (
    "Hultafors BT5M Big T pocket tape 5m",
    1,
    33.19,
    "https://www.amazon.ie/gp/product/B007GJN90Q",
)
saw_blade = (
    "Trend CSB/CC21660 216mm 60-tooth TCT blade, 2.6mm kerf",
    1,
    25.87,
    "https://www.amazon.ie/gp/product/B00DVND2P8",
)
stud_finder = ("stud finder, owned", 1, 0.0, "")
dowel_jig = (
    "EFUTURETIME self-centring dowel jig set, 6–10mm",
    1,
    17.0,
    "https://www.amazon.ie/gp/product/B0D4V9T7PZ",
)
