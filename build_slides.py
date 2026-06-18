"""
Build Slides 11 & 12 — Innova Solutions visual style
Uses only Python stdlib (zipfile, xml) — no python-pptx required.
Output: innova_slides_11_12.pptx
"""
import zipfile, os, textwrap

# ── EMU helpers ──────────────────────────────────────────────────────────────
def emu(inches): return int(inches * 914400)

W  = emu(13.333)   # slide width
H  = emu(7.5)      # slide height

# ── Colour palette ───────────────────────────────────────────────────────────
NAVY    = "1B2F5E"
TEAL1   = "1B7A8A"
TEAL2   = "2E9E9E"
PURPLE  = "6B3FA0"
LTBLUE  = "D6E4F0"
LTBLUE2 = "EAF2FB"
WHITE   = "FFFFFF"
DGRAY   = "333333"
MGRAY   = "555555"
LGRAY   = "E0E8F5"
BLUE_IT = "1B5E8A"

# ── XML helpers ──────────────────────────────────────────────────────────────
def rgb(h): return h  # already a hex string

def sp(id_, name, x, y, cx, cy, fill=None, line=None):
    """Minimal shape (rectangle) XML."""
    fill_xml = ""
    if fill == "none":
        fill_xml = "<p:spPr><a:xfrm><a:off x='{}' y='{}'/><a:ext cx='{}' cy='{}'/></a:xfrm><a:prstGeom prst='rect'><a:avLst/></a:prstGeom><a:noFill/>".format(x,y,cx,cy)
        line_xml = ("<a:ln><a:solidFill><a:srgbClr val='{}'/></a:solidFill></a:ln>".format(line) if line else "<a:ln><a:noFill/></a:ln>") + "</p:spPr>"
        return fill_xml + line_xml
    if fill:
        fill_xml = "<a:solidFill><a:srgbClr val='{}'/></a:solidFill>".format(fill)
    else:
        fill_xml = "<a:noFill/>"
    line_xml = ("<a:ln><a:solidFill><a:srgbClr val='{}'/></a:solidFill></a:ln>".format(line)) if line else "<a:ln><a:noFill/></a:ln>"
    return (
        "<p:spPr>"
        "<a:xfrm><a:off x='{x}' y='{y}'/><a:ext cx='{cx}' cy='{cy}'/></a:xfrm>"
        "<a:prstGeom prst='rect'><a:avLst/></a:prstGeom>"
        "{fill}{line}"
        "</p:spPr>"
    ).format(x=x, y=y, cx=cx, cy=cy, fill=fill_xml, line=line_xml)


def txbody(paras):
    """Build <p:txBody> from list of para dicts."""
    out = "<p:txBody><a:bodyPr wrap='square' lIns='45720' rIns='45720' tIns='36000' bIns='36000'><a:normAutofit/></a:bodyPr><a:lstStyle/>"
    for p in paras:
        spc_bef = "<a:spcBef><a:spcPts spc='{}'/></a:spcBef>".format(p.get("spBef", 0))
        spc_aft = "<a:spcAft><a:spcPts spc='{}'/></a:spcAft>".format(p.get("spAft", 0))
        algn = p.get("algn", "l")
        out += "<a:p><a:pPr algn='{}' indent='0' marL='0'>{}{}</a:pPr>".format(algn, spc_bef, spc_aft)
        for r in p.get("runs", []):
            bold  = "1" if r.get("bold")  else "0"
            italic= "1" if r.get("italic") else "0"
            sz    = r.get("sz", 1200)
            color = r.get("color", DGRAY)
            txt   = r.get("t", "").replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
            out += (
                "<a:r><a:rPr lang='en-US' sz='{sz}' b='{b}' i='{i}' dirty='0'>"
                "<a:solidFill><a:srgbClr val='{c}'/></a:solidFill>"
                "<a:latin typeface='+mj-lt'/>"
                "</a:rPr><a:t>{t}</a:t></a:r>"
            ).format(sz=sz, b=bold, i=italic, c=color, t=txt)
        out += "</a:p>"
    out += "</p:txBody>"
    return out

def shape_xml(id_, name, x, y, cx, cy, fill, line, paras):
    sp_xml = sp(id_, name, x, y, cx, cy, fill, line)
    tx_xml = txbody(paras)
    return (
        "<p:sp><p:nvSpPr>"
        "<p:cNvPr id='{id}' name='{nm}'/>"
        "<p:cNvSpPr><a:spLocks noGrp='1'/></p:cNvSpPr>"
        "<p:nvPr/></p:nvSpPr>"
        "{sp}{tx}</p:sp>"
    ).format(id=id_, nm=name, sp=sp_xml, tx=tx_xml)


