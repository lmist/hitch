# [Simon Willison’s Weblog](/)

[Subscribe](https://simonwillison.net/2025/Dec/18/code-proven-to-work/about/#subscribe) 

**Sponsored by:** [WorkOS](https://fandf.co/4v8pTAt) — Production-ready APIs for auth and access control, so you can ship faster.

## Your job is to deliver code you have proven to work

18th December 2025

In all of the debates about the value of AI-assistance in software development there’s one depressing anecdote that I keep on seeing: the junior engineer, empowered by some class of LLM tool, who deposits giant, untested PRs on their coworkers—or open source maintainers—and expects the “code review” process to handle the rest.

This is rude, a waste of other people’s time, and is honestly a dereliction of duty as a software developer.

**Your job is to deliver code you have proven to work.**

As software engineers we don’t just crank out code—in fact these days you could argue that’s what the LLMs are for. We need to deliver _code that works_—and we need to include _proof_ that it works as well. Not doing that directly shifts the burden of the actual work to whoever is expected to review our code.

#### How to prove it works [#](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2025/Dec/18/code-proven-to-work/#how-to-prove-it-works)

There are two steps to proving a piece of code works. Neither is optional.

The first is **manual testing**. If you haven’t seen the code do the right thing yourself, that code doesn’t work. If it does turn out to work, that’s honestly just pure chance.

Manual testing skills are genuine skills that you need to develop. You need to be able to get the system into an initial state that demonstrates your change, then exercise the change, then check and demonstrate that it has the desired effect.

If possible I like to reduce these steps to a sequence of terminal commands which I can paste, along with their output, into a comment in the code review. Here’s a [recent example](https://github.com/simonw/llm-gemini/issues/116#issuecomment-3666551798).

Some changes are harder to demonstrate. It’s still your job to demonstrate them! Record a screen capture video and add that to the PR. Show your reviewers that the change you made actually works.

Once you’ve tested the happy path where everything works you can start trying the edge cases. Manual testing is a skill, and finding the things that break is the next level of that skill that helps define a senior engineer.

The second step in proving a change works is **automated testing**. This is so much easier now that we have LLM tooling, which means there’s no excuse at all for skipping this step.

Your contribution should [bundle the change](https://simonwillison.net/2022/Oct/29/the-perfect-commit/) with an automated test that proves the change works. That test should fail if you revert the implementation.

The process for writing a test mirrors that of manual testing: get the system into an initial known state, exercise the change, assert that it worked correctly. Integrating a test harness to productively facilitate this is another key skill worth investing in.

Don’t be tempted to skip the manual test because you think the automated test has you covered already! Almost every time I’ve done this myself I’ve quickly regretted it.

#### Make your coding agent prove it first [#](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2025/Dec/18/code-proven-to-work/#make-your-coding-agent-prove-it-first)

The most important trend in LLMs in 2025 has been the explosive growth of **coding agents**—tools like Claude Code and Codex CLI that can actively execute the code they are working on to check that it works and further iterate on any problems.

To master these tools you need to learn how to get them to _prove their changes work_ as well.

This looks exactly the same as the process I described above: they need to be able to manually test their changes as they work, and they need to be able to build automated tests that guarantee the change will continue to work in the future.

Since they’re robots, automated tests and manual tests are effectively the same thing.

They do feel a little different though. When I’m working on CLI tools I’ll usually teach Claude Code how to run them itself so it can do one-off tests, even though the eventual automated tests will use a system like [Click’s CLIRunner](https://click.palletsprojects.com/en/stable/testing/).

When working on CSS changes I’ll often encourage my coding agent to take screenshots when it needs to check if the change it made had the desired effect.

The good news about automated tests is that coding agents need very little encouragement to write them. If your project has tests already most agents will extend that test suite without you even telling them to do so. They’ll also reuse patterns from existing tests, so keeping your test code well organized and populated with patterns you like is a great way to help your agent build testing code to your taste.

Developing good taste in testing code is another of those skills that differentiates a senior engineer.

#### The human provides the accountability [#](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2025/Dec/18/code-proven-to-work/#the-human-provides-the-accountability)

[A computer can never be held accountable](https://simonwillison.net/2025/Feb/3/a-computer-can-never-be-held-accountable/). That’s your job as the human in the loop.

Almost anyone can prompt an LLM to generate a thousand-line patch and submit it for code review. That’s no longer valuable. What’s valuable is contributing _code that is proven to work_.

Next time you submit a PR, make sure you’ve included your evidence that it works as it should.

Posted [18th December 2025](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2025/Dec/18/) at 2:49 pm · Follow me on [Mastodon](https://fedi.simonwillison.net/@simon), [Bluesky](https://bsky.app/profile/simonwillison.net), [Twitter](https://twitter.com/simonw) or [subscribe to my newsletter](https://simonwillison.net/about/#subscribe)

## More recent articles

* [The Axios supply chain attack used individually targeted social engineering](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2026/Apr/3/supply-chain-social-engineering/) \- 3rd April 2026
* [Highlights from my conversation about agentic engineering on Lenny's Podcast](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2026/Apr/2/lennys-podcast/) \- 2nd April 2026
* [Mr. Chatterbox is a (weak) Victorian-era ethically trained model you can run on your own computer](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2026/Mar/30/mr-chatterbox/) \- 30th March 2026

This is **Your job is to deliver code you have proven to work** by Simon Willison, posted on [18th December 2025](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2025/Dec/18/).

Part of series **[My open source process](https://simonwillison.net/2025/Dec/18/code-proven-to-work/series/open-source-process/)**

1. [Things I've learned about building CLI tools in Python](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2023/Sep/30/cli-tools-python/) \- Sept. 30, 2023, 12:12 a.m.
2. [Publish Python packages to PyPI with a python-lib cookiecutter template and GitHub Actions](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2024/Jan/16/python-lib-pypi/) \- Jan. 16, 2024, 9:59 p.m.
3. [A selfish personal argument for releasing code as Open Source](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2025/Jan/24/selfish-open-source/) \- Jan. 24, 2025, 9:46 p.m.
4. **Your job is to deliver code you have proven to work** \- Dec. 18, 2025, 2:49 p.m.

[ programming158 ](https://simonwillison.net/2025/Dec/18/code-proven-to-work/tags/programming/) [ careers73 ](https://simonwillison.net/2025/Dec/18/code-proven-to-work/tags/careers/) [ ai1947 ](https://simonwillison.net/2025/Dec/18/code-proven-to-work/tags/ai/) [ generative-ai1728 ](https://simonwillison.net/2025/Dec/18/code-proven-to-work/tags/generative-ai/) [ llms1695 ](https://simonwillison.net/2025/Dec/18/code-proven-to-work/tags/llms/) [ ai-assisted-programming371 ](https://simonwillison.net/2025/Dec/18/code-proven-to-work/tags/ai-assisted-programming/) [ ai-ethics286 ](https://simonwillison.net/2025/Dec/18/code-proven-to-work/tags/ai-ethics/) [ vibe-coding80 ](https://simonwillison.net/2025/Dec/18/code-proven-to-work/tags/vibe-coding/) [ coding-agents190 ](https://simonwillison.net/2025/Dec/18/code-proven-to-work/tags/coding-agents/) 

**Next:** [Cooking with Claude](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2025/Dec/23/cooking-with-claude/)

**Previous:** [Gemini 3 Flash](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2025/Dec/17/gemini-3-flash/)

###  Monthly briefing

 Sponsor me for **$10/month** and get a curated email digest of the month's most important LLM developments.

 Pay me to send you less!

[ Sponsor & subscribe](https://github.com/sponsors/simonw/) 

* [Disclosures](https://simonwillison.net/2025/Dec/18/code-proven-to-work/about/#disclosures)
* [Colophon](https://simonwillison.net/2025/Dec/18/code-proven-to-work/about/#about-site)
* ©
* [2002](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2002/)
* [2003](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2003/)
* [2004](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2004/)
* [2005](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2005/)
* [2006](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2006/)
* [2007](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2007/)
* [2008](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2008/)
* [2009](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2009/)
* [2010](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2010/)
* [2011](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2011/)
* [2012](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2012/)
* [2013](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2013/)
* [2014](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2014/)
* [2015](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2015/)
* [2016](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2016/)
* [2017](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2017/)
* [2018](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2018/)
* [2019](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2019/)
* [2020](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2020/)
* [2021](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2021/)
* [2022](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2022/)
* [2023](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2023/)
* [2024](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2024/)
* [2025](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2025/)
* [2026](https://simonwillison.net/2025/Dec/18/code-proven-to-work/2026/)