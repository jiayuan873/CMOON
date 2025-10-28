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
            Process process = new ProcessBuilder("python", "test.py").start();
            BufferedReader reader = new BufferedReader(new InputStreamReader(process.getInputStream()));
            StringBuilder output = new StringBuilder();
            String line;
            while ((line = reader.readLine()) != null) {
                output.append(line).append("\n");
            }
            return output.toString();
        } catch (Exception e) {
            e.printStackTrace();
            return "Error running script: " + e.getMessage();
        }
    }
}