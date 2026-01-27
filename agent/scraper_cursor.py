import os
import sys
import time
import re
import json
from collections import Counter
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Optional, Set
from urllib.parse import urlparse, urljoin

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_FILE = os.path.join(BASE_DIR, "contexto_para_cursor.txt")

# --- DATA STRUCTURES ---

@dataclass
class MetaData:
    site_name: str = ""
    url: str = ""
    language: str = "pt-br"
    business_type: str = "Generic"
    title: str = ""
    description: str = ""

@dataclass
class ColorPalette:
    brand_primary: str = ""
    cta_color: str = ""
    accent_color: str = ""
    neutral_base: str = ""

@dataclass
class BrandAssets:
    logo_url: str = ""
    logo_type: str = "" # svg, png
    colors: ColorPalette = field(default_factory=ColorPalette)

@dataclass
class ContentBlock:
    intent: str # VALUE_PROP, SERVICE, TRUST, CTA
    text: str
    tag: str

@dataclass
class SectionStatus:
    name: str
    found: bool
    confidence: str

@dataclass
class DesignHeuristics:
    visual_density: str = "Medium"
    layout_style: str = "Structured"
    industry_vibe: str = "Corporate"

@dataclass
class ScrapedContext:
    metadata: MetaData = field(default_factory=MetaData)
    brand: BrandAssets = field(default_factory=BrandAssets)
    content: List[ContentBlock] = field(default_factory=list)
    sections: List[SectionStatus] = field(default_factory=list)
    heuristics: DesignHeuristics = field(default_factory=DesignHeuristics)
    raw_images: List[str] = field(default_factory=list)

# --- UTILS ---

def clean_text(text: str) -> str:
    if not text: return ""
    # Remove excessive whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def is_valid_color(color_str: str) -> bool:
    if not color_str: return False
    if color_str == 'rgba(0, 0, 0, 0)': return False
    if 'rgb' in color_str or '#' in color_str: return True
    return False

def rgb_to_hex(rgb_str):
    # Basic conversion if needed, or keep rgb
    # For simplicity, keeping as is if it's valid css
    return rgb_str

# --- LAYERS IMPLEMENTATION ---

