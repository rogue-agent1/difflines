#!/usr/bin/env python3
"""difflines - Side-by-side and unified text diff."""
import argparse, difflib, sys

def main():
    p = argparse.ArgumentParser(description='Text file diff tool')
    p.add_argument('file1')
    p.add_argument('file2')
    p.add_argument('-s', '--side', action='store_true', help='Side-by-side view')
    p.add_argument('-c', '--context', type=int, default=3, help='Context lines')
    p.add_argument('--html', action='store_true', help='HTML output')
    p.add_argument('--stats', action='store_true', help='Show statistics only')
    p.add_argument('--words', action='store_true', help='Word-level diff')
    args = p.parse_args()

    with open(args.file1) as f: a = f.readlines()
    with open(args.file2) as f: b = f.readlines()

    if args.stats:
        sm = difflib.SequenceMatcher(None, a, b)
        added = removed = changed = 0
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == 'insert': added += j2 - j1
            elif tag == 'delete': removed += i2 - i1
            elif tag == 'replace': changed += max(i2-i1, j2-j1)
        ratio = sm.ratio()
        print(f"Files: {args.file1} ↔ {args.file2}")
        print(f"Lines: {len(a)} → {len(b)}")
        print(f"Added:   +{added}")
        print(f"Removed: -{removed}")
        print(f"Changed: ~{changed}")
        print(f"Similarity: {ratio:.1%}")
        return

    if args.html:
        d = difflib.HtmlDiff()
        print(d.make_file(a, b, args.file1, args.file2, context=True, numlines=args.context))
    elif args.side:
        width = 80
        for line in difflib.ndiff(a, b):
            print(line, end='')
    else:
        diff = difflib.unified_diff(a, b, fromfile=args.file1, tofile=args.file2, n=args.context)
        has_diff = False
        for line in diff:
            has_diff = True
            if line.startswith('+'): sys.stdout.write(f"\033[32m{line}\033[0m")
            elif line.startswith('-'): sys.stdout.write(f"\033[31m{line}\033[0m")
            elif line.startswith('@'): sys.stdout.write(f"\033[36m{line}\033[0m")
            else: sys.stdout.write(line)
        if not has_diff:
            print("Files are identical.")

if __name__ == '__main__':
    main()
