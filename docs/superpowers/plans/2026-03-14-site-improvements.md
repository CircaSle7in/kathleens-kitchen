# Kathleen's Kitchen Site Improvements — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Improve the Kathleen's Kitchen website with quick wins (SEO, pricing, nav CTA, image performance), medium effort features (testimonials, special occasions section, expanded How It Works), and new additions (FAQ section, custom inquiry form, image lazy loading).

**Architecture:** All changes are to the single `index.html` file (inline CSS + HTML + JS). No build system. New FAQ page is a standalone `faq.html`. Custom inquiry form uses Formspree or similar serverless form handler. Images are converted to WebP with PNG fallbacks. LocalBusiness schema is JSON-LD in the `<head>`.

**Tech Stack:** HTML/CSS/JS (vanilla, no framework), Vercel hosting, Square checkout API, Google Fonts (Great Vibes, Cormorant Garamond, Work Sans)

---

## Chunk 1: Quick Wins

### Task 1: Add prices to product showcase cards

**Files:**
- Modify: `index.html:1588-1695` (showcase items HTML)
- Modify: `index.html:725-765` (showcase CSS)

The showcase section has 12 product cards with no prices. Add a price element to each card matching the prices from the order form.

- [ ] **Step 1: Add price CSS**

In the `<style>` block, after `.showcase-tag` styles (around line 740), add:

```css
.showcase-price {
    font-family: 'Work Sans', sans-serif;
    font-size: 0.78rem;
    font-weight: 500;
    color: var(--pink-dark);
    margin-top: 0.3rem;
}
```

- [ ] **Step 2: Add price to each showcase item**

Add a `<div class="showcase-price">` inside each `.showcase-info` div, after `.showcase-tag`. Prices from the order form:

| Product | Price |
|---------|-------|
| Grandma's Dinner Rolls | $22/doz |
| Cinnamon Rolls | $24/6-pack |
| Cheese Rolls | $25/doz |
| Crescent Rolls | $22/doz |
| Mom's Wheat Bread | $10/loaf |
| Soft French Bread | $8/loaf |
| Cookie Dough Brownies | $20/dozen |
| Peanut Butter Bars | $18/dozen |
| Lemon Bars | $18/dozen |
| Caramel Rice Krispie Treats | $15/dozen |
| Chocolate Dipped Strawberries | $22/dozen |
| Chocolate Dipped Grapes | $18/container |

Example for first item:
```html
<div class="showcase-info">
    <div class="showcase-name">Grandma's Dinner Rolls</div>
    <div class="showcase-tag">Rolls</div>
    <div class="showcase-price">$22/doz</div>
    <div class="showcase-expand">tap for details</div>
</div>
```

- [ ] **Step 3: Verify prices are visible on cards and don't break expanded state**

Open `index.html` in browser, check each card shows price, click to expand and verify layout still works.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat: add prices to product showcase cards"
```

---

### Task 2: Add sticky "Order Now" button in nav

**Files:**
- Modify: `index.html:1268-1279` (nav HTML)
- Modify: `index.html` nav CSS section (around line 60-120)

There's already a floating order button (`#floatingOrderBtn`) at the bottom-right. The nav needs a persistent CTA that's always visible, especially on mobile where the menu is hidden behind a hamburger.

- [ ] **Step 1: Add Order Now button to nav HTML**

After the `<button class="nav-toggle">` element (line 1278), add:

```html
<a href="#order" class="nav-order-btn">Order Now</a>
```

- [ ] **Step 2: Add nav order button CSS**

In the nav CSS section (after `.nav-toggle` styles), add:

```css
.nav-order-btn {
    font-family: 'Work Sans', sans-serif;
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 0.6rem 1.4rem;
    background: var(--pink);
    color: white;
    text-decoration: none;
    transition: background 0.3s;
}
.nav-order-btn:hover {
    background: var(--pink-dark);
}
```

In the mobile media query (around line 1080), ensure the button is visible even when nav is collapsed:

```css
@media (max-width: 768px) {
    .nav-order-btn {
        position: absolute;
        right: 60px;
        top: 50%;
        transform: translateY(-50%);
        font-size: 0.6rem;
        padding: 0.5rem 1rem;
    }
}
```

