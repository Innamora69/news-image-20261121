import { spawnSync } from "node:child_process";
import { copyFileSync, existsSync, mkdirSync, readFileSync } from "node:fs";
import { createHash } from "node:crypto";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const target = join("/output", "entry.png");

function digest(path: string): string {
  return createHash("sha256").update(readFileSync(path)).digest("hex");
}

function drawInto(tmp: string): void {
  const run = spawnSync("python3", ["draw.py"], {
    cwd: root,
    env: { ...process.env, OUT: tmp },
    encoding: "utf8",
  });
  if (run.status !== 0) {
    console.error(run.stderr || "draw.py failed");
    process.exit(1);
  }
  if (!existsSync(tmp)) {
    console.error("draw.py wrote no image");
    process.exit(1);
  }
}

function main(): void {
  // Draw twice and keep the run only when both bytes agree.
  const first = "/tmp/news-image-a.png";
  const second = "/tmp/news-image-b.png";
  drawInto(first);
  drawInto(second);
  if (digest(first) !== digest(second)) {
    console.error("draw.py is not deterministic");
    process.exit(1);
  }
  mkdirSync("/output", { recursive: true });
  copyFileSync(first, target);
  console.log("wrote", target, digest(target));
}

main();
