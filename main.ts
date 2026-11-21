// news-image-20261121 entrypoint.
//
// The front page is rendered ahead of time by draw.py (Pillow, no network,
// no randomness) and committed here as entry.png. All this program does is
// carry those exact bytes to the grader's output file, after checking the
// PNG is whole and inside the competition gates (<= 1 MiB, <= 1024x1024).
// Byte-for-byte copying keeps the two grading runs identical.
//
// Local check:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_SIGNATURE = [0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a];
const BYTE_LIMIT = 1024 * 1024;
const SIDE_LIMIT = 1024;

type PngInfo = { bytes: Buffer; width: number; height: number };

function loadEntryPng(path: string): PngInfo {
  if (!existsSync(path)) {
    throw new Error(`missing entry image: ${path}`);
  }
  const bytes = readFileSync(path);
  if (bytes.length > BYTE_LIMIT) {
    throw new Error(`entry.png is ${bytes.length} bytes, over the 1 MiB cap`);
  }
  const magic = [...bytes.subarray(0, 8)];
  if (magic.some((b, i) => b !== PNG_SIGNATURE[i])) {
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

function run(): void {
  const here = dirname(fileURLToPath(import.meta.url));
  const png = loadEntryPng(join(here, "entry.png"));
  if (png.width > SIDE_LIMIT || png.height > SIDE_LIMIT) {
    throw new Error(
      `entry.png is ${png.width}x${png.height}, over the 1024x1024 cap`,
    );
  }
  const outDir = process.env.MAKEFUN_OUTPUT_DIR || "/output";
  mkdirSync(outDir, { recursive: true });
  const dest = join(outDir, "entry.png");
  writeFileSync(dest, png.bytes);
  const again = readFileSync(dest);
  if (!again.equals(png.bytes)) {
    throw new Error("copy check failed: bytes on disk differ from entry.png");
  }
  console.log(
    `wrote ${dest} (${png.bytes.length} bytes, ${png.width}x${png.height})`,
  );
}

try {
  run();
} catch (err) {
  console.error(`error: ${err instanceof Error ? err.message : err}`);
  process.exit(1);
}