# ── Slide wrapper ─────────────────────────────────────────────────────────────
SLIDE_HEADER = (
    '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
    '<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
    ' xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
    ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">'
    '<p:cSld><p:spTree>'
    '<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>'
    '<p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{W}" cy="{H}"/>'
    '<a:chOff x="0" y="0"/><a:chExt cx="{W}" cy="{H}"/></a:xfrm></p:grpSpPr>'
).format(W=W, H=H)
SLIDE_FOOTER = '</p:spTree></p:cSld></p:sld>'

def bg_rect():
    """White background."""
    return (
        "<p:sp><p:nvSpPr><p:cNvPr id='2' name='bg'/>"
        "<p:cNvSpPr><a:spLocks noGrp='1'/></p:cNvSpPr><p:nvPr/></p:nvSpPr>"
        "<p:spPr><a:xfrm><a:off x='0' y='0'/><a:ext cx='{W}' cy='{H}'/></a:xfrm>"
        "<a:prstGeom prst='rect'><a:avLst/></a:prstGeom>"
        "<a:solidFill><a:srgbClr val='FFFFFF'/></a:solidFill>"
        "<a:ln><a:noFill/></a:ln></p:spPr>"
        "<p:txBody><a:bodyPr/><a:lstStyle/></p:txBody></p:sp>"
    ).format(W=W, H=H)

def footer_bar():
    """Dark navy footer bar at bottom."""
    fy = H - emu(0.28)
    return shape_xml(3, "footer", 0, fy, W, emu(0.28), NAVY, None, [
        {"algn":"l","runs":[{"t":"  1455 LINCOLN PARKWAY EAST, 8TH FLOOR, ATLANTA, GA 30346  |  WWW.INNOVASOLUTIONS.COM",
                              "sz":700,"color":WHITE}]}
    ])

def title_block(id_start, title, subtitle):
    """Slide title + subtitle top-left."""
    shapes = []
    shapes.append(shape_xml(id_start, "title", emu(0.35), emu(0.28), emu(8.5), emu(0.6), None, None, [
        {"algn":"l","runs":[{"t":title,"sz":3200,"bold":True,"color":NAVY}]}
    ]))
    shapes.append(shape_xml(id_start+1, "subtitle", emu(0.35), emu(0.88), emu(8.5), emu(0.38), None, None, [
        {"algn":"l","runs":[{"t":subtitle,"sz":1000,"italic":True,"color":MGRAY}]}
    ]))
    return shapes

