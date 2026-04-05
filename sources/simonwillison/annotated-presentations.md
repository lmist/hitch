# [Simon Willison’s Weblog](/)

[Subscribe](https://simonwillison.net/2023/Aug/6/annotated-presentations/about/#subscribe) 

**Sponsored by:** [WorkOS](https://fandf.co/4v8pTAt) — Production-ready APIs for auth and access control, so you can ship faster.

## How I make annotated presentations

6th August 2023

Giving a talk is a lot of work. I go by a rule of thumb I learned from [Damian Conway](https://en.wikipedia.org/wiki/Damian%5FConway): a minimum of ten hours of preparation for every one hour spent on stage.

If you’re going to put that much work into something, I think it’s worth taking steps to maximize the value that work produces—both for you and for your audience.

One of my favourite ways of getting “paid” for a talk is when the event puts in the work to produce a really good video of that talk, and then shares that video online. [North Bay Python](https://2023.northbaypython.org) is a fantastic example of an event that does this well: they team up with [Next Day Video](https://nextdayvideo.com) and [White Coat Captioning](https://whitecoatcaptioning.com) and have talks professionally recorded, captioned and uploaded to YouTube within 24 hours of the talk being given.

Even with that quality of presentation, I don’t think a video on its own is enough. My most recent talk was 40 minutes long—I’d love people to watch it, but I myself watch very few 40m long YouTube videos each year.

So I like to publish my talks with a text and image version of the talk that can provide as much of the value as possible to people who don’t have the time or inclination to sit through a 40m talk (or 20m if you run it at 2x speed, which I do for many of the talks I watch myself).

#### Annotated presentations

My preferred format for publishing these documents is as an _annotated presentation_—a single document (no clicking “next” dozens of times) combining key slides from the talk with custom written text to accompany each one, plus additional links and resources.

Here’s my most recent example: [Catching up on the weird world of LLMs](https://simonwillison.net/2023/Aug/3/weird-world-of-llms/), from North Bay Python last week.

More examples (see also my [annotated-talks tag](https://simonwillison.net/tags/annotated-talks/)):

* [Prompt injection explained, with video, slides, and a transcript](https://simonwillison.net/2023/May/2/prompt-injection-explained/) for a LangChain webinar in May 2023.
* [Coping strategies for the serial project hoarder](https://simonwillison.net/2022/Nov/26/productivity/) for DjangoCon US 2022.
* [How to build, test and publish an open source Python library](https://simonwillison.net/2021/Nov/4/publish-open-source-python-library/) for PyGotham 2021
* [Video introduction to Datasette and sqlite-utils](https://simonwillison.net/2021/Feb/7/video/) for FOSDEM February 2021
* [Datasette—an ecosystem of tools for working with small data](https://simonwillison.net/2021/Jul/22/small-data/) for PyGotham 2020.
* [Personal Data Warehouses: Reclaiming Your Data](https://simonwillison.net/2020/Nov/14/personal-data-warehouses/) for the GitHub OCTO speaker series in November 2020.
* [Redis tutorial](https://static.simonwillison.net/static/2010/redis-tutorial/) for NoSQL Europe 2010 (my first attempt at this format).

I don’t tend to write a detailed script for my talks in advance. If I did, I might use that as a starting point, but I usually prepare the outline of the talk and then give it off-the-cuff on the day. I find this fits my style (best described as “enthusiastic rambling”) better.

Instead, I’ll assemble notes for each slide from re-watching the video after it has been released.

I don’t just cover the things I said in the the talk—I’ll also add additional context, and links to related resources. The annotated presentation isn’t just for people who didn’t watch the talk, it’s aimed at providing extra context for people who did watch it as well.

#### A custom tool for building annotated presentations

For this most recent talk I finally built something I’ve been wanting for _years_: a custom tool to help me construct the annotated presentation as quickly as possible.

Annotated presentations look deceptively simple: each slide is an image and one or two paragraphs of text.

There are a few extra details though:

* The images really need good `alt=` text—a big part of the information in the presentation is conveyed by those images, so they need to have good descriptions both for screen reader users and to index in search engines / for retrieval augmented generation.
* Presentations might have dozens of slides—just assembling the image tags in the correct order can be a frustrating task.
* For editing the annotations I like to use Markdown, as it’s quicker to write than HTML. Making this as easy as possible encourages me to add more links, bullet points and code snippets.

One of my favourite use-cases for tools like ChatGPT is to quickly create one-off custom tools. This was a perfect fit for that.

You can see the tool I create here: [Annotated presentation creator](https://til.simonwillison.net/tools/annotated-presentations) ([source code here](https://github.com/simonw/til/blob/main/templates/pages/tools/annotated-presentations.html)).

The first step is to export the slides as images, being sure to have filenames which sort alphabetically in the correct order. I use Apple Keynote for my slides and it has an “Export” feature which does this for me.

Next, open those images using the annotation tool.

The tool is written in JavaScript and works entirely in your browser—it asks you to select images but doesn’t actually upload them to a server, just displays them directly inline in the page.

Anything you type in a `textarea` as work-in-progress will be saved to `localStorage`, so a browser crash or restart shouldn’t lose any of your work.

It uses [Tesseract.js](https://tesseract.projectnaptha.com/) to run OCR against your images, providing a starting point for the `alt=` attributes for each slide.

Annotations can be entered in Markdown and are rendered to HTML as a live preview using the [Marked](https://marked.js.org/) library.

Finally, it offers a templating mechanism for the final output, which works using JavaScript template literals. So once you’ve finished editing the `alt=` text and writing the annotations, click “Execute template” at the bottom of the page and copy out the resulting HTML.

Here’s an animated GIF demo of the tool in action:

![Animated demo of the tool. I load 90 images, each one of which becomes a slide. Then I click the OCR button and it starts populating the alt textareas with OCR text from the slides. I type some markdown into an annotation box, then scroll to the bottom and click the Execute template button to get back the final HTML.](https://static.simonwillison.net/static/2023/annotated-presentation-creator.gif)

I ended up putting this together with the help of multiple different ChatGPT sessions. You can see those here:

* [HTML and JavaScript in a single document to create an app that lets me do the following...](https://chat.openai.com/share/61cd85f6-7002-4676-b204-0349a723232a)
* [JavaScript and HTML app on one page. User can select multiple image files on their own computer...](https://chat.openai.com/share/5218799e-0423-49ad-88ba-c72ee27e3fe3)
* [JavaScript that runs once every 1s and builds a JavaScript object of every textarea on the page where the key is the name= attribute of that textarea and the value is its current contents. That whole object is then stored in localStorage in a key called savedTextAreas...](https://chat.openai.com/share/7867657b-aa29-4ad0-8ab3-1d353c29a224)
* [Write a JavaScript function like this: executeTemplates(template, arrayOfObjects)...](https://chat.openai.com/share/4e6fd644-de57-4597-a1cc-412483c2adf3)

#### Cleaning up the transcript with Claude

Since the video was already up on YouTube when I started writing the annotations, I decided to see if I could get a head start on writing them using the YouTube generated transcript.

I used my [Action Transcription](https://simonwillison.net/2022/Sep/30/action-transcription/) tool to extract the transcript, but it was pretty low quality—you can see [a copy of it here](https://gist.github.com/simonw/3d8a335244711c675c456db147aa05fa). A sample:

```
okay hey everyone it's uh really
exciting to be here so yeah I call this
court talk catching up on the weird
world of llms I'm going to try and give
you the last few years of of llm
developments in 35 minutes this is
impossible so uh hopefully I'll at least
give you a flavor of some of the weirder
corners of the space because the thing
about language models is the more I look
at the more I think they're practically
interesting any particular aspect of
them anything at all if you zoom in
there are just more questions there are
just more unknowns about it there are
more interesting things to get into lots
of them are deeply disturbing and
unethical lots of them are fascinating
it's um I've called it um it's it's
impossible to tear myself away from this
I I just keep on keep on finding new
aspects of it that are interesting

```

It’s basically one big run-on sentence, with no punctuation, little capitalization and lots of umms and ahs.

Anthropic’s [Claude 2](https://claude.ai) was [released last month](https://www.anthropic.com/index/claude-2) and supports up to 100,000 tokens per prompt—a huge improvement on ChatGPT (4,000) and GPT-4 (8,000). I decided to see if I could use that to clean up my transcript.

I pasted it into Claude and tried a few prompts... until I hit upon this one:

> Reformat this transcript into paragraphs and sentences, fix the capitalization and make very light edits such as removing ums

![Claude interface: Taming Large Language Models. I have pasted in a paste.txt file with 42KB of data, then prompted it to reformat. It outputs Here is the reformatted transcript: followed by that transcript.](https://static.simonwillison.net/static/2023/claude-transcript.jpg)

This worked really, really well! Here’s the first paragraph it produced, based on the transcript I show above:

> Okay everyone, it’s really exciting to be here. Yeah I call this talk “Catching Up on the Weird World of LLMs.” I’m going to try and give you the last few years of LLMs developments in 35 minutes. This is impossible, so hopefully I’ll at least give you a flavor of some of the weirder corners of the space. The thing about language models is the more I look at them, the more I think they’re practically interesting. Focus on any particular aspect, and there are just more questions, more unknowns, more interesting things to get into.

Note that I said “fractally interesting”, not “practically interesting”—but that error was there in the YouTube transcript, so Claude picked it up from there.

Here’s the [full generated transcript](https://gist.github.com/simonw/f6d83d69cca018c07b58aaadfb4c918c).

It’s really impressive! At one point it even turns my dialogue into a set of bullet points:

> Today the best are ChatGPT (aka GPT-3.5 Turbo), GPT-4 for capability, and Claude 2 which is free. Google has PaLM 2 and Bard. Llama and Claude are from Anthropic, a splinter of OpenAI focused on ethics. Google and Meta are the other big players.
> 
> Some tips:
> 
> * OpenAI models cutoff at September 2021 training data. Anything later isn’t in there. This reduces issues like recycling their own text.
> * Claude and Palm have more recent data, so I’ll use them for recent events.
> * Always consider context length. GPT has 4,000 tokens, GPT-4 has 8,000, Claude 100,000.
> * If a friend who read the Wikipedia article could answer my question, I’m confident feeding it in directly. The more obscure, the more likely pure invention.
> * Avoid superstitious thinking. Long prompts that “always work” are usually mostly pointless.
> * Develop an immunity to hallucinations. Notice signs and check answers.

Compare that to [my rambling original](https://gist.github.com/simonw/3d8a335244711c675c456db147aa05fa#file-transcription-txt-L327-L469) to see quite how much of an improvement this is.

But, all of that said... I specified “make very light edits” and it clearly did a whole lot more than just that.

I didn’t use the Claude version directly. Instead, I copied and pasted chunks of it into my annotation tool that made the most sense, then directly edited them to better fit what I was trying to convey.

As with so many things in LLM/AI land: a significant time saver, but no silver bullet.

#### For workshops, publish the handout

I took the Software Carpentries [instructor training](https://carpentries.org/become-instructor/) a few years ago, which was a really great experience.

A key idea I got from that is that a great way to run a workshop is to prepare an extensive, detailed handout in advance—and then spend the actual workshop time working through that handout yourself, at a sensible pace, in a way that lets the attendees follow along.

A bonus of this approach is that it forces you to put together a really high quality handout which you can distribute after the event.

I used this approach for the 3 hour workshop I ran at PyCon US 2023: [Data analysis with SQLite and Python](https://datasette.io/tutorials/data-analysis). I turned that into a new official tutorial on the Datasette website, accompanied by the video but also useful for people who don’t want to spend three hours watching me talk!

#### More people should do this

I’m writing this in the hope that I can inspire more people to give their talks this kind of treatment. It’s not a zero amount of work—it takes me 2-3 hours any time I do this—but it greatly increases the longevity of the talk and ensures that the work I’ve already put into it provides maximum value, both to myself (giving talks is partly a selfish act!) and to the people I want to benefit from it.

Posted [6th August 2023](https://simonwillison.net/2023/Aug/6/annotated-presentations/2023/Aug/6/) at 5:15 pm · Follow me on [Mastodon](https://fedi.simonwillison.net/@simon), [Bluesky](https://bsky.app/profile/simonwillison.net), [Twitter](https://twitter.com/simonw) or [subscribe to my newsletter](https://simonwillison.net/about/#subscribe)

## More recent articles

* [The Axios supply chain attack used individually targeted social engineering](https://simonwillison.net/2023/Aug/6/annotated-presentations/2026/Apr/3/supply-chain-social-engineering/) \- 3rd April 2026
* [Highlights from my conversation about agentic engineering on Lenny's Podcast](https://simonwillison.net/2023/Aug/6/annotated-presentations/2026/Apr/2/lennys-podcast/) \- 2nd April 2026
* [Mr. Chatterbox is a (weak) Victorian-era ethically trained model you can run on your own computer](https://simonwillison.net/2023/Aug/6/annotated-presentations/2026/Mar/30/mr-chatterbox/) \- 30th March 2026

This is **How I make annotated presentations** by Simon Willison, posted on [6th August 2023](https://simonwillison.net/2023/Aug/6/annotated-presentations/2023/Aug/6/).

Part of series **[How I use LLMs and ChatGPT](https://simonwillison.net/2023/Aug/6/annotated-presentations/series/using-llms/)**

1. [I built a ChatGPT plugin to answer questions about data hosted in Datasette](https://simonwillison.net/2023/Aug/6/annotated-presentations/2023/Mar/24/datasette-chatgpt-plugin/) \- March 24, 2023, 3:43 p.m.
2. [AI-enhanced development makes me more ambitious with my projects](https://simonwillison.net/2023/Aug/6/annotated-presentations/2023/Mar/27/ai-enhanced-development/) \- March 27, 2023, 2:38 p.m.
3. [Running Python micro-benchmarks using the ChatGPT Code Interpreter alpha](https://simonwillison.net/2023/Aug/6/annotated-presentations/2023/Apr/12/code-interpreter/) \- April 12, 2023, 1:14 a.m.
4. **How I make annotated presentations** \- Aug. 6, 2023, 5:15 p.m.
5. [Exploring GPTs: ChatGPT in a trench coat?](https://simonwillison.net/2023/Aug/6/annotated-presentations/2023/Nov/15/gpts/) \- Nov. 15, 2023, 3:39 p.m.
6. [Claude and ChatGPT for ad-hoc sidequests](https://simonwillison.net/2023/Aug/6/annotated-presentations/2024/Mar/22/claude-and-chatgpt-case-study/) \- March 22, 2024, 7:44 p.m.
7. [Building and testing C extensions for SQLite with ChatGPT Code Interpreter](https://simonwillison.net/2023/Aug/6/annotated-presentations/2024/Mar/23/building-c-extensions-for-sqlite-with-chatgpt-code-interpreter/) \- March 23, 2024, 5:50 p.m.
8. [… more](https://simonwillison.net/2023/Aug/6/annotated-presentations/series/using-llms/)

[ alt-text14 ](https://simonwillison.net/2023/Aug/6/annotated-presentations/tags/alt-text/) [ localstorage7 ](https://simonwillison.net/2023/Aug/6/annotated-presentations/tags/localstorage/) [ ocr25 ](https://simonwillison.net/2023/Aug/6/annotated-presentations/tags/ocr/) [ tools53 ](https://simonwillison.net/2023/Aug/6/annotated-presentations/tags/tools/) [ speaking119 ](https://simonwillison.net/2023/Aug/6/annotated-presentations/tags/speaking/) [ my-talks90 ](https://simonwillison.net/2023/Aug/6/annotated-presentations/tags/my-talks/) [ projects523 ](https://simonwillison.net/2023/Aug/6/annotated-presentations/tags/projects/) [ claude264 ](https://simonwillison.net/2023/Aug/6/annotated-presentations/tags/claude/) [ anthropic266 ](https://simonwillison.net/2023/Aug/6/annotated-presentations/tags/anthropic/) [ llms1695 ](https://simonwillison.net/2023/Aug/6/annotated-presentations/tags/llms/) [ annotated-talks30 ](https://simonwillison.net/2023/Aug/6/annotated-presentations/tags/annotated-talks/) [ ai1947 ](https://simonwillison.net/2023/Aug/6/annotated-presentations/tags/ai/) [ generative-ai1728 ](https://simonwillison.net/2023/Aug/6/annotated-presentations/tags/generative-ai/) [ ai-assisted-programming371 ](https://simonwillison.net/2023/Aug/6/annotated-presentations/tags/ai-assisted-programming/) 

**Next:** [Datasette Cloud, Datasette 1.0a3, llm-mlc and more](https://simonwillison.net/2023/Aug/6/annotated-presentations/2023/Aug/16/datasette-cloud-weeknotes/)

**Previous:** [Weeknotes: Plugins for LLM, sqlite-utils and Datasette](https://simonwillison.net/2023/Aug/6/annotated-presentations/2023/Aug/5/weeknotes-plugins/)

###  Monthly briefing

 Sponsor me for **$10/month** and get a curated email digest of the month's most important LLM developments.

 Pay me to send you less!

[ Sponsor & subscribe](https://github.com/sponsors/simonw/) 

* [Disclosures](https://simonwillison.net/2023/Aug/6/annotated-presentations/about/#disclosures)
* [Colophon](https://simonwillison.net/2023/Aug/6/annotated-presentations/about/#about-site)
* ©
* [2002](https://simonwillison.net/2023/Aug/6/annotated-presentations/2002/)
* [2003](https://simonwillison.net/2023/Aug/6/annotated-presentations/2003/)
* [2004](https://simonwillison.net/2023/Aug/6/annotated-presentations/2004/)
* [2005](https://simonwillison.net/2023/Aug/6/annotated-presentations/2005/)
* [2006](https://simonwillison.net/2023/Aug/6/annotated-presentations/2006/)
* [2007](https://simonwillison.net/2023/Aug/6/annotated-presentations/2007/)
* [2008](https://simonwillison.net/2023/Aug/6/annotated-presentations/2008/)
* [2009](https://simonwillison.net/2023/Aug/6/annotated-presentations/2009/)
* [2010](https://simonwillison.net/2023/Aug/6/annotated-presentations/2010/)
* [2011](https://simonwillison.net/2023/Aug/6/annotated-presentations/2011/)
* [2012](https://simonwillison.net/2023/Aug/6/annotated-presentations/2012/)
* [2013](https://simonwillison.net/2023/Aug/6/annotated-presentations/2013/)
* [2014](https://simonwillison.net/2023/Aug/6/annotated-presentations/2014/)
* [2015](https://simonwillison.net/2023/Aug/6/annotated-presentations/2015/)
* [2016](https://simonwillison.net/2023/Aug/6/annotated-presentations/2016/)
* [2017](https://simonwillison.net/2023/Aug/6/annotated-presentations/2017/)
* [2018](https://simonwillison.net/2023/Aug/6/annotated-presentations/2018/)
* [2019](https://simonwillison.net/2023/Aug/6/annotated-presentations/2019/)
* [2020](https://simonwillison.net/2023/Aug/6/annotated-presentations/2020/)
* [2021](https://simonwillison.net/2023/Aug/6/annotated-presentations/2021/)
* [2022](https://simonwillison.net/2023/Aug/6/annotated-presentations/2022/)
* [2023](https://simonwillison.net/2023/Aug/6/annotated-presentations/2023/)
* [2024](https://simonwillison.net/2023/Aug/6/annotated-presentations/2024/)
* [2025](https://simonwillison.net/2023/Aug/6/annotated-presentations/2025/)
* [2026](https://simonwillison.net/2023/Aug/6/annotated-presentations/2026/)