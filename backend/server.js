const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');
const path = require('path');
const fs = require('fs');
const multer = require('multer');

const app = express();
const port = 3000;
const upload = multer({ dest: 'uploads/' }); // saves files to /uploads

// ✅ CORS setup
app.use(cors({
  origin: ['http://localhost:5500', 'http://127.0.0.1:5500'],
  methods: ['GET', 'POST', 'OPTIONS'],
  credentials: true
}));


app.get('/run-script', (req, res) => {
  console.log('Button clicked, running Python script...');
  const scriptPath = "test.py";

  exec(`python "${scriptPath}"`, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error: ${error.message}`);
      return res.status(500).send('Script failed to run');
    }
    if (stderr) console.error(`Stderr: ${stderr}`);
    console.log(`Output:\n${stdout}`);
    res.send(`<pre>${stdout}</pre>`);
  });
});

app.post('/convert', upload.single('stlFile'), (req, res) => {
  console.log("Received request to /convert");
  console.log("File received:", req.file);
  if (!req.file) return res.status(400).send('No file uploaded');

  const inputPath = req.file.path.replace(/\\/g, '/');
  const outputFile = 'result.stp';
  const dockerCmd = `docker run -v "${__dirname.replace(/\\/g, '/')}/:/data" stltostp stltost "/data/${inputPath}" /data/${outputFile}`;

  exec(dockerCmd, (error, stdout, stderr) => {
    if (error) {
      console.error(`Docker error: ${error.message}`);
      return res.status(500).send('Conversion failed');
    }

    console.log(`Docker output: ${stdout}`);
    const filePath = path.join(__dirname, outputFile);
    console.log(`Sending file: ${filePath}`);

    res.setHeader('Content-Type', 'application/octet-stream');
    res.setHeader('Content-Disposition', 'attachment; filename="converted.step"');

    res.sendFile(filePath, err => {
      if (err) {
        console.error('Send file error:', err);
        res.status(500).send('Failed to send converted file');
      }
    });
  });
});

app.get('/download', (req, res) => {
  const filePath = path.join(__dirname, 'result.stp');
  res.download(filePath, 'converted.step', err => {
    if (err) {
      console.error('Download error:', err);
      res.status(500).send('File not found or download failed');
    }
  });
});

app.post('/upload', upload.single('stlFile'), (req, res) => {
  const uploadedPath = req.file.path.replace(/\\/g, '/');
  const outputFile = 'result.stp';

  const dockerCmd = `docker run -v "${__dirname.replace(/\\/g, '/')}/:/data" stltostp stltost "/data/${uploadedPath}" /data/${outputFile}`;

  exec(dockerCmd, (error, stdout, stderr) => {
    if (error) {
      console.error(`Error: ${error.message}`);
      return res.status(500).send('Conversion failed');
    }
    console.log(`Docker output: ${stdout}`);
    res.download(path.join(__dirname, outputFile), 'converted.step');
  });
});

app.listen(port, '127.0.0.1', () => {
  console.log(`✅ Server running at http://127.0.0.1:${port}`);
});
