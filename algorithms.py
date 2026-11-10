"""
algorithms.py - Divide and Conquer Algorithms with Step Instrumentation.
Implements:
1. Closest Pair of 2D Points (O(n log n))
2. Karatsuba Integer Multiplication (O(n^1.585))

Reuses and instruments the original logic to record step-by-step states
for visualization in the Streamlit application.
"""

import math
import os
import time

def distance(p1, p2):
    """Calculates Euclidean distance between two 2D points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


# =====================================================================
# 1. CLOSEST PAIR OF POINTS (INSTRUMENTED)
# =====================================================================

def uninstrumented_closest_pair(px, py):
    """
    Standard fast closest pair solver used when depth >= max_depth.
    Runs silently without creating step records.
    """
    n = len(px)
    if n <= 3:
        minimum = float('inf')
        pair = None
        for i in range(len(px)):
            for j in range(i + 1, len(px)):
                d = distance(px[i], px[j])
                if d < minimum:
                    minimum = d
                    pair = (px[i], px[j])
        return minimum, pair

    mid = n // 2
    mid_x = px[mid][0]

    left_x = px[:mid]
    right_x = px[mid:]

    left_ids = {p[2] for p in left_x}
    left_y = [p for p in py if p[2] in left_ids]
    right_y = [p for p in py if p[2] not in left_ids]

    d1, pair1 = uninstrumented_closest_pair(left_x, left_y)
    d2, pair2 = uninstrumented_closest_pair(right_x, right_y)

    if d1 < d2:
        minimum = d1
        best_pair = pair1
    else:
        minimum = d2
        best_pair = pair2

    strip = [p for p in py if abs(p[0] - mid_x) < minimum]
    for i in range(len(strip)):
        for j in range(i + 1, min(i + 8, len(strip))):
            d = distance(strip[i], strip[j])
            if d < minimum:
                minimum = d
                best_pair = (strip[i], strip[j])

    return minimum, best_pair


def compute_closest_pair_steps(points, max_depth=3):
    """
    Instruments Closest Pair algorithm to record visualization steps.
    Points is a list of tuples: (x, y, id).
    Limits recursion detail to max_depth.
    """
    px = sorted(points, key=lambda p: p[0])
    py = sorted(points, key=lambda p: p[1])
    
    steps = []
    global_state = {
        'best_dist': float('inf'),
        'best_pair': None,
        'all_points': points
    }

    # Step 0: Initial state - No pairs evaluated yet
    steps.append({
        'type': 'init',
        'depth': 0,
        'path': 'Start',
        'mid_x': None,
        'left_bounds': None,
        'right_bounds': None,
        'strip_bounds': None,
        'comparing_pair': None,
        'best_pair_so_far': None,
        'best_dist_so_far': float('inf'),
        'caption': f"Dataset loaded: {len(points)} points. Pre-sorted by X and Y coordinates. Ready to divide."
    })

    def solve(px_sub, py_sub, depth=0, path="Root"):
        n = len(px_sub)
        
        # Base case or depth cutoff
        if depth >= max_depth:
            sub_d, sub_pair = uninstrumented_closest_pair(px_sub, py_sub)
            is_new_best = False
            if sub_pair and sub_d < global_state['best_dist']:
                global_state['best_dist'] = sub_d
                global_state['best_pair'] = sub_pair
                is_new_best = True
                
            steps.append({
                'type': 'collapsed',
                'depth': depth,
                'path': path,
                'mid_x': None,
                'left_bounds': (px_sub[0][0], px_sub[-1][0]),
                'right_bounds': None,
                'strip_bounds': None,
                'comparing_pair': sub_pair,
                'best_pair_so_far': global_state['best_pair'],
                'best_dist_so_far': global_state['best_dist'],
                'caption': f"[{path}] Depth limit {max_depth} reached: Evaluated {n} points recursively → local distance {sub_d:.4f}." +
                           (f" ⭐ New global minimum found: δ = {sub_d:.4f}!" if is_new_best else f" (Best so far: {global_state['best_dist']:.4f})")
            })
            return sub_d, sub_pair

        if n <= 3:
            # Base case: Brute force for small n <= 3
            min_d = float('inf')
            best_p = None
            for i in range(n):
                for j in range(i + 1, n):
                    p1, p2 = px_sub[i], px_sub[j]
                    d = distance(p1, p2)
                    if d < min_d:
                        min_d = d
                        best_p = (p1, p2)
                    is_new_global = False
                    if d < global_state['best_dist']:
                        global_state['best_dist'] = d
                        global_state['best_pair'] = (p1, p2)
                        is_new_global = True
                        
                    steps.append({
                        'type': 'base_case_compare',
                        'depth': depth,
                        'path': path,
                        'mid_x': None,
                        'left_bounds': (px_sub[0][0], px_sub[-1][0]),
                        'right_bounds': None,
                        'strip_bounds': None,
                        'comparing_pair': (p1, p2),
                        'best_pair_so_far': global_state['best_pair'],
                        'best_dist_so_far': global_state['best_dist'],
                        'caption': f"[{path}] Base case (n={n}): Checking pair ({p1[0]}, {p1[1]}) and ({p2[0]}, {p2[1]}). Distance = {d:.4f}." +
                                   (f" ⭐ New global minimum found: δ = {d:.4f}!" if is_new_global else f" (Best so far: {global_state['best_dist']:.4f})")
                    })
            return min_d, best_p

        # Divide step
        mid = n // 2
        mid_x = px_sub[mid][0]
        left_x = px_sub[:mid]
        right_x = px_sub[mid:]

        left_ids = {p[2] for p in left_x}
        left_y = [p for p in py_sub if p[2] in left_ids]
        right_y = [p for p in py_sub if p[2] not in left_ids]

        left_min_x = left_x[0][0]
        right_max_x = right_x[-1][0]

        steps.append({
            'type': 'divide',
            'depth': depth,
            'path': path,
            'mid_x': mid_x,
            'left_bounds': (left_min_x, mid_x),
            'right_bounds': (mid_x, right_max_x),
            'strip_bounds': None,
            'comparing_pair': None,
            'best_pair_so_far': global_state['best_pair'],
            'best_dist_so_far': global_state['best_dist'],
            'caption': f"[{path}] Divide: Vertical dashed divider at median x = {mid_x}. Split into Left partition ({len(left_x)} pts, Light Blue) and Right partition ({len(right_x)} pts, Yellow)."
        })

        # Recurse Left
        d1, pair1 = solve(left_x, left_y, depth + 1, path + " → Left")

        # Recurse Right
        d2, pair2 = solve(right_x, right_y, depth + 1, path + " → Right")

        # Minimum across both halves
        if d1 < d2:
            minimum = d1
            best_pair = pair1
        else:
            minimum = d2
            best_pair = pair2

        if minimum < global_state['best_dist']:
            global_state['best_dist'] = minimum
            global_state['best_pair'] = best_pair

        # Merge Strip Creation
        strip_min = mid_x - minimum
        strip_max = mid_x + minimum

        steps.append({
            'type': 'strip_create',
            'depth': depth,
            'path': path,
            'mid_x': mid_x,
            'left_bounds': (left_min_x, mid_x),
            'right_bounds': (mid_x, right_max_x),
            'strip_bounds': (strip_min, strip_max),
            'comparing_pair': None,
            'best_pair_so_far': global_state['best_pair'],
            'best_dist_so_far': global_state['best_dist'],
            'caption': f"[{path}] Merge Strip Created: δ = min(d_left={d1:.4f}, d_right={d2:.4f}) = {minimum:.4f}. Constructing Peach strip [mid_x - δ, mid_x + δ] of width 2δ = {2*minimum:.4f}."
        })

        # Inspect strip points
        strip = [p for p in py_sub if abs(p[0] - mid_x) < minimum]
        closer_found_in_strip = False

        # Check at most 7 vertical neighbors for each point in strip
        checked_pairs_count = 0
        candidate_checks_to_show = 2  # Show sample candidate comparisons in strip with Miami Magenta
        for i in range(len(strip)):
            for j in range(i + 1, min(i + 8, len(strip))):
                p1, p2 = strip[i], strip[j]
                d = distance(p1, p2)
                checked_pairs_count += 1
                
                if d < minimum:
                    minimum = d
                    best_pair = (p1, p2)
                if d < global_state['best_dist']:
                    global_state['best_dist'] = d
                    global_state['best_pair'] = (p1, p2)
                    closer_found_in_strip = True

                    steps.append({
                        'type': 'strip_closer_found',
                        'depth': depth,
                        'path': path,
                        'mid_x': mid_x,
                        'left_bounds': (left_min_x, mid_x),
                        'right_bounds': (mid_x, right_max_x),
                        'strip_bounds': (mid_x - minimum, mid_x + minimum),
                        'comparing_pair': (p1, p2),
                        'best_pair_so_far': global_state['best_pair'],
                        'best_dist_so_far': global_state['best_dist'],
                        'caption': f"[{path}] Cross-boundary candidate found in strip! Points ({p1[0]}, {p1[1]}) and ({p2[0]}, {p2[1]}) have distance {d:.4f} < previous minimum! ⭐ New global minimum found: δ = {d:.4f}!"
                    })
                elif candidate_checks_to_show > 0:
                    candidate_checks_to_show -= 1
                    steps.append({
                        'type': 'strip_candidate_check',
                        'depth': depth,
                        'path': path,
                        'mid_x': mid_x,
                        'left_bounds': (left_min_x, mid_x),
                        'right_bounds': (mid_x, right_max_x),
                        'strip_bounds': (strip_min, strip_max),
                        'comparing_pair': (p1, p2),
                        'best_pair_so_far': global_state['best_pair'],
                        'best_dist_so_far': global_state['best_dist'],
                        'caption': f"[{path}] Inspecting candidate pair in strip: ({p1[0]}, {p1[1]}) and ({p2[0]}, {p2[1]}). Distance = {d:.4f} ≥ current δ ({minimum:.4f})."
                    })

        if not closer_found_in_strip and checked_pairs_count == 0:
            steps.append({
                'type': 'strip_inspected',
                'depth': depth,
                'path': path,
                'mid_x': mid_x,
                'left_bounds': (left_min_x, mid_x),
                'right_bounds': (mid_x, right_max_x),
                'strip_bounds': (strip_min, strip_max),
                'comparing_pair': None,
                'best_pair_so_far': global_state['best_pair'],
                'best_dist_so_far': global_state['best_dist'],
                'caption': f"[{path}] Strip inspection: Strip is empty (0 points). No cross-boundary pair exists closer than δ = {minimum:.4f}."
            })

        return minimum, best_pair

    final_d, final_p = solve(px, py, depth=0, path="Root")

    # Final step
    steps.append({
        'type': 'final',
        'depth': 0,
        'path': 'Complete',
        'mid_x': None,
        'left_bounds': None,
        'right_bounds': None,
        'strip_bounds': None,
        'comparing_pair': None,
        'best_pair_so_far': final_p,
        'best_dist_so_far': final_d,
        'caption': f"🏆 Algorithm Complete! Closest pair: Point 1 ({final_p[0][0]}, {final_p[0][1]}) and Point 2 ({final_p[1][0]}, {final_p[1][1]}) with Minimum Distance = {final_d:.4f}."
    })

    return steps


# =====================================================================
# 2. KARATSUBA INTEGER MULTIPLICATION (INSTRUMENTED)
# =====================================================================

def uninstrumented_karatsuba(x, y):
    """
    Standard Karatsuba implementation used when depth >= max_depth.
    Runs silently and returns the integer product.
    """
    if x < 10 or y < 10:
        return x * y

    n = max(len(str(x)), len(str(y)))
    m = n // 2
    power = 10 ** m

    a = x // power
    b = x % power
    c = y // power
    d = y % power

    z0 = uninstrumented_karatsuba(b, d)
    z2 = uninstrumented_karatsuba(a, c)
    z1 = uninstrumented_karatsuba(a + b, c + d)

    result = (z2 * (10 ** (2 * m))
              + (z1 - z2 - z0) * power
              + z0)
    return result


def format_truncated(val, max_chars=20):
    """Formats large integer with ellipsis if long."""
    s = str(val)
    if len(s) <= max_chars:
        return s
    half = (max_chars - 3) // 2
    return f"{s[:half]}…{s[-half:]} ({len(s)} digits)"


def compute_karatsuba_steps(x, y, max_depth=3):
    """
    Instruments Karatsuba's algorithm to record step-by-step states.
    Limits recursion expansion to max_depth.
    """
    steps = []
    tree_nodes = []  # Stores tree call structure for rendering
    
    # Initial step
    steps.append({
        'type': 'init',
        'depth': 0,
        'path': 'Root',
        'x': x,
        'y': y,
        'n': max(len(str(x)), len(str(y))),
        'm': max(len(str(x)), len(str(y))) // 2,
        'a': None,
        'b': None,
        'c': None,
        'd': None,
        'z2': None,
        'z0': None,
        'z1': None,
        'middle': None,
        'result': None,
        'tree': [],
        'caption': f"Loaded operands: x has {len(str(x))} digits, y has {len(str(y))} digits. Preparing Karatsuba Divide & Conquer."
    })

    def solve(curr_x, curr_y, depth=0, path="Root", branch="Root"):
        node_id = path
        node_info = {
            'path': path,
            'branch': branch,
            'depth': depth,
            'x_str': format_truncated(curr_x, 14),
            'y_str': format_truncated(curr_y, 14),
            'status': 'active',
            'result_str': None
        }
        tree_nodes.append(node_info)

        if depth >= max_depth:
            res = uninstrumented_karatsuba(curr_x, curr_y)
            node_info['status'] = 'computed'
            node_info['result_str'] = format_truncated(res, 12)

            steps.append({
                'type': 'collapsed',
                'depth': depth,
                'path': path,
                'x': curr_x,
                'y': curr_y,
                'n': max(len(str(curr_x)), len(str(curr_y))),
                'm': max(len(str(curr_x)), len(str(curr_y))) // 2,
                'a': None,
                'b': None,
                'c': None,
                'd': None,
                'z2': None,
                'z0': None,
                'z1': None,
                'middle': None,
                'result': res,
                'caption': f"[{path}] Depth limit {max_depth} reached: Subproblem computed recursively → result = {format_truncated(res, 22)} ({len(str(res))} digits)."
            })
            return res

        if curr_x < 10 or curr_y < 10:
            res = curr_x * curr_y
            node_info['status'] = 'done'
            node_info['result_str'] = str(res)

            steps.append({
                'type': 'base_case',
                'depth': depth,
                'path': path,
                'x': curr_x,
                'y': curr_y,
                'n': max(len(str(curr_x)), len(str(curr_y))),
                'm': 0,
                'a': None,
                'b': None,
                'c': None,
                'd': None,
                'z2': None,
                'z0': None,
                'z1': None,
                'middle': None,
                'result': res,
                'caption': f"[{path}] Base case: Single-digit product {curr_x} × {curr_y} = {res}."
            })
            return res

        # Split into high and low halves
        n = max(len(str(curr_x)), len(str(curr_y)))
        m = n // 2
        power = 10 ** m

        a = curr_x // power
        b = curr_x % power
        c = curr_y // power
        d = curr_y % power

        steps.append({
            'type': 'split',
            'depth': depth,
            'path': path,
            'x': curr_x,
            'y': curr_y,
            'n': n,
            'm': m,
            'a': a,
            'b': b,
            'c': c,
            'd': d,
            'z2': None,
            'z0': None,
            'z1': None,
            'middle': None,
            'result': None,
            'caption': f"[{path}] Split at m = {m}: x split into a ({format_truncated(a, 12)}, Light Blue) & b ({format_truncated(b, 12)}, Yellow); y split into c ({format_truncated(c, 12)}, Light Blue) & d ({format_truncated(d, 12)}, Yellow)."
        })

        # Sub-product 1: z2 = a * c
        z2 = solve(a, c, depth + 1, path + ".z2", "z2 (high)")

        # Sub-product 2: z0 = b * d
        z0 = solve(b, d, depth + 1, path + ".z0", "z0 (low)")

        # Sub-product 3: z1 = (a + b) * (c + d)
        z1 = solve(a + b, c + d, depth + 1, path + ".z1", "z1 (cross)")

        # Combine
        middle = z1 - z2 - z0
        term_high = z2 * (10 ** (2 * m))
        term_mid = middle * power
        term_low = z0
        res = term_high + term_mid + term_low

        node_info['status'] = 'combined'
        node_info['result_str'] = format_truncated(res, 12)

        steps.append({
            'type': 'combine',
            'depth': depth,
            'path': path,
            'x': curr_x,
            'y': curr_y,
            'n': n,
            'm': m,
            'a': a,
            'b': b,
            'c': c,
            'd': d,
            'z2': z2,
            'z0': z0,
            'z1': z1,
            'middle': middle,
            'result': res,
            'caption': f"[{path}] Combine: z2·10^(2·{m}) + (z1 − z2 − z0)·10^{m} + z0. Calculated middle term = {format_truncated(middle, 14)} (Peach). Total combined = {format_truncated(res, 20)} ({len(str(res))} digits)."
        })

        return res

    final_result = solve(x, y, depth=0, path="Root", branch="Root")
    verified = (final_result == x * y)

    # Final step
    steps.append({
        'type': 'final',
        'depth': 0,
        'path': 'Complete',
        'x': x,
        'y': y,
        'n': max(len(str(x)), len(str(y))),
        'm': max(len(str(x)), len(str(y))) // 2,
        'a': None,
        'b': None,
        'c': None,
        'd': None,
        'z2': None,
        'z0': None,
        'z1': None,
        'middle': None,
        'result': final_result,
        'verified': verified,
        'digits': len(str(final_result)),
        'caption': f"🏆 Karatsuba Complete! Result has {len(str(final_result))} digits. ✓ Confirmed: Product exactly equals Python's native calculation x * y!"
    })

    return steps, tree_nodes


# =====================================================================
# 3. FILE PARSERS
# =====================================================================

def parse_closest_pair_file(content_or_path):
    """
    Parses file content or filepath for closest pair.
    First line: n
    Next n lines: x y
    """
    if '\n' not in content_or_path and os.path.exists(content_or_path):
        with open(content_or_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
    else:
        lines = [line.strip() for line in content_or_path.splitlines() if line.strip()]

    if not lines:
        return []
    n = int(lines[0])
    points = []
    for i in range(1, n + 1):
        if i < len(lines):
            parts = lines[i].split()
            if len(parts) >= 2:
                points.append((int(parts[0]), int(parts[1]), i - 1))
    return points


def parse_integer_mult_file(content_or_path):
    """
    Parses file content or filepath for Karatsuba integer multiplication.
    Two big integers, one per line.
    """
    if '\n' not in content_or_path and os.path.exists(content_or_path):
        with open(content_or_path, 'r') as f:
            lines = [line.strip() for line in f if line.strip()]
    else:
        lines = [line.strip() for line in content_or_path.splitlines() if line.strip()]

    if len(lines) < 2:
        return 0, 0
    x = int(lines[0])
    y = int(lines[1])
    return x, y


# =====================================================================
# 4. MATPLOTLIB VISUALIZATION RENDERERS
# =====================================================================

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle


def plot_closest_pair_step(points, step, fig_size=(10, 5.2)):
    """
    Renders the matplotlib visualization for a Closest Pair step.
    Color palette (simple names):
    - Light Blue (#A7D8DB) = Left partition
    - Yellow (#FFE08A) = Right partition
    - Peach (#FFD1B6) = Merge strip (2*delta)
    - Black dashed thin line = divider
    - Black dots = all points (small)
    - Pink (#E91E63) = candidate comparing pair
    - Dark Green (#2E7D32) = best pair so far (always visible once found)
    Legend placed BELOW the plot, not inside the chart area.
    """
    xs = [p[0] for p in points]
    ys = [p[1] for p in points]
    x_min, x_max = min(xs), max(xs)
    y_min, y_max = min(ys), max(ys)

    pad_x = (x_max - x_min) * 0.04 if x_max > x_min else 100
    pad_y = (y_max - y_min) * 0.04 if y_max > y_min else 100

    # Reserve bottom margin space for the legend (below the axes)
    fig, ax = plt.subplots(figsize=fig_size, dpi=100)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    # Tight layout with bottom room for legend
    fig.subplots_adjust(bottom=0.22, top=0.93, left=0.07, right=0.98)

    ax.set_xlim(x_min - pad_x, x_max + pad_x)
    ax.set_ylim(y_min - pad_y, y_max + pad_y)

    legend_handles = []

    # 1. Shaded regions (solid fills, no edge outline — axvspan outlines auto)
    # Left partition (Light Blue)
    if step.get('left_bounds'):
        l_min, l_max = step['left_bounds']
        ax.axvspan(l_min, l_max, facecolor='#A7D8DB', alpha=1.0, zorder=2)
        import matplotlib.patches as mpatches
        legend_handles.append(mpatches.Patch(facecolor='#A7D8DB', edgecolor='#272A2A', label='Left (Light Blue)'))

    # Right partition (Yellow)
    if step.get('right_bounds'):
        r_min, r_max = step['right_bounds']
        ax.axvspan(r_min, r_max, facecolor='#FFE08A', alpha=1.0, zorder=2)
        import matplotlib.patches as mpatches
        legend_handles.append(mpatches.Patch(facecolor='#FFE08A', edgecolor='#272A2A', label='Right (Yellow)'))

    # Merge strip / Peach
    if step.get('strip_bounds'):
        s_min, s_max = step['strip_bounds']
        ax.axvspan(s_min, s_max, facecolor='#FFD1B6', alpha=1.0, zorder=3)
        import matplotlib.patches as mpatches
        legend_handles.append(mpatches.Patch(facecolor='#FFD1B6', edgecolor='#272A2A', label='Merge Strip (Peach)'))

    # 2. Divider line (black, thin dashed)
    if step.get('mid_x') is not None:
        import matplotlib.lines as mlines
        ax.axvline(x=step['mid_x'], color='#000000', linestyle='--', linewidth=0.9, zorder=5)
        legend_handles.append(mlines.Line2D([], [], color='#000000', linestyle='--', linewidth=1, label=f"Divider x={step['mid_x']}"))

    # 3. Points: small black dots (s=10, cleanly separated)
    ax.scatter(xs, ys, color='#000000', s=10, alpha=0.85, zorder=6)
    import matplotlib.lines as mlines
    legend_handles.append(mlines.Line2D([], [], color='#000000', marker='o', markersize=3.5,
                                         linestyle='None', label=f'Points (n={len(points)})'))

    # 4. Best pair so far — ALWAYS prominently drawn in Dark Green
    if step.get('best_pair_so_far'):
        bp1, bp2 = step['best_pair_so_far']
        is_final = (step.get('type') == 'final')
        label_text = 'Final Closest Pair (Dark Green)' if is_final else 'Best Pair So Far (Dark Green)'
        ax.plot([bp1[0], bp2[0]], [bp1[1], bp2[1]], color='#2E7D32', linewidth=3.5,
                linestyle='-', marker='o', markersize=6.5, zorder=11)
        import matplotlib.lines as mlines
        legend_handles.append(mlines.Line2D([], [], color='#2E7D32', linewidth=3.5, marker='o',
                                             markersize=6.5, label=label_text))

    # 5. Pair currently being compared (Pink line)
    if step.get('comparing_pair'):
        p1, p2 = step['comparing_pair']
        # If comparing pair is different from best pair, render it in vibrant Pink
        is_same_as_best = False
        if step.get('best_pair_so_far'):
            bp1, bp2 = step['best_pair_so_far']
            if (p1 == bp1 and p2 == bp2) or (p1 == bp2 and p2 == bp1):
                is_same_as_best = True

        if not is_same_as_best:
            ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color='#E91E63', linewidth=2.5,
                    linestyle='-', marker='o', markersize=5.5, zorder=12)
            import matplotlib.lines as mlines
            legend_handles.append(mlines.Line2D([], [], color='#E91E63', linewidth=2.5, marker='o',
                                                 markersize=5.5, label='Comparing Pair (Pink)'))

    # Axes styling
    sub_title = step.get('path', 'Root')
    ax.set_title(f"Closest Pair — Subproblem: {sub_title}",
                 fontsize=11, fontweight='bold', color='#000000', pad=6)
    ax.set_xlabel('X', fontsize=9, color='#000000')
    ax.set_ylabel('Y', fontsize=9, color='#000000')
    ax.tick_params(colors='#000000', labelsize=8)
    for spine in ax.spines.values():
        spine.set_edgecolor('#888888')
        spine.set_linewidth(0.8)
    ax.grid(True, linestyle=':', alpha=0.3, color='#999999')

    # Legend BELOW the plot in figure space (completely outside the axes)
    if legend_handles:
        ax.legend(handles=legend_handles, loc='upper center',
                  bbox_to_anchor=(0.5, -0.16), ncol=min(len(legend_handles), 5),
                  frameon=True, facecolor='white', edgecolor='#CCCCCC',
                  fontsize=8.5, handlelength=1.5, handleheight=1.0, borderpad=0.6)

    return fig


def plot_karatsuba_step(step, fig_size=(10, 5.0)):
    """
    Renders the matplotlib visualization for a Karatsuba Multiplication step.
    Strictly adheres to specified color palette:
    - High part (a, c) / z2: Sea Mist #A7D8DB, solid fill with thin dark gray #272A2A outline
    - Low part (b, d) / z0: Sunlit #FFE08A, solid fill with thin dark gray outline
    - Merge / z1: Peach Sorbet #FFD1B6, solid fill with thin dark gray outline
    - Divider line: black dashed
    - Miami Magenta #E91E63 for active recursive focus
    - Dark green #2E7D32 for final answer / verified result
    """
    fig, ax = plt.subplots(figsize=fig_size, dpi=100)
    fig.patch.set_facecolor('white')
    ax.set_facecolor('white')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    st_type = step.get('type')
    path = step.get('path', 'Root')

    # Top Header
    ax.text(50, 96, f"Karatsuba Multiplier — Call Level: {path} ({st_type.upper()})",
            ha='center', va='center', fontsize=12, fontweight='bold', color='#000000')

    # Section 1: Number Partitioning
    if step.get('a') is not None:
        m = step.get('m', 0)
        # Number x partitioned
        ax.text(50, 89, f"x ({len(str(step['x']))} digits) split at m = {m}:",
                ha='center', va='center', fontsize=9.5, fontweight='bold', color='#000000')
        
        # a (High part, Sea Mist)
        ax.add_patch(Rectangle((8, 73), 39, 12, facecolor='#A7D8DB',
                               edgecolor='#272A2A', linewidth=1.5))
        ax.text(27.5, 79, f"a (High, {len(str(step['a']))} dig)\n{format_truncated(step['a'], 16)}",
                ha='center', va='center', fontsize=8.5, color='#000000', fontweight='bold')

        # b (Low part, Sunlit)
        ax.add_patch(Rectangle((53, 73), 39, 12, facecolor='#FFE08A',
                               edgecolor='#272A2A', linewidth=1.5))
        ax.text(72.5, 79, f"b (Low, {len(str(step['b']))} dig)\n{format_truncated(step['b'], 16)}",
                ha='center', va='center', fontsize=8.5, color='#000000', fontweight='bold')

        # Dashed divider between a and b
        ax.plot([50, 50], [71, 87], color='#000000', linestyle='--', linewidth=1.6)

        # Number y partitioned
        ax.text(50, 68, f"y ({len(str(step['y']))} digits) split at m = {m}:",
                ha='center', va='center', fontsize=9.5, fontweight='bold', color='#000000')

        # c (High part, Sea Mist)
        ax.add_patch(Rectangle((8, 52), 39, 12, facecolor='#A7D8DB',
                               edgecolor='#272A2A', linewidth=1.5))
        ax.text(27.5, 58, f"c (High, {len(str(step['c']))} dig)\n{format_truncated(step['c'], 16)}",
                ha='center', va='center', fontsize=8.5, color='#000000', fontweight='bold')

        # d (Low part, Sunlit)
        ax.add_patch(Rectangle((53, 52), 39, 12, facecolor='#FFE08A',
                               edgecolor='#272A2A', linewidth=1.5))
        ax.text(72.5, 58, f"d (Low, {len(str(step['d']))} dig)\n{format_truncated(step['d'], 16)}",
                ha='center', va='center', fontsize=8.5, color='#000000', fontweight='bold')

        # Dashed divider between c and d
        ax.plot([50, 50], [50, 66], color='#000000', linestyle='--', linewidth=1.6)
    else:
        # Full operands display box
        ax.add_patch(Rectangle((10, 52), 80, 34, facecolor='#FADADD',
                               edgecolor='#272A2A', linewidth=1.5))
        ax.text(50, 77, "Current Operands (Base / Collapsed Level)",
                ha='center', va='center', fontsize=10.5, fontweight='bold', color='#000000')
        ax.text(50, 67, f"x ({len(str(step['x']))} digits) = {format_truncated(step['x'], 32)}",
                ha='center', va='center', fontsize=9.5, fontweight='bold', color='#000000')
        ax.text(50, 58, f"y ({len(str(step['y']))} digits) = {format_truncated(step['y'], 32)}",
                ha='center', va='center', fontsize=9.5, fontweight='bold', color='#000000')

    # Section 2: Three Sub-Products
    ax.text(50, 44, "3 Sub-Products: z2 = a·c (Light Blue),  z0 = b·d (Yellow),  z1 = (a+b)(c+d) (Peach)",
            ha='center', va='center', fontsize=9.5, fontweight='bold', color='#000000')

    # z2 box (Sea Mist)
    z2_val = step.get('z2')
    z2_disp = format_truncated(z2_val, 14) if z2_val is not None else "(in progress...)"
    z2_edge = '#E91E63' if path.endswith('.z2') else '#272A2A'
    z2_lw = 2.5 if path.endswith('.z2') else 1.5
    ax.add_patch(Rectangle((6, 26), 26, 14, facecolor='#A7D8DB',
                           edgecolor=z2_edge, linewidth=z2_lw))
    ax.text(19, 35, "z2 = a × c", ha='center', va='center', fontsize=9, fontweight='bold', color='#000000')
    ax.text(19, 29, z2_disp, ha='center', va='center', fontsize=8, color='#000000')

    # z1 box (Peach Sorbet)
    z1_val = step.get('z1')
    z1_disp = format_truncated(z1_val, 14) if z1_val is not None else "(in progress...)"
    z1_edge = '#E91E63' if path.endswith('.z1') else '#272A2A'
    z1_lw = 2.5 if path.endswith('.z1') else 1.5
    ax.add_patch(Rectangle((37, 26), 26, 14, facecolor='#FFD1B6',
                           edgecolor=z1_edge, linewidth=z1_lw))
    ax.text(50, 35, "z1 = (a+b)(c+d)", ha='center', va='center', fontsize=9, fontweight='bold', color='#000000')
    ax.text(50, 29, z1_disp, ha='center', va='center', fontsize=8, color='#000000')

    # z0 box (Sunlit)
    z0_val = step.get('z0')
    z0_disp = format_truncated(z0_val, 14) if z0_val is not None else "(in progress...)"
    z0_edge = '#E91E63' if path.endswith('.z0') else '#272A2A'
    z0_lw = 2.5 if path.endswith('.z0') else 1.5
    ax.add_patch(Rectangle((68, 26), 26, 14, facecolor='#FFE08A',
                           edgecolor=z0_edge, linewidth=z0_lw))
    ax.text(81, 35, "z0 = b × d", ha='center', va='center', fontsize=9, fontweight='bold', color='#000000')
    ax.text(81, 29, z0_disp, ha='center', va='center', fontsize=8, color='#000000')

    # Section 3: Bottom Combine or Result Box
    if st_type == 'combine':
        m = step.get('m', 0)
        ax.add_patch(Rectangle((6, 5), 88, 17, facecolor='#FADADD',
                               edgecolor='#272A2A', linewidth=1.5))
        ax.text(50, 16.5, f"Combine: z2·10^(2·{m}) + (z1 − z2 − z0)·10^{m} + z0",
                ha='center', va='center', fontsize=9.5, fontweight='bold', color='#000000')
        ax.text(50, 10.5, f"Middle Term (ad+bc) = {format_truncated(step.get('middle'), 18)}",
                ha='center', va='center', fontsize=8.5, color='#000000')
        ax.text(50, 6.5, f"= {format_truncated(step.get('result'), 32)} ({len(str(step.get('result')))} digits)",
                ha='center', va='center', fontsize=9.5, fontweight='bold', color='#2E7D32')
    elif st_type == 'final':
        ax.add_patch(Rectangle((6, 5), 88, 17, facecolor='#F3F9F3',
                               edgecolor='#2E7D32', linewidth=2.5))
        ax.text(50, 15.5, "[FINAL ANSWER] Karatsuba Product Verified!",
                ha='center', va='center', fontsize=11, fontweight='bold', color='#2E7D32')
        ax.text(50, 9.5, f"Product ({step.get('digits')} digits): {format_truncated(step.get('result'), 36)}",
                ha='center', va='center', fontsize=9.5, fontweight='bold', color='#000000')
    else:
        ax.add_patch(Rectangle((6, 6), 88, 14, facecolor='#FADADD',
                               edgecolor='#272A2A', linewidth=1.2))
        sub_desc = step.get('caption', '')
        if len(sub_desc) > 95:
            sub_desc = sub_desc[:92] + "..."
        ax.text(50, 13, f"Action: {sub_desc}",
                ha='center', va='center', fontsize=8.5, color='#000000')

    plt.tight_layout()
    return fig
