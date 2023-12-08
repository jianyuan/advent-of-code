use std::collections::HashMap;

fn main() {
    let input = include_str!("./input.txt");
    let output = solve(input);
    dbg!(output);
}

#[derive(Debug)]
enum Direction {
    Left,
    Right,
}

#[derive(Debug)]
struct Path<'a> {
    left: &'a str,
    right: &'a str,
}

fn solve<'a>(input: &'a str) -> u32 {
    let (instructions, input) = input.split_once("\n\n").unwrap();
    let instructions = instructions
        .chars()
        .map(|c| match c {
            'L' => Direction::Left,
            'R' => Direction::Right,
            _ => unreachable!(),
        })
        .collect::<Vec<_>>();

    let map = input
        .lines()
        .map(|line| {
            let (from, paths) = line.split_once(" = ").unwrap();
            let (left, right) = paths[1..paths.len() - 1].split_once(", ").unwrap();
            let path = Path { left, right };
            (from, path)
        })
        .collect::<HashMap<_, _>>();

    let mut steps = 0u32;
    let mut current = "AAA";
    loop {
        for instruction in &instructions {
            let path = &map[current];
            current = match instruction {
                Direction::Left => path.left,
                Direction::Right => path.right,
            };
            steps += 1;
            if current == "ZZZ" {
                return steps;
            }
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let result = solve(
            "\
RL

AAA = (BBB, CCC)
BBB = (DDD, EEE)
CCC = (ZZZ, GGG)
DDD = (DDD, DDD)
EEE = (EEE, EEE)
GGG = (GGG, GGG)
ZZZ = (ZZZ, ZZZ)",
        );
        assert_eq!(result, 2);

        let result = solve(
            "\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)",
        );
        assert_eq!(result, 6);
    }
}
