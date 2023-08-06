<h1 id="multidimensional-analysis-tagger-of-mandarin-chinese">Multidimensional-Analysis-Tagger-of-Mandarin-Chinese</h1>
<p>Multidimensional Analysis Tagger of Mandarin Chinese (<strong>MulDi Chinese</strong>) adapts Biber’s register analysis of English (1988) to Mandarin Chinese. It aims to describe dimensions of register variation in a text. The programme tags 54 linguistic features based on ICTCLAS (H.-P. Zhang, Yu, Xiong, &amp; Liu, 2003) and word lists collected from Chinese linguistics research. It performs factor analysis to generate 5 dimensions of register variation and plots the variation of the input text or corpus against 15 registers in an upsampled ToRCH2014 corpus (available at http://corpus.bfsu.edu.cn/info/1070/1387.htm; TORCH 2009 available at http://114.251.154.212/cqp/torch09/, username: test, password: test). </p>
<h1 id="referencing-the-tagger">Referencing the tagger</h1>
<p>Liu, N. 2019. Multidimensional Analysis Tagger of Mandarin Chinese. Available at: <a href="https://github.com/Nannan-Liu/Multidimensional-Analysis-Tagger-of-Mandarin-Chinese">https://github.com/Nannan-Liu/Multidimensional-Analysis-Tagger-of-Mandarin-Chinese</a>.</p>
<p>This programme is based on the ICTCLAS, and it is advised to reference ICTCLAS when MulDi Chinese is used. Please refer to <a href="https://dl.acm.org/citation.cfm?id=1119280">https://dl.acm.org/citation.cfm?id=1119280</a>.</p>
<h2 id="requirements">Requirements</h2>
<p>This programme requires Python to run (<a href="https://www.python.org/">https://www.python.org/</a>). Python packages needed are NLTK (Bird, Loper, &amp; Klein, 2009), and Python wrapper of ICTCLAS – PyNLPIR (<a href="https://pypi.org/project/PyNLPIR/">https://pypi.org/project/PyNLPIR/</a>).</p>
<h2 id="use-muldi-chinese">Use MulDi Chinese</h2>
<p>MulDi Chinese reads input plain text files in the format ‘.txt’. The user can use a folder of .txt files or a single .txt file. MulDi Chinese utilises ICTCLAS to segment and tag the files, and outputs a csv file containing standardised frequencies per 1000 of 54 linguistic features, and the files’ performance on 5 dimensions of register variation in Chinese.</p>
<h2 id="see-manual.pdf-for-more-details">See MulDi Chinese manual.pdf for more details</h2>
<p>The manual contains a detailed description of the 54 features.</p>

{"mode":"full","isActive":false}