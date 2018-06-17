# List of User Agent Strings in Machine Readable Formats

Are you looking for an enormous list of various User Agents, which you could use for your project? Maybe even in some very specific format as array or list in your favorite programming language? Well, then you have come into the right place.

**This repository contains**:

* JSON list of User Agents (...)[githublink-placeholder]
* Python list of User Agents (...)[githublink-placeholder]
* xxx...

## How to use these files

First two lines of each file are a commentary and one-liner ready to be copied directly to your project. One-liner is typically stored within a `user_agents_list` variable. It looks like this:

```[javascript]
// Unfiltered structure, one-liner assigned to variable user_agents_list
var user_agents_list = ["User agent string 1", "User agent string 2", ...]
```

If commentary is not applicable (in JSON for example), then it is omitted. 

After first two lines and two line breaks, human readable structure assigned to `user_agents_list_pretty` variable follows. It may look something like this:

```[javascript]
// Unfiltered structure, contents prettyfied
var user_agents_list_pretty = [
    "Mozilla/5.0 (compatible; U; ABrowse 0.6; Syllable) AppleWebKit/420+ (KHTML, like Gecko)",
    "Mozilla/5.0 (compatible; U; ABrowse 0.6;  Syllable) AppleWebKit/420+ (KHTML, like Gecko)",
    "..."
]
```

You can either download and include desired file in your project directly, or you can just copy-paste the part that you are interested in, be it a one-liner or human readable formatted data structure.

## How it works

There is this one awesome page, [User Agent String.com](http://useragentstring.com), which contains a huge list of various User Agents. I wrote a simple python script that will scrape the page and retrieve list of user agents, which it subsequently writes to output files as data structures in various programming languages. You can then come here, and copy paste these to your projects and simply work withe them from there.

**Possible future todos**: Output files could contain categorized data structures to enable you to choose only a specific type of user agents (for example all non-bot/non-crawler user agents). 
