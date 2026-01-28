import json
import re
import time
import sys
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, asdict, field

from bs4 import BeautifulSoup, Tag, Comment
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
OUTPUT_JSON_FILE = "extraction_output.json"
OUTPUT_CONTEXT_FILE = "contexto_para_cursor.txt"
OUTPUT_CLEAN_HTML_FILE = "clean_source.html" # New file for inspection
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(CURRENT_DIR)
CONTEXT_FILE_PATH = os.path.join(PROJECT_ROOT, "contexto_para_cursor.txt")
CLEAN_HTML_PATH = os.path.join(CURRENT_DIR, OUTPUT_CLEAN_HTML_FILE)

# --- DATA STRUCTURES (Mirroring AppConfig.ts) ---

@dataclass
class LogoData:
    url: str = ""
    width: int = 200
    height: int = 50
    alt: str = "Logo"

@dataclass
class HeroData:
    title: str = ""
    highlight: str = ""
    description: str = ""
    button: str = ""
    secondaryButton: str = ""
    buttonLink: str = "#"
    image: str = ""

@dataclass
class TrustStat:
    value: str
    label: str

@dataclass
class TrustData:
    stats: List[TrustStat] = field(default_factory=list)

@dataclass
class ProblemData:
    title: str = ""
    description: str = ""
    items: List[str] = field(default_factory=list)

@dataclass
class SolutionCard:
    title: str
    description: str

@dataclass
class SolutionData:
    title: str = ""
    subtitle: str = ""
    cards: List[SolutionCard] = field(default_factory=list)

@dataclass
class HowItWorksStep:
    title: str
    description: str

@dataclass
class HowItWorksData:
    title: str = ""
    steps: List[HowItWorksStep] = field(default_factory=list)

@dataclass
class BenefitsData:
    title: str = ""
    items: List[str] = field(default_factory=list)

@dataclass
class Testimonial:
    name: str
    role: str
    text: str

@dataclass
class SocialProofData:
    title: str = ""
    testimonials: List[Testimonial] = field(default_factory=list)
    logos: List[str] = field(default_factory=list)

@dataclass
class FAQItem:
    q: str
    a: str

@dataclass
class FAQData:
    title: str = ""
    questions: List[FAQItem] = field(default_factory=list)

@dataclass
class CTAData:
    title: str = ""
    subtitle: str = ""
    button: str = ""
    link: str = "#"

@dataclass
class FooterLink:
    label: str
    link: str

@dataclass
class FooterData:
    company_name: str = ""
    description: str = ""
    contacts: List[str] = field(default_factory=list)
    links: List[FooterLink] = field(default_factory=list)

@dataclass
class FeatureItem:
    title: str
    description: str
    image: str
    imageAlt: str
    reverse: bool

@dataclass
class StructuralSection:
    tag: str
    headings: List[str]
    has_form: bool
    image_count: int
    card_count: int
    text_length: int

@dataclass
class StructuralMap:
    total_sections: int
    total_forms: int
    total_images: int
    total_navs: int
    total_footers: int
    sections: List[StructuralSection] = field(default_factory=list)

@dataclass
class AppConfigData:
    site_name: str = ""
    title: str = ""
    description: str = ""
    locale: str = "pt-br"
    logo: LogoData = field(default_factory=LogoData)
    hero: HeroData = field(default_factory=HeroData)
    trust: Optional[TrustData] = None
    problem: Optional[ProblemData] = None
    solution: Optional[SolutionData] = None
    howItWorks: Optional[HowItWorksData] = None
    benefits: Optional[BenefitsData] = None
    socialProof: Optional[SocialProofData] = None
    faq: Optional[FAQData] = None
    cta: Optional[CTAData] = None
    footer: FooterData = field(default_factory=FooterData)
    features: List[FeatureItem] = field(default_factory=list) 
    primaryColorCandidate: str = "" 
    structural_map: Optional[StructuralMap] = None # Added Structural Map

