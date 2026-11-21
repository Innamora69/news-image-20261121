// news-image-20261121 entrypoint (Node 22, standard library only).
//
// The image is drawn at build time by draw.py (pure Pillow: flat vector
// pictograms and wrapped text, no network, no randomness) and shipped in
// this repository as entry.png. This program only moves those exact bytes
// to /output/entry.png, after proving they are a whole PNG inside the
// competition's gate (at most 1 MiB, at most 1024 by 1024 pixels). Copying
// bytes keeps both grader runs byte-identical by construction.
//
// Local run: mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const PNG_MAGIC = Buffer.from([
  0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a,
]);
const MAX_BYTES = 1048576;
const MAX_PX = 1024;

function pngDimensions(bytes: Buffer): [number, number] {
  // A PNG starts with an 8-byte signature, then a 4-byte length, "IHDR",
  // then width and height as big-endian uint32. Anything else is not a
  // whole PNG header.
  if (bytes.length < 33) {
    throw new Error("entry.png is too short to hold a PNG header");
  }
  if (!bytes.subarray(0, PNG_MAGIC.length).equals(PNG_MAGIC)) {
    throw new Error("entry.png is not a PNG file");
  }
  if (bytes.toString("latin1", 12, 16) !== "IHDR") {
    throw new Error("entry.png has no IHDR chunk where a PNG must");
  }
  return [bytes.readUInt32BE(16), bytes.readUInt32BE(20)];
}

function main(): void {
  const repoDir = dirname(fileURLToPath(import.meta.url));
  const source = join(repoDir, "entry.png");
  const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
  const target = join(outDir, "entry.png");

  const bytes = readFileSync(source);
  if (bytes.length > MAX_BYTES) {
    throw new Error(
      `entry.png is ${bytes.length} bytes, over the 1 MiB gate`,
    );
  }
  const [width, height] = pngDimensions(bytes);
  if (width > MAX_PX || height > MAX_PX) {
    throw new Error(
      `entry.png is ${width}x${height}, over the 1024x1024 gate`,
    );
  }

  mkdirSync(outDir, { recursive: true });
  writeFileSync(target, bytes);
  // Prove the copy landed whole: the bytes on disk must match the source
  // exactly, so both grader runs see the same image.
  const written = readFileSync(target);
  if (!written.equals(bytes)) {
    throw new Error("written entry.png does not match the source bytes");
  }
  console.log(`wrote ${target} (${bytes.length} bytes, ${width}x${height})`);
}

main();
