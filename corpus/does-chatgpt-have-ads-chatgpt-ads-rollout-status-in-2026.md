---
title: Does ChatGPT Have Ads? ChatGPT Ads Rollout Status in 2026
source_url: https://cloro.dev/blog/chatgpt-ads-rollout/
company: openai-ecosystem
date: '2026-07-16'
evidence_tier: 4
language: en
track: ai_era_ads
full_text: complete
---

ChatGPT now carries paid ads. OpenAI shipped them in February 2026 at $60 CPM with a $200,000 minimum buy.

Five months in, the ad surface has cycled through a full turbulence loop and is now sitting at levels above the May spike in every lead market. Our original April-May measurement put ads in 0.42% of responses; the updated penetration study measured 26.5% on 2026-05-26 (49.1% US), a mid-June dip to under 1% (0.05% on 2026-06-14), then a re-ramp starting 2026-06-26 that stabilized at 51% US, 54% CA, 50% AU, and — new since May — 19% JP over the 7 days ending 2026-07-03. This post is the ChatGPT ads rollout summary: what shipped, what it costs, who’s buying, and what to watch for.

The short version: ads are real and now common across four English-speaking markets plus Japan, pricing keeps dropping, the buyer pool has fully rotated at least twice (May and July advertisers barely overlap), and OpenAI is clearly still tuning inventory throttles in real time.

## ChatGPT ads rollout timeline: how it launched

The ChatGPT ads rollout wasn’t really one launch. It was six months of monetization signals that gradually tightened into a product.

The gap between “ads ship” and “ads appear at meaningful rates” was about eight weeks. OpenAI built up advertiser inventory before turning on visibility, which is the opposite of the usual launch-with-a-splash playbook and the defining pattern of the ChatGPT ads rollout. The pricing also flipped from CPM to CPC inside the first quarter, which tells you the fixed-rate auction wasn’t clearing inventory.

The numbers behind the speed are loud. The Next Web reports OpenAI projecting $2.5 billion in 2026 ad revenue, $11 billion by 2027, and $100 billion by 2030. IntuitionLabs’ deck analysis puts advertising at $112 billion of non-subscription revenue from free-tier users over five years, with $46 billion in 2030 alone.

Worth pairing those numbers with an outside view. Evercore ISI’s Mark Mahaney published research in January 2026 projecting ChatGPT advertising as a $25 billion annual business by 2030, roughly a quarter of OpenAI’s internal number but still meaningful. The gap between the two forecasts is mostly about whether per-response ad rates climb toward Google’s classic SERP rate (1.05%) or stay in the lower 0.2-0.5% band measured so far.

## What ChatGPT ads look like today

A ChatGPT ad renders as a Sponsored card under the response sources. Brand name, icon, one-line headline, short body, deep link. No preroll, no banner, no sidebar display ad. The placement sits inside the answer flow.

Programmatically, ads show up in response.result.ads[] on the ChatGPT response. Each entry has a brand object (name, URL, favicon) and a cards[] array with the creative (image, title, body, URL). Creative assets are served from bzrcdn.openai.com . Destination URLs carry utm_source=chatgpt.com&utm_medium=src .

That UTM tagging is what cleanly identifies a paid placement. OpenAI applies it specifically to ads so advertisers can attribute conversions. Organic citations don’t carry it.

A few things that look like ads but aren’t:

- inlineProducts[] are multi-merchant product comparison rows from shopping queries. Commercial, but not paid.

- shoppingCards[] are single-merchant product cards. Also commercial, also not flagged as paid.

- The citation source links at the bottom of an answer are organic retrieval, not placements.

If you’re measuring ad penetration, count ads[] and only ads[] . We covered the other commercial surfaces separately in our ChatGPT shopping post.

## Pricing: from $60 CPM to $3-5 CPC in ten weeks

Pricing is the loudest signal in the ChatGPT ads rollout right now, and it has moved fast.

The February 2026 launch was $60 CPM with a $200,000 advertiser minimum, per ALM Corp’s pricing analysis . That minimum priced out most mid-market advertisers. At $60 CPM, $200K buys 3.3M impressions, which is a starter commitment for a Fortune 500 brand and a nonstarter for a startup with a $50K monthly ad budget.

By April 2026, OpenAI had moved to cost-per-click bidding. The Next Web put the effective CPM at $25, a 58% drop in three months. CPC bid ranges leaked to active advertisers:

The drop has a boring explanation. Demand at $60 CPM wasn’t deep enough to clear inventory at full price, so OpenAI let the auction discover the real rate.