# --- UTILITIES ---

def clean_text(text: str) -> str:
    if not text: return ""
    return re.sub(r'\s+', ' ', text).strip()

def make_absolute_url(base_url: str, link: str) -> str:
    if not link: return ""
    if link.startswith('data:'): return link
    if link.startswith('http'): return link
    if link.startswith('//'): return 'https:' + link
    base = base_url.rstrip('/')
    if link.startswith('/'): return base + link
    return base + '/' + link

def normalize_url(url: str) -> str:
    url = url.strip()
    if not url.startswith('http'):
        return 'https://' + url
    return url

def rgb_to_hex(rgb_string: str) -> Optional[str]:
    if not rgb_string or 'rgba(0, 0, 0, 0)' in rgb_string or 'transparent' in rgb_string:
        return None
    match = re.search(r'rgba?\((\d+),\s*(\d+),\s*(\d+)', rgb_string)
    if match:
        r, g, b = map(int, match.groups())
        return '#{:02x}{:02x}{:02x}'.format(r, g, b)
    if rgb_string.startswith('#'):
        return rgb_string
    return None

def is_neutral_color(hex_color: str) -> bool:
    if not hex_color or not hex_color.startswith('#'): return True
    hex_color = hex_color.lstrip('#')
    if len(hex_color) == 3: hex_color = ''.join([c*2 for c in hex_color])
    try:
        r, g, b = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
    except ValueError: return True
    variance = max(r, g, b) - min(r, g, b)
    if variance < 20: return True 
    if hex_color.lower() in ['e0e0e0', 'f5f5f5', 'cccccc', 'd1d5db', '9ca3af', 'ffffff', '000000']: return True
    return False

# --- STRUCTURAL ANALYZER ---

class StructuralAnalyzer:
    def __init__(self, html_source: str):
        self.soup = BeautifulSoup(html_source, 'html.parser')
    
    def clean_dom(self) -> str:
        """Removes noise tags and returns clean HTML."""
        for tag in self.soup(["script", "style", "noscript", "iframe", "svg", "link", "meta"]):
            tag.decompose()
        
        # Remove comments
        for comment in self.soup.find_all(string=lambda text: isinstance(text, Comment)):
            comment.extract()
            
        return self.soup.prettify()

    def count_cards(self, container: Tag) -> int:
        """Heuristic: Count repeating children with similar structure."""
        children = container.find_all(recursive=False)
        if len(children) < 2: return 0
        
        # Simple check: do children have the same tag and similar class?
        # Or are they list items?
        count = 0
        prev_sig = None
        
        for child in children:
            if not isinstance(child, Tag): continue
            # Signature: Tag name + class length (rough proxy for structure)
            sig = (child.name, len(child.get("class", [])))
            if sig == prev_sig:
                count += 1
            prev_sig = sig
            
        return count if count > 1 else 0

    def generate_map(self) -> StructuralMap:
        sections_data = []
        
        # Identify main containers. Prioritize <section>, then top-level <div>s if no sections found
        containers = self.soup.find_all('section')
        if not containers:
            # Fallback: Look for divs that look like sections (direct children of body or main)
            main = self.soup.find('main')
            scope = main if main else self.soup.body
            if scope:
                containers = [c for c in scope.find_all('div', recursive=False) if isinstance(c, Tag)]

        for section in containers:
            # Headings
            headings = [clean_text(h.get_text())[:50] for h in section.find_all(re.compile('^h[1-4]$'))]
            
            # Form
            has_form = bool(section.find('form'))
            
            # Images
            img_count = len(section.find_all('img'))
            
            # Text Length (rough)
            text_len = len(clean_text(section.get_text()))
            
            # Repeated Cards
            # Look for inner containers (grid/flex) that might hold cards
            card_count = 0
            inner_divs = section.find_all('div')
            for div in inner_divs: # Check deeper divs
                cc = self.count_cards(div)
                if cc > card_count:
                    card_count = cc
            # Also check if the section itself is a list
            if section.name in ['ul', 'ol']:
                card_count = len(section.find_all('li'))

            sections_data.append(StructuralSection(
                tag=section.name,
                headings=headings,
                has_form=has_form,
                image_count=img_count,
                card_count=card_count,
                text_length=text_len
            ))

        return StructuralMap(
            total_sections=len(sections_data),
            total_forms=len(self.soup.find_all('form')),
            total_images=len(self.soup.find_all('img')),
            total_navs=len(self.soup.find_all('nav')),
            total_footers=len(self.soup.find_all('footer')),
            sections=sections_data
        )

