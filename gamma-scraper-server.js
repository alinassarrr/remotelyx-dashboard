const express = require("express");
const puppeteer = require("puppeteer-extra");
const StealthPlugin = require("puppeteer-extra-plugin-stealth");

puppeteer.use(StealthPlugin());

const app = express();
app.use(express.json());

async function scrapeGamma(url) {
  const browser = await puppeteer.launch({
    headless: true,
    args: ["--no-sandbox", "--disable-setuid-sandbox"],
  });

  const page = await browser.newPage();

  try {
    await page.goto(url, { waitUntil: "networkidle2", timeout: 60000 });
    await page.waitForSelector("h1, [data-card-id]", { timeout: 60000 });

    const data = await page.evaluate(() => {
      const content = [];

      function traverse(node) {
        if (!node) return;
        const textTags = [
          "H1",
          "H2",
          "H3",
          "H4",
          "H5",
          "H6",
          "P",
          "LI",
          "SPAN",
          "DIV",
        ];
        if (textTags.includes(node.nodeName) && node.innerText?.trim()) {
          content.push(node.innerText.trim());
        }
        node.childNodes.forEach(traverse);
      }

      traverse(document.body);

      return {
        title: document.querySelector("h1")?.innerText || null,
        url: window.location.href,
        content,
      };
    });

    return { success: true, data };
  } catch (err) {
    return { success: false, error: err.message };
  } finally {
    await browser.close();
  }
}

app.post("/scrape", async (req, res) => {
  const { url } = req.body;

  if (!url) {
    return res.status(400).json({ error: "URL is required" });
  }

  try {
    const result = await scrapeGamma(url);
    res.json(result);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Gamma scraper server running on port ${PORT}`);
});
