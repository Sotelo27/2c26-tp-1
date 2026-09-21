import os
import sys

from loaders import load_cadvisor_dataframe, load_meta
from styles import apply_latex_style
from panels.resources import generate_resources_plot

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, 'data')
FIGURES_DIR = os.path.join(BASE_DIR, 'figures')

# python3 -m venv venv
# source .venv/bin/activate
# python3 main.py rates_0000000000
def main():
    if len(sys.argv) != 2:
        print(f'uso: {sys.argv[0]} <directorio-en-data>', file=sys.stderr)
        return 1
    scenario = os.path.basename(sys.argv[1].rstrip('/'))

    meta = load_meta(os.path.join(DATA_DIR, scenario, 'meta.json'))
    cadvisor_dataframe = load_cadvisor_dataframe(os.path.join(DATA_DIR, scenario, 'cadvisor.json'))
    #artillery_dataframe = load_artillery_dataframe(os.path.join(DATA_DIR, scenario, 'artillery.json'))
    #currency_dataframe = load_currency_dataframe(os.path.join(DATA_DIR, scenario, 'currency.json'))

    output_path = os.path.join(FIGURES_DIR, scenario)
    os.makedirs(output_path, exist_ok=True)
    apply_latex_style()
    generate_resources_plot(cadvisor_dataframe, meta['start'], output_path)
    return 0

if __name__ == "__main__":
    sys.exit(main())