# --- EXTRACTOR LOGIC ---

class WebScraper:
    def __init__(self):
        self.options = Options()
        self.options.add_argument("--headless=new")
        self.options.add_argument("--no-sandbox")
        self.options.add_argument("--disable-dev-shm-usage")
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
        self.driver = None

    def start_driver(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=self.options)

    def stop_driver(self):
        if self.driver:
            self.driver.quit()

    def fetch_page(self, url: str) -> str:
        if not self.driver:
            self.start_driver()
        print(f"🕵️ Fetching {url}...", file=sys.stderr)
        self.driver.get(url)
        time.sleep(3)
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)
        self.driver.execute_script("window.scrollTo(0, 0);")
        return self.driver.page_source

    def analyze_colors(self) -> str:
        candidates = {}
        selectors_high = ["a[href*='contact']", "button[type='submit']", ".btn-primary", ".button-primary"]
        selectors_med = ["nav a", "h1", "h2", "footer a"]

        def score_color(selector, weight):
            try:
                elements = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for el in elements[:5]:
                    if not el.is_displayed(): continue
                    bg = rgb_to_hex(el.value_of_css_property('background-color'))
                    fg = rgb_to_hex(el.value_of_css_property('color'))
                    for color in [bg, fg]:
                        if color and not is_neutral_color(color):
                            candidates[color] = candidates.get(color, 0) + weight
            except: pass

        for sel in selectors_high: score_color(sel, 3)
        for sel in selectors_med: score_color(sel, 1)

        if candidates:
            return max(candidates, key=candidates.get)
        return "#6366F1"