- [ ] **Step 3: Verify on desktop and mobile widths**

Check that the Order Now button appears in the nav bar on both desktop and mobile. On mobile it should be visible next to the hamburger, not hidden inside the menu.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat: add persistent Order Now button to nav"
```

---

### Task 3: Add LocalBusiness structured data (JSON-LD)

**Files:**
- Modify: `index.html:6-28` (head section)

Add JSON-LD schema markup to help Google understand this is a local bakery business.

- [ ] **Step 1: Add JSON-LD script block**

After the Twitter Card meta tags (after line 23), add:

```html
<!-- Structured Data -->
<script type="application/ld+json">
{
    "@context": "https://schema.org",
    "@type": "HomeBasedBusiness",
    "name": "Kathleen's Kitchen",
    "description": "Homemade breads and sweet treats baked fresh in Sandy, Utah.",
    "url": "https://kathleens.kitchen",
    "image": "https://kathleens.kitchen/images/hero-bakery-spread.png",
    "address": {
        "@type": "PostalAddress",
        "addressLocality": "Sandy",
        "addressRegion": "UT",
        "addressCountry": "US"
    },
    "geo": {
        "@type": "GeoCoordinates",
        "latitude": 40.5649,
        "longitude": -111.8590
    },
    "priceRange": "$",
    "servesCuisine": ["Bakery", "Breads", "Desserts"],
    "sameAs": [
        "https://instagram.com/kathleens.kitchen.ut"
    ],
    "contactPoint": {
        "@type": "ContactPoint",
        "email": "kathleens.kitchen.ut@gmail.com",
        "contactType": "customer service"
    }
}
</script>
```

- [ ] **Step 2: Validate with Google's Rich Results Test**

Copy the JSON-LD and paste into https://search.google.com/test/rich-results to verify it's valid.

- [ ] **Step 3: Commit**

```bash
git add index.html
git commit -m "feat: add LocalBusiness JSON-LD structured data"
```

---

### Task 4: Convert product images to WebP with lazy loading

**Files:**
- Modify: `images/` directory (create WebP versions)
- Modify: `index.html` (all `<img>` tags and CSS `background-image` references)

Convert the PNG product photos to WebP for ~50-70% file size reduction. Add `loading="lazy"` to all images below the fold. Keep the hero image as preloaded PNG.

- [ ] **Step 1: Convert PNGs to WebP**

```bash
cd images
for f in *.png; do
    # Skip hero image (stays as preloaded PNG)
    if [ "$f" = "hero-bakery-spread.png" ]; then continue; fi
    cwebp -q 85 "$f" -o "${f%.png}.webp"
done
ls -la *.webp
```

If `cwebp` is not installed: `brew install webp`

- [ ] **Step 2: Update showcase items to use WebP with PNG fallback**

The showcase items use CSS `background-image`. Update each to prefer WebP:

```css
/* Add at top of showcase CSS */
.showcase-icon.has-image {
    background-size: cover;
    background-position: center;
}
```

For each showcase item, change the inline style from:
```html
style="background-image: url('images/grandmas-rolls.png')"
```
to:
```html
style="background-image: url('images/grandmas-rolls.webp')"
```

Do this for all 12 showcase items and the about-image background.

- [ ] **Step 3: Add lazy loading to images below the fold**

The QR code images in the order form and any `<img>` tags below the hero should get `loading="lazy"`. The showcase items use CSS backgrounds (not `<img>` tags), so they don't need this attribute.

For any `<img>` tags in the events section or order section, add:
```html
loading="lazy"
```

- [ ] **Step 4: Verify images load correctly**

Open the site in browser, scroll through all sections. Check DevTools Network tab to confirm WebP images are loading. Check that lazy-loaded images appear when scrolled into view.

- [ ] **Step 5: Commit**

```bash
git add images/*.webp index.html
git commit -m "perf: convert images to WebP and add lazy loading"
```

---

## Chunk 2: Medium Effort Features

### Task 5: Add testimonials/social proof section

**Files:**
- Modify: `index.html` (add section HTML after About section, around line 1353)
- Modify: `index.html` (add testimonials CSS in style block)

Add a section between About and Events with 3-4 customer testimonials. Use a clean card layout consistent with the site's aesthetic.

- [ ] **Step 1: Add testimonials CSS**

In the `<style>` block, after the about section styles, add:

```css
/* ═══════════════════════════════════════════
   TESTIMONIALS
   ═══════════════════════════════════════════ */
