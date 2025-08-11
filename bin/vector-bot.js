#!/usr/bin/env node
/**
 * Vector Bot CLI wrapper for Node.js
 * This wrapper checks for Python and the vector-bot package,
 * then delegates to the Python CLI.
 */

const { spawn } = require('child_process');
const path = require('path');
const fs = require('fs');
const which = require('which');
const chalk = require('chalk');
const ora = require('ora');

async function checkPython() {
  try {
    // Check for Python 3
    const pythonPaths = ['python3', 'python'];
    for (const pythonPath of pythonPaths) {
      try {
        const resolvedPath = await which(pythonPath);
        // Verify it's Python 3.10+
        return new Promise((resolve, reject) => {
          const checkVersion = spawn(pythonPath, ['--version']);
          let version = '';
          
          checkVersion.stdout.on('data', (data) => {
            version += data.toString();
          });
          
          checkVersion.stderr.on('data', (data) => {
            version += data.toString();
          });
          
          checkVersion.on('close', (code) => {
            if (code === 0 && version.includes('Python 3.')) {
              const versionMatch = version.match(/Python 3\.(\d+)/);
              if (versionMatch && parseInt(versionMatch[1]) >= 10) {
                resolve(pythonPath);
              } else {
                reject(new Error('Python 3.10 or higher is required'));
              }
            } else {
              reject(new Error('Failed to check Python version'));
            }
          });
        });
      } catch (e) {
        continue;
      }
    }
    throw new Error('Python not found');
  } catch (error) {
    console.error(chalk.red('Error: Python 3.10+ is required but not found.'));
    console.error(chalk.yellow('Please install Python from https://www.python.org/'));
    process.exit(1);
  }
}

async function checkVectorBot(pythonPath) {
  return new Promise((resolve) => {
    const checkPackage = spawn(pythonPath, ['-c', 'import rag']);
    
    checkPackage.on('close', (code) => {
      resolve(code === 0);
    });
  });
}

async function installVectorBot(pythonPath) {
  const spinner = ora('Installing vector-bot Python package...').start();
  
  return new Promise((resolve, reject) => {
    const install = spawn(pythonPath, ['-m', 'pip', 'install', 'vector-bot'], {
      stdio: 'pipe'
    });
    
    let errorOutput = '';
    install.stderr.on('data', (data) => {
      errorOutput += data.toString();
    });
    
    install.on('close', (code) => {
      if (code === 0) {
        spinner.succeed('Vector Bot Python package installed successfully');
        resolve();
      } else {
        spinner.fail('Failed to install Vector Bot Python package');
        console.error(errorOutput);
        reject(new Error('Installation failed'));
      }
    });
  });
}

async function runVectorBot(pythonPath, args) {
  const vectorBot = spawn(pythonPath, ['-m', 'rag.cli', ...args], {
    stdio: 'inherit',
    timeout: 300000 // 5 minute timeout
  });
  
  vectorBot.on('error', (err) => {
    console.error(chalk.red('Error running Vector Bot:'), err.message);
    process.exit(1);
  });
  
  vectorBot.on('close', (code) => {
    process.exit(code || 0);
  });
}

async function main() {
  try {
    // Check for Python
    const pythonPath = await checkPython();
    
    // Check if vector-bot is installed
    const isInstalled = await checkVectorBot(pythonPath);
    
    if (!isInstalled) {
      console.log(chalk.yellow('Vector Bot Python package not found.'));
      
      // Check if auto-install is disabled
      if (process.env.VECTOR_BOT_NO_AUTO_INSTALL === 'true') {
        console.log(chalk.red('Please install the Python package manually:'));
        console.log(chalk.cyan(`  ${pythonPath} -m pip install vector-bot`));
        process.exit(1);
      }
      
      // Only prompt for installation in interactive mode
      if (!process.stdin.isTTY) {
        console.log(chalk.red('Non-interactive mode detected. Cannot prompt for installation.'));
        console.log(chalk.cyan(`Please install manually: ${pythonPath} -m pip install vector-bot`));
        process.exit(1);
      }
      
      const readline = require('readline');
      const rl = readline.createInterface({
        input: process.stdin,
        output: process.stdout
      });
      
      await new Promise((resolve) => {
        rl.question('Would you like to install the Python package now? (y/n) ', (answer) => {
          rl.close();
          if (answer.toLowerCase() === 'y' || answer.toLowerCase() === 'yes') {
            resolve();
          } else {
            console.log(chalk.yellow('Installation cancelled.'));
            console.log(chalk.cyan(`To install manually: ${pythonPath} -m pip install vector-bot`));
            process.exit(1);
          }
        });
      });
      
      await installVectorBot(pythonPath);
    }
    
    // Run vector-bot with provided arguments
    const args = process.argv.slice(2);
    await runVectorBot(pythonPath, args);
    
  } catch (error) {
    console.error(chalk.red('Error:'), error.message);
    process.exit(1);
  }
}

main();