class ContentExtractor:
    def __init__(self, html: str, url: str, scraper: WebScraper):
        self.soup = BeautifulSoup(html, 'html.parser')
        self.url = url
        self.scraper = scraper
        self.raw_text = self.get_raw_text()

    def get_raw_text(self) -> str:
        # Clone soup to not destroy original
        clean_soup = BeautifulSoup(str(self.soup), 'html.parser')
        for script in clean_soup(["script", "style", "noscript", "iframe", "svg"]):
            script.extract()
        return clean_text(clean_soup.get_text())

    def extract_logo(self) -> LogoData:
        logo_url = ""
        # Improved heuristic: prioritizing header logos
        header = self.soup.find('header')
        candidates = []
        
        if header:
            candidates.extend(header.find_all("img"))
            
        candidates.extend(self.soup.find_all("img", {"class": re.compile(r'logo|brand', re.I)}))
        
        for img in candidates:
            src = img.get('src')
            if src and not any(x in src.lower() for x in ['icon', 'search', 'user', 'facebook', 'twitter']):
                logo_url = make_absolute_url(self.url, src)
                # If it's SVG or clearly named logo, stop
                if 'logo' in src.lower() or src.endswith('.svg'):
                    break
        
        return LogoData(url=logo_url, alt="Logo")

    def extract_hero(self) -> HeroData:
        hero = HeroData()
        # Look for Hero/Banner section explicitly
        hero_section = self.soup.find(lambda tag: tag.name in ['header', 'section', 'div'] and 
                                      any(c in (tag.get('class') or []) for c in ['hero', 'banner', 'intro']))
        
        scope = hero_section if hero_section else self.soup

        h1 = scope.find('h1')
        if h1:
            hero.title = clean_text(h1.get_text())
            p = h1.find_next('p')
            if p: hero.description = clean_text(p.get_text())
        
        # Image in hero
        img = scope.find("img")
        if img: 
            src = img.get('src', '')
            if 'logo' not in src.lower() and 'icon' not in src.lower():
                hero.image = make_absolute_url(self.url, src)
        
        # CTA
        btn = scope.find("a", string=re.compile(r'fale|contato|orçamento|começar', re.I))
        if btn:
            hero.button = clean_text(btn.get_text())
            hero.buttonLink = make_absolute_url(self.url, btn.get('href', '#'))
        else:
            hero.button = "Falar com Especialista"

        return hero

    def extract_trust_stats(self) -> Optional[TrustData]:
        # Improved: Structural validation
        # Looking for containers with Number + Text pairs
        stats = []
        
        # Regex for "Stat-like" strings: "+10", "100%", "500"
        num_pattern = re.compile(r'^(\+?\d+[\d\.,]*[kK%+]?)$')
        
        potential_stats = self.soup.find_all(string=num_pattern)
        
        for s in potential_stats:
            parent = s.parent
            # Check for label nearby (next sibling or parent's sibling)
            label = ""
            # Case 1: Label is next sibling element
            next_el = parent.find_next_sibling()
            if next_el and len(clean_text(next_el.get_text())) < 30:
                label = clean_text(next_el.get_text())
            # Case 2: Label is in same container but after
            elif parent.parent:
                text_content = clean_text(parent.parent.get_text())
                parts = text_content.split(s)
                if len(parts) > 1 and len(parts[1].strip()) < 30:
                    label = parts[1].strip()
            
            if label and len(label) > 2:
                stats.append(TrustStat(value=s.strip(), label=label))
        
        if len(stats) >= 2:
            return TrustData(stats=stats[:4])
        return None

    def extract_solution_cards(self) -> Optional[SolutionData]:
        # Structural check: Find a container with repeated children structure
        # (Title + Desc) x 3+
        
        possible_roots = self.soup.find_all(lambda tag: tag.name in ['div', 'section', 'ul'])
        
        best_candidate = None
        best_count = 0
        
        for root in possible_roots:
            # Check direct children or list items
            children = root.find_all(['li', 'div'], recursive=False)
            if len(children) < 3: continue
            
            valid_cards = []
            for child in children:
                # Does it have a header?
                h = child.find(re.compile('^h[3-6]$'))
                # Does it have a paragraph?
                p = child.find('p')
                
                if h and p:
                    title = clean_text(h.get_text())
                    desc = clean_text(p.get_text())
                    if 3 < len(title) < 50 and 10 < len(desc) < 200:
                        valid_cards.append(SolutionCard(title=title, description=desc))
            
            if len(valid_cards) > best_count:
                best_count = len(valid_cards)
                best_candidate = valid_cards
                
        if best_candidate and best_count >= 3:
            return SolutionData(
                title="Nossas Soluções",
                subtitle="O que oferecemos",
                cards=best_candidate[:6]
            )
        return None

    def extract_social_proof(self) -> Optional[SocialProofData]:
        # 1. Testimonials: Look for Quote structure
        testimonials = []
        quotes = self.soup.find_all('blockquote')
        for q in quotes:
            text = clean_text(q.get_text())
            # Try find author nearby
            author = "Cliente"
            footer = q.find('footer')
            if footer: author = clean_text(footer.get_text())
            else:
                # Check next sibling
                next_el = q.find_next_sibling()
                if next_el and len(clean_text(next_el.get_text())) < 30:
                    author = clean_text(next_el.get_text())
            
            if len(text) > 10:
                testimonials.append(Testimonial(name=author, role="Cliente", text=text))
                
        # 2. Logos: Look for "Strip" of images
        logos = []
        # Find containers with many images
        containers = self.soup.find_all(lambda tag: tag.name in ['div', 'section'] and len(tag.find_all('img')) >= 4)
        
        for cont in containers:
            # Check if keywords present in section text or class
            section_text = (cont.get('class') or []) + [cont.get_text()]
            if any(k in str(section_text).lower() for k in ['parceiros', 'clientes', 'partners', 'clients']):
                # This is likely a logo strip
                imgs = cont.find_all('img')
                for img in imgs:
                    src = make_absolute_url(self.url, img.get('src', ''))
                    if src: logos.append(src)
                break # Found one logo strip, stop
        
        if testimonials or logos:
            return SocialProofData(
                title="Quem confia em nós",
                testimonials=testimonials[:3],
                logos=logos[:8]
            )
        return None

    def extract_faq(self) -> Optional[FAQData]:
        # Look for Q&A pattern: Header + Hidden/Visible Text
        questions = []
        
        # Check for keywords
        faq_section = self.soup.find(lambda tag: tag.name in ['section', 'div'] and 
                                     any(k in clean_text(tag.get_text()).lower()[:50] for k in ['faq', 'perguntas', 'dúvidas']))
        
        if faq_section:
            # Try to find repeating pairs
            elements = faq_section.find_all(recursive=False)
            # Flatten if nested
            if len(elements) == 1: elements = elements[0].find_all(recursive=False)
            
            # Simple heuristic: Look for H tags followed by P/Div tags
            for i in range(len(elements) - 1):
                curr = elements[i]
                nxt = elements[i+1]
                
                # Identify Question
                is_q = curr.name in ['h3', 'h4', 'h5', 'dt', 'button'] or 'pergunta' in str(curr.get('class'))
                # Identify Answer
                is_a = nxt.name in ['p', 'div', 'dd'] or 'resposta' in str(nxt.get('class'))
                
                if is_q and is_a:
                    q_text = clean_text(curr.get_text())
                    a_text = clean_text(nxt.get_text())
                    if '?' in q_text and len(a_text) > 10:
                        questions.append(FAQItem(q=q_text, a=a_text))
                        
        if len(questions) >= 2:
            return FAQData(title="Perguntas Frequentes", questions=questions)
        return None

    def extract_how_it_works(self) -> Optional[HowItWorksData]:
        # Pattern: Ordered List or Numbered Steps
        steps = []
        
        # Check for <ol> first
        ols = self.soup.find_all('ol')
        for ol in ols:
            lis = ol.find_all('li')
            if len(lis) >= 3:
                for li in lis:
                    # Split title/desc if possible
                    txt = clean_text(li.get_text())
                    if len(txt) > 10:
                        parts = txt.split('.', 1)
                        title = parts[0] if len(parts) > 1 else f"Passo {len(steps)+1}"
                        desc = parts[1] if len(parts) > 1 else txt
                        steps.append(HowItWorksStep(title=title, description=desc))
                if steps: break
        
        # Fallback: Check for "1.", "2." text patterns in headers
        if not steps:
            headers = self.soup.find_all(re.compile('^h[3-5]$'), string=re.compile(r'^\d+\.'))
            for h in headers:
                title = clean_text(h.get_text())
                desc = ""
                p = h.find_next('p')
                if p: desc = clean_text(p.get_text())
                steps.append(HowItWorksStep(title=title, description=desc))

        if len(steps) >= 3:
            return HowItWorksData(title="Como Funciona", steps=steps)
        return None

    def extract_footer(self, company_name: str) -> FooterData:
        footer = FooterData(company_name=company_name)
        footer_el = self.soup.find('footer')
        if footer_el:
            # Extract emails
            emails = set(re.findall(r'[\w\.-]+@[\w\.-]+', footer_el.get_text()))
            phones = set(re.findall(r'\(?\d{2}\)?\s?\d{4,5}-?\d{4}', footer_el.get_text()))
            footer.contacts = list(emails) + list(phones)
            
            p = footer_el.find('p')
            if p: footer.description = clean_text(p.get_text())[:150]
            
            # Links
            for a in footer_el.find_all('a', href=True):
                txt = clean_text(a.get_text())
                if txt and len(txt) < 20:
                    footer.links.append(FooterLink(label=txt, link=make_absolute_url(self.url, a['href'])))
                    if len(footer.links) >= 6: break
        return footer

    # Problem/Benefits are harder to structurally detect without semantic understanding.
    # We will leave them as None (Disabled) unless specific keywords are extremely strong, 
    # effectively defaulting to a safer "don't show" policy to avoid hallucination.
    def extract_problem(self) -> Optional[ProblemData]: return None
    def extract_benefits(self) -> Optional[BenefitsData]: return None


