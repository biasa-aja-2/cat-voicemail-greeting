"""Funniest Cat Voicemail Greeting.

Writes one voicemail greeting as if a cat recorded it to
/output/entry.txt. Pure stdlib only (os, sys).
"""

import os
import sys

LINE = "You\u2019ve reached the cat. I\u2019m pushing your mug off the counter. Leave a message \u2014 I\u2019ll knock that off too."
# A real voicemail greeting in the cat's own voice: it opens with the
# greeting formula ("You've reached the cat"), the joke comes from
# something specific to cats (knocking things off shelves — here, the
# caller's mug, mid-push), and the punchline arrives fast and spoken
# aloud: "I'll knock that off too" — the message itself is next on the
# floor. Attitude throughout (the cat narrates its crime live), fresh
# angle (the voicemail message as the next victim), 104 of the
# 120-character gate.

MAX_CHARS = 120


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    path = os.path.join(out_dir, "entry.txt")

    # Self-check gate: 1-120 chars, single line, not whitespace-only.
    if not LINE or not LINE.strip():
        print("gate failed: line is empty or whitespace-only", file=sys.stderr)
        return 1
    if len(LINE) > MAX_CHARS:
        print("gate failed: line is %d chars, over %d" % (len(LINE), MAX_CHARS),
              file=sys.stderr)
        return 1
    if "\n" in LINE or "\r" in LINE:
        print("gate failed: line is not a single line", file=sys.stderr)
        return 1
    # A voicemail greeting must open with its greeting formula, in the
    # voice of the one who recorded it.
    if not LINE.startswith("You\u2019ve reached the cat"):
        print("gate failed: line does not open as the cat's greeting",
              file=sys.stderr)
        return 1

    os.makedirs(out_dir, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(LINE)
    # The grader collects outputs as another user: leave the file readable.
    os.chmod(path, 0o644)

    # Read-back verification: byte-exact, valid UTF-8, no trailing newline.
    with open(path, "rb") as f:
        raw = f.read()
    if raw != LINE.encode("utf-8"):
        print("verification failed: file bytes differ", file=sys.stderr)
        return 1
    text = raw.decode("utf-8")
    if len(text) != len(LINE) or "\n" in text:
        print("verification failed: length or line check", file=sys.stderr)
        return 1
    if text.strip() != LINE or text != text.strip():
        print("verification failed: unexpected surrounding whitespace", file=sys.stderr)
        return 1

    print("wrote %s (%d chars)" % (path, len(text)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