class ScraperEngine:
    def __init__(self, url, client_name_hint=""):
        self.url = url
        if not self.url.startswith('http'):
            self.url = 'https://' + self.url
        self.client_name_hint = client_name_hint
        self.driver = None
        self.soup = None
        self.context = ScrapedContext()

    def _init_driver(self):
        options = Options()
        options.add_argument("--headless=new")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36")
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    def scrape(self):
        print(f"🚀 [ENGINE] Starting extraction for: {self.url}")
        self._init_driver()
        try:
            self.driver.get(self.url)
            time.sleep(3) # Wait for JS
            
            # Scroll to trigger lazy load
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
            time.sleep(1)
            self.driver.execute_script("window.scrollTo(0, 0);")

            self.soup = BeautifulSoup(self.driver.page_source, 'html.parser')

            # EXECUTE LAYERS
            self._layer_metadata()
            self._layer_brand_signals()
            self._layer_content_intent()
            self._layer_structural_sections()
            self._layer_design_heuristics()
            self._layer_noise_filtering()

            return self.context
        except Exception as e:
            print(f"❌ [ERROR] Scraping failed: {e}")
            import traceback
            traceback.print_exc()
            return None
        finally:
            if self.driver:
                self.driver.quit()

    # --- 1. METADATA LAYER ---
    def _layer_metadata(self):
        print("🔹 [LAYER 1] Metadata...")
        meta = self.context.metadata
        meta.url = self.url
        
        # Title & Desc
        if self.soup.title:
            meta.title = clean_text(self.soup.title.string)
        
        desc_tag = self.soup.find("meta", attrs={"name": "description"})
        if desc_tag:
            meta.description = clean_text(desc_tag.get("content"))

        # Site Name (OpenGraph or Title fallback)
        og_site_name = self.soup.find("meta", property="og:site_name")
        if og_site_name:
            meta.site_name = clean_text(og_site_name.get("content"))
        elif self.client_name_hint:
            meta.site_name = self.client_name_hint
        else:
            meta.site_name = meta.title.split('|')[0].strip()

        # Language Detection (Hard enforcement)
        html_lang = self.soup.html.get('lang', '').lower()
        body_text = self.soup.body.get_text().lower()
        pt_score = sum(1 for word in ['você', 'atendimento', 'serviços', 'contato', 'brasil', 'solicite'] if word in body_text)
        
        if 'pt' in html_lang or pt_score > 0:
            meta.language = 'pt-br'
        else:
            # Fallback if unsure, but prompt requested enforcement if PT dominates.
            # Assuming PT context for this tool
            meta.language = 'pt-br'

    # --- 2. BRAND SIGNALS LAYER ---
    def _layer_brand_signals(self):
        print("🔹 [LAYER 2] Brand Signals...")
        # A) Logo Extraction
        logo_url = ""
        
        # Strategy: Look for img with 'logo' in class/id/alt inside header
        candidates = []
        for img in self.soup.find_all('img'):
            score = 0
            src = img.get('src', '')
            if not src: continue
            
            src_lower = src.lower()
            alt_lower = (img.get('alt') or '').lower()
            class_id = (str(img.get('class')) + str(img.get('id'))).lower()

            if 'logo' in class_id: score += 5
            if 'logo' in src_lower: score += 3
            if 'logo' in alt_lower: score += 2
            if '.svg' in src_lower: score += 2 # Prefer SVG
            
            # Check parent (is it in header?)
            parents = [p.name for p in img.parents]
            if 'header' in parents or 'nav' in parents:
                score += 3

            if score > 0:
                full_url = urljoin(self.url, src)
                candidates.append((score, full_url))

        if candidates:
            candidates.sort(key=lambda x: x[0], reverse=True)
            logo_url = candidates[0][1]
        
        self.context.brand.logo_url = logo_url
        self.context.brand.logo_type = 'svg' if '.svg' in logo_url.lower() else 'bitmap'

        # B) Color Extraction via Computed Styles (Selenium)
        # We need to find "Action" elements
        def get_computed_color(selector, prop='background-color'):
            try:
                el = self.driver.find_element(By.CSS_SELECTOR, selector)
                return el.value_of_css_property(prop)
            except:
                return None

        # Try to find primary button color
        btn_selectors = [
            "a[href*='contact']", "button[type='submit']", 
            ".btn-primary", ".button-primary", "a.button", 
            "header a[href]" # CTA in header often
        ]
        
        primary_candidates = []
        for sel in btn_selectors:
            col = get_computed_color(sel)
            if is_valid_color(col):
                primary_candidates.append(col)
        
        # Defaults
        brand_primary = primary_candidates[0] if primary_candidates else "#0ea5e9" # Default fallback
        
        # Try to find footer bg for neutral
        neutral = get_computed_color("footer", 'background-color') or "#f7fafc"

        self.context.brand.colors.brand_primary = brand_primary
        self.context.brand.colors.cta_color = brand_primary # Often same, can be differentiated later
        self.context.brand.colors.neutral_base = neutral

    # --- 3. CONTENT INTENT LAYER ---
    def _layer_content_intent(self):
        print("🔹 [LAYER 3] Content Intent...")
        
        # Extract H1/H2 for Value Prop
        h1s = self.soup.find_all('h1')
        for h1 in h1s:
            text = clean_text(h1.get_text())
            if len(text) > 5:
                self.context.content.append(ContentBlock("VALUE_PROPOSITION", text, "h1"))

        # Extract H2/H3 for Service Descriptions
        # Look for sections containing "Serviços", "Services", "O que fazemos"
        services_section = self.soup.find(lambda tag: tag.name in ['section', 'div'] and ('serviço' in tag.get_text().lower() or 'service' in tag.get_text().lower()))
        
        if services_section:
            for item in services_section.find_all(['h3', 'h4', 'li']):
                text = clean_text(item.get_text())
                if len(text) > 5 and len(text) < 100:
                    self.context.content.append(ContentBlock("SERVICE_DESCRIPTION", text, item.name))
        
        # Extract Trust Signals (numbers, badges)
        # Heuristic: Look for short blocks with numbers + text
        # (Simplified for now)

    # --- 4. STRUCTURAL SECTIONS LAYER ---
    def _layer_structural_sections(self):
        print("🔹 [LAYER 4] Structural Sections...")
        full_text = self.soup.get_text().lower()
        
        checks = {
            "HERO": True, # Almost always exists
            "SERVICES": any(x in full_text for x in ['serviços', 'services', 'soluções']),
            "TESTIMONIALS": any(x in full_text for x in ['depoimentos', 'clientes', 'opiniões', 'reviews']),
            "SPONSORS": len(self.soup.find_all('img')) > 5, # Weak heuristic, but a proxy
            "CONTACT_FORM": bool(self.soup.find('form') or 'contato' in full_text),
            "FOOTER": bool(self.soup.find('footer'))
        }

        for name, found in checks.items():
            self.context.sections.append(SectionStatus(name, found, "High" if found else "Low"))

    # --- 5. DESIGN HEURISTICS LAYER ---
    def _layer_design_heuristics(self):
        print("🔹 [LAYER 5] Design Heuristics...")
        # Simple Logic based on content length
        text_len = len(self.soup.get_text())
        if text_len < 2000:
            self.context.heuristics.visual_density = "Low (Minimalist)"
        elif text_len > 10000:
            self.context.heuristics.visual_density = "High (Content Heavy)"
        
        # Industry guess based on keywords
        full_text = self.soup.get_text().lower()
        if any(x in full_text for x in ['saúde', 'médico', 'clínica', 'estética']):
            self.context.heuristics.industry_vibe = "Health & Wellness"
        elif any(x in full_text for x in ['construção', 'engenharia', 'obra', 'reforma']):
            self.context.heuristics.industry_vibe = "Construction & Engineering"
        elif any(x in full_text for x in ['advogado', 'direito', 'jurídico']):
            self.context.heuristics.industry_vibe = "Legal & Corporate"

    # --- 6. NOISE FILTERING LAYER ---
    def _layer_noise_filtering(self):
        # Filter duplicates in content blocks
        seen = set()
        unique_content = []
        for block in self.context.content:
            if block.text not in seen:
                seen.add(block.text)
                unique_content.append(block)
        self.context.content = unique_content

