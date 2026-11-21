// news-image-20261121, v2 entrypoint.
//
// v2 keeps the same job as v1: the front page is already drawn by
// draw.py (Pillow, no network, no randomness) and committed here as
// entry.png. This program only carries those exact bytes to the
// grader's output file, after proving the PNG is whole and inside the
// competition gates (at most 1 MiB, at most 1024 by 1024). Copying
// byte for byte keeps the two grading runs identical, so a v2 image
// that scores better in development keeps that score in the final.
//
// Local check:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const MAGIC = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
const MAX_BYTES = 1024 * 1024;
const MAX_SIDE = 1024;

function readEntry(path: string) {
  if (!existsSync(path)) {
    throw new Error(`missing entry image: ${path}`);
  }
  const bytes = readFileSync(path);
  if (bytes.length > MAX_BYTES) {
    throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
  }
  const head = [...bytes.subarray(0, 8)];
  if (head.some((b, i) => b !== MAGIC[i])) {
    throw new Error("entry.png does not start with a PNG signature");
  }
  if (bytes.length < 29 || bytes.toString("ascii", 12, 16) !== "IHDR") {
    throw new Error("entry.png has no IHDR chunk in the expected place");
  }
  return {
    bytes,
    width: bytes.readUInt32BE(16),
    height: bytes.readUInt32BE(20),
  };
}

function main(): void {
  const here = dirname(fileURLToPath(import.meta.url));
  const png = readEntry(join(here, "entry.png"));
  if (png.width > MAX_SIDE || png.height > MAX_SIDE) {
    throw new Error(
      `entry.png is ${png.width}x${png.height}, over the 1024x1024 cap`,
    );
  }
  const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
  mkdirSync(outDir, { recursive: true });
  const dest = join(outDir, "entry.png");
  writeFileSync(dest, png.bytes);
  const back = readFileSync(dest);
  if (!back.equals(png.bytes)) {
    throw new Error("copy check failed: bytes on disk differ from entry.png");
  }
  console.log(
    `wrote ${dest} (${png.bytes.length} bytes, ${png.width}x${png.height})`,
  );
}

try {
  main();
} catch (err) {
  console.error(`error: ${err instanceof Error ? err.message : err}`);
  process.exit(1);
}
