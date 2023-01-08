# App Info

toXiv gives arXiv daily new submissions by toots, abstracts
by replies, cross-lists by boosts, and replacements by
toots and boosts.  We use python3 scripts. toXiv is not
affiliated with arXiv.


## Setup

* Install Mastodon.py, pandas, ratelimit, semanticscholar, mastodon, nameparser, and beautifulsoup4. 

	```
	% pip3 install  Mastodon.py pandas ratelimit semanticscholar nameparser beautifulsoup4
	```

* Let toXiv.py be executable.
 
	 ```
	 % chmod +x toXiv.py
	 ```

*  Put the following python scripts in the same directory.

	- toXiv.py
	- toXiv_post.py 	
	- toXiv_format.py
	- toXiv_daily_feed.py 	
	- extended_date_match.py
	- Semantic_Scholar_url.py
	- arXiv_feed_parser.py
	- variables.py


* Configure switches.json, logfiles.json, and aliases.json in the
  tests directory for your settings.

	- accesses.json specifies mastodon access tokens
	and whether to use
	new submissions/abstracts/cross-lists/replacements by toXiv.

    - logfiles.json indicates logfile locations.  You can check their
	formats by samples in the tests/logfiles directory.  toXiv
	needs a toot log file for cross-lists and replacements. 
		
	- aliases.json tells toXiv aliases of arXiv category
    names.  For example, math.IT is an alias of
    cs.IT. Without this file, toXiv of rss feeds returns no
    new submissions, when you take the category name
    math.IT.  If provided, toXiv replaces category names by
    their aliases for new submissions, cross-lists, and
    replacements.
	
* Configure variables.py for your settings. 

   - variables.py assigns format parameters for toXiv toots 
   and access frequencies for arXiv and mastodon.

## Notes

* Outputs of toXiv can differ from arXiv new submission web
  pages.  First, items of arXiv rss feeds are not
  necessarily the same as those of arXiv new submission web
  pages.  Second, arXiv_feed_parser for an arXiv category C
  gives new submissions whose primary subjects are the
  category C.  Then, toXiv for the category C counts and
  toots a new paper whose principal subject matches the
  category C.  This avoids duplicate toots and clarifies
  what toXiv toots, boosts, and unboosts for each paper, as
  toXiv runs on multiple categories.

	- For example, let us assume that there is no new paper whose
	principal subject matches the category C, but there is a
	new paper P whose non-principal subject matches the
	category C. Then, the arXiv new submission web page of
	the category C lists the paper P as a new submission of
	the category C, not as a cross-list.  However, toXiv
	keeps considering the paper P as a cross-list for the
	category C.  Then, the output of toXiv for the category
	C differs from the arXiv new submission web page of the
	category C.

