# Glossary of Terms 1984
From: [[doc/XanaduSDF1984OCR.pdf]] 

This document is a comprehensive glossary of all the new terms introduced in the Xanadu documents. Terms are listed in alphabetical order, followed by their definitions. Little effort has been made to avoid circular definitions: for more complete explanations, read the relevant documents. Etymological notes are given in some cases for historical value and the amusement of the reader. These are enclosed in round brackets  changed from square brackets ("[" and "]") in the source as it makes it easier with Markdown. This is Obsidian-flavoured Markdown, except for the use of the currently unstandardized definition list construct. The caret plus identifiers at the end of some paragraphs (eg. "^bottom-crum") are Obsidian block anchor syntax.

append
: One of the fundamental operations on enfilades. Adds new data items to an enfilade at the "end" of some dimension of index space.  ^append

atom
: One of the fundamental primitive entities that the Xanadu System deals with. There are two types of atoms: characters and orgls.  ^atom

backend
: The component of a Xanadu System responsible for managing the actual storage and retrieval of atoms. ^backend

bert
: A locking identifier associated with the top of an orgl. Identifies the particular version of an orgl being dealt with when that orgl has been changed but not assigned a permanent address. Also prevents deadlock between processes by allowing concurrent access to documents. (Berts are named after Bertrand Russell, because they represent a fanatical effort to keep things consistent.) ^bert

bottom crum
: A crum at the bottom level of an enfilade. May be different regular crums since it may contain actual data that the upper crums do not contain. ^bottom-crum

core
: The term we prefer for a computer's local high-speed random access memory. (We like the term "core" even though it is archaic because 1) the term IlRAMII is misleading, since disk is random access too: 2) the term "semiconductor memory" is as implementation technology specific and as likely to eventually become archaic, as well as being an unwieldy mouthful of words; 3) the term "core" is short, pithy and easy to remember; 4) everybody knows what you mean anyway.) ^core

core/disk memory model
: The memory model used in the Xanadu System architecture which assumes a limited amount of high speed core memory coupled with large quantities of disk storage. ^core-disk-memory-model

