# [Simon Willison’s Weblog](/)

[Subscribe](https://simonwillison.net/2026/Feb/19/gemini-31-pro/about/#subscribe) 

**Sponsored by:** [WorkOS](https://fandf.co/4v8pTAt) — Production-ready APIs for auth and access control, so you can ship faster.

19th February 2026 - Link Blog

**[Gemini 3.1 Pro](https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/)**. The first in the Gemini 3.1 series, priced the same as Gemini 3 Pro ($2/million input, $12/million output under 200,000 tokens, $4/$18 for 200,000 to 1,000,000). That's less than half the price of Claude Opus 4.6 with very similar benchmark scores to that model.

They boast about its improved SVG animation performance compared to Gemini 3 Pro in the announcement!

I tried "Generate an SVG of a pelican riding a bicycle" [in Google AI Studio](https://aistudio.google.com/app/prompts?state=%7B%22ids%22:%5B%221ugF9fBfLGxnNoe8%5FrLlluzo9NSPJDWuF%22%5D,%22action%22:%22open%22,%22userId%22:%22106366615678321494423%22,%22resourceKeys%22:%7B%7D%7D&usp=sharing) and it thought for 323.9 seconds ([thinking trace here](https://gist.github.com/simonw/03a755865021739a3659943a22c125ba#thinking-trace)) before producing this one:

![Whimsical flat-style illustration of a pelican wearing a blue and white baseball cap, riding a red bicycle with yellow-rimmed wheels along a road. The pelican has a large orange bill and a green scarf. A small fish peeks out of a brown basket on the handlebars. The background features a light blue sky with a yellow sun, white clouds, and green hills.](https://static.simonwillison.net/static/2026/gemini-3.1-pro-pelican.png)

It's good to see the legs clearly depicted on both sides of the frame (should [satisfy Elon](https://twitter.com/elonmusk/status/2023833496804839808)), the fish in the basket is a nice touch and I appreciated this comment in [the SVG code](https://gist.github.com/simonw/03a755865021739a3659943a22c125ba#response):

```
<!-- Black Flight Feathers on Wing Tip -->
<path d="M 420 175 C 440 182, 460 187, 470 190 C 450 210, 430 208, 410 198 Z" fill="#374151" />

```

I've [added](https://github.com/simonw/llm-gemini/issues/121) the two new model IDs `gemini-3.1-pro-preview` and `gemini-3.1-pro-preview-customtools` to my [llm-gemini plugin](https://github.com/simonw/llm-gemini) for [LLM](https://llm.datasette.io/). That "custom tools" one is [described here](https://ai.google.dev/gemini-api/docs/models/gemini-3.1-pro-preview#gemini-31-pro-preview-customtools) \- apparently it may provide better tool performance than the default model in some situations.

The model appears to be _incredibly_ slow right now - it took 104s to respond to a simple "hi" and a few of my other tests met "Error: This model is currently experiencing high demand. Spikes in demand are usually temporary. Please try again later." or "Error: Deadline expired before operation could complete" errors. I'm assuming that's just teething problems on launch day.

It sounds like last week's [Deep Think release](https://simonwillison.net/2026/Feb/12/gemini-3-deep-think/) was our first exposure to the 3.1 family:

> Last week, we released a major update to Gemini 3 Deep Think to solve modern challenges across science, research and engineering. Today, we’re releasing the upgraded core intelligence that makes those breakthroughs possible: Gemini 3.1 Pro.

**Update**: In [What happens if AI labs train for pelicans riding bicycles?](https://simonwillison.net/2025/nov/13/training-for-pelicans-riding-bicycles/) last November I said:

> If a model finally comes out that produces an excellent SVG of a pelican riding a bicycle you can bet I’m going to test it on all manner of creatures riding all sorts of transportation devices.

Google's Gemini Lead Jeff Dean [tweeted this video](https://x.com/JeffDean/status/2024525132266688757) featuring an animated pelican riding a bicycle, plus a frog on a penny-farthing and a giraffe driving a tiny car and an ostrich on roller skates and a turtle kickflipping a skateboard and a dachshund driving a stretch limousine.

I've been saying for a while that I wish AI labs would highlight things that their new models can do that their older models could not, so top marks to the Gemini team for this video.

**Update 2**: I used `llm-gemini` to run my [more detailed Pelican prompt](https://simonwillison.net/2025/Nov/18/gemini-3/#and-a-new-pelican-benchmark), with [this result](https://gist.github.com/simonw/a3bdd4ec9476ba9e9ba7aa61b46d8296):

![Flat-style illustration of a brown pelican riding a teal bicycle with dark blue-rimmed wheels against a plain white background. Unlike the previous image's white cartoon pelican, this pelican has realistic brown plumage with detailed feather patterns, a dark maroon head, yellow eye, and a large pink-tinged pouch bill. The bicycle is a simpler design without a basket, and the scene lacks the colorful background elements like the sun, clouds, road, hills, cap, and scarf from the first illustration, giving it a more minimalist feel.](https://static.simonwillison.net/static/2026/gemini-3.1-pro-pelican-2.png)

From the SVG comments:

```
<!-- Pouch Gradient (Breeding Plumage: Red to Olive/Green) -->
...
<!-- Neck Gradient (Breeding Plumage: Chestnut Nape, White/Yellow Front) -->

```

Posted [19th February 2026](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2026/Feb/19/) at 5:58 pm

## Recent articles

* [The Axios supply chain attack used individually targeted social engineering](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2026/Apr/3/supply-chain-social-engineering/) \- 3rd April 2026
* [Highlights from my conversation about agentic engineering on Lenny's Podcast](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2026/Apr/2/lennys-podcast/) \- 2nd April 2026
* [Mr. Chatterbox is a (weak) Victorian-era ethically trained model you can run on your own computer](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2026/Mar/30/mr-chatterbox/) \- 30th March 2026

This is a **link post** by Simon Willison, posted on [19th February 2026](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2026/Feb/19/).

[ google400 ](https://simonwillison.net/2026/Feb/19/gemini-31-pro/tags/google/) [ svg52 ](https://simonwillison.net/2026/Feb/19/gemini-31-pro/tags/svg/) [ ai1947 ](https://simonwillison.net/2026/Feb/19/gemini-31-pro/tags/ai/) [ generative-ai1728 ](https://simonwillison.net/2026/Feb/19/gemini-31-pro/tags/generative-ai/) [ llms1695 ](https://simonwillison.net/2026/Feb/19/gemini-31-pro/tags/llms/) [ llm584 ](https://simonwillison.net/2026/Feb/19/gemini-31-pro/tags/llm/) [ gemini181 ](https://simonwillison.net/2026/Feb/19/gemini-31-pro/tags/gemini/) [ pelican-riding-a-bicycle102 ](https://simonwillison.net/2026/Feb/19/gemini-31-pro/tags/pelican-riding-a-bicycle/) [ llm-release186 ](https://simonwillison.net/2026/Feb/19/gemini-31-pro/tags/llm-release/) 

###  Monthly briefing

 Sponsor me for **$10/month** and get a curated email digest of the month's most important LLM developments.

 Pay me to send you less!

[ Sponsor & subscribe](https://github.com/sponsors/simonw/) 

* [Disclosures](https://simonwillison.net/2026/Feb/19/gemini-31-pro/about/#disclosures)
* [Colophon](https://simonwillison.net/2026/Feb/19/gemini-31-pro/about/#about-site)
* ©
* [2002](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2002/)
* [2003](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2003/)
* [2004](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2004/)
* [2005](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2005/)
* [2006](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2006/)
* [2007](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2007/)
* [2008](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2008/)
* [2009](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2009/)
* [2010](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2010/)
* [2011](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2011/)
* [2012](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2012/)
* [2013](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2013/)
* [2014](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2014/)
* [2015](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2015/)
* [2016](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2016/)
* [2017](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2017/)
* [2018](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2018/)
* [2019](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2019/)
* [2020](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2020/)
* [2021](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2021/)
* [2022](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2022/)
* [2023](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2023/)
* [2024](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2024/)
* [2025](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2025/)
* [2026](https://simonwillison.net/2026/Feb/19/gemini-31-pro/2026/)