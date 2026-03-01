import json
import csv
import sys

class Block:
    def __init__(self, block_id, view):
        self.id = block_id
        self.view = view

class Vote:
    def __init__(self, block_id):
        self.block_id = block_id

class ChainBuilder:
    def __init__(self):
        self.chain = []
        self.votes = []
        self.waiting = []
    
    def add_vote(self, vote):
        self.votes.append(vote.block_id)
        self._check_waiting()
    
    def add_block(self, block):
        if block.id in self.votes:
            if block.view == 0 and len(self.chain) == 0:
                self.chain.append(block)
                self._check_waiting()
                return
            elif len(self.chain) == block.view and self.chain[-1].view == block.view - 1:
                self.chain.append(block)
                self._check_waiting()
                return
        
        self.waiting.append(block)
    
    def _check_waiting(self):
        i = 0
        while i < len(self.waiting):
            block = self.waiting[i]
            if block.id in self.votes:
                if block.view == 0 and len(self.chain) == 0:
                    self.chain.append(block)
                    self.waiting.pop(i)
                elif len(self.chain) == block.view and self.chain[-1].view == block.view - 1:
                    self.chain.append(block)
                    self.waiting.pop(i)
                else:
                    i += 1
            else:
                i += 1
    
    def run(self, inputs):
        for item in inputs:
            if 'view' in item:
                self.add_block(Block(item['id'], item['view']))
            else:
                self.add_vote(Vote(item['block_id']))
        return self.chain

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
            writer.writerow([i, block.id, block.view])

def main():
    if len(sys.argv) < 2:
        print("Usage:")
        print("  IO0 mode: python lab2_class.py --cmd block:0x54b:0 vote:0x54b")
        print("  IO1 mode: python lab2_class.py --csv input.csv")
        sys.exit(1)

    mode = sys.argv[1]
    
    if mode == "--cmd":
        if len(sys.argv) < 3:
            print("Error: missing arguments after --cmd")
            sys.exit(1)
        inputs = parse_cmd_args(sys.argv[2:])
        builder = ChainBuilder()
        chain = builder.run(inputs)
        print("Final chain:")
        for block in chain:
            print(f"id={block.id}, view={block.view}")
        
    elif mode == "--csv":
        if len(sys.argv) < 3:
            print("Error: missing CSV filename")
            sys.exit(1)
        inputs = parse_csv_file(sys.argv[2])
        builder = ChainBuilder()
        chain = builder.run(inputs)
        output_file = 'output.csv'
        save_chain_to_csv(chain, output_file)
        print(f"Chain saved to {output_file}")
        
    else:
        print("Unknown mode. Use --cmd or --csv.")
        sys.exit(1)

if __name__ == "__main__":
    main()
