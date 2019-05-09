use std::collections::HashSet;
use std::io::{self, Read};

type Result<T> = std::result::Result<T, Box<std::error::Error>>;

fn main() -> Result<()> {
    let mut raw_input = String::new();
    io::stdin().read_to_string(&mut raw_input)?;

    let input: Vec<i32> = raw_input
        .lines()
        .map(|line| line.parse().unwrap())
        .collect();

    println!("Part 1: {}", part1(&input)?);
    println!("Part 2: {}", part2(&input)?);

    Ok(())
}

fn part1(input: &Vec<i32>) -> Result<i32> {
    Ok(input.iter().sum())
}

fn part2(input: &Vec<i32>) -> Result<i32> {
    let mut freq = 0;
    let mut seen = HashSet::new();
    seen.insert(0);

    loop {
        for change in input {
            freq += change;
            if seen.contains(&freq) {
                return Ok(freq);
            }
            seen.insert(freq);
        }
    }
}
