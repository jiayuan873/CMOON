package com.example.demo;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;
import java.io.BufferedReader;
import java.io.InputStreamReader;

@RestController
public class ScriptController {

    @GetMapping("/run-script")
    public String runScript() {
        try {
            // Get the path to the Python script relative to the demo directory
            String scriptPath = "src/main/java/com/example/demo/test.py";
            
            // Create process builder with correct working directory
            ProcessBuilder processBuilder = new ProcessBuilder("python", scriptPath);
            processBuilder.redirectErrorStream(true); // Capture stderr with stdout
            
            Process process = processBuilder.start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }
            
            // Wait for process to complete and get exit code
            int exitCode = process.waitFor();
            if (exitCode != 0) {
                output.append("Process exited with code: ").append(exitCode);
            }
            
            return output.toString();
        } catch (Exception e) {
            e.printStackTrace();
            return "Error running script: " + e.getMessage();
        }
    }
}