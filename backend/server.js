const express = require('express');
const bodyParser = require('body-parser');
const path = require('path');
const { exec } = require('child_process');

const app = express();
app.use(bodyParser.json());

app.post('/graph_rag/send_query', async (req, res) => {
    try {
        const { query } = req.body; // Get user query
        if (!query) {
            return res.status(400).json({ error: 'Query is required' });
        }

        // Define absolute paths for the script and directories
        const scriptPath = path.resolve(__dirname, '../run.py');
        const bfPath = path.resolve(__dirname, '../test_before');
        const afPath = path.resolve(__dirname, '../test_after');

        console.log("Running GraphRAG query...");

        // Run the GraphRAG script with the provided query and paths
        exec(
            `python3 ${scriptPath} --query "${query}" --path_bf "${bfPath}" --path_af "${afPath}"`,
            (error, stdout, stderr) => {
                if (error) {
                    console.error(`Error: ${stderr}`);
                    return res.status(500).json({
                        error: 'Error running GraphRAG script',
                        details: stderr, // Include error details for debugging
                    });
                }

                try {
                    // Log the raw output for debugging
                    console.log("Raw output from Python script:", stdout);

                    // Parse the JSON output from the Python script
                    const result = JSON.parse(stdout);

                    // Return the result as a JSON response
                    res.json({ success: true, result });
                } catch (parseError) {
                    console.error("Error parsing Python script output:", parseError);
                    res.status(500).json({
                        error: 'Error parsing GraphRAG response',
                        details: stdout, // Include raw output for debugging
                    });
                }
            }
        );
    } catch (err) {
        console.error("Internal server error:", err);
        res.status(500).json({ error: 'Internal Server Error' });
    }
});

// Start server
const PORT = process.env.PORT || 3000;
app.listen(PORT, () => {
    console.log(`Server is running on port ${PORT}`);
});
