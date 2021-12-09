mod utils;

enum Instruction {
    Forward(u32),
    Up(u32),
    Down(u32),
}

struct Position {
    depth: u32,
    horizontal: u32,
    aim: u32,
}

impl Position {
    fn new() -> Position {
        Position {
            depth: 0,
            horizontal: 0,
            aim: 0,
        }
    }
}

fn get_instructions() -> Vec<Instruction> {
    utils::load("data/day02.txt")
        .lines()
        .map(|x| {
            let (instruction, raw_value) = x.split_once(" ").unwrap();
            let value = raw_value.parse().unwrap();
            match instruction {
                "forward" => Instruction::Forward(value),
                "up" => Instruction::Up(value),
                "down" => Instruction::Down(value),
                _ => panic!("invalid instruction"),
            }
        })
        .collect()
}

fn part1(instructions: &Vec<Instruction>) -> u32 {
    let mut position = Position::new();
    for instruction in instructions {
        match instruction {
            Instruction::Forward(value) => position.horizontal += value,
            Instruction::Up(value) => position.depth -= value,
            Instruction::Down(value) => position.depth += value,
        }
    }
    position.horizontal * position.depth
}

fn part2(instructions: &Vec<Instruction>) -> u32 {
    let mut position = Position::new();
    for instruction in instructions {
        match instruction {
            Instruction::Forward(value) => {
                position.horizontal += value;
                position.depth += position.aim * value;
            }
            Instruction::Up(value) => position.aim -= value,
            Instruction::Down(value) => position.aim += value,
        }
    }
    position.horizontal * position.depth
}

fn main() {
    let instructions = get_instructions();

    println!("Part 1: {}", part1(&instructions));
    println!("Part 2: {}", part2(&instructions));
}
