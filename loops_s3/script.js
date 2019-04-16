const puppeteer = require('puppeteer');
const block_code = '';
const base = 'http://scratchblocks.github.io/#?style=scratch3&script=';
const link = base + block_code;

(async () => {
  const browser = await puppeteer.launch({
  	headless : false
  });
  const page = await browser.newPage();
  const PNG_SELECTOR = '#export-png';
  await page.goto(link);
  // Redirect Download
  await page._client.send('Page.setDownloadBehavior', { behavior: 'allow', downloadPath: './img_files/' });
  await page.click(PNG_SELECTOR);
  setTimeout(() => { browser.close(); }, 300);
})();