def logo_block(id_):
    """Innova logo placeholder (text-based) top-right."""
    return shape_xml(id_, "logo", emu(10.9), emu(0.15), emu(2.1), emu(0.9), None, None, [
        {"algn":"r","runs":[{"t":"innova","sz":2000,"bold":True,"color":TEAL1}]},
        {"algn":"r","runs":[{"t":"SOLUTIONS","sz":1100,"bold":True,"color":NAVY}]},
    ])


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — MCP Servers: Connecting Claude to Enterprise Systems
# ═══════════════════════════════════════════════════════════════════════════════
def slide11():
    shapes = [bg_rect(), footer_bar()]
    shapes += title_block(10, "MCP Servers: Connecting Claude to Enterprise Systems",
        "Introduce how Claude securely connects to enterprise tools, databases, and applications via Model Context Protocol.")
    shapes.append(logo_block(14))

    # ── Hub-and-spoke layout ─────────────────────────────────────────────────
    # Center Claude bubble
    cx_center = emu(6.66)
    cy_center = emu(3.9)
    bubble_r  = emu(0.75)
    shapes.append(shape_xml(20,"hub",
        cx_center - bubble_r, cy_center - bubble_r,
        bubble_r*2, bubble_r*2,
        NAVY, None, [
            {"algn":"ctr","runs":[{"t":"Claude","sz":1600,"bold":True,"color":WHITE}]},
            {"algn":"ctr","runs":[{"t":"AI Core","sz":900,"color":LTBLUE}]},
        ]
    ))

    # Spoke nodes: (label, icon, color, x_offset, y_offset from center)
    spokes = [
        ("SharePoint",        "📁", TEAL1,   -emu(3.8),  -emu(1.5)),
        ("Jira",              "🎯", TEAL2,   -emu(3.8),   emu(0.0)),
        ("Salesforce",        "☁", PURPLE,  -emu(3.8),   emu(1.5)),
        ("SQL Database",      "🗄", TEAL1,    emu(3.8),  -emu(1.5)),
        ("APIs",              "🔌", TEAL2,    emu(3.8),   emu(0.0)),
        ("Healthcare KB",     "🏥", PURPLE,   emu(3.8),   emu(1.5)),
    ]

    node_w = emu(2.1)
    node_h = emu(0.7)
    id_ = 30

    for label, icon, color, dx, dy in spokes:
        nx = cx_center + dx - node_w//2
        ny = cy_center + dy - node_h//2
        # colored header strip for node
        shapes.append(shape_xml(id_, "node_hdr_"+label,
            nx, ny, node_w, emu(0.28), color, None,
            [{"algn":"l","runs":[{"t":f"  {icon}  {label}","sz":1000,"bold":True,"color":WHITE}]}]
        ))
        id_ += 1
        # connector line hint (thin colored rect acting as line)
        # draw thin horizontal/vertical bar from node edge toward center
        if dx < 0:  # left side — line goes right from node
            lx = nx + node_w
            ly = cy_center + dy - emu(0.02)
            lw = cx_center - bubble_r - lx
            shapes.append(shape_xml(id_, "line_"+label, lx, ly, max(lw,emu(0.05)), emu(0.04), LGRAY, None, []))
        else:       # right side — line goes left from node
            lx = cx_center + bubble_r
            ly = cy_center + dy - emu(0.02)
            lw = nx - lx
            shapes.append(shape_xml(id_, "line_"+label, lx, ly, max(lw,emu(0.05)), emu(0.04), LGRAY, None, []))
        id_ += 1

    # ── "Without MCP / With MCP" comparison panel (top strip) ───────────────
    # Without box
    shapes.append(shape_xml(id_,"without_hdr", emu(0.35), emu(1.45), emu(2.8), emu(0.35), PURPLE, None,
        [{"algn":"ctr","runs":[{"t":"Without MCP","sz":1000,"bold":True,"color":WHITE}]}]
    ))
    id_+=1
    shapes.append(shape_xml(id_,"without_body", emu(0.35), emu(1.8), emu(2.8), emu(0.6), LTBLUE2, LGRAY,
        [{"algn":"l","runs":[{"t":"  Claude only knows what users type","sz":900,"color":DGRAY}]}]
    ))
    id_+=1

    # With box
    shapes.append(shape_xml(id_,"with_hdr", emu(3.35), emu(1.45), emu(2.8), emu(0.35), TEAL1, None,
        [{"algn":"ctr","runs":[{"t":"With MCP","sz":1000,"bold":True,"color":WHITE}]}]
    ))
    id_+=1
    shapes.append(shape_xml(id_,"with_body", emu(3.35), emu(1.8), emu(2.8), emu(0.85), LTBLUE2, LGRAY,
        [{"algn":"l","runs":[{"t":"  Retrieve data  •  Query databases","sz":900,"color":DGRAY}]},
         {"algn":"l","runs":[{"t":"  Access documents  •  Read knowledge bases","sz":900,"color":DGRAY}]},
         {"algn":"l","runs":[{"t":"  Interact with enterprise applications","sz":900,"color":DGRAY}]}]
    ))
    id_+=1

    # ── Bottom callout ───────────────────────────────────────────────────────
    shapes.append(shape_xml(id_,"callout_bg", emu(0.35), emu(6.45), emu(12.6), emu(0.55), NAVY, None,
        [{"algn":"ctr","spBef":100,"runs":[
            {"t":'"MCP transforms Claude from a chatbot into an enterprise assistant."',
             "sz":1300,"italic":True,"bold":True,"color":WHITE}
        ]}]
    ))

    return SLIDE_HEADER + "".join(shapes) + SLIDE_FOOTER


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — AI Agents: Moving Beyond Questions & Answers
# ═══════════════════════════════════════════════════════════════════════════════
def slide12():
    shapes = [bg_rect(), footer_bar()]
    shapes += title_block(10, "AI Agents: Moving Beyond Questions & Answers",
        "How AI evolves from responding to prompts into executing multi-step business workflows.")
    shapes.append(logo_block(14))

    # ── Workflow pipeline ─────────────────────────────────────────────────────
    steps = [
        ("01","Goal",    "🎯", NAVY),
        ("02","Plan",    "🗺", TEAL1),
        ("03","Tools",   "🔧", TEAL2),
        ("04","Execute", "⚡", TEAL1),
        ("05","Validate","✅", PURPLE),
        ("06","Outcome", "📊", NAVY),
    ]
    step_w = emu(1.85)
    step_h = emu(0.8)
    gap    = emu(0.22)
    start_x= emu(0.35)
    row_y  = emu(1.5)
    id_    = 20

    for i,(num,label,icon,color) in enumerate(steps):
        sx = start_x + i*(step_w + gap)
        # header
        shapes.append(shape_xml(id_, f"step_hdr_{i}",
            sx, row_y, step_w, emu(0.35), color, None,
            [{"algn":"ctr","runs":[{"t":f"{num}  {icon}  {label}","sz":1050,"bold":True,"color":WHITE}]}]
        ))
        id_+=1
        # body placeholder
        body_texts = {
            "Goal":    "Define the\nobjective clearly",
            "Plan":    "Break into\nsteps & sub-tasks",
            "Tools":   "Select APIs,\ndatabases, models",
            "Execute": "Run tasks,\ncall systems",
            "Validate":"Check accuracy\n& completeness",
            "Outcome": "Deliver result\nto user",
        }
        shapes.append(shape_xml(id_, f"step_body_{i}",
            sx, row_y+emu(0.35), step_w, step_h, LTBLUE2, LGRAY,
            [{"algn":"ctr","runs":[{"t":body_texts[label],"sz":900,"color":DGRAY}]}]
        ))
        id_+=1
        # arrow between steps
        if i < len(steps)-1:
            ax = sx + step_w
            shapes.append(shape_xml(id_, f"arrow_{i}",
                ax, row_y + emu(0.47), gap, emu(0.06), TEAL1, None, []
            ))
            id_+=1

    # ── Two example cards ─────────────────────────────────────────────────────
    # Healthcare card
    hc_x = emu(0.35); hc_y = emu(2.7)
    hc_w = emu(6.0);  hc_h = emu(3.6)
    shapes.append(shape_xml(id_,"hc_hdr", hc_x, hc_y, hc_w, emu(0.42), TEAL1, None,
        [{"algn":"l","runs":[{"t":"  🏥  Healthcare Example — Prior Authorization Review Agent","sz":1100,"bold":True,"color":WHITE}]}]
    ))
    id_+=1
    hc_steps = [
        "1.  Receives authorization request",
        "2.  Retrieves CMS / MCG guidelines",
        "3.  Reviews clinical documentation",
        "4.  Identifies missing information",
        "5.  Generates recommendation",
        "6.  Creates rationale for reviewer",
        "7.  Routes to nurse or physician",
    ]
    hc_paras = [{"algn":"l","spBef":60,"runs":[{"t":f"  {s}","sz":950,"color":DGRAY}]} for s in hc_steps]
    shapes.append(shape_xml(id_,"hc_body", hc_x, hc_y+emu(0.42), hc_w, hc_h-emu(0.42), LTBLUE2, LGRAY, hc_paras))
    id_+=1

    # Business card
    biz_x = emu(6.7); biz_y = emu(2.7)
    biz_w = emu(6.28); biz_h = emu(3.6)
    shapes.append(shape_xml(id_,"biz_hdr", biz_x, biz_y, biz_w, emu(0.42), PURPLE, None,
        [{"algn":"l","runs":[{"t":"  📈  Business Example — Market Research Agent","sz":1100,"bold":True,"color":WHITE}]}]
    ))
    id_+=1
    biz_steps = [
        "1.  Receives research brief",
        "2.  Searches web & internal databases",
        "3.  Collects competitor data",
        "4.  Identifies key trends & gaps",
        "5.  Analyzes findings with reasoning",
        "6.  Drafts executive summary",
        "7.  Delivers formatted report",
    ]
    biz_paras = [{"algn":"l","spBef":60,"runs":[{"t":f"  {s}","sz":950,"color":DGRAY}]} for s in biz_steps]
    shapes.append(shape_xml(id_,"biz_body", biz_x, biz_y+emu(0.42), biz_w, biz_h-emu(0.42), LTBLUE2, LGRAY, biz_paras))
    id_+=1

    # ── Characteristics strip ─────────────────────────────────────────────────
    chars = [
        ("🧠","Understands\nObjectives"),
        ("🔀","Breaks Work\ninto Steps"),
        ("🛠","Uses Tools &\nSystems"),
        ("💡","Decides Based\non Context"),
        ("🔁","Iteratively\nImproves"),
    ]
    char_w = emu(2.35); char_h = emu(0.75)
    char_y = emu(6.42)
    char_gap = emu(0.16)
    char_sx = emu(0.35)
    for j,(icon,text) in enumerate(chars):
        cx2 = char_sx + j*(char_w+char_gap)
        col = [TEAL1,TEAL2,PURPLE,TEAL1,TEAL2][j]
        shapes.append(shape_xml(id_,"char_"+str(j), cx2, char_y, char_w, char_h, col, None,
            [{"algn":"ctr","runs":[{"t":f"{icon}  {text}","sz":900,"bold":True,"color":WHITE}]}]
        ))
        id_+=1

    return SLIDE_HEADER + "".join(shapes) + SLIDE_FOOTER


