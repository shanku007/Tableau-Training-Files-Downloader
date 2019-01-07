# Tableau-Training-Files-Downloader
Tableau Training files downloader download training videos, and other files like data sets and workbook from tableau website and save it to the computer in the same file structure it is present.
<h3>The following python modules are required for running this script</h5>
<ol>
  <li> BeautifulSoup </li>
  <li> requests </li>
  <li> selenium </li>
  <li> os </li>

The use of this is very simple. Either download the jupyter workbook or the python script.
On Ubuntu install selenium and download <a href="https://github.com/mozilla/geckodriver/releases">geckodriver</a>, a firefox webdriver for selenium. This is required because videos are played on tableau website using javascript and the link need to be opened in a web browser for crawling. 

After downloading geckodriver extract it to /usr/local/bin. 

Now just run the script or run the jupyter cells and select your desired options.
