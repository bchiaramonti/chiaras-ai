#!/usr/bin/env node
/**
 * M7 D3 Chart Renderer
 *
 * Renders a D3.js chart HTML file to PNG using Puppeteer.
 * The HTML must set data-rendered="true" on <html> when rendering is complete.
 *
 * Usage:
 *   node render_chart.js <input.html> <output.png> [width] [height]
 *
 * Defaults: 1760x700 (2x resolution of 880x350 chart area)
 *
 * Requirements:
 *   npm install puppeteer
 */

const puppeteer = require('puppeteer');
const path = require('path');

async function renderChart(inputHtml, outputPng, width = 1760, height = 700) {
  const absolutePath = path.resolve(inputHtml);

  const browser = await puppeteer.launch({
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox'],
  });

  try {
    const page = await browser.newPage();

    // Set viewport to 2x chart dimensions for crisp rendering
    await page.setViewport({ width, height, deviceScaleFactor: 1 });

    // Load the HTML file
    await page.goto(`file://${absolutePath}`, { waitUntil: 'networkidle0' });

    // Wait for D3 to finish rendering (signaled by data-rendered="true")
    await page.waitForFunction(
      () => document.documentElement.getAttribute('data-rendered') === 'true',
      { timeout: 15000 }
    );

    // Small delay for any final paint operations
    await new Promise(resolve => setTimeout(resolve, 200));

    // Screenshot the SVG chart element
    const chartElement = await page.$('#chart');
    if (chartElement) {
      await chartElement.screenshot({
        path: outputPng,
        type: 'png',
        omitBackground: false,
      });
    } else {
      // Fallback: screenshot full page with clip
      await page.screenshot({
        path: outputPng,
        type: 'png',
        clip: { x: 0, y: 0, width: width / 2, height: height / 2 },
        omitBackground: false,
      });
    }

    console.log(`Rendered: ${outputPng} (${width}x${height})`);
  } finally {
    await browser.close();
  }
}

// CLI execution
const args = process.argv.slice(2);

if (args.length < 2) {
  console.error('Usage: node render_chart.js <input.html> <output.png> [width] [height]');
  console.error('Defaults: 1760x700 (2x resolution)');
  process.exit(1);
}

const [inputHtml, outputPng] = args;
const width = parseInt(args[2]) || 1760;
const height = parseInt(args[3]) || 700;

renderChart(inputHtml, outputPng, width, height)
  .catch(err => {
    console.error('Render failed:', err.message);
    process.exit(1);
  });