.testimonials {
    background: var(--pink-pale);
    padding: 5rem 2rem;
}
.testimonial-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
    gap: 2rem;
    max-width: 1000px;
    margin: 0 auto;
}
.testimonial-card {
    background: white;
    padding: 2rem;
    border: 1px solid var(--border);
    position: relative;
}
.testimonial-card::before {
    content: '\201C';
    font-family: 'Cormorant Garamond', serif;
    font-size: 4rem;
    color: var(--pink-light);
    position: absolute;
    top: 0.5rem;
    left: 1rem;
    line-height: 1;
}
.testimonial-text {
    font-family: 'Work Sans', sans-serif;
    font-size: 0.9rem;
    font-weight: 300;
    color: var(--charcoal);
    line-height: 1.7;
    margin-bottom: 1rem;
    padding-top: 1.5rem;
}
.testimonial-author {
    font-family: 'Cormorant Garamond', serif;
    font-weight: 600;
    font-size: 0.95rem;
    color: var(--pink-dark);
}
.testimonial-context {
    font-size: 0.75rem;
    color: var(--taupe);
    margin-top: 0.2rem;
}
```

- [ ] **Step 2: Add testimonials HTML**

After the About section closing `</section>` tag (line 1353), before the wave divider, add:

```html
<!-- ═══════════════════════════════════════════
     TESTIMONIALS
     ═══════════════════════════════════════════ -->
<section class="testimonials section">
    <div class="section-wide">
        <div class="section-header fade-in">
            <div class="section-label">Kind Words</div>
            <h2 class="section-title">What People Are Saying</h2>
            <div class="section-divider"></div>
        </div>
        <div class="testimonial-grid fade-in">
            <div class="testimonial-card">
                <div class="testimonial-text">The cinnamon rolls were absolutely incredible. My whole family fought over the last one. We'll be ordering these for every holiday from now on!</div>
                <div class="testimonial-author">Sarah M.</div>
                <div class="testimonial-context">Easter Brunch Order</div>
            </div>
            <div class="testimonial-card">
                <div class="testimonial-text">Kathleen's dinner rolls taste exactly like the ones my grandmother used to make. They brought tears to my eyes. Thank you for sharing this gift.</div>
                <div class="testimonial-author">Jennifer R.</div>
                <div class="testimonial-context">Thanksgiving Order</div>
            </div>
            <div class="testimonial-card">
                <div class="testimonial-text">I ordered the cookie dough brownies for a work event and they were gone in minutes. Everyone wanted to know where they came from!</div>
                <div class="testimonial-author">David L.</div>
                <div class="testimonial-context">Office Event</div>
            </div>
        </div>
    </div>
</section>
```

**Note:** These are placeholder testimonials. Replace with real customer quotes as they come in. Mom mentioned people are reaching out — collect those messages!

- [ ] **Step 3: Verify section renders between About and Events**

Open in browser, scroll past About, verify testimonials appear with the right styling before the wave divider and Events section.

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat: add testimonials section with customer quotes"
```

---

### Task 6: Add "Special Occasions" callout section

**Files:**
- Modify: `index.html` (add section HTML after How It Works, before Order Form)
- Modify: `index.html` (add CSS)

Mom specifically asked to highlight special occasion orders. This section goes between How It Works and the Order Form, serving as both a callout and a soft lead into the custom inquiry form (Task 9).

- [ ] **Step 1: Add special occasions CSS**

