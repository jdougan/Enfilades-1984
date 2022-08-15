# Enfilades-1984
Several Python 3 implementations of Enfilades.
Currently there is just one implementation, but the plan is to do more later (Model-T, Implicit Data, etc.)
As the source and documentation I've generated this from is under MIT license, this is also.

## Grant Application
`enfilade-grant.py` is based on the description in the [Xanadu Operating Company's 1984 grant application to the System Development Foundation (SDF)](doc/XanaduSDF1984OCR.pdf).
Note that some of the pseudo-code samples there don't actually work.
Chip Morningstar claims they are just mistakes as they were trying to show everything to justify the grant, so my earlier theories about deliberate mistakes to keep trade secrets are just wrong.
I've tried to debug them based on the declared intent, but I may have misunderstood.
Functions that are suffixed with "Grant" are straight translations of the pseudo-code that are broken.
The code is intended for pedagogical purposes and I make no efficiency or universality guarantees; or for that matter it being at all idiomatic Python.
What I have tried to do is convert some of the idiosyncratic Xanadu terminology into modern terminology.

The tests are in `grant-test.py` and currenty do not test cuts, recombines or rearranges.

### Issues
* does weird things with zero (.0.) keys, seems they should not be used, but no mention of this or error checking.
* Unclear what empty and single element enfilades
 should be like.
* There are a couple possible ways to reconstruct retrieve(), not sure what was intended.
* Node splitting in append is getting disps wrong in the new node.

### Sources 
* Announcement of finding the grant app front mattter with the curse: http://habitatchronicles.com/2006/06/things-you-find-while-cleaning-your-office/
* Announcement of finding the grant app: http://habitatchronicles.com/2019/03/a-lost-treasure-of-xanadu/
    * [Local copy of original PDF](doc/XanaduSDF1984OCR.pdf)
* Announcement of HTML formatting: https://sentido-labs.com/en/library/#xanadu-1986
* [Online HTML formatting of grant proposal](https://sentido-labs.com/en/library/201904240732/Xanadu%20Hypertext%20Documents.html)
    * [Online DocBook source](Xanadu%20Hypertext%20Documents-20220801.xml)
    * [Local HTML copy as of 2022-08-01](XHD-20220801/Xanadu%20Hypertext%20Documents.htm)
    * [Local DocBook source copy as of 2022-08-01](Xanadu%20Hypertext%20Documents-20220801.xml)
    * [Local MHTML copy as of 2022-08-01](doc/XHD-20220801.mhtml)
  
### Terms Substituted
This terminology is mostly Xanadu Green/xu88.1 specific.
Gold/xu92.1 walked back a lot of the Green terminology as well as generating some of its own.

A cleaned up Markdown version of the complete glossary in [[doc/XanaduSDF1984OCR.pdf]] is in [[doc/Glossary-1984.md]].

* crum
    * (tree) node
* loaf
    * child-block
    * children
    * It was split out so I/O packing behavior could be specified.
* wid
    * width
* dsp, disp
    * displacement, position, delta
    * These are keys that are relative to the parent node 
* enwidify()
    * calculateWidth()
* index
    * key
* thing
    * domain
* adopt, disown
	* addChild, removeChild
	* Haven't decided to changed code refs yet.
* childSet
    * Not a set.
    * A pair of nodes, labelled left and right
    * used to carry a cut result for splicing
* cutSet
    * Also not a set.
    * Sorted collection of keys specifying where the enfilade should split nodes, ordered by .<. / keyLessThan().
    * These get modified in place during the cut, but not resorted.

One of the reasons they used the names wids and dsps (besides for abbreviation) is because they connote a specific set of mathematical properties that the enfilade depends on, and functions and types with these properties may not involve actual widths or displacements.
They thought introducing new terminology would be clearer as it comes with no expectations.

## Model-T
To be determined.

## Implicit 2D
To be determined.


