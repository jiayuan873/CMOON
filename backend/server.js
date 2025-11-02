const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');
const path = require('path');
const app = express();
const port = 3000;

app.use(cors());

app.get('/run-script', (req, res) => {
  console.log('Button clicked, running Python script...');
  const scriptPath = "test.py";

  exec(`python "${scriptPath}"`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error: ${error.message}`);
      return res.status(500).send('Script failed to run');
    }
    if (stderr) {
      console.error(`Stderr: ${stderr}`);
    }

    console.log(`Output:\n${stdout}`);
    res.send(`<pre>${stdout}</pre>`);
  });
});

app.get('/convert', (req, res) => {
  const inputFile = 'Part Studio 1 - DEMOSTL.stl';
  const outputFile = 'result.stp';

  const dockerCmd = `docker run -v "${__dirname.replace(/\\/g, '/')}/:/data" stltostp stltost "/data/${inputFile}" /data/${outputFile}`;

  exec(dockerCmd, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error: ${error.message}`);
      return res.status(500).send('Conversion failed');
    }
    console.log(`Output: ${stdout}`);
    res.download(path.join(__dirname, outputFile));
  });
});

app.get('/download', (req, res) => {
  const filePath = path.join(__dirname, 'result.stp');
  res.download(filePath, 'converted.step', (err) => {
    if (err) {
      console.error('Download error:', err);
      res.status(500).send('File not found or download failed');
    }
  });
});

// ✅ Move this OUTSIDE all routes
app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});
