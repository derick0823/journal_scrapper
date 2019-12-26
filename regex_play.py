import re


text = """<input class="article_checkbox" name="article-id[]" type="checkbox" value="aj/100/1/1"><span class="indent10"></span><span style="font-size: 13px; font-weight: bold;">
<em>Agronomy Journal</em>
 Turns One Hundred





</span><br/>doi:10.2134/agronj2006.0312c<br/>Agronomy Journal 2008 100:1-8<br/><a href="/publications/aj/abstracts/100/1/1" onmouseout='hideAbstract("abstract0")' onmouseover='showAbstract("abstract0")'>[ Abstract ]</a><a href="/publications/aj/articles/100/1/1">[ Full Text ]</a>
<a href="/publications/aj/pdfs/100/1/1">[ PDF ]</a>
<a href="/publications/aj/articles/100/1/1?show-t-f=tables&amp;wrapper=no">[ Tables Only ]</a>
<a href="/publications/aj/articles/100/1/1?show-t-f=figures&amp;wrapper=no">[ Figures Only ]</a>
<div class="hidden" id="abstract0" style="background-color: #eee; padding: 10px;"><strong>Abstract</strong><br/><abstract xml:lang="">
<p>During 2008 we celebrate the centennial anniversary of <em>Agronomy Journal</em> Many people have certainly been influenced in some way by the science published during the 100-yr existence of the journal. From Volume 1 up through Volume 98 (2006) there have been more than 30,290 authors who published 15,232 articles totaling 89,056 pages. More than 2545 editors were required to review and edit the papers published in <em>Agronomy Journal</em>, in addition to the manuscripts submitted but not published. As a current snapshot of <em>Agronomy Journal</em>, we published 60% of the manuscripts submitted in 2005. In both 2003 and 2004, we accepted 55% of the manuscripts submitted. In a comparison of 48 peer journals in 2005, the impact factor of <em>Agronomy journal</em> ranked 12th at 1.473 and the total citations for the journal ranked fourth at 6723. Commentaries on the early history of <em>Agronomy Journal</em> have been previously published. In our article, we focus on the journal's history during the past 25 yr. We fully expect that the future of <em>Agronomy Journal</em> will be even more exciting, rewarding, challenging, and valued as the past 100 yr. We eagerly look forward to the next 100 yr of <em>Agronomy Journal</em></p>
</abstract></div>
</input>"""

p2 = r'doi:(?P<doi_str>.*?)<br/>'
r1 = re.compile(p2)
d2 = r1.search(text) 
print(d2.group('doi_str'))