```css
/* ═══════════════════════════════════════════
   SPECIAL OCCASIONS
   ═══════════════════════════════════════════ */
.special-occasions {
    background: linear-gradient(135deg, var(--purple-light) 0%, var(--pink-pale) 100%);
    padding: 5rem 2rem;
    text-align: center;
}
.special-occasions-content {
    max-width: 700px;
    margin: 0 auto;
}
.special-occasions h2 {
    font-family: 'Cormorant Garamond', serif;
    font-size: 2rem;
    font-weight: 500;
    color: var(--charcoal);
    margin-bottom: 0.5rem;
}
.special-occasions h2 span {
    font-family: 'Great Vibes', cursive;
    font-size: 2.5rem;
    color: var(--pink-dark);
}
.special-occasions p {
    font-family: 'Work Sans', sans-serif;
    font-weight: 300;
    color: var(--taupe);
    font-size: 0.95rem;
    line-height: 1.7;
    margin-bottom: 1.5rem;
}
.occasion-tags {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 0.8rem;
    margin: 1.5rem 0 2rem;
}
.occasion-tag {
    font-family: 'Work Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 400;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    padding: 0.5rem 1.2rem;
    background: white;
    color: var(--taupe);
    border: 1px solid var(--border);
}
```

- [ ] **Step 2: Add special occasions HTML**

After the How It Works section closing `</section>` (line 1728), add:

```html
<!-- ═══════════════════════════════════════════
     SPECIAL OCCASIONS
     ═══════════════════════════════════════════ -->
<section class="special-occasions section" id="special-occasions">
    <div class="special-occasions-content fade-in">
        <div class="section-label">Beyond the Events</div>
        <h2>Have a <span>Special Occasion</span>?</h2>
        <p>
            Whether it's a birthday, baby shower, family reunion, or just a Tuesday that deserves
            something homemade — I'd love to help make it special. Reach out and let's talk
            about what you're looking for.
        </p>
        <div class="occasion-tags">
            <span class="occasion-tag">Birthdays</span>
            <span class="occasion-tag">Baby Showers</span>
            <span class="occasion-tag">Holidays</span>
            <span class="occasion-tag">Family Reunions</span>
            <span class="occasion-tag">Teacher Gifts</span>
            <span class="occasion-tag">Neighbor Treats</span>
        </div>
        <a href="#custom-inquiry" class="btn btn-pink">Send a Custom Request</a>
    </div>
</section>
```

- [ ] **Step 3: Verify the section renders correctly**

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat: add special occasions callout section"
```

---

### Task 7: Expand "How It Works" with delivery/pickup details

**Files:**
- Modify: `index.html:1710-1727` (How It Works steps HTML)

The current 3 steps are too vague. Expand them with specific details about pickup/delivery and add a note about the Sandy, Utah area.

- [ ] **Step 1: Update the step descriptions**

Replace the existing step descriptions (lines 1710-1727):

```html
<div class="steps fade-in">
    <div class="step">
        <div class="step-number">1</div>
        <h4 class="step-title">Browse Events</h4>
        <p class="step-desc">Each event is a small-batch bake with limited spots. Pick the one that fits your occasion and browse the available items.</p>
    </div>
    <div class="step">
        <div class="step-number">2</div>
        <h4 class="step-title">Claim Your Spot</h4>
        <p class="step-desc">Select your items, choose quantities, and check out securely. You'll get a text from Kathleen to confirm your order.</p>
    </div>
    <div class="step">
        <div class="step-number">3</div>
        <h4 class="step-title">Pickup or Delivery</h4>
        <p class="step-desc">Pick up fresh-baked items in Sandy, Utah on the event date. Local delivery is available for an additional fee within the Sandy/Draper area.</p>
    </div>
