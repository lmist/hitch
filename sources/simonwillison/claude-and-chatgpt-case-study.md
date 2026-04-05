# [Simon Willison’s Weblog](/)

[Subscribe](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/about/#subscribe) 

**Sponsored by:** [WorkOS](https://fandf.co/4v8pTAt) — Production-ready APIs for auth and access control, so you can ship faster.

## Claude and ChatGPT for ad-hoc sidequests

22nd March 2024

Here is a short, illustrative example of one of the ways in which I use Claude and ChatGPT on a daily basis.

I recently learned that the [Adirondack Park](https://en.wikipedia.org/wiki/Adirondack%5FPark) is the single largest park in the contiguous United States, taking up a fifth of the state of New York.

Naturally, my first thought was that it would be neat to have a GeoJSON file representing the boundary of the park.

A quick search landed me on the [Adirondack Park Agency GIS data page](https://apa.ny.gov/gis/ApaData.html), which offered me a shapefile of the “Outer boundary of the New York State Adirondack Park as described in Section 9-0101 of the New York Environmental Conservation Law”. Sounds good!

I knew there were tools for converting shapefiles to GeoJSON, but I couldn’t remember what they were. Since I had a terminal window open already, I typed the following:

llm -m opus -c 'give me options on macOS for CLI tools to turn a shapefile into GeoJSON'

Here I am using my [LLM tool](https://llm.datasette.io/) (and [llm-claude-3](https://github.com/simonw/llm-claude-3) plugin) to run a prompt through the new [Claude 3 Opus](https://www.anthropic.com/news/claude-3-family), my current favorite language model.

It [replied with a couple of options](https://gist.github.com/simonw/331918e46f33e27e997afb4e7c62fc74), but the first was this:

ogr2ogr -f GeoJSON output.geojson input.shp

So I ran that against the shapefile, and then pasted [the resulting GeoJSON](https://gist.github.com/simonw/c941f3454cdec7e10f500dc5a752b614) into [geojson.io](https://geojson.io/) to check if it worked... and nothing displayed. Then I looked at the GeoJSON and spotted this:

`"coordinates": [ [ -8358911.527799999341369, 5379193.197800002992153 ] ...`

That didn’t look right. Those co-ordinates aren’t the correct scale for latitude and longitude values.

So I sent a follow-up prompt to the model (the `-c` option means “continue previous conversation”):

llm -c 'i tried using ogr2ogr but it gave me back GeoJSON with a weird coordinate system that was not lat/lon that i am used to'

It suggested this new command:

ogr2ogr -f GeoJSON -t_srs EPSG:4326 output.geojson input.shp

This time [it worked](https://gist.github.com/simonw/6c4cf102a8ea532dc365c2773f0eb6ea)! The shapefile has now been converted to GeoJSON.

Time elapsed so far: 2.5 minutes (I can tell from [my LLM logs](https://llm.datasette.io/en/stable/logging.html)).

I pasted it into [Datasette](https://datasette.io/) (with [datasette-paste](https://github.com/datasette/datasette-paste) and [datasette-leaflet-geojson](https://datasette.io/plugins/datasette-leaflet-geojson)) to take a look at it more closely, and got this:

![A Datasette table with 106 rows. The first two are shown - both have properties and a geometry, and the geometry is a single line on a map. The first one has a ECL_Text of thence southerly along the westerly line of lots 223, 241, 259, 276, 293, 309, 325 and 340 to the southwesterly corner of lot number 340 in the Brantingham Tract and the second has thence westerly along the northern line of lots 204 and 203 to the midpoint of the northern line of lot 203](https://static.simonwillison.net/static/2024/datasette-adirondack-boundaries.jpg)

That’s not a single polygon! That’s 106 line segments... and they are fascinating. Look at those descriptions:

> thence westerly along the northern line of lots 204 and 203 to the midpoint of the northern line of lot 203

This is utterly delightful. The shapefile description did say “as described in Section 9-0101 of the New York Environmental Conservation Law”, so I guess this is how you write geographically boundaries into law!

But it’s not what I wanted. I want a single polygon of the whole park, not 106 separate lines.

I decided to switch models. ChatGPT has access to Code Interpreter, and I happen to know that Code Interpreter is quite effective at processing GeoJSON.

I opened a new ChatGPT (with GPT-4) browser tab, uploaded my GeoJSON file and prompted it:

> This GeoJSON file is full of line segments. Use them to create me a single shape that is a Polygon

![ChatGPT screenshot - it shows some Python code with a result of <shapely.geometry.polygon.Polygon at 0x7eba83f9fca0 />, then says: I've created a polygon from the line segments in the GeoJSON file. You can now use this polygon for further analysis or visualization. If you have specific requirements for the polygon or need it in a particular format, please let me know! ​​](https://static.simonwillison.net/static/2024/shapely-chatgpt-1.jpg)

OK, so it wrote some Python code and ran it. But did it work?

I happen to know that Code Interpreter can save files to disk and provide links to download them, so I told it to do that:

> Save it to a GeoJSON file for me to download

![ChatGPT screenshot - this time it writes more Python code to define a GeoJSON polygon, then saves that to a file called /mnt/data/polygon.geojson and gives me a link to download it.​​](https://static.simonwillison.net/static/2024/shapely-chatgpt-2.jpg)

I pasted [that](https://gist.github.com/simonw/c1002dbf5249de7addd0b65cb774d3e9) into [geojson.io](https://geojson.io/), and it was clearly wrong:

![geojson.io screenshot - a triangle shape sits on top of an area of upstate New York, clearly not in the shape of the park](https://static.simonwillison.net/static/2024/shapely-chatgpt-bad-map.jpg)

So I told it to try again. I didn’t think very hard about this prompt, I basically went with a version of “do better”:

> that doesn’t look right to me, check that it has all of the lines in it

![ChatGPT screenshot - it writes more Python code and outputs a link to complete_polygon.geojson​​](https://static.simonwillison.net/static/2024/shapely-chatgpt-3.jpg)

It gave me a new file, optimistically named `complete_polygon.geojson`. Here’s what that one looked like:

![ChatGPT screenshot - it writes more Python code and outputs a link to complete_polygon.geojson​​](https://static.simonwillison.net/static/2024/shapely-chatgpt-almost.jpg)

This is getting a lot closer! Note how the right hand boundary of the park looks correct, but the rest of the image is scrambled.

I had a hunch about the fix. I pasted in a screenshot of where we were so far and added my hunch about the solution:

> That almost works but you need to sort the line segments first, it looked like this:

Honestly, pasting in the screenshot probably wasn’t necessary here, but it amused me.

![That almost works but you need to sort the line segments first, it looked like this: an a screenshot of a map](https://static.simonwillison.net/static/2024/shapely-chatgpt-4.jpg)

... and ChatGPT churned away again ...

![More Python code - link to the full transcript is below](https://static.simonwillison.net/static/2024/shapely-chatgpt-5.jpg)

[sorted\_polygon.geojson](https://gist.github.com/simonw/b9e4325b76e4a3813ff5482aa278c342) is spot on! Here’s what it looks like:

![A shaded polygon showing the exact shape of the boundary of Adirondack Park, overlayed on a map of the area](https://static.simonwillison.net/static/2024/shapely-good-map.jpg)

Total time spent in ChatGPT: 3 minutes and 35 seconds. Plus 2.5 minutes with Claude 3 earlier, so an overall total of just over 6 minutes.

Here’s [the full Claude transcript](https://gist.github.com/simonw/0343cdd3568bbe28cad15d1097b1b1c7) and the [full transcript from ChatGPT](https://gist.github.com/simonw/3eb845823c5ad4c48d2b4eb7586f1533).

#### This isn’t notable [#](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2024/Mar/22/claude-and-chatgpt-case-study/#not-notable)

The most notable thing about this example is how completely _not_ notable it is.

I get results like this from these tools several times a day. I’m not at all surprised that this worked, in fact, I would’ve been mildly surprised if it had not.

Could I have done this without LLM assistance? Yes, but not nearly as quickly. And this was not a task on my critical path for the day—it was a sidequest at best and honestly more of a distraction.

So, without LLM tools, I would likely have given this one up at the first hurdle.

A year ago I wrote about how [AI-enhanced development makes me more ambitious with my projects](https://simonwillison.net/2023/Mar/27/ai-enhanced-development/). They are now so firmly baked into my daily work that they influence not just side projects but tiny sidequests like this one as well.

#### This certainly wasn’t simple [#](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2024/Mar/22/claude-and-chatgpt-case-study/#not-simple)

Something else I like about this example is that it illustrates quite how much depth there is to getting great results out of these systems.

In those few minutes I used two different interfaces to call two different models. I sent multiple follow-up prompts. I triggered Code Interpreter, took advantage of GPT-4 Vision and mixed in external tools like [geojson.io](https://geojson.io/) and Datasette as well.

I leaned a lot on my existing knowledge and experience:

* I knew that tools existed for commandline processing of shapefiles and GeoJSON
* I instinctively knew that Claude 3 Opus was likely to correctly answer my initial prompt
* I knew the capabilities of Code Interpreter, including that it has libraries that can process geometries, what to say to get it to kick into action and how to get it to give me files to download
* My limited GIS knowledge was strong enough to spot a likely coordinate system problem, and I guessed the fix for the jumbled lines
* My prompting intuition is developed to the point that I didn’t have to think very hard about what to say to get the best results

If you have the right combination of domain knowledge and hard-won experience driving LLMs, you can _fly_ with these things.

#### Isn’t this a bit trivial? [#](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2024/Mar/22/claude-and-chatgpt-case-study/#a-bit-trivial)

Yes it is, and that’s the point. This was a five minute sidequest. Writing about it here took ten times longer than the exercise itself.

I take on LLM-assisted sidequests like this one dozens of times a week. Many of them are substantially larger and more useful. They are having a very material impact on my work: I can get more done and solve much more interesting problems, because I’m not wasting valuable cycles figuring out `ogr2ogr` invocations or mucking around with polygon libraries.

Not to mention that I find working this way _fun_! It feels like science fiction every time I do it. Our AI-assisted future is here right now and I’m still finding it weird, fascinating and deeply entertaining.

#### LLMs are useful [#](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2024/Mar/22/claude-and-chatgpt-case-study/#llms-are-useful)

There are many legitimate criticisms of LLMs. The copyright issues involved in their training, their enormous power consumption and the risks of people trusting them when they shouldn’t (considering both accuracy and bias) are three that I think about a lot.

The one criticism I wont accept is that they aren’t _useful_.

One of the greatest misconceptions concerning LLMs is the idea that they are easy to use. They really aren’t: getting great results out of them requires a great deal of experience and hard-fought intuition, combined with deep domain knowledge of the problem you are applying them to.

I use these things every day. They help me take on much more interesting and ambitious problems than I could otherwise. I would miss them terribly if they were no longer available to me.

Posted [22nd March 2024](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2024/Mar/22/) at 7:44 pm · Follow me on [Mastodon](https://fedi.simonwillison.net/@simon), [Bluesky](https://bsky.app/profile/simonwillison.net), [Twitter](https://twitter.com/simonw) or [subscribe to my newsletter](https://simonwillison.net/about/#subscribe)

## More recent articles

* [The Axios supply chain attack used individually targeted social engineering](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2026/Apr/3/supply-chain-social-engineering/) \- 3rd April 2026
* [Highlights from my conversation about agentic engineering on Lenny's Podcast](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2026/Apr/2/lennys-podcast/) \- 2nd April 2026
* [Mr. Chatterbox is a (weak) Victorian-era ethically trained model you can run on your own computer](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2026/Mar/30/mr-chatterbox/) \- 30th March 2026

This is **Claude and ChatGPT for ad-hoc sidequests** by Simon Willison, posted on [22nd March 2024](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2024/Mar/22/).

Part of series **[How I use LLMs and ChatGPT](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/series/using-llms/)**

1. [Running Python micro-benchmarks using the ChatGPT Code Interpreter alpha](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2023/Apr/12/code-interpreter/) \- April 12, 2023, 1:14 a.m.
2. [How I make annotated presentations](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2023/Aug/6/annotated-presentations/) \- Aug. 6, 2023, 5:15 p.m.
3. [Exploring GPTs: ChatGPT in a trench coat?](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2023/Nov/15/gpts/) \- Nov. 15, 2023, 3:39 p.m.
4. **Claude and ChatGPT for ad-hoc sidequests** \- March 22, 2024, 7:44 p.m.
5. [Building and testing C extensions for SQLite with ChatGPT Code Interpreter](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2024/Mar/23/building-c-extensions-for-sqlite-with-chatgpt-code-interpreter/) \- March 23, 2024, 5:50 p.m.
6. [llm cmd undo last git commit - a new plugin for LLM](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2024/Mar/26/llm-cmd/) \- March 26, 2024, 3:37 p.m.
7. [Running OCR against PDFs and images directly in your browser](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2024/Mar/30/ocr-pdfs-images/) \- March 30, 2024, 5:59 p.m.
8. [… more](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/series/using-llms/)

[ geospatial82 ](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/tags/geospatial/) [ shapefiles7 ](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/tags/shapefiles/) [ geojson15 ](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/tags/geojson/) [ ai1947 ](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/tags/ai/) [ openai403 ](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/tags/openai/) [ generative-ai1728 ](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/tags/generative-ai/) [ chatgpt191 ](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/tags/chatgpt/) [ llms1695 ](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/tags/llms/) [ ai-assisted-programming371 ](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/tags/ai-assisted-programming/) [ anthropic266 ](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/tags/anthropic/) [ claude264 ](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/tags/claude/) [ code-interpreter29 ](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/tags/code-interpreter/) [ coding-agents190 ](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/tags/coding-agents/) [ leaflet46 ](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/tags/leaflet/) 

**Next:** [Building and testing C extensions for SQLite with ChatGPT Code Interpreter](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2024/Mar/23/building-c-extensions-for-sqlite-with-chatgpt-code-interpreter/)

**Previous:** [Weeknotes: the aftermath of NICAR](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2024/Mar/16/weeknotes-the-aftermath-of-nicar/)

###  Monthly briefing

 Sponsor me for **$10/month** and get a curated email digest of the month's most important LLM developments.

 Pay me to send you less!

[ Sponsor & subscribe](https://github.com/sponsors/simonw/) 

* [Disclosures](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/about/#disclosures)
* [Colophon](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/about/#about-site)
* ©
* [2002](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2002/)
* [2003](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2003/)
* [2004](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2004/)
* [2005](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2005/)
* [2006](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2006/)
* [2007](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2007/)
* [2008](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2008/)
* [2009](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2009/)
* [2010](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2010/)
* [2011](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2011/)
* [2012](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2012/)
* [2013](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2013/)
* [2014](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2014/)
* [2015](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2015/)
* [2016](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2016/)
* [2017](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2017/)
* [2018](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2018/)
* [2019](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2019/)
* [2020](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2020/)
* [2021](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2021/)
* [2022](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2022/)
* [2023](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2023/)
* [2024](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2024/)
* [2025](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2025/)
* [2026](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/2026/)