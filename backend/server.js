const express = require('express');
const cors = require('cors');
const { exec } = require('child_process');
const app = express();
const port = 3000;

app.use(cors());

app.get('/run-script', (req, res) => {
    console.log('Button clicked, running Python script...');

    const scriptPath = "test.py";  // path to your Python script

    exec(`python "${scriptPath}"`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            res.status(500).send('Script failed to run');
            return;
        }
        if (stderr) {
            console.error(`Stderr: ${stderr}`);
        }

        console.log(`Output:\n${stdout}`);  // prints in Node terminal
        res.send(`<pre>${stdout}</pre>`);  // send output to frontend
    });
});

app.listen(port, () => {
    console.log(`Server running at http://localhost:${port}`);
});