# ═══════════════════════════════════════════════════════════════════════════════
# PPTX packaging — pure zipfile construction
# ═══════════════════════════════════════════════════════════════════════════════

CONTENT_TYPES = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">
  <Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>
  <Default Extension="xml"  ContentType="application/xml"/>
  <Override PartName="/ppt/presentation.xml"
    ContentType="application/vnd.openxmlformats-officedocument.presentationml.presentation.main+xml"/>
  <Override PartName="/ppt/slides/slide1.xml"
    ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slides/slide2.xml"
    ContentType="application/vnd.openxmlformats-officedocument.presentationml.slide+xml"/>
  <Override PartName="/ppt/slideLayouts/slideLayout1.xml"
    ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideLayout+xml"/>
  <Override PartName="/ppt/slideMasters/slideMaster1.xml"
    ContentType="application/vnd.openxmlformats-officedocument.presentationml.slideMaster+xml"/>
  <Override PartName="/ppt/theme/theme1.xml"
    ContentType="application/vnd.openxmlformats-officedocument.theme+xml"/>
</Types>'''

ROOT_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
  <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument"
    Target="ppt/presentation.xml"/>
</Relationships>'''

def prs_xml(n_slides):
    sld_ids = "".join(
        f'<p:sldId id="{256+i}" r:id="rId{i+1}"/>' for i in range(n_slides)
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<p:presentation xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"'
        ' xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"'
        ' xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"'
        f' saveSubsetFonts="1">'
        f'<p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId99"/></p:sldMasterIdLst>'
        f'<p:sldIdLst>{sld_ids}</p:sldIdLst>'
        f'<p:sldSz cx="{W}" cy="{H}" type="screen16x9"/>'
        f'<p:notesSz cx="{emu(7.5)}" cy="{emu(10)}"/>'
        '</p:presentation>'
    )

