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

fn gcd(a: u64, b: u64) -> u64 {
    if b == 0 {
        return a;
    }
    gcd(b, a % b)
}

fn lcm(nums: &[u64]) -> u64 {
    if nums.len() == 1 {
        return nums[0];
    }
    let a = nums[0];
    let b = lcm(&nums[1..]);
    a * b / gcd(a, b)
}

fn solve<'a>(input: &'a str) -> u64 {
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

    let starts = map
        .keys()
        .filter_map(|k| if k.ends_with('A') { Some(k) } else { None })
        .cloned()
        .collect::<Vec<_>>();
    let mut all_steps = Vec::new();

    for start in starts {
        let mut steps = 0u64;
        let mut current = start;
        'done: loop {
            for instruction in &instructions {
                let path = &map[current];
                current = match instruction {
                    Direction::Left => path.left,
                    Direction::Right => path.right,
                };
                steps += 1;
                if current.ends_with('Z') {
                    break 'done;
                }
            }
        }
        all_steps.push(steps);
    }

    lcm(&all_steps)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let result = solve(
            "\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)",
        );
        assert_eq!(result, 6);
    }
}