Moving to CPC also shifted risk off the advertiser, since you only pay on clicks. That lets OpenAI serve more impressions per advertiser without inflating their cost. The $25 effective CPM under CPC is, for most advertisers, a better deal than $60 CPM under fixed billing.

The broader market is moving fast too. US AI search ad spend is projected to grow from $1 billion in 2025 to $25.9 billion by 2029, about 13.6% of all US search ad spending. Whether ChatGPT captures the dominant share or splits it with Google AI Overview is the question for the next 18 months.

## How often ads actually appear

Pricing matters less than penetration when you’re deciding whether ChatGPT is a real ad channel for your category. We’ve measured the ChatGPT ads rollout three times, and the story keeps moving.

Original April-May measurement. Across our 19-day monitoring window (2026-04-14 to 2026-05-02), 0.42% of ChatGPT responses carried at least one paid placement. Adthena’s parallel analysis on a different prompt mix clocked roughly 0.8% in the same window.

2026-05-26 spike. 26.5% of responses carried an ad overall, with 49.1% within the US. Canada 33.6%, Australia 19.8%, UK 1.5%, Japan 0%.

2026-07-03 plateau (trailing 7 days). US 51.0%, Canada 53.6%, Australia 49.8%, Japan 18.8%. Overall 12.2% (dragged down by DE/FR/BR/IL/AE at 0% making up ~two-thirds of the corpus). Between May 26 and July 3 the rate collapsed to 0.05% on 2026-06-14 before re-ramping.

ChatGPT’s US rate is roughly 49× Google’s classic SERP rate and ~200× Google’s in-AI-Overview rate. The original “ChatGPT looks close to equilibrium for AI-native ads around 0.2-0.5%” framing was wrong. The actual surface sits at ~50% in lead markets, has held at that level through a full ramp/throttle/re-ramp cycle, and has added Japan as a fourth ad-serving market.

The remaining open question in the ChatGPT ads rollout is where the next inflection lands. A fifth market lighting up (UK is the obvious candidate on English coverage alone, but is still at 0% after 372 responses in the trailing 7 days), a further US ramp toward 70%+, or another throttling episode are all consistent with what we’ve seen so far.

See the updated penetration study for the country and advertiser breakdowns and the full daily trend through the June cycle.

## Who is advertising on ChatGPT today

The story changed dramatically between measurements, and across the ChatGPT ads rollout the buyer pool has rotated more than once.

Original April-May window (16 distinct advertisers, 35 placements across 19 days): B2B SaaS dominated — Rippling (3), Semrush (3), HubSpot (2), CrowdStrike (2), 11x AI (2), Attio (2). Consumer and media filled the tail: Adobe Acrobat, Forbes, WSJ (2), McAfee, Lenovo, Shutterstock, Top10.com, Biom, Zapier, Pottery Barn.

2026-05-26 sample : order-of-magnitude wider advertiser pool. Consumer commerce dominated — e.l.f. Cosmetics, Pottery Barn, IKEA, Home Depot, Ralph Lauren, Macy’s. Affiliate aggregators heavy: Top10.com, BestMoney, Insurify, Capterra. Mid-market SaaS expanded: Cursor, Jotform, Monday.com, Datarails, Tapistro, Smith.ai. B2B enterprise (Expedia, Booking.com, Mastercard, ADP, Shopify) still present but no longer the headline.

2026-07-03 7-day sample : buyer pool has rotated again. The May 26 consumer-commerce leaders — e.l.f., Pottery Barn, IKEA, Ralph Lauren, Macy’s — don’t appear in the top 80. Only Top10.com survives from both April-May and May 26 as a top-tier advertiser. New shape:

