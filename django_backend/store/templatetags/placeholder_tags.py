"""Template tags for generating placeholder images"""
from django import template
import hashlib
import base64

register = template.Library()

COLORS = [
    ('#16a34a', '#15803d'), ('#059669', '#047857'), ('#0d9488', '#0f766e'),
    ('#0891b2', '#0e7490'), ('#0284c7', '#0369a1'), ('#2563eb', '#1d4ed8'),
    ('#4f46e5', '#4338ca'), ('#7c3aed', '#6d28d9'), ('#9333ea', '#7e22ce'),
    ('#c026d3', '#a21caf'), ('#db2777', '#be185d'), ('#e11d48', '#be123c'),
    ('#ea580c', '#c2410c'), ('#d97706', '#b45309'), ('#65a30d', '#4d7c0f'),
]

def get_color_for_text(text):
    hash_val = int(hashlib.md5(text.encode()).hexdigest(), 16)
    return COLORS[hash_val % len(COLORS)]

@register.simple_tag
def placeholder_svg(name, width=400, height=300):
    color1, color2 = get_color_for_text(name)
    display_name = name[:20] + '...' if len(name) > 20 else name
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">
        <defs>
            <linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:{color1}"/>
                <stop offset="100%" style="stop-color:{color2}"/>
            </linearGradient>
        </defs>
        <rect width="100%" height="100%" fill="url(#g)"/>
        <circle cx="50%" cy="40%" r="60" fill="white" opacity="0.2"/>
        <text x="50%" y="70%" font-size="22" fill="white" text-anchor="middle" font-weight="bold">{display_name}</text>
        <text x="50%" y="85%" font-size="14" fill="rgba(255,255,255,0.8)" text-anchor="middle">Ayurvedic Product</text>
    </svg>'''
    
    encoded = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    return f"data:image/svg+xml;base64,{encoded}"

@register.simple_tag
def category_icon_svg(name, size=80):
    color1, color2 = get_color_for_text(name)
    safe_name = name.replace(' ', '')
    
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24">
        <defs>
            <linearGradient id="cg{safe_name}" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" style="stop-color:{color1}"/>
                <stop offset="100%" style="stop-color:{color2}"/>
            </linearGradient>
        </defs>
        <circle cx="12" cy="12" r="11" fill="url(#cg{safe_name})"/>
        <circle cx="12" cy="12" r="5" fill="white" opacity="0.9"/>
    </svg>'''
    return svg
