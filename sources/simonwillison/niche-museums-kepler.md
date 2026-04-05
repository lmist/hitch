# [Simon Willison’s Weblog](/)

[Subscribe](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/about/#subscribe) 

**Sponsored by:** [WorkOS](https://fandf.co/4v8pTAt) — Production-ready APIs for auth and access control, so you can ship faster.

## Weeknotes: Niche Museums, Kepler, Trees and Streaks

28th October 2019

### Niche Museums [#](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2019/Oct/28/niche-museums-kepler/#Niche%5FMuseums%5F4)

Every now and then someone will ask “so when are you going to build Museums Near Me then?”, based on [my obsession with niche museums](https://twitter.com/simonw/status/1171159213436997633) and websites like [www.owlsnearme.com](https://www.owlsnearme.com/).

For my Strategic Communications course at Stanford last week I had to perform a midterm presentation—a six minute talk to convince my audience of something, accompanied by slides and a handout.

I chose “you should seek out and explore tiny museums” as my topic, and used it as an excuse to finally start the website!

[www.niche-museums.com](https://www.niche-museums.com/) is the result. It’s a small but growing collection of niche museums (17 so far, mostly in the San Francisco Bay Area) complete with the all important blue “Use my location” button to see museums near you.

Naturally I built it on [Datasette](https://github.com/simonw/datasette). I’ll be writing more about the implementation (and releasing the underlying code) soon. I also built a new plugin for it, [datasette-haversine](https://github.com/simonw/datasette-haversine ).

### Mapping museums against Starbucks [#](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2019/Oct/28/niche-museums-kepler/#Mapping%5Fmuseums%5Fagainst%5FStarbucks%5F16)

I needed a way to emphasize quite how many tiny museums there are in the USA. I decided to do this with a visualization.

It turns out there are 15,891 branches of Starbucks in the USA… and at least 30,132 museums!

![15,891 Starbucks](https://static.simonwillison.net/static/2019/starbucks.png)

![At least 30.132 museums!](https://static.simonwillison.net/static/2019/museums.png)

I made these maps using a couple of sources.

[All The Places](https://www.alltheplaces.xyz/) is a crowdsourced scraper project which aims to build scrapers for every company that has a “store locator” area of their website. Starbucks has [a store locator](https://www.starbucks.com/store-locator) and All The Places have [a scraper for it](https://github.com/alltheplaces/alltheplaces/blob/master/locations/spiders/starbucks.py), so you can download GeoJSON of every Starbucks. I wrote a quick script to import that GeoJSON into Datasette using sqlite-utils.

The [Institute of Museum and Library Services](https://www.imls.gov/) is an independent agency of the federal government that supports museums and libraries across the country. They publish a [dataset of Museums in the USA](https://www.imls.gov/research-evaluation/data-collection/museum-data-files) as a set of CSV files. I used [csvs-to-sqlite](https://github.com/simonw/csvs-to-sqlite) to load those into Datasette, than ran a union query to combine the three files together.

So I have Datasette instances (with a CSV export feature) for both Starbucks and USA museums, with altitudes and longitudes for each.

Now how to turn that into a map?

I turned to my new favourite GIS tool, [Kepler](https://kepler.gl/). Kepler is an open source GIS visualization tool released by Uber, based on WebGL. It’s astonishingly powerful and can be used directly in your browser by clicking the “Get Started” button on their website (which I assumed would take you to installation instructions, but no, it loads up the entire tool in your browser).

You can import millions of points of data into Kepler and it will visualize them for you directly. I used a Datasette query to export the CSVs, then loaded in my Starbucks CSV, exported an image, loaded in the Museums CSV as a separate colour and exported a second image. The whole project ended up taking about 15 minutes. Kepler is a great addition to the toolbelt!

### Animating the PG&E outages [#](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2019/Oct/28/niche-museums-kepler/#Animating%5Fthe%5FPGE%5Foutages%5F40)

My [PG&E outages scraper](https://simonwillison.net/2019/Oct/10/pge-outages/) continues to record a snapshot of the PG&E outage map JSON every ten minutes. I’m posting updates to [a thread on Twitter](https://twitter.com/simonw/status/1182440312590848001), but discovering Kepler inspired me to look at more sophisticated visualization options.

[This tutorial](https://medium.com/vis-gl/animating-40-years-of-california-earthquakes-e4ffcdd4a289) by Giuseppe Macrì tipped me off the the fact that you can use Kepler to animate points against timestamps!

Here’s the result: a video animation showing how PG&E’s outages have evolved since the 5th of October:

> Here’s a video animation of PG&E’s outages from October 5th up until just a few minutes ago [pic.twitter.com/50K3BrROZR](https://t.co/50K3BrROZR)
> 
> \- Simon Willison (@simonw) [October 28, 2019](https://twitter.com/simonw/status/1188612004572880896?ref%5Fsrc=twsrc%5Etfw)

### Hayes Valley Trees [#](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2019/Oct/28/niche-museums-kepler/#Hayes%5FValley%5FTrees%5F50)

The city announced plans to cut down 27 ficus trees in our neighborhood in San Francisco. I’ve been working with Natalie to help a small group of citizens organize an appeal, and this weekend I helped run a survey of the affected trees (recording their exact locations in a CSV file) and then built [www.hayes-valley-trees.com](https://www.hayes-valley-trees.com/) ([source on GitHub](https://github.com/simonw/hayes-valley-trees)) to link to from fliers attached to each affected tree.

It started out as [a Datasette](https://glitch.com/~hayes-valley-trees) (running on Glitch) but since it’s only 27 data points I ended up freezing the data in a static JSON file to avoid having to tolerate any cold start times. The site is deployed as static assets on Zeit Now using their handy [GitHub continuous deployment tool](https://zeit.co/github).

### Streaks [#](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2019/Oct/28/niche-museums-kepler/#Streaks%5F56)

It turns out I’m very motivated by streaks: I’m at 342 days for Duolingo Spanish and 603 days for an Apple Watch move streak. Could I apply this to other things in my life?

I [asked on Twitter](https://twitter.com/simonw/status/1186824721280593920) and was recommended the [Streaks iOS app](https://streaks.app/). It’s beautiful! I’m now tracking streaks for guitar practice, Duolingo, checking email, checking Slack, reading some books and adding a new museum to [www.niche-museums.com](http://www.niche-museums.com) (if I add one a day I can get from 17 museums today to 382 in a year!)

It seems to be working pretty well so far. I particularly like their iPhone widget.

![Streaks widget](https://static.simonwillison.net/static/2019/streaks-widget.jpg)

Posted [28th October 2019](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2019/Oct/28/) at 10:42 pm · Follow me on [Mastodon](https://fedi.simonwillison.net/@simon), [Bluesky](https://bsky.app/profile/simonwillison.net), [Twitter](https://twitter.com/simonw) or [subscribe to my newsletter](https://simonwillison.net/about/#subscribe)

## More recent articles

* [The Axios supply chain attack used individually targeted social engineering](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2026/Apr/3/supply-chain-social-engineering/) \- 3rd April 2026
* [Highlights from my conversation about agentic engineering on Lenny's Podcast](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2026/Apr/2/lennys-podcast/) \- 2nd April 2026
* [Mr. Chatterbox is a (weak) Victorian-era ethically trained model you can run on your own computer](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2026/Mar/30/mr-chatterbox/) \- 30th March 2026

This is **Weeknotes: Niche Museums, Kepler, Trees and Streaks** by Simon Willison, posted on [28th October 2019](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2019/Oct/28/).

[ museums144 ](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/tags/museums/) [ productivity32 ](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/tags/productivity/) [ projects523 ](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/tags/projects/) [ visualization27 ](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/tags/visualization/) [ weeknotes193 ](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/tags/weeknotes/) [ baked-data11 ](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/tags/baked-data/) [ streaks7 ](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/tags/streaks/) [ duolingo7 ](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/tags/duolingo/) 

**Next:** [Weeknotes: More releases, more museums](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2019/Nov/4/weeknotes-more-releases-more-museums/)

**Previous:** [Weeknotes: The Squirrel Census, Genome SQL query](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2019/Oct/21/weeknotes-squirrels-genome/)

###  Monthly briefing

 Sponsor me for **$10/month** and get a curated email digest of the month's most important LLM developments.

 Pay me to send you less!

[ Sponsor & subscribe](https://github.com/sponsors/simonw/) 

> Weeknotes! Niche Museums, Kepler, Trees and Streaks <https://t.co/5ePqvxi3j3>
> 
> — Simon Willison (@simonw) [October 28, 2019](https://twitter.com/simonw/status/1188949854409510912?ref%5Fsrc=twsrc%5Etfw)

* [Disclosures](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/about/#disclosures)
* [Colophon](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/about/#about-site)
* ©
* [2002](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2002/)
* [2003](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2003/)
* [2004](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2004/)
* [2005](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2005/)
* [2006](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2006/)
* [2007](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2007/)
* [2008](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2008/)
* [2009](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2009/)
* [2010](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2010/)
* [2011](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2011/)
* [2012](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2012/)
* [2013](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2013/)
* [2014](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2014/)
* [2015](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2015/)
* [2016](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2016/)
* [2017](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2017/)
* [2018](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2018/)
* [2019](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2019/)
* [2020](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2020/)
* [2021](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2021/)
* [2022](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2022/)
* [2023](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2023/)
* [2024](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2024/)
* [2025](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2025/)
* [2026](https://simonwillison.net/2019/Oct/28/niche-museums-kepler/2026/)