crum
: A "node" (in the traditional sense of the term) in an enfiladic data structure. Contains the wid and disp. (Named after a river in Pennsylvania on the banks of which the crum was invented. Also an acronym for "Chickens Running Under Mud" (don't ask).) Crums are collected into loafs. ^crum

crum-block
: A loaf. Usually used in the context of packing large numbers of crams together in a disk block for long-term storage. ^crum-block

cut
: One of the fundamental operations on enfilades. Makes splits in the data structure for purposes of insertion, deletion or rearrangement. Cut is also a noun referring to a split made in the data structure by the cut operation. ^cut

data disp
: A disp whose purpose is not the location of items in index space but rather the implicit containment of data itself. ^data-disp

<!-- Apr 25 12:47 1984 -- XII -- Glossary of Xanadu Terms -- Page 2 -->

data wid
: A wid whose purpose is not the location of items in index space but rather the implicit containment of data itself. A data wid is generally an abstraction or generalization of all the data stored beneath its crum. ^data-wid

data widdative function
: A function for computing a crum's data wid from the wids and disps of its children. ^data-widdative-function

delete
: One of the basic operations on enfilades. Removes material from a specified portion of the data structure. ^delete

disk
: The term we prefer for a computer's lower-speed high volume storage. (The term "disk", like "core", is preferred because of its simplicity and brevity, though it may not be totally accurate.) ^disk

disp
: One of the two principal components of a crum (the other being the wid). Indicates the crum's displacement in index space relative to its parent crum. ("Disp" is short for "displacement" but has come to be its own term, rather than an abbreviation, since in some sorts of index spaces it may not be a displacement per se.) ^disp

DIV poom
: An extended form of the poomfilade that adds an additional dimension to represent orgl-of-origin. ("DIV" stands for "Document-Invariant-Variant", the three dimensions of the DIV poom. Document is a historical term for one conventional type of orgl.) ^div-poom

document
: One of the standard types of orgls in a literature-based xanadu application. A document is an orgl with two V-spaces: a "text space" and a "link space". ^document

drexfilade
: An improved model of the spanmap.  (Named after Eric Drexler, the person who invented it.) ^drexfilade

end-set
: Generic term for the collections of V-spans connected by a link. (The most simplified notion of a link is as a "magic piece of string" from one piece of data to another. End-sets are what are found at the ends of the string.) ^end-set

enfilade
: One of a family of data structures characterized by being constant depth trees with wids and disps, rearrangability and the capacity for sub-tree sharing. ^enfilade

footnote link
: One of any number of possible standard link types. Represents a footnote. ^footnote-link

four-cut rearrange
: One of two "flavors" of rearrange operation. Four cuts are made in the enfilade and the material between the first two is swapped with the material between the second two. ^four-cut-rearrange

from-set
: The first end-set of a link. Contains the set of V-spans at the starting end of the directed connection represented by a link. ^from-set

frontend
: The component of the Xanadu System responsible for user interface and any functions which depend upon the content of the data stored in the backend (e.g., keyword searches). ^frontend

<!-- Apr 25 12:47 1984 -- XII -- Glossary of Xanadu Terms -- Page 3 -->

frontend-backend interface
: The frontend and the backend communicate with each other in an interface language called Phoebe over some sort of communications line or I/O port. The frontend asks the backend to do things for it and the backend responds to these requests via the frontend-backend interface. ^frontend-backend-interface

fulcrum
: The very topmost crum of an enfilade, from which all other crums are descended. (So called because it "contains" the full enfilade beneath it. Also, enfilades are frequently illustrated graphically as broad based isoceles triangles with the fulcrum at the peak (which does look like a fulcrum).) ^fulcrum

grandmap
: One of the primary components of the system. Maps from I-stream addresses to the physical locations where the corresponding atoms are stored. ^grandmap

granfilade
: One of the primary data structures in the system. Used to implement the grandmap. ("Granfilade" implies "grand enfilade". It is the largest single data structure, in the sense that it "contains" everything stored in the system.) ^granfilade

historical trace
: A more advanced (as yet unimplemented) facility of the Xanadu System which enables the state of an orgl at any point in its edit history to be determined. ^historical-trace

historical trace enfilade
: The enfilade with stores the history of a phylum so that the state of any of its orgls at any time may be reconstructed. ^historical-trace-enfilade

historical trace tree
: The branching pattern of changes and versions made to a phylum over time. ^historical-trace-tree

humber
: A form of infinite precision integer that can represent any number in a reasonably sized space. ("Humber" is derived from "Huffman encoded number". ) ^humber

index disp
: A disp whose primary purpose is the location and identification of data items, as opposed to a data disp. ^index-disp

index space
: The space in which an enfilade "lives". Locations in this space are used as the index values identifying things to retrieve and the places to make cuts. An index space may have multiple dimensions, where a dimension is defined in our context as simply a separable component of indexing information which may be used by itself in a sensible fashion to (perhaps only partially) identify or locate something. ^index-space

index wid
: A wid whose primary purpose is the location and identification of data items, as opposed to a data wid. ^index-wid

index widdative function
: A function that computes a crums index wid from the wids and disps of that crums children. ^index-widdative-function

insert
: One of the basic operations on enfilades. Adds material at some specified location in the data structure. This operation is redundant since it may be implemented by an append followed by a rearrange. ^insert

<!-- Apr 25 12:.7 1984 -- XII -- Glossary of Xanadu Terms -- Page 4 -->

invariant orgl identifier
: A tumbler which is both a V-stream address and an I-stream address which identifies a "top" level orgl (i.e., one that is directly accessible from the external world rather than being retrieved as the contents of some other orgl. ^invariant-orgl-identifier

invariant part
: The portion of a V-stream address which constitutes an invariant orgl identifier that identifies the orgl which maps the V-stream address to some I-stream address. It is a syntactically separable part of a V-stream address. ^invariant-part

invariant stream
: The address space in which atoms are stored. When initially placed in the system, each atom is assigned to the next available space on the invariant stream. ^invariant-stream

I-span
: A span of atoms on the I-stream. Consists of a starting position together with a length. The term "I-span" is variously used to refer to the addresses in such a span or to the atoms themselves, depending upon context. ^i-span

I-stream
: Abbreviation for "Invariant stream". Used acre commonly than the longer term. ^i-stream

I-stream address
: A location on the I-stream. ^i-stream-address

I-stream order
: The order in which atoms appear on the I-stream. ^i-stream-order

I-to-V mapping
: The correspondence between I-stream addresses and V-stream addresses which is represented by an orgl. ^i-to-v-mapping

jump link
: One of any number of possible standard link types. Represents the simplest possible connection from one place to another. ^jump-link

level pop
: one of the fundamental operations on enfilades. Makes the data structure smaller (in both actual and potential size) by removing a redundant fulcrum. ^level-pop

level push
: One of the fundamental operations on enfilades. Enlarges the potential size of the data structure by adding a level on top of the fulcrum. ^level-push

link
: One of the standard types of orgls in a literature-based Xanadu application. A link is an orgl with three V-spaces called "end-sets": the "from-set", the "to-set" and the "three-set". ^link

link space
: The V-space of a document orgl which contains links. ^link-space

loaf
: A group of crums together. Generally used in the context of the group of sibling crums that are the set children of some other crum. (A loaf is of course what you get when you pack a bunch of crum(b)s together.) ^loaf

marginal note link
: One of any number of possible standard link types. Represents the connection to a "marginal note". ^marginal-note-link

N-dimensional enfilade 
: A family of enfilades whose index spaces are N-dimensional euclidean spaces indexed by Cartesian coordinates. ^n-dimensional-enfilade

<!-- Apr 25 12:41 1984 -- XII -- Glossary of Xanadu Terms -- Page 5 -->

node 
: A computer in a distributed processing and data storage network. ^node

orgl 
: One of the primary data structures in the system. Maps from V-stream addresses to I-stream addresses and vice-versa. ("Orgl" is short for "ORGanizationaL thingie".)  ^orgl

Phoebe
: The name of the frontend-backend interface language. (Phoebe 1s derived from "fe-be" which in turn is short for "frontend-backend".) ^phoebe

phylum
: The collective group of orgls represented by an historical trace tree. (The term "phylum" denotes a tree-like family structure. It also sounds vaguely like "file".) ^phylum

POOM
: A permutation-matrix-like mapping which is implemented by the poomfilade. Used to represent orgls. ("POOM" stands for "Permutations On Ordering Matrix".) ^poom

poomfilade
: The enfilade used to represent POOMs and therefore orgls. ^poomfilade

process
: A particular connection to the backend that may request the storage or retrieval of characters and orgls. ^process

quote link
: One of any number of possible standard link types. Represents a quotation. ^quote-link

rearrangability
: One of the properties of enfilades. Rearrangability means that pieces can be reorganized on one level of the tree and descendant levels will automatically be reorganized accordingly. 

rearrange
: One of the fundamental operations on enfilades. Changes the order in index space of material. There are two types of rearrange operation called "three-cut rearrange" and "four-cut rearrange". ^rearrangability

recombine
: One of the fundamental operations on enfilades. "Heals" cuts and compacts the data structure after it has been fragmented by other operations. ^recombine

retrieve
: One of the fundamental operation on enfilades. Obtains the data item associated with a particular location in index space. ^retrieve

span
: A contiguous collection of things, usually characters. Usually represented as a starting address together with a length. The term is also sometimes used to refer to the length itself (as in "what is the span of this document?"). ^span

spanfilade
: One of the primary data structures in the system. Used to implement the spanmap. ("Spanfilade" implies "enfilade for dealing with spans".) ^spanfilade

spanmap
: One of the primary components of the system. Maps from the I-stream addresses of atoms in general to the I-stream addresses of orgls referencing those atoms. ^spanmap

sub-tree
: Some portion of an enfilade denoted by a crum and all of its descendants. A sub-tree is itself an enfilade with the crum its peak as the fulcrum. ^sub-tree

<!-- Apr 25 12:47 1984 -- XII -- Glossary of Xanadu Terms -- Page 6 -->

sub-tree sharability
: One of the properties of enfilades. Sub-tree sharability means that sub-trees can be shared between enfilades or between different parts of the same enfilade in a manner that is transparent to the fundamental operations that can be performed. ^sub-tree-sharability

sub-tree sharing
: The act of taking advantage of sub-tree sharability. ^sub-tree-sharing

text space
: The V-space of a document orgl which contains character atoms. ^text-space

three-cut rearrange
: One of two "flavors" of rearrange operation. Three cuts are made in the enfilade. The material between the first and second cuts is swapped with the material between the second and third cuts. This can also be seen as moving the material found between the first and second cuts to the location defined by the third cut, etc. ^three-cut-rearrange

three-set
: The third end-set of a link. Contains material the addresses or contents of which indicate something about the nature or type of the link. (The term is a pun, counting the end-sets "from, to, three" (one, two, three).) ^three-set

to-set
: The second end-set of a link. Contains the set of V-spans at the terminating end of the directed connection represented by a link.  ^to-set

tumbler
: The type of number used to address things inside the Xanadu System. A tumbler is a transfinitesimal number represented as a string of integers, for example "1.0.3.2.0.96.2.0.1.137". ("Tumbler" is sort of a contraction for "transfinitesimal humber".) ^tumbler

tumbler addition
: A form of non-commutative addition defined on tumblers for purposes of, among other things, implementing the fI.+." operator for enfilades constructed in tumbler space. ^tumbler-addition

upper crum
: A non-bottom crum. ^upper-crum

variant part
: The portion of a V-stream address which identifies a particular location inside the orgl identified by the invariant part. It is a syntactically separable part of a V-stream address. ^variant-part

variant stream
: The address space in which, to the outside world, atoms appear to be stored. Also called the "virtual stream" or "V-stream". (See "V-stream".] ^variant-stream

version
: An alternate form for some orgl, representing a past, future or current-but-different organization for the same body of material. ^version

versioning
: The process of storing alternate organizations for a given body of material by constructing multiple enfilades which use sub-tree sharing for the portions where they are the same. ^versioning

virtual copy
: 1. A copy of some set of atoms made not by duplicating the atoms but by mapping additional V-stream locations onto the atoms I I-stream locations. 2. Duplication of some portion of a data structure by using sub-tree sharing rather than by actually copying the material stored. ^virtual-copy

<!-- Apr 25 12:41 1984 -- XII -- Glossary of Xanadu Terms -- Page 7 -->
 
virtuality
: The "seeming" of something. "Virtuality" is to "reality" as "virtual" is to "real". (Virtuality is one of innumerable terms coined by Ted Nelson. Since it is a useful concept, the term has stuck with us.) ^virtuality

virtual space
: A separately addressable sub-region of an orgl. An orgl may have any number of virtual spaces. ^virtual-space

virtual stream
: The address space in which, to the outside world, atoms appear to be stored. Also called the "variant stream" or "V-stream". [[#^v-stream|(See "V-stream".)]] ^virtual-stream

virtual stream address
: A location on the virtual stream. ^virtual-stream-address

V-space
: Short for "virtual space". ^v-space

V-span
: A span on the V-stream. ^v-span

V-stream
: Short for "virtual stream" or "variant stream". (The "V" variously stands for "virtual" or "variant" because of the trade secret status of much of the Xanadu internals: "Virtual" is the public term, referring tc the order in which things appear to the outside world. "Variant" is the private term, referring to the relationship between the Variant (i.e., changing) order that is shown to the world and the Invariant (i.e., not changing) order in which things are actually stored.) ^v-stream

V-stream address
: Short for "virtual stream address". ^v-stream-address

V-stream order
: The order in which atoms appear on the V-stream. ^v-stream-order

V-to-I mapping
: The correspondence between V-stream addresses and I-stream addresses which is represented by an orgl. ^v-to-i-mapping

wid
: One of the two principal components of a crum (the other being the disp). Indicates the cram's width in index space (i.e., the volume of index space spanned by its children). ()"Wid" is short for "width" but has come to be its own term, rather than an abbreviation, since in some sorts of index spaces it may not be a width per se.) ^wid

widdative function
: The function, characteristic of any particular type of enfilade, which computes a crum's wid from the wids and disps of its children. A notable property of the widdative function is that it is associative. ^widdative-function

Xanadu
: The name of our favorite hypertext system. (Taken from the poem by Samuel Taylor Coleridge about a mythical paradise constructed by Kubla Khan.) ^xanadu

.\==.
: Notation for operator that tests for the "equality" of two index space locations . ^index-equality-test

.<.
: Notation for operator that tests whether one index space location "precedes" another. ^index-precedes-test

<!-- Apr 25 12:47 1984 -- XII -- Glossary of Xanadu Terms -- Page 8 -->

.<=.
: Notation for operator that tests whether one index space location is "less than or equal to" another. ^index-lessthanequal-test

.+.
: Notation for index space "addition" operator.  ^index-addition-operator

.-.
: Notation for index space "subtraction" operator.  ^index-subtraction-operator

.0.
: Notation for the origin of the index space . ^index-origin