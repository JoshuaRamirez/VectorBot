/**
 * Post-install script for vector-bot npm package
 * Checks Python availability and provides setup instructions
 */

const chalk = require('chalk');
const { execSync } = require('child_process');

console.log(chalk.blue('\n═══════════════════════════════════════'));
console.log(chalk.blue.bold('   Vector Bot Installation'));
console.log(chalk.blue('═══════════════════════════════════════\n'));

// Check for Python
let pythonAvailable = false;
let pythonVersion = '';

try {
  // Try python3 first
  pythonVersion = execSync('python3 --version', { encoding: 'utf8' }).trim();
  pythonAvailable = true;
} catch (e) {
  try {
    // Fall back to python
    pythonVersion = execSync('python --version', { encoding: 'utf8' }).trim();
    pythonAvailable = true;
  } catch (e2) {
    // Python not found
  }
}

if (pythonAvailable) {
  console.log(chalk.green('✓'), 'Python detected:', pythonVersion);
  
  // Check for Ollama
  let ollamaAvailable = false;
  try {
    execSync('ollama --version', { encoding: 'utf8' });
    ollamaAvailable = true;
    console.log(chalk.green('✓'), 'Ollama detected');
  } catch (e) {
    console.log(chalk.yellow('⚠'), 'Ollama not detected');
  }
  
  console.log('\n' + chalk.cyan('Next Steps:'));
  console.log('1. Run', chalk.bold('npx vector-bot --help'), 'to see available commands');
  
  if (!ollamaAvailable) {
    console.log('2. Install Ollama from', chalk.underline('https://ollama.ai'));
    console.log('3. Run', chalk.bold('ollama pull llama3.1'), 'to download a model');
  }
  
} else {
  console.log(chalk.yellow('⚠'), 'Python 3.10+ is required but not found');
  console.log('\n' + chalk.cyan('Installation Steps:'));
  console.log('1. Install Python 3.10+ from', chalk.underline('https://www.python.org/'));
  console.log('2. Install Ollama from', chalk.underline('https://ollama.ai'));
  console.log('3. Run', chalk.bold('npx vector-bot --help'), 'to get started');
}

console.log('\n' + chalk.gray('Documentation: https://github.com/joshuaramirez/vector-bot'));
console.log(chalk.blue('═══════════════════════════════════════\n'));