// news-image-20261121 entrypoint, third revision.
//
// The front page is drawn by draw.py (Pillow, offline, deterministic)
// and committed to this repository as entry.png. The grader's image
// only promises node, so this program never shells out to python:
// it checks the committed file and copies it byte for byte to the
// output directory, so both grading runs see the same image.
//
// Local check:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { existsSync, mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const BYTES_MAX = 1_048_576;
const SIDE_MAX = 1024;
const PNG_MAGIC = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);

function fail(message: string): never {
  console.error(`error: ${message}`);
  process.exit(1);
}

function main(): void {
  const here = dirname(fileURLToPath(import.meta.url));
  const source = join(here, "entry.png");
  if (!existsSync(source)) {
    fail("entry.png is missing from the repository root");
  }
  const image = readFileSync(source);
  if (image.length > BYTES_MAX) {
    fail(`entry.png is ${image.length} bytes, above the 1 MiB limit`);
  }
  if (!image.subarray(0, 8).equals(PNG_MAGIC)) {
    fail("entry.png is not a PNG file");
  }
  if (image.length < 33 || image.toString("ascii", 12, 16) !== "IHDR") {
    fail("entry.png has no readable IHDR chunk");
  }
  const width = image.readUInt32BE(16);
  const height = image.readUInt32BE(20);
  if (width > SIDE_MAX || height > SIDE_MAX) {
    fail(`entry.png is ${width}x${height}, above the 1024x1024 limit`);
  }
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  mkdirSync(outDir, { recursive: true });
  const dest = join(outDir, "entry.png");
  writeFileSync(dest, image);
  if (!readFileSync(dest).equals(image)) {
    fail("the copy in the output directory does not match entry.png");
  }
  console.log(`wrote ${dest} (${image.length} bytes, ${width}x${height})`);
}

main();