</div>
```

- [ ] **Step 2: Commit**

```bash
git add index.html
git commit -m "feat: expand How It Works with pickup/delivery details"
```

---

## Chunk 3: New Features

### Task 8: Create FAQ page

**Files:**
- Create: `faq.html`
- Modify: `index.html` footer links (line 1913-1918)

Create a standalone FAQ page covering common questions. Style it consistently with the main site. Link to it from the footer.

- [ ] **Step 1: Create faq.html**

Create `faq.html` in the project root with the site's shared styles (head, nav, footer) and an accordion-style FAQ section. Include these questions:

1. **How do I place an order?** — Browse upcoming events, pick items, check out online. You'll get a text to confirm.
2. **Do you deliver?** — Pickup in Sandy, UT. Local delivery available in Sandy/Draper area for a small fee.
3. **How far in advance should I order?** — Each event has limited spots. Order as soon as the event goes live for best selection.
4. **Can I order for a special occasion outside of events?** — Yes! Use the custom inquiry form to tell us about your event and we'll work something out.
5. **What allergens are in your products?** — Most items contain wheat, dairy, eggs, and sugar. Specific allergen info available on request.
6. **Are you a licensed bakery?** — We operate as a Utah Cottage Food producer. Our kitchen is a home kitchen, not inspected by the Dept. of Agriculture, as permitted under Utah cottage food law.
7. **Can I freeze your baked goods?** — Yes! Rolls and breads freeze beautifully. Wrap tightly and freeze within 24 hours. Thaw at room temperature or warm in the oven.
8. **What forms of payment do you accept?** — We accept all major credit cards through our secure Square checkout.

Use an accordion pattern with the same CSS variables and fonts as the main site. Include the nav bar and footer for consistent navigation.

- [ ] **Step 2: Add FAQ link to footer**

In the footer Quick Links section (line 1913-1918), add:

```html
<li><a href="faq.html">FAQ</a></li>
```

- [ ] **Step 3: Add FAQ link to nav**

In the nav links (line 1270-1274), add before Contact:

```html
<li><a href="faq.html">FAQ</a></li>
```

- [ ] **Step 4: Verify FAQ page renders correctly and links work**

Open `faq.html` in browser, verify styling matches main site, test accordion open/close, verify nav links back to main site sections.

- [ ] **Step 5: Commit**

```bash
git add faq.html index.html
git commit -m "feat: add FAQ page with accordion layout"
```

---

### Task 9: Add custom inquiry form for special occasions

**Files:**
- Modify: `index.html` (add form section after Special Occasions callout from Task 6)
- Modify: `index.html` (add form CSS)

Add a simple contact form for custom/special occasion requests. Use Formspree (free tier, no backend needed) to handle submissions.

- [ ] **Step 1: Add custom inquiry form CSS**

```css
/* ═══════════════════════════════════════════
   CUSTOM INQUIRY FORM
   ═══════════════════════════════════════════ */
.custom-inquiry {
    padding: 5rem 2rem;
    background: var(--warm-white);
}
.inquiry-form {
    max-width: 600px;
    margin: 0 auto;
    background: white;
    padding: 2.5rem;
    border: 1px solid var(--border);
}
.inquiry-form .form-group {
    margin-bottom: 1.5rem;
}
.inquiry-form label {
    display: block;
    font-family: 'Work Sans', sans-serif;
    font-size: 0.75rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--taupe);
    margin-bottom: 0.5rem;
}
.inquiry-form input,
.inquiry-form textarea,
.inquiry-form select {
    width: 100%;
    padding: 0.8rem 0;
    font-family: 'Work Sans', sans-serif;
    font-size: 0.95rem;
    font-weight: 300;
    color: var(--charcoal);
    border: none;
    border-bottom: 1px solid var(--border);
    background: transparent;
    transition: border-color 0.3s;
}
.inquiry-form input:focus,
.inquiry-form textarea:focus,
.inquiry-form select:focus {
    outline: none;
    border-bottom-color: var(--pink);
}
.inquiry-form textarea {
    resize: vertical;
    min-height: 100px;
}
```

- [ ] **Step 2: Add custom inquiry form HTML**

After the Special Occasions section (from Task 6), add:

```html
<!-- ═══════════════════════════════════════════
     CUSTOM INQUIRY
     ═══════════════════════════════════════════ -->
