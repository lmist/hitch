# [Simon Willison’s Weblog](/)

[Subscribe](https://simonwillison.net/2025/Jul/17/vibe-scraping/about/#subscribe) 

**Sponsored by:** [WorkOS](https://fandf.co/4v8pTAt) — Production-ready APIs for auth and access control, so you can ship faster.

## Vibe scraping and vibe coding a schedule app for Open Sauce 2025 entirely on my phone

17th July 2025

This morning, working entirely on my phone, I scraped a conference website and vibe coded up an alternative UI for interacting with the schedule using a combination of OpenAI Codex and Claude Artifacts.

This weekend is [Open Sauce 2025](https://opensauce.com/), the third edition of the Bay Area conference for YouTube creators in the science and engineering space. I have a couple of friends going and they were complaining that the official schedule was difficult to navigate on a phone—it’s not even linked from the homepage on mobile, and once you do find [the agenda](https://opensauce.com/agenda/) it isn’t particularly mobile-friendly.

We were out for coffee this morning so I only had my phone, but I decided to see if I could fix it anyway.

TLDR: Working entirely on my iPhone, using a combination of [OpenAI Codex](https://chatgpt.com/codex) in the ChatGPT mobile app and Claude Artifacts via the Claude app, I was able to scrape the full schedule and then build and deploy this: [tools.simonwillison.net/open-sauce-2025](https://tools.simonwillison.net/open-sauce-2025)

![Screenshot of a blue page, Open Sauce 2025, July 18-20 2025, Download Calendar ICS button, then Friday 18th and Saturday 18th and Sunday 20th pill buttons, Friday is selected, the Welcome to Open Sauce with William Osman event on the Industry Stage is visible.](https://static.simonwillison.net/static/2025/open-sauce-2025-card.jpg)

The site offers a faster loading and more useful agenda view, but more importantly it includes an option to “Download Calendar (ICS)” which allows mobile phone users (Android and iOS) to easily import the schedule events directly into their calendar app of choice.

Here are some detailed notes on how I built it.

#### Scraping the schedule [#](https://simonwillison.net/2025/Jul/17/vibe-scraping/2025/Jul/17/vibe-scraping/#scraping-the-schedule)

Step one was to get that schedule in a structured format. I don’t have good tools for viewing source on my iPhone, so I took a different approach to turning the schedule site into structured data.

My first thought was to screenshot the schedule on my phone and then dump the images into a vision LLM—but the schedule was long enough that I didn’t feel like scrolling through several different pages and stitching together dozens of images.

If I was working on a laptop I’d turn to scraping: I’d dig around in the site itself and figure out where the data came from, then write code to extract it out.

How could I do the same thing working on my phone?

I decided to use **OpenAI Codex**—the [hosted tool](https://simonwillison.net/2025/May/16/openai-codex/), not the confusingly named [CLI utility](https://simonwillison.net/2025/Apr/16/openai-codex/).

Codex recently [grew the ability](https://simonwillison.net/2025/Jun/3/codex-agent-internet-access/) to interact with the internet while attempting to resolve a task. I have a dedicated Codex “environment” configured against a GitHub repository that doesn’t do anything else, purely so I can run internet-enabled sessions there that can execute arbitrary network-enabled commands.

I started a new task there (using the Codex interface inside the ChatGPT iPhone app) and prompted:

> `Install playwright and use it to visit https://opensauce.com/agenda/ and grab the full details of all three day schedules from the tabs - Friday and Saturday and Sunday - then save and on Data in as much detail as possible in a JSON file and submit that as a PR`

Codex is frustrating in that you only get one shot: it can go away and work autonomously on a task for a long time, but while it’s working you can’t give it follow-up prompts. You can wait for it to finish entirely and then tell it to try again in a new session, but ideally the instructions you give it are enough for it to get to the finish state where it submits a pull request against your repo with the results.

I got lucky: my above prompt worked exactly as intended.

Codex churned for a _13 minutes_! I was sat chatting in a coffee shop, occasionally checking the logs to see what it was up to.

It tried a whole bunch of approaches, all involving running the Playwright Python library to interact with the site. You can see [the full transcript here](https://chatgpt.com/s/cd%5F687945dea5f48191892e0d73ebb45aa4). It includes notes like "_Looks like xxd isn’t installed. I’ll grab “vim-common” or “xxd” to fix it._".

Eventually it downloaded an enormous obfuscated chunk of JavaScript called [schedule-overview-main-1752724893152.js](https://opensauce.com/wp-content/uploads/2025/07/schedule-overview-main-1752724893152.js) (316KB) and then ran a complex sequence of grep, grep, sed, strings, xxd and dd commands against it to figure out the location of the raw schedule data in order to extract it out.

Here’s the eventual [extract\_schedule.py](https://github.com/simonw/.github/blob/f671bf57f7c20a4a7a5b0642837811e37c557499/extract%5Fschedule.py) Python script it wrote, which uses Playwright to save that `schedule-overview-main-1752724893152.js` file and then extracts the raw data using the following code (which calls Node.js inside Python, just so it can use the JavaScript `eval()` function):

node_script = (
    "const fs=require('fs');"
    f"const d=fs.readFileSync('{tmp_path}','utf8');"
    "const m=d.match(/var oo=(\\{.*?\\});/s);"
    "if(!m){throw new Error('not found');}"
    "const obj=eval('(' + m[1] + ')');"
    f"fs.writeFileSync('{OUTPUT_FILE}', JSON.stringify(obj, null, 2));"
)
subprocess.run(['node', '-e', node_script], check=True)

As instructed, it then filed [a PR against my repo](https://github.com/simonw/.github/pull/1). It included the Python Playwright script, but more importantly it also included that full extracted [schedule.json](https://github.com/simonw/.github/blob/f671bf57f7c20a4a7a5b0642837811e37c557499/schedule.json) file. That meant I now had the schedule data, with a `raw.githubusercontent.com` URL with open CORS headers that could be fetched by a web app!

#### Building the web app [#](https://simonwillison.net/2025/Jul/17/vibe-scraping/2025/Jul/17/vibe-scraping/#building-the-web-app)

Now that I had the data, the next step was to build a web application to preview it and serve it up in a more useful format.

I decided I wanted two things: a nice mobile friendly interface for browsing the schedule, and mechanism for importing that schedule into a calendar application, such as Apple or Google Calendar.

It took me several false starts to get this to work. The biggest challenge was getting that 63KB of schedule JSON data into the app. I tried a few approaches here, all on my iPhone while sitting in coffee shop and later while driving with a friend to drop them off at the closest BART station.

1. Using ChatGPT Canvas and o3, since unlike Claude Artifacts a Canvas can fetch data from remote URLs if you allow-list that domain. I later found out that [this had worked](https://chatgpt.com/share/687948b7-e8b8-8006-a450-0c07bdfd7f85) when I viewed it on my laptop, but on my phone it threw errors so I gave up on it.
2. Uploading the JSON to Claude and telling it to build an artifact that read the file directly—this [failed with an error](https://claude.ai/share/25297074-37a9-4583-bc2f-630f6dea5c5d) “undefined is not an object (evaluating ’window.fs.readFile’)”. The Claude 4 system prompt [had lead me to expect this to work](https://simonwillison.net/2025/May/25/claude-4-system-prompt/#artifacts-the-missing-manual), I’m not sure why it didn’t.
3. Having Claude copy the full JSON into the artifact. This took too long—typing out 63KB of JSON is not a sensible use of LLM tokens, and it flaked out on me when my connection went intermittent driving through a tunnel.
4. Telling Claude to fetch from the URL to that schedule JSON instead. This was my last resort because the Claude Artifacts UI blocks access to external URLs, so you have to copy and paste the code out to a separate interface (on an iPhone, which still lacks a “select all” button) making for a frustrating process.

That final option worked! Here’s the full sequence of prompts I used with Claude to get to a working implementation—[full transcript here](https://claude.ai/share/e391bbcc-09a2-4f86-9bec-c6def8fc8dc9):

> `Use your analyst tool to read this JSON file and show me the top level keys`

This was to prime Claude—I wanted to remind it about its `window.fs.readFile` function and have it read enough of the JSON to understand the structure.

> `Build an artifact with no react that turns the schedule into a nice mobile friendly webpage - there are three days Friday, Saturday and Sunday, which corresponded to the 25th and 26th and 27th of July 2025`
> 
> `Don’t copy the raw JSON over to the artifact - use your fs function to read it instead`
> 
> `Also include a button to download ICS at the top of the page which downloads a ICS version of the schedule`

I had noticed that the schedule data had keys for “friday” and “saturday” and “sunday” but no indication of the dates, so I told it those. It turned out later I’d got these wrong!

This got me a version of the page that failed with an error, because that `fs.readFile()` couldn’t load the data from the artifact for some reason. So I fixed that with:

> `Change it so instead of using the readFile thing it fetches the same JSON from https://raw.githubusercontent.com/simonw/.github/f671bf57f7c20a4a7a5b0642837811e37c557499/schedule.json`

... then copied the HTML out to a Gist and previewed it with [gistpreview.github.io](https://gistpreview.github.io/)—here’s [that preview](https://gistpreview.github.io/?06a5d1f3bf0af81d55a411f32b2f37c7).

Then we spot-checked it, since there are _so many ways_ this could have gone wrong. Thankfully the schedule JSON itself never round-tripped through an LLM so we didn’t need to worry about hallucinated session details, but this was almost pure vibe coding so there was a big risk of a mistake sneaking through.

I’d set myself a deadline of “by the time we drop my friend at the BART station” and I hit that deadline with just seconds to spare. I pasted the resulting HTML [into my simonw/tools GitHub repo](https://github.com/simonw/tools/blob/main/open-sauce-2025.html) using the GitHub mobile web interface which deployed it to that final [tools.simonwillison.net/open-sauce-2025](https://tools.simonwillison.net/open-sauce-2025) URL.

... then we noticed that we _had_ missed a bug: I had given it the dates of “25th and 26th and 27th of July 2025” but actually that was a week too late, the correct dates were July 18th-20th.

Thankfully I have Codex configured against my `simonw/tools` repo as well, so fixing that was a case of prompting a new Codex session with:

> `The open sauce schedule got the dates wrong - Friday is 18 July 2025 and Saturday is 19 and Sunday is 20 - fix it`

Here’s [that Codex transcript](https://chatgpt.com/s/cd%5F68794c97a3d88191a2cbe9de78103334), which resulted in [this PR](https://github.com/simonw/tools/pull/34) which I landed and deployed, again using the GitHub mobile web interface.

#### What this all demonstrates [#](https://simonwillison.net/2025/Jul/17/vibe-scraping/2025/Jul/17/vibe-scraping/#what-this-all-demonstrates)

So, to recap: I was able to scrape a website (without even a view source too), turn the resulting JSON data into a mobile-friendly website, add an ICS export feature and deploy the results to a static hosting platform (GitHub Pages) working entirely on my phone.

If I’d had a laptop this project would have been faster, but honestly aside from a little bit more hands-on debugging I wouldn’t have gone about it in a particularly different way.

I was able to do other stuff at the same time—the Codex scraping project ran entirely autonomously, and the app build itself was more involved only because I had to work around the limitations of the tools I was using in terms of fetching data from external sources.

As usual with this stuff, my 25+ years of previous web development experience was critical to being able to execute the project. I knew about Codex, and Artifacts, and GitHub, and Playwright, and CORS headers, and Artifacts sandbox limitations, and the capabilities of ICS files on mobile phones.

This whole thing was _so much fun!_ Being able to spin up multiple coding agents directly from my phone and have them solve quite complex problems while only paying partial attention to the details is a solid demonstration of why I continue to enjoying exploring the edges of [AI-assisted programming](https://simonwillison.net/tags/ai-assisted-programming/).

#### Update: I removed the speaker avatars [#](https://simonwillison.net/2025/Jul/17/vibe-scraping/2025/Jul/17/vibe-scraping/#update-i-removed-the-speaker-avatars)

Here’s a beautiful cautionary tale about the dangers of vibe-coding on a phone with no access to performance profiling tools. A commenter on Hacker News [pointed out](https://news.ycombinator.com/item?id=44597405#44597808):

> The web app makes 176 requests and downloads 130 megabytes.

And yeah, it did! Turns out those speaker avatar images weren’t optimized, and there were over 170 of them.

I told [a fresh Codex instance](https://chatgpt.com/s/cd%5F6879631d99c48191b1ab7f84dfab8dea) “Remove the speaker avatar images from open-sauce-2025.html” and now the page weighs 93.58 KB—about 1,400 times smaller!

#### Update 2: Improved accessibility [#](https://simonwillison.net/2025/Jul/17/vibe-scraping/2025/Jul/17/vibe-scraping/#update-2-improved-accessibility)

That same commenter [on Hacker News](https://news.ycombinator.com/item?id=44597405#44597808):

> It’s also `<div>` soup and largely inaccessible.

Yeah, this HTML isn’t great:

dayContainer.innerHTML = sessions.map(session => `
    <div class="session-card">
        <div class="session-header">
            <div>
                <span class="session-time">${session.time}</span>
                <span class="length-badge">${session.length} min</span>
            </div>
            <div class="session-location">${session.where}</div>
        </div>

I [opened an issue](https://github.com/simonw/tools/issues/36) and had both Claude Code and Codex look at it. Claude Code [failed to submit a PR](https://github.com/simonw/tools/issues/36#issuecomment-3085516331) for some reason, but Codex [opened one](https://github.com/simonw/tools/pull/37) with a fix that sounded good to me when I tried it with VoiceOver on iOS (using [a Cloudflare Pages preview](https://codex-make-open-sauce-2025-h.tools-b1q.pages.dev/open-sauce-2025)) so I landed that. Here’s [the diff](https://github.com/simonw/tools/commit/29c8298363869bbd4b4e7c51378c20dc8ac30c39), which added a hidden “skip to content” link, some `aria-` attributes on buttons and upgraded the HTML to use `<h3>` for the session titles.

Next time I’ll remember to specify accessibility as a requirement in the initial prompt. I’m disappointed that Claude didn’t consider that without me having to ask.

Posted [17th July 2025](https://simonwillison.net/2025/Jul/17/vibe-scraping/2025/Jul/17/) at 7:38 pm · Follow me on [Mastodon](https://fedi.simonwillison.net/@simon), [Bluesky](https://bsky.app/profile/simonwillison.net), [Twitter](https://twitter.com/simonw) or [subscribe to my newsletter](https://simonwillison.net/about/#subscribe)

## More recent articles

* [The Axios supply chain attack used individually targeted social engineering](https://simonwillison.net/2025/Jul/17/vibe-scraping/2026/Apr/3/supply-chain-social-engineering/) \- 3rd April 2026
* [Highlights from my conversation about agentic engineering on Lenny's Podcast](https://simonwillison.net/2025/Jul/17/vibe-scraping/2026/Apr/2/lennys-podcast/) \- 2nd April 2026
* [Mr. Chatterbox is a (weak) Victorian-era ethically trained model you can run on your own computer](https://simonwillison.net/2025/Jul/17/vibe-scraping/2026/Mar/30/mr-chatterbox/) \- 30th March 2026

This is **Vibe scraping and vibe coding a schedule app for Open Sauce 2025 entirely on my phone** by Simon Willison, posted on [17th July 2025](https://simonwillison.net/2025/Jul/17/vibe-scraping/2025/Jul/17/).

[ definitions51 ](https://simonwillison.net/2025/Jul/17/vibe-scraping/tags/definitions/) [ github183 ](https://simonwillison.net/2025/Jul/17/vibe-scraping/tags/github/) [ icalendar10 ](https://simonwillison.net/2025/Jul/17/vibe-scraping/tags/icalendar/) [ mobile40 ](https://simonwillison.net/2025/Jul/17/vibe-scraping/tags/mobile/) [ scraping38 ](https://simonwillison.net/2025/Jul/17/vibe-scraping/tags/scraping/) [ tools53 ](https://simonwillison.net/2025/Jul/17/vibe-scraping/tags/tools/) [ ai1947 ](https://simonwillison.net/2025/Jul/17/vibe-scraping/tags/ai/) [ playwright13 ](https://simonwillison.net/2025/Jul/17/vibe-scraping/tags/playwright/) [ openai403 ](https://simonwillison.net/2025/Jul/17/vibe-scraping/tags/openai/) [ generative-ai1728 ](https://simonwillison.net/2025/Jul/17/vibe-scraping/tags/generative-ai/) [ chatgpt191 ](https://simonwillison.net/2025/Jul/17/vibe-scraping/tags/chatgpt/) [ llms1695 ](https://simonwillison.net/2025/Jul/17/vibe-scraping/tags/llms/) [ ai-assisted-programming371 ](https://simonwillison.net/2025/Jul/17/vibe-scraping/tags/ai-assisted-programming/) [ claude264 ](https://simonwillison.net/2025/Jul/17/vibe-scraping/tags/claude/) [ claude-artifacts36 ](https://simonwillison.net/2025/Jul/17/vibe-scraping/tags/claude-artifacts/) [ ai-agents108 ](https://simonwillison.net/2025/Jul/17/vibe-scraping/tags/ai-agents/) [ vibe-coding80 ](https://simonwillison.net/2025/Jul/17/vibe-scraping/tags/vibe-coding/) [ coding-agents190 ](https://simonwillison.net/2025/Jul/17/vibe-scraping/tags/coding-agents/) [ async-coding-agents17 ](https://simonwillison.net/2025/Jul/17/vibe-scraping/tags/async-coding-agents/) [ prompt-to-app39 ](https://simonwillison.net/2025/Jul/17/vibe-scraping/tags/prompt-to-app/) 

**Next:** [Using GitHub Spark to reverse engineer GitHub Spark](https://simonwillison.net/2025/Jul/17/vibe-scraping/2025/Jul/24/github-spark/)

**Previous:** [Happy 20th birthday Django! Here's my talk on Django Origins from Django's 10th](https://simonwillison.net/2025/Jul/17/vibe-scraping/2025/Jul/13/django-birthday/)

###  Monthly briefing

 Sponsor me for **$10/month** and get a curated email digest of the month's most important LLM developments.

 Pay me to send you less!

[ Sponsor & subscribe](https://github.com/sponsors/simonw/) 

* [Disclosures](https://simonwillison.net/2025/Jul/17/vibe-scraping/about/#disclosures)
* [Colophon](https://simonwillison.net/2025/Jul/17/vibe-scraping/about/#about-site)
* ©
* [2002](https://simonwillison.net/2025/Jul/17/vibe-scraping/2002/)
* [2003](https://simonwillison.net/2025/Jul/17/vibe-scraping/2003/)
* [2004](https://simonwillison.net/2025/Jul/17/vibe-scraping/2004/)
* [2005](https://simonwillison.net/2025/Jul/17/vibe-scraping/2005/)
* [2006](https://simonwillison.net/2025/Jul/17/vibe-scraping/2006/)
* [2007](https://simonwillison.net/2025/Jul/17/vibe-scraping/2007/)
* [2008](https://simonwillison.net/2025/Jul/17/vibe-scraping/2008/)
* [2009](https://simonwillison.net/2025/Jul/17/vibe-scraping/2009/)
* [2010](https://simonwillison.net/2025/Jul/17/vibe-scraping/2010/)
* [2011](https://simonwillison.net/2025/Jul/17/vibe-scraping/2011/)
* [2012](https://simonwillison.net/2025/Jul/17/vibe-scraping/2012/)
* [2013](https://simonwillison.net/2025/Jul/17/vibe-scraping/2013/)
* [2014](https://simonwillison.net/2025/Jul/17/vibe-scraping/2014/)
* [2015](https://simonwillison.net/2025/Jul/17/vibe-scraping/2015/)
* [2016](https://simonwillison.net/2025/Jul/17/vibe-scraping/2016/)
* [2017](https://simonwillison.net/2025/Jul/17/vibe-scraping/2017/)
* [2018](https://simonwillison.net/2025/Jul/17/vibe-scraping/2018/)
* [2019](https://simonwillison.net/2025/Jul/17/vibe-scraping/2019/)
* [2020](https://simonwillison.net/2025/Jul/17/vibe-scraping/2020/)
* [2021](https://simonwillison.net/2025/Jul/17/vibe-scraping/2021/)
* [2022](https://simonwillison.net/2025/Jul/17/vibe-scraping/2022/)
* [2023](https://simonwillison.net/2025/Jul/17/vibe-scraping/2023/)
* [2024](https://simonwillison.net/2025/Jul/17/vibe-scraping/2024/)
* [2025](https://simonwillison.net/2025/Jul/17/vibe-scraping/2025/)
* [2026](https://simonwillison.net/2025/Jul/17/vibe-scraping/2026/)