def prs_rels(n_slides):
    rels = "".join(
        f'<Relationship Id="rId{i+1}" '
        f'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slide" '
        f'Target="slides/slide{i+1}.xml"/>\n' for i in range(n_slides)
    )
    rels += (
        '<Relationship Id="rId99" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster" '
        'Target="slideMasters/slideMaster1.xml"/>\n'
        '<Relationship Id="rId100" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme" '
        'Target="theme/theme1.xml"/>\n'
    )
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        + rels + '</Relationships>'
    )

def slide_rels():
    return (
        '<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
        '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
        '<Relationship Id="rId1" '
        'Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout" '
        'Target="../slideLayouts/slideLayout1.xml"/>'
        '</Relationships>'
    )

THEME = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<a:theme xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main" name="InnovaTheme">
  <a:themeElements>
    <a:clrScheme name="Innova">
      <a:dk1><a:srgbClr val="1B2F5E"/></a:dk1>
      <a:lt1><a:srgbClr val="FFFFFF"/></a:lt1>
      <a:dk2><a:srgbClr val="1B7A8A"/></a:dk2>
      <a:lt2><a:srgbClr val="D6E4F0"/></a:lt2>
      <a:accent1><a:srgbClr val="6B3FA0"/></a:accent1>
      <a:accent2><a:srgbClr val="2E9E9E"/></a:accent2>
      <a:accent3><a:srgbClr val="1B7A8A"/></a:accent3>
      <a:accent4><a:srgbClr val="6B3FA0"/></a:accent4>
      <a:accent5><a:srgbClr val="2E9E9E"/></a:accent5>
      <a:accent6><a:srgbClr val="1B2F5E"/></a:accent6>
      <a:hlink><a:srgbClr val="1B5E8A"/></a:hlink>
      <a:folHlink><a:srgbClr val="555555"/></a:folHlink>
    </a:clrScheme>
    <a:fontScheme name="Innova">
      <a:majorFont><a:latin typeface="Calibri"/><a:ea typeface=""/><a:cs typeface=""/></a:majorFont>
      <a:minorFont><a:latin typeface="Calibri"/><a:ea typeface=""/><a:cs typeface=""/></a:minorFont>
    </a:fontScheme>
    <a:fmtScheme name="Innova"><a:fillStyleLst>
      <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
      <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
      <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
    </a:fillStyleLst><a:lnStyleLst>
      <a:ln w="6350"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
      <a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
      <a:ln w="19050"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill></a:ln>
    </a:lnStyleLst><a:effectStyleLst>
      <a:effectStyle><a:effectLst/></a:effectStyle>
      <a:effectStyle><a:effectLst/></a:effectStyle>
      <a:effectStyle><a:effectLst/></a:effectStyle>
    </a:effectStyleLst><a:bgFillStyleLst>
      <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
      <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
      <a:solidFill><a:schemeClr val="phClr"/></a:solidFill>
    </a:bgFillStyleLst></a:fmtScheme>
  </a:themeElements>