<section class="custom-inquiry section" id="custom-inquiry">
    <div class="section-wide">
        <div class="section-header fade-in">
            <div class="section-label">Custom Orders</div>
            <h2 class="section-title">Send a Request</h2>
            <div class="section-divider"></div>
            <p class="section-desc">Tell me about your occasion and I'll get back to you within 24 hours.</p>
        </div>
        <form class="inquiry-form fade-in" action="https://formspree.io/f/YOUR_FORM_ID" method="POST">
            <div class="form-row">
                <div class="form-group">
                    <label for="inquiry-name">Your Name</label>
                    <input type="text" id="inquiry-name" name="name" required placeholder="First & Last">
                </div>
                <div class="form-group">
                    <label for="inquiry-contact">Phone or Email</label>
                    <input type="text" id="inquiry-contact" name="contact" required placeholder="Best way to reach you">
                </div>
            </div>
            <div class="form-group">
                <label for="inquiry-occasion">What's the Occasion?</label>
                <select id="inquiry-occasion" name="occasion">
                    <option value="">Select one...</option>
                    <option value="birthday">Birthday</option>
                    <option value="baby-shower">Baby Shower</option>
                    <option value="holiday">Holiday Gathering</option>
                    <option value="family-reunion">Family Reunion</option>
                    <option value="teacher-gift">Teacher / Neighbor Gift</option>
                    <option value="other">Other</option>
                </select>
            </div>
            <div class="form-group">
                <label for="inquiry-date">When Do You Need It?</label>
                <input type="date" id="inquiry-date" name="date">
            </div>
            <div class="form-group">
                <label for="inquiry-details">Tell Me More</label>
                <textarea id="inquiry-details" name="details" placeholder="How many people? Any specific items? Anything else I should know?"></textarea>
            </div>
            <input type="hidden" name="_subject" value="Custom Order Inquiry from kathleens.kitchen">
            <button type="submit" class="btn btn-pink" style="width: 100%;">Send Request</button>
        </form>
    </div>
</section>
```

**Note:** Replace `YOUR_FORM_ID` with a real Formspree form ID. Create one at formspree.io using `kathleens.kitchen.ut@gmail.com`.

- [ ] **Step 3: Verify form renders and submit redirects properly**

- [ ] **Step 4: Commit**

```bash
git add index.html
git commit -m "feat: add custom inquiry form for special occasions"
```

---

### Task 10: Improve hero CTA to reference next event

**Files:**
- Modify: `index.html:1306-1312` (hero content HTML)

The hero CTA is generic. Make it reference the next upcoming event to create urgency.

- [ ] **Step 1: Update hero content**

Replace the hero CTA area:

```html
<div class="hero-content">
    <div class="hero-badge">Sandy, Utah</div>
    <h1 class="hero-title">Kathleen's Kitchen</h1>
    <p class="hero-subtitle">Homemade Breads & Sweet Treats</p>
    <p class="hero-tagline">Baked with love for your family's table</p>
    <a href="#events" class="btn btn-pink">See Upcoming Events</a>
</div>
```

**Note:** When specific events are live, the tagline and CTA can be updated to reference them, e.g., "Now taking orders for Easter Weekend" and "Claim Your Spot — Apr 3". This should be manually updated when events change.

- [ ] **Step 2: Commit**

```bash
git add index.html
git commit -m "refine: update hero tagline and CTA copy"
```

---

### Task 11: Enhance footer with more info

**Files:**
- Modify: `index.html:1896-1935` (footer HTML)

Add FAQ link (if not done in Task 8), hours/availability note, and special occasions link.

- [ ] **Step 1: Update footer Get in Touch section**

Add to the "Get in Touch" footer column:

```html
<li><a href="#special-occasions">Special Occasion? Let's talk</a></li>
```

- [ ] **Step 2: Commit**

```bash
git add index.html
git commit -m "feat: enhance footer with special occasions and FAQ links"
```

---

## Implementation Order

Execute tasks in this order for clean, incremental progress:

1. **Task 3** — JSON-LD schema (smallest change, head only)
2. **Task 4** — WebP images + lazy loading (asset changes)
3. **Task 1** — Showcase prices (HTML additions)
4. **Task 2** — Nav order button (nav changes)
5. **Task 7** — How It Works expansion (content update)
6. **Task 5** — Testimonials section (new section)
7. **Task 6** — Special Occasions section (new section)
8. **Task 9** — Custom inquiry form (new section, depends on Task 6)
9. **Task 10** — Hero CTA refinement (content update)
10. **Task 11** — Footer enhancements (depends on Tasks 6, 8)
11. **Task 8** — FAQ page (new file, depends on nothing but link in Task 11)

Each task produces a working site at every commit point.