# --- OUTPUT GENERATOR ---

def generate_context_file(context: ScrapedContext):
    lines = []
    lines.append("==========================================")
    lines.append("   CONTEXTO GERADO PELO SCRAPER V2.0")
    lines.append("==========================================")
    lines.append("")
    
    # 1. METADATA
    lines.append("## 1. METADATA LAYER")
    lines.append(f"SITE_NAME: {context.metadata.site_name}")
    lines.append(f"ORIGIN_URL: {context.metadata.url}")
    lines.append(f"LANGUAGE: {context.metadata.language} (MANDATORY)")
    lines.append(f"BUSINESS_TYPE: {context.metadata.business_type}")
    lines.append(f"TITLE: {context.metadata.title}")
    lines.append(f"DESCRIPTION: {context.metadata.description}")
    lines.append("")

    # 2. BRAND SIGNALS
    lines.append("## 2. BRAND SIGNALS LAYER")
    lines.append(f"LOGO_URL: {context.brand.logo_url}")
    lines.append(f"LOGO_FORMAT: {context.brand.logo_type}")
    lines.append(f"PRIMARY_COLOR: {context.brand.colors.brand_primary}")
    lines.append(f"CTA_COLOR: {context.brand.colors.cta_color}")
    lines.append(f"NEUTRAL_BASE: {context.brand.colors.neutral_base}")
    lines.append("")

    # 3. STRUCTURAL SECTIONS
    lines.append("## 3. DETECTED SECTIONS")
    for sec in context.sections:
        status = "FOUND" if sec.found else "NOT FOUND"
        lines.append(f"- {sec.name}: {status}")
    lines.append("")

    # 4. DESIGN HEURISTICS
    lines.append("## 4. DESIGN GUIDANCE")
    lines.append(f"DENSITY: {context.heuristics.visual_density}")
    lines.append(f"LAYOUT_STYLE: {context.heuristics.layout_style}")
    lines.append(f"INDUSTRY_VIBE: {context.heuristics.industry_vibe}")
    lines.append("")

    # 5. EXTRACTED CONTENT (INTENT-BASED)
    lines.append("## 5. KEY CONTENT BLOCKS")
    
    value_props = [b.text for b in context.content if b.intent == "VALUE_PROPOSITION"]
    services = [b.text for b in context.content if b.intent == "SERVICE_DESCRIPTION"]
    
    lines.append("--- VALUE PROPOSITIONS (HERO/HEADLINES) ---")
    for vp in value_props[:3]: # Limit to top 3
        lines.append(f"> {vp}")
    
    lines.append("\n--- SERVICES / KEY FEATURES ---")
    for s in services[:6]: # Limit to top 6
        lines.append(f"* {s}")

    lines.append("\n--- IMAGE ASSETS (CANDIDATES) ---")
    # (Optional: Add scraped image list here if needed, keeping it clean for now)
    
    return "\n".join(lines)

def main():
    if len(sys.argv) < 2:
        print("Usage: python scraper_cursor.py <ClientName> <URL>")
        # Fallback for interactive testing
        client = input("Client Name: ")
        url = input("URL: ")
        if not url: return
    else:
        client = sys.argv[1]
        url = sys.argv[2]

    engine = ScraperEngine(url, client)
    context = engine.scrape()

    if context:
        output_text = generate_context_file(context)
        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            f.write(output_text)
        print(f"\n✅ Context file generated at: {OUTPUT_FILE}")
        
        # Print preview
        print("\n--- PREVIEW ---")
        print(output_text[:500] + "...\n(see file for full content)")

if __name__ == "__main__":
    main()