</a:theme>'''

SLIDE_MASTER = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldMaster xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
 xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships">
 <p:cSld><p:spTree>
  <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
  <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>
   <a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
 </p:spTree></p:cSld>
 <p:clrMap bg1="lt1" tx1="dk1" bg2="lt2" tx2="dk2" accent1="accent1" accent2="accent2"
  accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" hlink="hlink" folHlink="folHlink"/>
 <p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst>
 <p:txStyles>
  <p:titleStyle><a:lvl1pPr><a:defRPr lang="en-US"/></a:lvl1pPr></p:titleStyle>
  <p:bodyStyle><a:lvl1pPr><a:defRPr lang="en-US"/></a:lvl1pPr></p:bodyStyle>
  <p:otherStyle><a:lvl1pPr><a:defRPr lang="en-US"/></a:lvl1pPr></p:otherStyle>
 </p:txStyles>
</p:sldMaster>'''

MASTER_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideLayout"
  Target="../slideLayouts/slideLayout1.xml"/>
 <Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/theme"
  Target="../theme/theme1.xml"/>
</Relationships>'''

SLIDE_LAYOUT = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<p:sldLayout xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
 xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main"
 xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships"
 type="blank" preserve="1">
 <p:cSld name="Blank"><p:spTree>
  <p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr>
  <p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/>
   <a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>
 </p:spTree></p:cSld>
 <p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr>
</p:sldLayout>'''

LAYOUT_RELS = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">
 <Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/slideMaster"
  Target="../slideMasters/slideMaster1.xml"/>
</Relationships>'''


def build_pptx(output_path):
    slides = [slide11(), slide12()]
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr("[Content_Types].xml", CONTENT_TYPES)
        z.writestr("_rels/.rels", ROOT_RELS)
        z.writestr("ppt/presentation.xml", prs_xml(len(slides)))
        z.writestr("ppt/_rels/presentation.xml.rels", prs_rels(len(slides)))
        z.writestr("ppt/theme/theme1.xml", THEME)
        z.writestr("ppt/slideMasters/slideMaster1.xml", SLIDE_MASTER)
        z.writestr("ppt/slideMasters/_rels/slideMaster1.xml.rels", MASTER_RELS)
        z.writestr("ppt/slideLayouts/slideLayout1.xml", SLIDE_LAYOUT)
        z.writestr("ppt/slideLayouts/_rels/slideLayout1.xml.rels", LAYOUT_RELS)
        for i, xml in enumerate(slides):
            z.writestr(f"ppt/slides/slide{i+1}.xml", xml)
            z.writestr(f"ppt/slides/_rels/slide{i+1}.xml.rels", slide_rels())
    print(f"Created: {output_path}  ({os.path.getsize(output_path):,} bytes)")


if __name__ == "__main__":
    out = "/projects/sandbox/innova_slides_11_12.pptx"
    build_pptx(out)
