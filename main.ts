// news-image-20261121 entrypoint, second revision.
//
// draw.py (Pillow, offline, deterministic) already produced the
// front page as entry.png in this directory. All this program does
// is gate that file and copy it byte for byte to the output the
// grader reads, so both grading runs see the same image.
//
// Local check:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const CAP = 1_048_576;
const MAX_SIDE = 1024;
const MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

function main(): void {
  const here = dirname(fileURLToPath(import.meta.url));
  const src = join(here, "entry.png");
  if (!existsSync(src)) {
    throw new Error("entry.png is missing from the repository root");
  }
  const data = readFileSync(src);
  if (data.length > CAP) {
    throw new Error(`entry.png is ${data.length} bytes, above the 1 MiB limit`);
  }
  if (!data.subarray(0, 8).equals(MAGIC)) {
    throw new Error("entry.png is not a PNG file");
  }
  if (data.toString("ascii", 12, 16) !== "IHDR" || data.length < 33) {
    throw new Error("entry.png has no readable IHDR chunk");
  }
  const width = data.readUInt32BE(16);
  const height = data.readUInt32BE(20);
  if (width > MAX_SIDE || height > MAX_SIDE) {
    throw new Error(`entry.png is ${width}x${height}, above the 1024x1024 limit`);
  }
  const dir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  mkdirSync(dir, { recursive: true });
  const dest = join(dir, "entry.png");
  writeFileSync(dest, data);
  if (!readFileSync(dest).equals(data)) {
    throw new Error("the copy in the output directory does not match entry.png");
  }
  console.log(`wrote ${dest} (${data.length} bytes, ${width}x${height})`);
}

try {
  main();
} catch (err) {
  console.error(`error: ${err instanceof Error ? err.message : err}`);
  process.exit(1);
}
