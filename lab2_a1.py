import json
import csv
import sys

def create_block(block_id, view):
    return {'id': block_id, 'view': view}

def create_vote(block_id):
    return {'block_id': block_id}

def can_add_block(block, chain, votes):
    if block['id'] not in votes:
        return False
    if block['view'] == 0:
        return len(chain) == 0
    return len(chain) == block['view'] and chain[-1]['view'] == block['view'] - 1

def check_waiting(chain, votes, waiting):
    i = 0
    while i < len(waiting):
        block = waiting[i]
        if can_add_block(block, chain, votes):
            chain.append(block)
            waiting.pop(i)
        else:
            i += 1
    return chain, waiting

def process_item(chain, votes, waiting, item):
    if 'view' in item:
        if can_add_block(item, chain, votes):
            chain.append(item)
            chain, waiting = check_waiting(chain, votes, waiting)
        else:
            waiting.append(item)
    else:
        votes.append(item['block_id'])
        chain, waiting = check_waiting(chain, votes, waiting)
    return chain, votes, waiting

def build_chain(items):
    chain = []
    votes = []
    waiting = []
    for item in items:
        chain, votes, waiting = process_item(chain, votes, waiting, item)
    return chain

def parse_cmd_args(args):
    inputs = []
    for arg in args:
        parts = arg.split(':')
        if parts[0] == 'block':
            inputs.append({'id': parts[1], 'view': int(parts[2])})
        elif parts[0] == 'vote':
            inputs.append({'block_id': parts[1]})
    return inputs

def parse_csv_file(filename):
    inputs = []
    with open(filename, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    for line in lines[1:]:
        line = line.strip()
        if not line:
            continue
        parts = line.split(',')
        if parts[0] == 'block':
            inputs.append({'id': parts[1], 'view': int(parts[2])})
        elif parts[0] == 'vote':
            inputs.append({'block_id': parts[3]})
    return inputs

def save_chain_to_csv(chain, filename):
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['position', 'id', 'view'])
        for i, block in enumerate(chain):
            writer.writerow([i, block['id'], block['view']])

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  IO0 mode: python lab2_func.py --cmd block:0x54b:0 vote:0x54b")
        print("  IO1 mode: python lab2_func.py --csv input.csv")
        sys.exit(1)

    mode = sys.argv[1]
    
    if mode == "--cmd":
        if len(sys.argv) < 3:
            print("Error: missing arguments after --cmd")
            sys.exit(1)
        inputs = parse_cmd_args(sys.argv[2:])
        chain = build_chain(inputs)
        print("Final chain:")
        for block in chain:
            print(f"id={block['id']}, view={block['view']}")
        
    elif mode == "--csv":
        if len(sys.argv) < 3:
            print("Error: missing CSV filename")
            sys.exit(1)
        inputs = parse_csv_file(sys.argv[2])
        chain = build_chain(inputs)
        output_file = 'output.csv'
        save_chain_to_csv(chain, output_file)
        print(f"Chain saved to {output_file}")
        
    else:
        print("Unknown mode. Use --cmd or --csv.")
        sys.exit(1)

if __name__ == "__main__":
    main()
