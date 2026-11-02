"""Producer-approved arrangement contract for new AXEZENT review renders.

Five distinct sections, with a full 24-bar verse pocket to allow vocals.
Exactly 48 bars: intro 4 + hook 8 + verse 24 + hook 8 + outro 4.
Existing published/private MP3s are NOT modified by this specification.
"""
SECTIONS = (
    ("intro", 0, 4),
    ("hook", 4, 12),
    ("verse", 12, 36),
    ("hook", 36, 44),
    ("outro", 44, 48),
)
TOTAL_BARS = 48

def section_for_bar(bar):
    if not isinstance(bar,int) or not 0 <= bar < TOTAL_BARS:
        raise ValueError("bar must be an integer from 0 to 47")
    return next(name for name,start,end in SECTIONS if start <= bar < end)

def hook_ranges():
    return tuple((start,end) for name,start,end in SECTIONS if name=="hook")

def phrase_boundaries():
    return tuple(start for name,start,end in SECTIONS if name!="intro")
