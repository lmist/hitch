# [Simon Willison’s Weblog](/)

[Subscribe](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/about/#subscribe) 

**Sponsored by:** [WorkOS](https://fandf.co/4v8pTAt) — Production-ready APIs for auth and access control, so you can ship faster.

## Running OCR against PDFs and images directly in your browser

30th March 2024

I attended the [Story Discovery At Scale](https://biglocalnews.org/content/events/) data journalism conference at Stanford this week. One of the perennial hot topics at any journalism conference concerns data extraction: how can we best get data out of PDFs and images?

I’ve been having some very promising results with Gemini Pro 1.5, Claude 3 and GPT-4 Vision recently—I’ll write more about that soon. But those tools are still inconvenient for most people to use.

Meanwhile, older tools like [Tesseract OCR](https://github.com/tesseract-ocr/tesseract) are still extremely useful—if only they were easier to use as well.

Then I remembered that Tesseract runs happily in a browser these days thanks to the excellent [Tesseract.js](https://tesseract.projectnaptha.com/) project. And PDFs can be processed using JavaScript too thanks to Mozilla’s extremely mature and well-tested [PDF.js](https://mozilla.github.io/pdf.js/) library.

So I built a new tool!

**[tools.simonwillison.net/ocr](https://tools.simonwillison.net/ocr)** provides a single page web app that can run Tesseract OCR against images or PDFs that are opened in (or dragged and dropped onto) the app.

Crucially, everything runs in the browser. There is no server component here, and nothing is uploaded. Your images and documents never leave your computer or phone.

Here’s an animated demo:

![First an image file is dragged onto the page, which then shows that image and accompanying OCR text. Then the drop zone is clicked and a PDF file is selected - that PDF is rendered a page at a time down the page with OCR text displayed beneath each page.](https://static.simonwillison.net/static/2024/ocr-demo.gif)

It’s not perfect: multi-column PDFs (thanks, academia) will be treated as a single column, illustrations or photos may result in garbled ASCII-art and there are plenty of other edge cases that will trip it up.

But... having Tesseract OCR available against PDFs in a web browser (including in Mobile Safari) is still a really useful thing.

#### How I built this [#](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2024/Mar/30/ocr-pdfs-images/#ocr-how-i-built-this)

_For more recent examples of projects I’ve built with the assistance of LLMs, see [Building and testing C extensions for SQLite with ChatGPT Code Interpreter](https://simonwillison.net/2024/Mar/23/building-c-extensions-for-sqlite-with-chatgpt-code-interpreter/) and [Claude and ChatGPT for ad-hoc sidequests](https://simonwillison.net/2024/Mar/22/claude-and-chatgpt-case-study/)._

I built the first version of this tool in just a few minutes, using Claude 3 Opus.

I already had my own JavaScript code lying around for the two most important tasks: running Tesseract.js against an images and using PDF.js to turn a PDF into a series of images.

The OCR code came from the system I built and explained in [How I make annotated presentations](https://simonwillison.net/2023/Aug/6/annotated-presentations/) (built with the help of [multiple ChatGPT sessions](https://simonwillison.net/2023/Aug/6/annotated-presentations/#chatgpt-sessions)). The PDF to images code was from an [unfinished experiment](https://gist.github.com/simonw/e58796324abb0e729b2dcd351f46728a#prompt-2) which I wrote with the aid of Claude 3 Opus a week ago.

I composed the following prompt for Claude 3, where I pasted in both of my code examples and then added some instructions about what I wanted it to build at the end:

> This code shows how to open a PDF and turn it into an image per page:
> 
> <!DOCTYPE html>
> <html>
> <head>
>  <title>PDF to Images</title>
>  <script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.9.359/pdf.min.js"></script>
>  <style>
>    .image-container img {
>      margin-bottom: 10px;
>    }
>    .image-container p {
>      margin: 0;
>      font-size: 14px;
>      color: #888;
>    }
>  </style>
> </head>
> <body>
>  <input type="file" id="fileInput" accept=".pdf" />
>  <div class="image-container"></div>
> 
>  <script>
>  const desiredWidth = 800;
>    const fileInput = document.getElementById('fileInput');
>    const imageContainer = document.querySelector('.image-container');
> 
>    fileInput.addEventListener('change', handleFileUpload);
> 
>    pdfjsLib.GlobalWorkerOptions.workerSrc = 'https://cdnjs.cloudflare.com/ajax/libs/pdf.js/2.9.359/pdf.worker.min.js';
> 
>    async function handleFileUpload(event) {
>      const file = event.target.files[0];
>      const imageIterator = convertPDFToImages(file);
> 
>      for await (const { imageURL, size } of imageIterator) {
>        const imgElement = document.createElement('img');
>        imgElement.src = imageURL;
>        imageContainer.appendChild(imgElement);
> 
>        const sizeElement = document.createElement('p');
>        sizeElement.textContent = `Size: ${formatSize(size)}`;
>        imageContainer.appendChild(sizeElement);
>      }
>    }
> 
>    async function* convertPDFToImages(file) {
>      try {
>        const pdf = await pdfjsLib.getDocument(URL.createObjectURL(file)).promise;
>        const numPages = pdf.numPages;
> 
>        for (let i = 1; i <= numPages; i++) {
>          const page = await pdf.getPage(i);
>          const viewport = page.getViewport({ scale: 1 });
>          const canvas = document.createElement('canvas');
>          const context = canvas.getContext('2d');
>          canvas.width = desiredWidth;
>          canvas.height = (desiredWidth / viewport.width) * viewport.height;
>          const renderContext = {
>            canvasContext: context,
>            viewport: page.getViewport({ scale: desiredWidth / viewport.width }),
>          };
>          await page.render(renderContext).promise;
>          const imageURL = canvas.toDataURL('image/jpeg', 0.8);
>          const size = calculateSize(imageURL);
>          yield { imageURL, size };
>        }
>      } catch (error) {
>        console.error('Error:', error);
>      }
>    }
> 
>    function calculateSize(imageURL) {
>      const base64Length = imageURL.length - 'data:image/jpeg;base64,'.length;
>      const sizeInBytes = Math.ceil(base64Length * 0.75);
>      return sizeInBytes;
>    }
> 
>    function formatSize(size) {
>      const sizeInKB = (size / 1024).toFixed(2);
>      return `${sizeInKB} KB`;
>    }
>  </script>
> </body>
> </html>
> 
> This code shows how to OCR an image:
> 
> async function ocrMissingAltText() {
>    // Load Tesseract
>    var s = document.createElement("script");
>    s.src = "https://unpkg.com/tesseract.js@v2.1.0/dist/tesseract.min.js";
>    document.head.appendChild(s);
> 
>    s.onload = async () => {
>      const images = document.getElementsByTagName("img");
>      const worker = Tesseract.createWorker();
>      await worker.load();
>      await worker.loadLanguage("eng");
>      await worker.initialize("eng");
>      ocrButton.innerText = "Running OCR...";
> 
>      // Iterate through all the images in the output div
>      for (const img of images) {
>        const altTextarea = img.parentNode.querySelector(".textarea-alt");
>        // Check if the alt textarea is empty
>        if (altTextarea.value === "") {
>          const imageUrl = img.src;
>          var {
>            data: { text },
>          } = await worker.recognize(imageUrl);
>          altTextarea.value = text; // Set the OCR result to the alt textarea
>          progressBar.value += 1;
>        }
>      }
> 
>      await worker.terminate();
>      ocrButton.innerText = "OCR complete";
>    };
>  }
> 
> Use these examples to put together a single HTML page with embedded HTML and CSS and JavaScript that provides a big square which users can drag and drop a PDF file onto and when they do that the PDF has every page converted to a JPEG and shown below on the page, then OCR is run with tesseract and the results are shown in textarea blocks below each image.

I saved this prompt to a `prompt.txt` file and ran it using my [llm-claude-3](https://github.com/simonw/llm-claude-3) plugin for [LLM](https://llm.datasette.io/):

llm -m claude-3-opus < prompt.txt

It gave me [a working initial version](https://static.simonwillison.net/static/2024/pdf-ocr-v1.html) on the first attempt!

![A square dotted border around the text Drag and drop PDF file here](https://static.simonwillison.net/static/2024/ocr-v1.jpg)

[Here’s the full transcript](https://gist.github.com/simonw/6a9f077bf8db616e44893a24ae1d36eb), including my follow-up prompts and their responses. Iterating on software in this way is _so_ much fun.

First follow-up:

> Modify this to also have a file input that can be used—dropping a file onto the drop area fills that input
> 
> make the drop zone 100% wide but have a 2em padding on the body. it should be 10em high. it should turn pink when an image is dragged over it.
> 
> Each textarea should be 100% wide and 10em high
> 
> At the very bottom of the page add a h2 that says Full document—then a 30em high textarea with all of the page text in it separated by two newlines

[Here’s the interactive result](https://static.simonwillison.net/static/2024/pdf-ocr-v2.html).

![A PDF file is dragged over the box and it turned pink. The heading Full document displays below](https://static.simonwillison.net/static/2024/ocr-v2.jpg)

Rather delightfully it used the neater pattern where the file input itself is hidden but can be triggered by clicking on the large drop zone, and it updated the copy on the drop zone to reflect that—without me suggesting those requirements.

And then:

> get rid of the code that shows image sizes. Set the placeholder on each textarea to be Processing... and clear that placeholder when the job is done.

[Which gave me this](https://static.simonwillison.net/static/2024/pdf-ocr-v3.html).

I realized it would be useful if it could handle non-PDF images as well. So I fired up ChatGPT (for no reason other than curiosity to see how well it did) and got GPT-4 to add that feature for me. I [pasted in the code so far and added](https://chat.openai.com/share/665eca31-3b5d-4cd9-a3cb-85ab608169a6):

> Modify this so jpg and png and gif images can be dropped or opened too—they skip the PDF step and get appended to the page and OCRd directly. Also move the full document heading and textarea above the page preview and hide it u til there is data to be shown in it

Then I spotted that the Tesseract worker was being created multiple times in a loop, which is inefficient—so I prompted:

> Create the worker once and use it for all OCR tasks and terminate it at the end

I’d tweaked the HTML and CSS a little before feeding it to GPT-4, so now the site had a title and rendered in Helvetica.

Here’s [the version GPT-4 produced for me](https://static.simonwillison.net/static/2024/pdf-ocr-v4.html).

![A heading reads OCR a PDF or Image - This tool runs entirely in your browser. No files are uploaded to a server. The dotted box now contains text that reads Drag and drop a PDF, JPG, PNG, or GIF file here or click to select a file](https://static.simonwillison.net/static/2024/ocr-v4.jpg)

#### Manual finishing touches [#](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2024/Mar/30/ocr-pdfs-images/#ocr-finishing-touches)

Fun though it was iterating on this project entirely through prompting, I decided it would be more productive to make the finishing touches myself. You can see those [in the commit history](https://github.com/simonw/tools/commits/cc609194a0d0a54c2ae676dae962e14b3e3a9d22/). They’re not particularly interesting:

* I added [Plausible](https://plausible.io/) analytics (which I like because they use no cookies).
* I added better progress indicators, including the text that shows how many pages of the PDF have been processed so far.
* I bumped up the width of the rendered PDF page images from 800 to 1000\. This seemed to improve OCR quality—in particular, the [Claude 3 model card PDF](https://www-cdn.anthropic.com/de8ba9b01c9ab7cbabf5c33b80b7bbc618857627/Model%5FCard%5FClaude%5F3.pdf) now has less OCR errors than it did before.
* I upgraded both Tesseract.js and PDF.js to the most recent versions. Unsurprisingly, Claude 3 Opus had used older versions of both libraries.

I’m really pleased with this project. I consider it _finished_—it does the job I designed it to do and I don’t see any need to keep on iterating on it. And because it’s all static JavaScript and WebAssembly I expect it to continue working effectively forever.

**Update:** OK, a few more features: I added [language selection](https://github.com/simonw/tools/issues/4), [paste support](https://github.com/simonw/tools/issues/7) and some [basic automated tests](https://github.com/simonw/tools/issues/8) using Playwright Python.

Posted [30th March 2024](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2024/Mar/30/) at 5:59 pm · Follow me on [Mastodon](https://fedi.simonwillison.net/@simon), [Bluesky](https://bsky.app/profile/simonwillison.net), [Twitter](https://twitter.com/simonw) or [subscribe to my newsletter](https://simonwillison.net/about/#subscribe)

## More recent articles

* [The Axios supply chain attack used individually targeted social engineering](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2026/Apr/3/supply-chain-social-engineering/) \- 3rd April 2026
* [Highlights from my conversation about agentic engineering on Lenny's Podcast](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2026/Apr/2/lennys-podcast/) \- 2nd April 2026
* [Mr. Chatterbox is a (weak) Victorian-era ethically trained model you can run on your own computer](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2026/Mar/30/mr-chatterbox/) \- 30th March 2026

This is **Running OCR against PDFs and images directly in your browser** by Simon Willison, posted on [30th March 2024](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2024/Mar/30/).

Part of series **[How I use LLMs and ChatGPT](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/series/using-llms/)**

1. [Claude and ChatGPT for ad-hoc sidequests](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2024/Mar/22/claude-and-chatgpt-case-study/) \- March 22, 2024, 7:44 p.m.
2. [Building and testing C extensions for SQLite with ChatGPT Code Interpreter](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2024/Mar/23/building-c-extensions-for-sqlite-with-chatgpt-code-interpreter/) \- March 23, 2024, 5:50 p.m.
3. [llm cmd undo last git commit - a new plugin for LLM](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2024/Mar/26/llm-cmd/) \- March 26, 2024, 3:37 p.m.
4. **Running OCR against PDFs and images directly in your browser** \- March 30, 2024, 5:59 p.m.
5. [Building files-to-prompt entirely using Claude 3 Opus](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2024/Apr/8/files-to-prompt/) \- April 8, 2024, 8:40 p.m.
6. [AI for Data Journalism: demonstrating what we can do with this stuff right now](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2024/Apr/17/ai-for-data-journalism/) \- April 17, 2024, 9:04 p.m.
7. [Building search-based RAG using Claude, Datasette and Val Town](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2024/Jun/21/search-based-rag/) \- June 21, 2024, 8:44 p.m.
8. [… more](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/series/using-llms/)

[ data-journalism76 ](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/tags/data-journalism/) [ ocr25 ](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/tags/ocr/) [ pdf39 ](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/tags/pdf/) [ projects523 ](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/tags/projects/) [ tesseract3 ](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/tags/tesseract/) [ ai-assisted-programming370 ](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/tags/ai-assisted-programming/) 

**Next:** [Building files-to-prompt entirely using Claude 3 Opus](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2024/Apr/8/files-to-prompt/)

**Previous:** [llm cmd undo last git commit - a new plugin for LLM](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2024/Mar/26/llm-cmd/)

###  Monthly briefing

 Sponsor me for **$10/month** and get a curated email digest of the month's most important LLM developments.

 Pay me to send you less!

[ Sponsor & subscribe](https://github.com/sponsors/simonw/) 

* [Disclosures](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/about/#disclosures)
* [Colophon](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/about/#about-site)
* ©
* [2002](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2002/)
* [2003](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2003/)
* [2004](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2004/)
* [2005](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2005/)
* [2006](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2006/)
* [2007](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2007/)
* [2008](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2008/)
* [2009](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2009/)
* [2010](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2010/)
* [2011](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2011/)
* [2012](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2012/)
* [2013](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2013/)
* [2014](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2014/)
* [2015](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2015/)
* [2016](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2016/)
* [2017](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2017/)
* [2018](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2018/)
* [2019](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2019/)
* [2020](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2020/)
* [2021](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2021/)
* [2022](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2022/)
* [2023](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2023/)
* [2024](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2024/)
* [2025](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2025/)
* [2026](https://simonwillison.net/2024/Mar/30/ocr-pdfs-images/2026/)