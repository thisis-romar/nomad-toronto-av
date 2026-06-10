#!/usr/bin/env node
/**
 * Codex ImageGen MCP Server
 * Exposes gpt-image-2 image generation as MCP tools for Claude Code.
 *
 * Tools:
 *   generate_image  — generate/edit an equipment diagram via gpt-image-2
 *   check_quota     — check OpenAI API key status and model availability
 *
 * Env:
 *   OPENAI_API_KEY  — required, project-scoped key from platform.openai.com
 *
 * Usage (via .mcp.json):
 *   { "command": "node", "args": ["scripts/codex-mcp-server.mjs"] }
 */

import { createInterface } from 'node:readline';
import { readFileSync, writeFileSync, mkdirSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { tmpdir } from 'node:os';
import { execFileSync } from 'node:child_process';

const OPENAI_API_KEY = process.env.OPENAI_API_KEY;
const MODEL = process.env.CODEX_IMAGEGEN_MODEL ?? 'gpt-image-2';
const API_BASE = 'https://api.openai.com/v1';

if (!OPENAI_API_KEY) {
  process.stderr.write('Error: OPENAI_API_KEY not set\n');
  process.exit(1);
}

// ── Minimal MCP JSON-RPC server (stdio transport) ────────────────────────────

const tools = [
  {
    name: 'generate_image',
    description:
      'Generate or refine an equipment diagram image using gpt-image-2. ' +
      'Accepts a source PNG path and a text prompt. Returns the output PNG path.',
    inputSchema: {
      type: 'object',
      properties: {
        source_path: {
          type: 'string',
          description: 'Absolute or relative path to the source PNG file',
        },
        output_path: {
          type: 'string',
          description: 'Where to save the generated PNG',
        },
        prompt: {
          type: 'string',
          description: 'Image generation prompt',
          default:
            'Clean technical line drawing, white background, precise engineering illustration, ' +
            'no text annotations or callout numbers, no legend boxes, accurate detail',
        },
        size: {
          type: 'string',
          enum: ['1024x1024', '1024x1536', '1536x1024'],
          default: '1024x1024',
          description: 'Output image dimensions',
        },
      },
      required: ['source_path', 'output_path'],
    },
  },
  {
    name: 'check_quota',
    description: 'Verify the OpenAI API key is valid and check available models.',
    inputSchema: { type: 'object', properties: {} },
  },
];

async function callOpenAI(path, method, body, formData) {
  const { default: https } = await import('node:https');
  return new Promise((resolve, reject) => {
    const isForm = !!formData;
    const headers = {
      Authorization: `Bearer ${OPENAI_API_KEY}`,
    };

    let postData;
    if (isForm) {
      // multipart/form-data via Python subprocess (simpler than native Node multipart)
      resolve({ _useSubprocess: true, formData });
      return;
    } else {
      postData = JSON.stringify(body);
      headers['Content-Type'] = 'application/json';
      headers['Content-Length'] = Buffer.byteLength(postData);
    }

    const options = {
      hostname: 'api.openai.com',
      path,
      method,
      headers,
    };

    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', (chunk) => (data += chunk));
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, body: JSON.parse(data) });
        } catch {
          resolve({ status: res.statusCode, body: data });
        }
      });
    });
    req.on('error', reject);
    if (postData) req.write(postData);
    req.end();
  });
}

async function handleGenerateImage(params) {
  const { source_path, output_path, prompt, size = '1024x1024' } = params;

  // Use the Python script for the actual generation (handles multipart/form-data)
  const scriptPath = new URL('./codex-imagegen.py', import.meta.url).pathname
    .replace(/^\/([A-Z]:)/, '$1');  // Windows path fix

  try {
    const result = execFileSync('python3', [
      scriptPath,
      source_path,
      output_path,
      '--prompt', prompt ?? 'Clean technical line drawing, white background, no annotations',
      '--no-score',
      '--max-iter', '1',
    ], {
      env: { ...process.env, OPENAI_API_KEY },
      encoding: 'utf8',
      timeout: 120_000,
    });
    return { success: true, output_path, log: result };
  } catch (err) {
    return { success: false, error: err.message, stderr: err.stderr };
  }
}

async function handleCheckQuota() {
  const res = await callOpenAI('/v1/models', 'GET', null);
  if (res.status === 200) {
    const imageModels = res.body.data
      ?.filter((m) => m.id.includes('image') || m.id.includes('dall-e'))
      .map((m) => m.id) ?? [];
    return {
      valid: true,
      model: MODEL,
      image_models_available: imageModels,
    };
  }
  return { valid: false, status: res.status, error: res.body };
}

// ── JSON-RPC dispatch ─────────────────────────────────────────────────────────

async function handleRequest(req) {
  const { id, method, params } = req;

  if (method === 'initialize') {
    return {
      id,
      result: {
        protocolVersion: '2024-11-05',
        serverInfo: { name: 'codex-imagegen', version: '1.0.0' },
        capabilities: { tools: {} },
      },
    };
  }

  if (method === 'tools/list') {
    return { id, result: { tools } };
  }

  if (method === 'tools/call') {
    const { name, arguments: args } = params;
    let content;
    try {
      if (name === 'generate_image') {
        const result = await handleGenerateImage(args);
        content = [{ type: 'text', text: JSON.stringify(result, null, 2) }];
      } else if (name === 'check_quota') {
        const result = await handleCheckQuota();
        content = [{ type: 'text', text: JSON.stringify(result, null, 2) }];
      } else {
        throw new Error(`Unknown tool: ${name}`);
      }
    } catch (err) {
      content = [{ type: 'text', text: `Error: ${err.message}` }];
    }
    return { id, result: { content } };
  }

  if (method === 'notifications/initialized') {
    return null; // no response needed
  }

  return { id, error: { code: -32601, message: `Method not found: ${method}` } };
}

// ── stdio loop ────────────────────────────────────────────────────────────────

const rl = createInterface({ input: process.stdin });

rl.on('line', async (line) => {
  if (!line.trim()) return;
  let req;
  try {
    req = JSON.parse(line);
  } catch {
    return;
  }
  const response = await handleRequest(req);
  if (response !== null) {
    process.stdout.write(JSON.stringify(response) + '\n');
  }
});