def run_scraper(url: str, client_name: str = "Unknown"):
    scraper = WebScraper()
    try:
        html = scraper.fetch_page(url)
        
        # --- NEW STRUCTURAL LAYER ---
        struct_analyzer = StructuralAnalyzer(html)
        
        # 1. Clean HTML
        clean_html = struct_analyzer.clean_dom()
        
        # 2. Save Clean HTML
        with open(CLEAN_HTML_PATH, "w", encoding="utf-8") as f:
            f.write(clean_html)
        print(f"✅ Clean HTML saved to: {CLEAN_HTML_PATH}", file=sys.stderr)
        
        # 3. Generate Structural Map
        struct_map = struct_analyzer.generate_map()
        
        # --- EXISTING EXTRACTION LAYER ---
        # Pass the ALREADY CLEANED html to the ContentExtractor to avoid double cleaning
        extractor = ContentExtractor(clean_html, url, scraper)
        
        # --- EXECUTE EXTRACTORS ---
        logo = extractor.extract_logo()
        hero = extractor.extract_hero()
        trust = extractor.extract_trust_stats()
        solution = extractor.extract_solution_cards() # Replaces Services
        how_it_works = extractor.extract_how_it_works()
        social_proof = extractor.extract_social_proof()
        faq = extractor.extract_faq()
        footer = extractor.extract_footer(client_name)
        
        # Disabled for safety (require stronger signals)
        problem = extractor.extract_problem()
        benefits = extractor.extract_benefits()
        cta = None # Usually constructed generically

        # Primary Color Analysis
        primary_color = scraper.analyze_colors()

        # Build Config
        config = AppConfigData(
            site_name=client_name,
            title=f"{client_name} - {hero.title[:40]}...",
            description=hero.description[:160],
            logo=logo,
            hero=hero,
            trust=trust,
            problem=problem,
            solution=solution,
            howItWorks=how_it_works,
            benefits=benefits,
            socialProof=social_proof,
            faq=faq,
            cta=cta,
            footer=footer,
            primaryColorCandidate=primary_color,
            structural_map=struct_map # Include the map in output
        )

        # Output JSON
        json_str = json.dumps(asdict(config), indent=2, ensure_ascii=False)
        output_path = os.path.join(CURRENT_DIR, OUTPUT_JSON_FILE)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(json_str)
        print(f"✅ Data saved to: {output_path}", file=sys.stderr)

        # Context File
        context_content = f"""=== CONFIGURAÇÃO EXTRAÍDA ===
{json_str}

=== STRUCTURAL MAP ===
{json.dumps(asdict(struct_map), indent=2)}

=== TEXTO DO SITE ===
{extractor.raw_text[:5000]}
"""
        with open(CONTEXT_FILE_PATH, "w", encoding="utf-8") as f:
            f.write(context_content)
        print(f"✅ Contexto salvo em: {CONTEXT_FILE_PATH}", file=sys.stderr)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc()
    finally:
        scraper.stop_driver()

def main():
    if len(sys.argv) < 3:
        try:
            client = input("Client Name: ")
            url = input("URL: ")
            if url: run_scraper(normalize_url(url), client)
        except: pass
    else:
        run_scraper(normalize_url(sys.argv[2]), sys.argv[1])

if __name__ == "__main__":
    main()