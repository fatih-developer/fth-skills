#!/usr/bin/env node

"use strict";

const fs = require("node:fs");
const path = require("node:path");

function fail(message, code = 1) {
  process.stderr.write(`${message}\n`);
  process.exit(code);
}

function parseArgs(argv) {
  const options = {
    encoding: null,
    model: null,
    files: [],
    texts: [],
  };

  for (let index = 0; index < argv.length; index += 1) {
    const argument = argv[index];
    const value = argv[index + 1];

    if (argument === "--encoding" && value) {
      options.encoding = value;
      index += 1;
    } else if (argument === "--model" && value) {
      options.model = value;
      index += 1;
    } else if (argument === "--file" && value) {
      options.files.push(value);
      index += 1;
    } else if (argument === "--text" && value) {
      options.texts.push(value);
      index += 1;
    } else if (argument === "--help") {
      process.stdout.write(
        [
          "Usage:",
          "  node count_tokens.cjs --encoding o200k_base --file prompt.txt",
          "  node count_tokens.cjs --model <model> --file a.txt --file b.txt",
          "  node count_tokens.cjs --encoding cl100k_base --text \"Prompt\"",
          "  printf input | node count_tokens.cjs --encoding o200k_base",
          "",
        ].join("\n"),
      );
      process.exit(0);
    } else {
      fail(`Unknown or incomplete argument: ${argument}`);
    }
  }

  if (options.encoding && options.model) {
    fail("Use either --encoding or --model, not both.");
  }

  if (!options.encoding && !options.model) {
    fail("Specify --encoding or --model.");
  }

  return options;
}

function loadTokenizer() {
  try {
    return require("tiktoken");
  } catch (error) {
    fail(
      [
        "The tiktoken package is required for exact counts.",
        "Install it in an isolated environment or make it available through NODE_PATH.",
        `Details: ${error.message}`,
      ].join("\n"),
      2,
    );
  }
}

function collectInputs(options) {
  const inputs = [];

  for (const file of options.files) {
    const resolved = path.resolve(file);
    inputs.push({
      source: resolved,
      text: fs.readFileSync(resolved, "utf8"),
    });
  }

  options.texts.forEach((text, index) => {
    inputs.push({
      source: `text:${index + 1}`,
      text,
    });
  });

  if (inputs.length === 0) {
    if (process.stdin.isTTY) {
      fail("Provide --file, --text, or stdin.");
    }
    inputs.push({
      source: "stdin",
      text: fs.readFileSync(0, "utf8"),
    });
  }

  return inputs;
}

const options = parseArgs(process.argv.slice(2));
const tiktoken = loadTokenizer();
let tokenizer;

try {
  tokenizer = options.model
    ? tiktoken.encoding_for_model(options.model)
    : tiktoken.get_encoding(options.encoding);
} catch (error) {
  fail(
    `Tokenizer resolution failed for ${options.model || options.encoding}: ${error.message}`,
    3,
  );
}

try {
  const results = collectInputs(options).map(({ source, text }) => ({
    source,
    characters: [...text].length,
    utf8_bytes: Buffer.byteLength(text, "utf8"),
    tokens: tokenizer.encode(text).length,
  }));

  process.stdout.write(
    `${JSON.stringify(
      {
        tokenizer: options.model
          ? { model: options.model }
          : { encoding: options.encoding },
        results,
      },
      null,
      2,
    )}\n`,
  );
} finally {
  if (typeof tokenizer.free === "function") {
    tokenizer.free();
  }
}