* 	On the use of metadata of arXiv articles, there is the
   web page of [Terms of Use for arXiv
   APIs](https://arxiv.org/help/api/tou). As of the revision
   0.9.5, this says that " You are free to use descriptive
   metadata about arXiv e-prints under the terms of the
   Creative Commons Universal (CC0 1.0) Public Domain
   Declaration." and "Descriptive metadata includes
   information for discovery and identification purposes,
   and includes fields such as title, abstract, authors,
   identifiers, and classification terms."



## Usage

```
% ./toXiv.py -h
usage: toXiv.py [-h] --switches_keys SWITCHES_KEYS
                [--logfiles LOGFILES] [--aliases ALIASES]
                [--captions CAPTIONS] [--mode {0,1}]

arXiv daily new submissions by toots, abstracts by
replies, cross-lists by boosts, and replacements by
toots and boosts.

optional arguments:
  -h, --help            show this help message and exit
  --switches_keys SWITCHES_KEYS, -s SWITCHES_KEYS
                        output switches and api keys in
                        json
  --logfiles LOGFILES, -l LOGFILES
                        log file names in json
  --aliases ALIASES, -a ALIASES
                        aliases of arXiv categories in
                        json
  --captions CAPTIONS, -c CAPTIONS
                        captions of arXiv categories in
                        json
  --mode {0,1}, -m {0,1}
                        1 for mastodon and 0 for stdout
                        only
```

## Sample stdouts


* New submissions for math.CA:

```
%toXiv ./toXiv.py -s var/test_switches.json  -l var/logfiles.json -a var/aliases.json -c var/captions.json -m 1
**process started at 2022-xx-xx xx:xx:xx (UTC)
starting a thread of retrieval/new submissions/abstracts for math.CA
getting daily entries for math.CA
joining threads of retrieval/new submissions/abstracts
new submissions for math.CA

utc: 2022-xx-xx xx:xx:xx
thread arXiv category: math.CA
arXiv id: 
username: @xxxx@xxxx
url: https://xxxx
aim: newsubmission_summary
post method: toot
post mode: 1
url: https://xxxx
text: [2022-xx-xx Sun (UTC), 1 new article found for math.CA Classical Analysis and ODEs]


utc: 2022-xx-xx xx:xx:xx
thread arXiv category: math.CA
arXiv id: xxxx.xxxxx
username: @xxxx@xxxx
url: https://xxxx
aim: newsubmission
post method: toot
post mode: 1
url: https://xxxx
text: xxxxxxxxxxxxxxxxxxxxxx


utc: 2022-xx-xx xx:xx:xx
thread arXiv category: math.CA
arXiv id: xxxx.xxxxx
username: @xxxx@xxxx
url: https://xxxx
aim: abstract
post method: reply
post mode: 1
url: https://xxxx
text:


utc: 2022-xx-xx xx:xx:xx
thread arXiv category: math.CA
arXiv id: xxxx.xxxxx
username: @xxxx@xxxx
url: https://xxxx
aim: abstractp
ost method: reply
post mode: 1
url: https://xxxx
text:


**crosslisting process started at 2022-xx-xx xx:xx:xx (UTC) 
**elapsed time from the start: xx:xx:xx

**replacement process started at 2022-xx-xx xx:xx:xx (UTC)
**elapsed time from the start: xx:xx:xx
**elapsed time from the crosslisting start: xx:xx:xx

**checking replacement entries

**toot-replacement starts

**boost-replacement starts

**process ended at 2022-xx-xx xx:xx:xx (UTC)
**elapsed time from the start: xx:xx:xx
**elapsed time from the crosslisting start: xx:xx:xx
**elapsed time from the replacement start: xx:xx:xx
```

* Without the option ```-c tests/captions.json```above, you get

```
text: [2022-xx-xx Sun (UTC), 1 new article found for math.CA]
```

 instead of

```
text: [2022-xx-xx Sun (UTC), 1 new articles found for math.CA Classical Analysis and ODEs]
```

## Versions

* 0.0.1

  * 2022-05, initial release.

## List of Bots

   - https://mastoxiv.page/@arXiv_csAI_bot : cs.AI Computer Science - Artificial Intelligence
   - https://mastoxiv.page/@arXiv_csAR_bot : cs.AR Computer Science - Hardware Architecture
   - https://mastoxiv.page/@arXiv_csCC_bot : cs.CC Computer Science - Computational Complexity
   - https://mastoxiv.page/@arXiv_csCE_bot : cs.CE Computer Science - Computational Engineering, Finance, and Science
   - https://mastoxiv.page/@arXiv_csCG_bot : cs.CG Computer Science - Computational Geometry
   - https://mastoxiv.page/@arXiv_csCL_bot : cs.CL Computer Science - Computation and Language
   - https://mastoxiv.page/@arXiv_csCR_bot : cs.CR Computer Science - Cryptography and Security
   - https://mastoxiv.page/@arXiv_csCV_bot : cs.CV Computer Science - Computer Vision and Pattern Recognition
   - https://mastoxiv.page/@arXiv_csCY_bot : cs.CY Computer Science - Computers and Society
   - https://mastoxiv.page/@arXiv_csDB_bot : cs.DB Computer Science - Databases
   - https://mastoxiv.page/@arXiv_csDC_bot : cs.DC Computer Science - Distributed, Parallel, and Cluster Computing
   - https://mastoxiv.page/@arXiv_csDL_bot : cs.DL Computer Science - Digital Libraries
   - https://mastoxiv.page/@arXiv_csDM_bot : cs.DM Computer Science - Discrete Mathematics
   - https://mastoxiv.page/@arXiv_csDS_bot : cs.DS Computer Science - Data Structures and Algorithms
   - https://mastoxiv.page/@arXiv_csET_bot : cs.ET Computer Science - Emerging Technologies
   - https://mastoxiv.page/@arXiv_csFL_bot : cs.FL Computer Science - Formal Languages and Automata Theory
   - https://mastoxiv.page/@arXiv_csGL_bot : cs.GL Computer Science - General Literature
   - https://mastoxiv.page/@arXiv_csGR_bot : cs.GR Computer Science - Graphics
   - https://mastoxiv.page/@arXiv_csGT_bot : cs.GT Computer Science - Computer Science and Game Theory
   - https://mastoxiv.page/@arXiv_csHC_bot : cs.HC Computer Science - Human-Computer Interaction
   - https://mastoxiv.page/@arXiv_csIR_bot : cs.IR Computer Science - Information Retrieval
   - https://mastoxiv.page/@arXiv_csIT_bot : cs.IT Computer Science - Information Theory
   - https://mastoxiv.page/@arXiv_csLG_bot : cs.LG Computer Science - Machine Learning
   - https://mastoxiv.page/@arXiv_csLO_bot : cs.LO Computer Science - Logic in Computer Science
   - https://mastoxiv.page/@arXiv_csMA_bot : cs.MA Computer Science - Multiagent Systems
   - https://mastoxiv.page/@arXiv_csMM_bot : cs.MM Computer Science - Multimedia
   - https://mastoxiv.page/@arXiv_csMS_bot : cs.MS Computer Science - Mathematical Software
   - https://mastoxiv.page/@arXiv_csNE_bot : cs.NE Computer Science - Neural and Evolutionary Computing
   - https://mastoxiv.page/@arXiv_csNI_bot : cs.NI Computer Science - Networking and Internet Architecture
   - https://mastoxiv.page/@arXiv_csOH_bot : cs.OH Computer Science - Other Computer Science
   - https://mastoxiv.page/@arXiv_csOS_bot : cs.OS Computer Science - Operating Systems
   - https://mastoxiv.page/@arXiv_csPF_bot : cs.PF Computer Science - Performance
   - https://mastoxiv.page/@arXiv_csPL_bot : cs.PL Computer Science - Programming Languages
   - https://mastoxiv.page/@arXiv_csRO_bot : cs.RO Computer Science - Robotics
   - https://mastoxiv.page/@arXiv_csSC_bot : cs.SC Computer Science - Symbolic Computation
   - https://mastoxiv.page/@arXiv_csSD_bot : cs.SD Computer Science - Sound
   - https://mastoxiv.page/@arXiv_csSE_bot : cs.SE Computer Science - Software Engineering
   - https://mastoxiv.page/@arXiv_csSI_bot : cs.SI Computer Science - Social and Information Networks
   - https://mastoxiv.page/@arXiv_econEM_bot : econ.EM Economics - Econometrics
   - https://mastoxiv.page/@arXiv_econGN_bot : econ.GN Economics - General Economics
   - https://mastoxiv.page/@arXiv_econTH_bot : econ.TH Economics - Theoretical Economics
   - https://mastoxiv.page/@arXiv_eessAS_bot : eess.AS Electrical Engineering and Systems Science - Audio and Speech Processing
   - https://mastoxiv.page/@arXiv_eessIV_bot : eess.IV Electrical Engineering and Systems Science - Image and Video Processing
   - https://mastoxiv.page/@arXiv_eessSP_bot : eess.SP Electrical Engineering and Systems Science - Signal Processing
   - https://mastoxiv.page/@arXiv_eessSY_bot : eess.SY Electrical Engineering and Systems Science - Systems and Control
   - https://mastoxiv.page/@arXiv_mathAC_bot : math.AC Mathematics - Commutative Algebra
   - https://mastoxiv.page/@arXiv_mathAG_bot : math.AG Mathematics - Algebraic Geometry
   - https://mastoxiv.page/@arXiv_mathAP_bot : math.AP Mathematics - Analysis of PDEs
   - https://mastoxiv.page/@arXiv_mathAT_bot : math.AT Mathematics - Algebraic Topology
   - https://mastoxiv.page/@arXiv_mathCA_bot : math.CA Mathematics - Classical Analysis and ODEs
   - https://mastoxiv.page/@arXiv_mathCO_bot : math.CO Mathematics - Combinatorics
   - https://mastoxiv.page/@arXiv_mathCT_bot : math.CT Mathematics - Category Theory
   - https://mastoxiv.page/@arXiv_mathCV_bot : math.CV Mathematics - Complex Variables
   - https://mastoxiv.page/@arXiv_mathDG_bot : math.DG Mathematics - Differential Geometry
   - https://mastoxiv.page/@arXiv_mathDS_bot : math.DS Mathematics - Dynamical Systems
   - https://mastoxiv.page/@arXiv_mathFA_bot : math.FA Mathematics - Functional Analysis
   - https://mastoxiv.page/@arXiv_mathGM_bot : math.GM Mathematics - General Mathematics
   - https://mastoxiv.page/@arXiv_mathGN_bot : math.GN Mathematics - General Topology
   - https://mastoxiv.page/@arXiv_mathGR_bot : math.GR Mathematics - Group Theory
   - https://mastoxiv.page/@arXiv_mathGT_bot : math.GT Mathematics - Geometric Topology
   - https://mastoxiv.page/@arXiv_mathHO_bot : math.HO Mathematics - History and Overview
   - https://mastoxiv.page/@arXiv_mathKT_bot : math.KT Mathematics - K-Theory and Homology
   - https://mastoxiv.page/@arXiv_mathLO_bot : math.LO Mathematics - Logic
   - https://mastoxiv.page/@arXiv_mathMG_bot : math.MG Mathematics - Metric Geometry
   - https://mastoxiv.page/@arXiv_mathNA_bot : math.NA Mathematics - Numerical Analysis
   - https://mastoxiv.page/@arXiv_mathNT_bot : math.NT Mathematics - Number Theory
   - https://mastoxiv.page/@arXiv_mathOA_bot : math.OA Mathematics - Operator Algebras
   - https://mastoxiv.page/@arXiv_mathOC_bot : math.OC Mathematics - Optimization and Control
   - https://mastoxiv.page/@arXiv_mathPR_bot : math.PR Mathematics - Probability
   - https://mastoxiv.page/@arXiv_mathQA_bot : math.QA Mathematics - Quantum Algebra
   - https://mastoxiv.page/@arXiv_mathRA_bot : math.RA Mathematics - Rings and Algebras
   - https://mastoxiv.page/@arXiv_mathRT_bot : math.RT Mathematics - Representation Theory
   - https://mastoxiv.page/@arXiv_mathSG_bot : math.SG Mathematics - Symplectic Geometry
   - https://mastoxiv.page/@arXiv_mathSP_bot : math.SP Mathematics - Spectral Theory
   - https://mastoxiv.page/@arXiv_mathST_bot : math.ST Mathematics - Statistics Theory
   - https://mastoxiv.page/@arXiv_astrophCO_bot : astro-ph.CO Physics - Astrophysics - Cosmology and Nongalactic Astrophysics
   - https://mastoxiv.page/@arXiv_astrophEP_bot : astro-ph.EP Physics - Astrophysics - Earth and Planetary Astrophysics
   - https://mastoxiv.page/@arXiv_astrophGA_bot : astro-ph.GA Physics - Astrophysics - Astrophysics of Galaxies
   - https://mastoxiv.page/@arXiv_astrophHE_bot : astro-ph.HE Physics - Astrophysics - High Energy Astrophysical Phenomena
   - https://mastoxiv.page/@arXiv_astrophIM_bot : astro-ph.IM Physics - Astrophysics - Instrumentation and Methods for Astrophysics
   - https://mastoxiv.page/@arXiv_astrophSR_bot : astro-ph.SR Physics - Astrophysics - Solar and Stellar Astrophysics
   - https://mastoxiv.page/@arXiv_condmatdisnn_bot : cond-mat.dis-nn Physics - Condensed Matter - Disordered Systems and Neural Networks
   - https://mastoxiv.page/@arXiv_condmatmeshall_bot : cond-mat.mes-hall Physics - Condensed Matter - Mesoscale and Nanoscale Physics
   - https://mastoxiv.page/@arXiv_condmatmtrlsci_bot : cond-mat.mtrl-sci Physics - Condensed Matter - Materials Science
   - https://mastoxiv.page/@arXiv_condmatother_bot : cond-mat.other Physics - Condensed Matter - Other Condensed Matter
   - https://mastoxiv.page/@arXiv_condmatquantgas_bot : cond-mat.quant-gas Physics - Condensed Matter - Quantum Gases
   - https://mastoxiv.page/@arXiv_condmatsoft_bot : cond-mat.soft Physics - Condensed Matter - Soft Condensed Matter
   - https://mastoxiv.page/@arXiv_condmatstatmech_bot : cond-mat.stat-mech Physics - Condensed Matter - Statistical Mechanics
   - https://mastoxiv.page/@arXiv_condmatstrel_bot : cond-mat.str-el Physics - Condensed Matter - Strongly Correlated Electrons
   - https://mastoxiv.page/@arXiv_condmatsuprcon_bot : cond-mat.supr-con Physics - Condensed Matter - Superconductivity
   - https://mastoxiv.page/@arXiv_grqc_bot : gr-qc Physics - General Relativity and Quantum Cosmology
   - https://mastoxiv.page/@arXiv_hepex_bot : hep-ex Physics - High Energy Physics - Experiment
   - https://mastoxiv.page/@arXiv_heplat_bot : hep-lat Physics - High Energy Physics - Lattice
   - https://mastoxiv.page/@arXiv_hepph_bot : hep-ph Physics - High Energy Physics - Phenomenology
   - https://mastoxiv.page/@arXiv_hepth_bot : hep-th Physics - High Energy Physics - Theory
   - https://mastoxiv.page/@arXiv_mathph_bot : math-ph Physics - Mathematical Physics
   - https://mastoxiv.page/@arXiv_nlinAO_bot : nlin.AO Physics - Nonlinear Sciences - Adaptation and Self-Organizing Systems
   - https://mastoxiv.page/@arXiv_nlinCD_bot : nlin.CD Physics - Nonlinear Sciences - Chaotic Dynamics
   - https://mastoxiv.page/@arXiv_nlinCG_bot : nlin.CG Physics - Nonlinear Sciences - Cellular Automata and Lattice Gases
   - https://mastoxiv.page/@arXiv_nlinPS_bot : nlin.PS Physics - Nonlinear Sciences - Pattern Formation and Solitons
   - https://mastoxiv.page/@arXiv_nlinSI_bot : nlin.SI Physics - Nonlinear Sciences - Exactly Solvable and Integrable Systems
  - https://mastoxiv.page/@arXiv_nuclex_bot : nucl-ex Physics - Nuclear Experiment
  - https://mastoxiv.page/@arXiv_nuclth_bot : nucl-th Physics - Nuclear Theory
  - https://mastoxiv.page/@arXiv_physicsaccph_bot : physics.acc-ph Physics - Accelerator Physics
  - https://mastoxiv.page/@arXiv_physicsaoph_bot : physics.ao-ph Physics - Atmospheric and Oceanic Physics
  - https://mastoxiv.page/@arXiv_physicsappph_bot : physics.app-ph Physics - Applied Physics
  - https://mastoxiv.page/@arXiv_physicsatmclus_bot : physics.atm-clus Physics - Atomic and Molecular Clusters
  - https://mastoxiv.page/@arXiv_physicsatomph_bot : physics.atom-ph Physics - Atomic Physics
  - https://mastoxiv.page/@arXiv_physicsbioph_bot : physics.bio-ph Physics - Biological Physics
  - https://mastoxiv.page/@arXiv_physicschemph_bot : physics.chem-ph Physics - Chemical Physics
  - https://mastoxiv.page/@arXiv_physicsclassph_bot : physics.class-ph Physics - Classical Physics
  - https://mastoxiv.page/@arXiv_physicscompph_bot : physics.comp-ph Physics - Computational Physics
  - https://mastoxiv.page/@arXiv_physicsdataan_bot : physics.data-an Physics - Data Analysis, Statistics and Probability
  - https://mastoxiv.page/@arXiv_physicsedph_bot : physics.ed-ph Physics - Physics Education
  - https://mastoxiv.page/@arXiv_physicsfludyn_bot : physics.flu-dyn Physics - Fluid Dynamics
  - https://mastoxiv.page/@arXiv_physicsgenph_bot : physics.gen-ph Physics - General Physics
  - https://mastoxiv.page/@arXiv_physicsgeoph_bot : physics.geo-ph Physics - Geophysics
  - https://mastoxiv.page/@arXiv_physicshistph_bot : physics.hist-ph Physics - History and Philosophy of Physics
  - https://mastoxiv.page/@arXiv_physicsinsdet_bot : physics.ins-det Physics - Instrumentation and Detectors
  - https://mastoxiv.page/@arXiv_physicsmedph_bot : physics.med-ph Physics - Medical Physics
  - https://mastoxiv.page/@arXiv_physicsoptics_bot : physics.optics Physics - Optics
  - https://mastoxiv.page/@arXiv_physicsplasmph_bot : physics.plasm-ph Physics - Plasma Physics
  - https://mastoxiv.page/@arXiv_physicspopph_bot : physics.pop-ph Physics - Popular Physics
  - https://mastoxiv.page/@arXiv_physicssocph_bot : physics.soc-ph Physics - Physics and Society
  - https://mastoxiv.page/@arXiv_physicsspaceph_bot : physics.space-ph Physics - Space Physics
  - https://mastoxiv.page/@arXiv_quantph_bot : quant-ph Physics - Quantum Physics
  - https://mastoxiv.page/@arXiv_qbioBM_bot : q-bio.BM Quantitative Biology - Biomolecules
  - https://mastoxiv.page/@arXiv_qbioCB_bot : q-bio.CB Quantitative Biology - Cell Behavior
  - https://mastoxiv.page/@arXiv_qbioGN_bot : q-bio.GN Quantitative Biology - Genomics
  - https://mastoxiv.page/@arXiv_qbioMN_bot : q-bio.MN Quantitative Biology - Molecular Networks
  - https://mastoxiv.page/@arXiv_qbioNC_bot : q-bio.NC Quantitative Biology - Neurons and Cognition
  - https://mastoxiv.page/@arXiv_qbioOT_bot : q-bio.OT Quantitative Biology - Other Quantitative Biology
  - https://mastoxiv.page/@arXiv_qbioPE_bot : q-bio.PE Quantitative Biology - Populations and Evolution
  - https://mastoxiv.page/@arXiv_qbioQM_bot : q-bio.QM Quantitative Biology - Quantitative Methods
  - https://mastoxiv.page/@arXiv_qbioSC_bot : q-bio.SC Quantitative Biology - Subcellular Processes
  - https://mastoxiv.page/@arXiv_qbioTO_bot : q-bio.TO Quantitative Biology - Tissues and Organs
  - https://mastoxiv.page/@arXiv_qfinCP_bot : q-fin.CP Quantitative Finance - Computational Finance
  - https://mastoxiv.page/@arXiv_qfinGN_bot : q-fin.GN Quantitative Finance - General Finance
  - https://mastoxiv.page/@arXiv_qfinMF_bot : q-fin.MF Quantitative Finance - Mathematical Finance
  - https://mastoxiv.page/@arXiv_qfinPM_bot : q-fin.PM Quantitative Finance - Portfolio Management
  - https://mastoxiv.page/@arXiv_qfinPR_bot : q-fin.PR Quantitative Finance - Pricing of Securities
  - https://mastoxiv.page/@arXiv_qfinRM_bot : q-fin.RM Quantitative Finance - Risk Management
  - https://mastoxiv.page/@arXiv_qfinST_bot : q-fin.ST Quantitative Finance - Statistical Finance
  - https://mastoxiv.page/@arXiv_qfinTR_bot : q-fin.TR Quantitative Finance - Trading and Market Microstructure
  - https://mastoxiv.page/@arXiv_statME_bot : stat.ME Statitics - Methodology
  - https://mastoxiv.page/@arXiv_statML_bot : stat.ML Statitics - Machine Learning
  - https://mastoxiv.page/@arXiv_statOT_bot : stat.OT Statitics - Other Statistics

## Author
So Okada, so.okada@gmail.com, https://so-okada.github.io/

## Motivation

Since 2013-04, the author has been running twitter bots for
all arXiv math categories (see
https://github.com/so-okada/twXiv#motivation).
Since 2023-05, the author has written toXiv for all arXiv categories on
mastodon.


## Contributing
Pull requests are welcome. For major changes, please open an 
issue first to discuss what you would like to change.

## License
[AGPLv3](https://www.gnu.org/licenses/agpl-3.0.en.html)


