"""
Sprint 01: Verifier Noise & Search Collapse Simulation
Zero external dependencies (pure Python standard library).
Simulates Best-of-N vs. Beam Search under varying Verifier Accuracy.
Outputs an ASCII results table and an SVG plot.
"""

import math
import random

def run_simulation(num_trials=2000, depth=4, beam_width=2, n_bon=8):
    # Verifier accuracies from 60% to 98%
    accuracies = [round(0.60 + 0.03 * i, 2) for i in range(13)]
    
    bon_success = []
    beam_success = []
    
    random.seed(42)
    
    for acc in accuracies:
        # 1. Best-of-N Simulation (Outcome-level ranking)
        bon_correct_trials = 0
        p_step_correct = 0.5
        p_full_correct = p_step_correct ** depth
        
        for _ in range(num_trials):
            # Model samples N solutions independently
            # Binomial test: did at least one candidate hit ground-truth?
            correct_count = sum(1 for _ in range(n_bon) if random.random() < p_full_correct)
            
            if correct_count > 0:
                # Verifier evaluates all N candidates
                # With probability 'acc', the verifier selects the correct candidate
                if random.random() < acc:
                    bon_correct_trials += 1
                    
        bon_success.append(bon_correct_trials / num_trials)
        
        # 2. Beam Search Simulation (Sequential Step Filtering)
        beam_correct_trials = 0
        for _ in range(num_trials):
            truth_in_beam = True
            
            for step in range(depth):
                if not truth_in_beam:
                    break
                
                # At each step, verifier filters intermediate candidates
                # The true path survives only if verifier does not make a false negative
                if random.random() >= acc:
                    truth_in_beam = False
                    
            if truth_in_beam:
                beam_correct_trials += 1
                
        beam_success.append(beam_correct_trials / num_trials)
        
    return accuracies, bon_success, beam_success

def print_table(accuracies, bon, beam):
    print("=" * 60)
    print(f"{'Verifier Accuracy':<20} | {'Best-of-N Win%':<18} | {'Beam Search Win%':<18}")
    print("=" * 60)
    for a, bo, be in zip(accuracies, bon, beam):
        print(f"{a*100:>17.0f}% | {bo*100:>15.1f}% | {be*100:>15.1f}%")
    print("=" * 60)

def generate_svg(accuracies, bon, beam, filename="experiments/search_collapse_curve.svg"):
    width, height = 700, 420
    padding = 60
    
    x_min, x_max = 60, 100
    y_min, y_max = 0, 100
    
    def to_svg_coords(x, y):
        sx = padding + (x - x_min) / (x_max - x_min) * (width - 2 * padding)
        sy = height - padding - (y - y_min) / (y_max - y_min) * (height - 2 * padding)
        return sx, sy

    svg = [
        f'<svg width="{width}" height="{height}" xmlns="http://www.w3.org/2000/svg" style="background:#fafafa; font-family:sans-serif;">',
        f'<text x="{width/2}" y="35" text-anchor="middle" font-size="16" font-weight="bold" fill="#111">The Search Collapse Vulnerability: Beam Search vs. Best-of-N</text>',
        f'<text x="{width/2}" y="52" text-anchor="middle" font-size="11" fill="#666">Sequential step pruning suffers exponential error decay when verifier accuracy drops</text>',
        
        # Grid lines and labels
        f'<line x1="{padding}" y1="{height-padding}" x2="{width-padding}" y2="{height-padding}" stroke="#ccc" stroke-width="1.5"/>',
        f'<line x1="{padding}" y1="{padding}" x2="{padding}" y2="{height-padding}" stroke="#ccc" stroke-width="1.5"/>'
    ]
    
    # Y axis labels (0% to 100%)
    for y_val in range(0, 101, 20):
        _, sy = to_svg_coords(x_min, y_val)
        svg.append(f'<line x1="{padding}" y1="{sy}" x2="{width-padding}" y2="{sy}" stroke="#eee" stroke-width="1"/>')
        svg.append(f'<text x="{padding-10}" y="{sy+4}" text-anchor="end" font-size="10" fill="#777">{y_val}%</text>')

    # X axis labels (60% to 100%)
    for x_val in range(60, 101, 10):
        sx, _ = to_svg_coords(x_val, y_min)
        svg.append(f'<line x1="{sx}" y1="{padding}" x2="{sx}" y2="{height-padding}" stroke="#eee" stroke-width="1"/>')
        svg.append(f'<text x="{sx}" y="{height-padding+18}" text-anchor="middle" font-size="10" fill="#777">{x_val}%</text>')
        
    svg.append(f'<text x="{width/2}" y="{height-15}" text-anchor="middle" font-size="12" fill="#333" font-weight="600">Verifier Accuracy (%)</text>')
    svg.append(f'<text x="20" y="{height/2}" text-anchor="middle" font-size="12" fill="#333" font-weight="600" transform="rotate(-90, 20, {height/2})">Solution Success Rate (%)</text>')

    # 80% mark indicator (typical real world PRM accuracy)
    sx_80, _ = to_svg_coords(80, 0)
    svg.append(f'<line x1="{sx_80}" y1="{padding}" x2="{sx_80}" y2="{height-padding}" stroke="#ffaa00" stroke-width="1.5" stroke-dasharray="4"/>')
    svg.append(f'<text x="{sx_80+5}" y="{padding+20}" font-size="10" fill="#b37400">Typical PRM (~80%)</text>')

    # Plot Beam Search line (red)
    beam_points = [to_svg_coords(a * 100, b * 100) for a, b in zip(accuracies, beam)]
    beam_d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in beam_points)
    svg.append(f'<path d="{beam_d}" fill="none" stroke="#e63946" stroke-width="3"/>')
    for x, y in beam_points:
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="4" fill="#e63946"/>')

    # Plot Best-of-N line (blue)
    bon_points = [to_svg_coords(a * 100, b * 100) for a, b in zip(accuracies, bon)]
    bon_d = "M " + " L ".join(f"{x:.1f},{y:.1f}" for x, y in bon_points)
    svg.append(f'<path d="{bon_d}" fill="none" stroke="#1d3557" stroke-width="3" stroke-dasharray="6,4"/>')
    for x, y in bon_points:
        svg.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.5" fill="#1d3557"/>')

    # Legend
    leg_x = padding + 20
    leg_y = padding + 25
    svg.append(f'<rect x="{leg_x}" y="{leg_y}" width="220" height="55" fill="white" stroke="#ddd" rx="4"/>')
    svg.append(f'<line x1="{leg_x+10}" y1="{leg_y+18}" x2="{leg_x+35}" y2="{leg_y+18}" stroke="#e63946" stroke-width="3"/>')
    svg.append(f'<text x="{leg_x+42}" y="{leg_y+22}" font-size="11" fill="#111" font-weight="600">Beam Search (Step-level PRM)</text>')
    svg.append(f'<line x1="{leg_x+10}" y1="{leg_y+38}" x2="{leg_x+35}" y2="{leg_y+38}" stroke="#1d3557" stroke-width="3" stroke-dasharray="6,4"/>')
    svg.append(f'<text x="{leg_x+42}" y="{leg_y+42}" font-size="11" fill="#111" font-weight="600">Best-of-N (Outcome Ranking)</text>')

    svg.append('</svg>')
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("\n".join(svg))
    print(f"SVG plot saved to: {filename}")

if __name__ == '__main__':
    accs, bon, beam = run_simulation()
    print_table(accs, bon, beam)
    generate_svg(accs, bon, beam)