- Japanese consumer/telco is a full-blown vertical: Carsensor (#1 overall at 131 placements), Onamae.com, U-NEXT, NURO 光, Audi Japan, Honda, SOMPO Direct, Duskin, ahamo, WECARS, HP Japan.

- Consumer commerce (US/CA/AU) : Amazon, Best Buy, Target, DSW, Home Depot, JCPenney, L.L.Bean, Samsung, Coterie Baby, iHerb, Faire, Hungryroot, Volcanica Coffee, ALO, PlantPaper, BISSELL, Chipolo, Babylist.

- Travel is now a discrete category: Booking.com (#2), Expedia (#13), Luxury Escapes (#17), Hilton.

- Telco/connectivity : AT&T, Xfinity, Optus, Boost Mobile, Visible by Verizon, ahamo, amaysim, Flip TV Australia.

- B2B SaaS : Monday.com, Zoho, ZoomInfo, Oracle, New Relic, Greenhouse, Crowdstrike, Oxylabs, Criteo (adtech buying inside ChatGPT), Lovable (rank 3 overall — displaces Cursor as the top vibecoding advertiser).

- Affiliate aggregators : Top10.com, Capterra, Expert Market, CompareGround.

The full top-80 list is in the penetration study update . One thing worth flagging: Profound , a competitor in AI brand visibility, dropped out of the sample entirely versus its confirmed presence in May.

The SaaS skew in the original April-May data was partly real and partly methodology. Software had (and still has) the highest published CPC bids ($8-18), so high-margin SaaS got the most value per placement. cloro’s prompt corpus also skews toward brand queries, comparisons, recommendations, and B2B-software topics, which inflates SaaS visibility versus a random sample. The corpus bias didn’t change between measurements; what changed is OpenAI expanding the active advertiser pool into consumer commerce and affiliate aggregators (May), then further into Japanese consumer/telco brands and adtech (July).

One pattern worth calling out: AI labs are buying paid placements on Google’s AI Overview SERPs. chatgpt.com, perplexity.ai, and claude.ai all showed up in Google’s classic sponsored slot on AI-Overview-triggering queries during the same window. Whatever the public story about AI engines competing with Google Search, the labs are paying Google to drive traffic from those queries. Tells you something about where commercial intent still lives.

## How users feel about it (so far)

User research is mixed but worth tracking. Verve Group findings from October 2025 showed consumers increasingly willing to accept advertising in exchange for free access to AI tools. At the same time, privacy concerns around AI data usage are rising in parallel.

IAB research from January 2026 surfaced Gen Z skepticism toward AI-delivered ads, even though that demographic is generally comfortable with AI as a technology. Privacy concerns appear to override the broader tech enthusiasm. OpenAI’s own beta-period reports claim no measurable negative impact on consumer trust metrics, which is the kind of statement worth verifying with independent measurement before you take it at face value.

OpenAI’s published ad policy frames the rollout around four principles: answer independence (advertisers can’t influence the conversational response itself), conversation privacy (advertisers don’t get access to chat content, history, or memories), choice and control, and exclusion of ads from “sensitive user contexts” like mental health, vulnerability, or distress signals. How rigorously those principles hold up under revenue pressure is the open question.

## What’s coming next

A few shifts that haven’t shipped yet but feel inevitable given the revenue OpenAI is chasing.

### A self-serve ChatGPT Ads Manager

The biggest gap right now is the lack of a self-serve dashboard. OpenAI sells direct through enterprise sales, which works fine at $200K commitments but won’t scale to the long tail of mid-market advertisers needed to hit the $2.5B 2026 number.

Self-serve solves that. It also changes the visibility math: ten thousand advertisers buying directly means more inventory per impression and likely a higher per-response ad rate. I’d expect a beta in 2026, probably opened first to existing OpenAI API customers since they’re the closest match for the buyer profile.

### Programmatic and audience targeting

The current product targets queries (category and keyword signals), not users (audience cohorts). That mirrors Google’s classic search ads model and avoids the privacy minefield of behavioral targeting inside an AI conversation.

The economic pressure to add audience signals will be real, though. ChatGPT knows a lot about its 900 million weekly active users: conversation history, professional context, product preferences. The product team has been careful with that data so far. Whether that holds up once the ad business needs to scale past category targeting is the open question, and the one I find most uncomfortable.

### Native ad formats inside the answer

Today’s ads[] placement is a Sponsored card, visually separate from the answer text. Conservative, clear, easy to disclose. The pressure to relax that separation will come from advertisers wanting better blend rates and OpenAI wanting higher click-through.

The grim version of this is sponsored mentions inside the answer text, formally disclosed but blurring the line. The product-safe version is richer cards: video creative, interactive carousels, comparison tables inside a Sponsored block. Either way, effective CPM goes up from $25.

## How to prepare

If you’re deciding whether to start spending on ChatGPT today, the honest version is: this far into the ChatGPT ads rollout, access still runs through OpenAI’s sales team with five- to six-figure minimums, and the buyer pool — while far wider than at launch — is still hundreds of brands, not a self-serve auction. It’s not a serious paid-acquisition channel for most companies yet.

What it is today is a brand visibility and category-defense play, and the urgency has held since May. With penetration at 51% US, 54% CA, 50% AU, and now 19% JP (over the 7 days ending 2026-07-03), a competitor buying placements on your priority queries can show up on roughly half of the responses you care about across the entire English-speaking market plus Japan. That’s not “lose category positioning over a year” anymore — it’s “lose category positioning this quarter.” And the buyer-pool rotation between May and July shows that “we’re not seeing them yet” doesn’t mean “we won’t see them next month.”

A few things are worth doing now regardless of whether you buy.

Audit whether your competitors are advertising. Run your top 50 category-defining queries through ChatGPT (or a monitoring tool) and check ads[] for competitor brands. If competitors are showing up where you aren’t, the category-defense math is worth pricing.

Monitor your own brand mentions across AI ad surfaces. Even if you never spend on ChatGPT, knowing where your brand shows up (organically, or in someone else’s ad copy) is the baseline that justifies every downstream decision. cloro’s AI brand visibility tracker covers that.

Track the pricing trajectory. $60 CPM ten weeks ago is $25 effective CPM today. If it keeps drifting toward $10-15, ChatGPT opens up to a much broader set of advertisers. A quarterly check on effective rate, category bid ranges, and self-serve availability is enough.

For the measurement side, how to detect programmatically when an ad has rendered, see the companion monitor ChatGPT ads guide. For the API surface itself — parsed ads[] array on every response with brand, creative, and country breakdowns — see the ChatGPT Ads API .

About the author

## Ricardo Batista

Founder, cloro

Ricardo is one of the founders and engineers behind its SERP and AI-search scraping infrastructure. Before cloro he scaled a financial comparison site to $7M ARR and ran the full-country operations of a unicorn to $65M ARR, then went back to building. He writes about search engine scraping, generative-engine optimization, and turning live search and AI-answer data into something teams can act on.

## Frequently asked questions

Yes, and the rate has cycled through a full turbulence loop. OpenAI launched paid ads in February 2026. Our original April-May measurement was 0.42%; 2026-05-26 spiked to 26.5% overall / 49.1% US; the rate then crashed back to under 1% by mid-June before re-spiking on 2026-06-26. Over the 7 days ending 2026-07-03, 51% of US responses, 54% Canadian, 50% Australian, and 19% Japanese responses carried a paid ad. See the penetration study for the full breakdown.

OpenAI launched ChatGPT ads in February 2026 at $60 CPM with a $200,000 minimum advertiser commitment. The first observed ads in cloro's monitoring corpus appeared on 2026-04-14, suggesting a gradual rollout to general visibility over the first two months.

Pricing has moved fast. The February launch was $60 CPM with a $200K minimum. Within ten weeks the effective CPM eroded to ~$25, and OpenAI shifted to cost-per-click bidding. Current bids run $3-5 generally, $8-18 for software and finance categories, and $3-5 for ecommerce and retail.

They already did, then dipped, then came back. As of the 7 days ending 2026-07-03, ChatGPT ads sit at 51% of US responses (roughly 49× Google's classic SERP rate of 1.05% and ~200× Google's in-AI-Overview rate of 0.24%). Between the May 26 spike and the July 3 plateau the rate collapsed to 0.05% on 2026-06-14 before re-ramping. The current level looks structural, not transient — the question is whether the next inflection is a further ramp, another dip, or a new geographic expansion.

The current advertiser pool spans consumer commerce (Amazon, Best Buy, Target, DSW, Home Depot, JCPenney, L.L.Bean, Samsung, Hilton, iHerb), travel (Booking.com, Expedia, Luxury Escapes), telco/connectivity (AT&T, Xfinity, Optus, Boost Mobile, Visible by Verizon, ahamo), B2B SaaS (Monday.com, Zoho, ZoomInfo, Oracle, New Relic, Greenhouse, Crowdstrike, Oxylabs, Criteo, Lovable), affiliate aggregators (Top10.com, Capterra, Expert Market, CompareGround), and a heavy new Japanese layer (Carsensor, U-NEXT, Honda, Audi Japan, NURO 光, SOMPO Direct, Duskin, WECARS).

Not yet. As of July 2026, ChatGPT ads are sold direct through OpenAI's sales team with category-specific bid ranges. A self-serve dashboard hasn't shipped. Our read of OpenAI's revenue trajectory ($2.5B projected for 2026, $100B by 2030 per The Next Web) makes a self-serve product almost certain, but the timeline isn't public.

## Related reading

## ChatGPT ads penetration study: 51% in the US, and Japan just lit up (July 2026 update)

ChatGPT ads over the last 7 days measure 51.0% of US responses, 53.6% CA, 49.8% AU, and — new since May — 18.8% JP. Everywhere else remains near zero. The surface reverted then re-spiked in June and now looks structural, not transient.

## Google Ads Transparency vs SERP Ads: Which to Use When

The Google Ads Transparency Center is a public historical ad archive; live SERP ads are real-time sponsored results. Different products — which to use when.

## ChatGPT Shopping: How Product Discovery Works

ChatGPT Shopping turns product research into a conversation. See how product cards, reviews, schema, and feeds affect AI product discovery in 2026.
