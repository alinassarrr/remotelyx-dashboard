const express = require("express");
const { spawn } = require("child_process");

const app = express();
app.use(express.json());

app.post("/scrape", async (req, res) => {
  const { job_url } = req.body;

  if (!job_url) {
    return res.status(400).json({ error: "job_url is required" });
  }

  console.log(`Starting scrape for: ${job_url}`);

  try {
    // Run the scrapegamma.js script directly
    const nodeProcess = spawn("node", ["scrapegamma.js", job_url], {
      stdio: ["pipe", "pipe", "pipe"],
      cwd: __dirname,
    });

    let stdout = "";
    let stderr = "";

    nodeProcess.stdout.on("data", (data) => {
      stdout += data.toString();
    });

    nodeProcess.stderr.on("data", (data) => {
      stderr += data.toString();
    });

    let responseHandled = false;

    nodeProcess.on("close", (code) => {
      if (responseHandled) return;
      responseHandled = true;
      clearTimeout(timeoutId);

      if (code !== 0) {
        console.error(`Node.js scraper failed with code ${code}`);
        console.error(`STDERR: ${stderr}`);
        return res.status(500).json({
          error: `Scraper failed with exit code ${code}`,
          stderr: stderr,
        });
      }

      try {
        // Parse the JSON output from scrapegamma.js
        const result = JSON.parse(stdout);

        if (result.error) {
          console.error(`Scraper error: ${result.error}`);
          return res.status(500).json({ error: result.error });
        }

        console.log(
          `Successfully scraped ${result.content?.length || 0} content items`
        );
        res.json({ success: true, data: result });
      } catch (parseError) {
        console.error(`Failed to parse scraper output: ${parseError.message}`);
        console.error(`Raw output: ${stdout.substring(0, 500)}...`);
        res.status(500).json({
          error: "Failed to parse scraper output",
          raw_output: stdout.substring(0, 500),
        });
      }
    });

    // Set a timeout
    const timeoutId = setTimeout(() => {
      if (responseHandled) return;
      responseHandled = true;
      nodeProcess.kill("SIGKILL");
      res.status(500).json({ error: "Scraping timeout" });
    }, 120000); // 2 minute timeout
  } catch (error) {
    console.error(`Server error: ${error.message}`);
    res.status(500).json({ error: error.message });
  }
});

const PORT = process.env.PORT || 3001;
app.listen(PORT, () => {
  console.log(`Simple Gamma scraper server running on port ${PORT}`);
});
