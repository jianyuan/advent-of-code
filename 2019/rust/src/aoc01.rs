use std::io::{self, Read};
use std::iter;

fn main() -> io::Result<()> {
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

fn part1(input: &Vec<i32>) -> io::Result<i32> {
    Ok(input.iter().map(|&w| calculate_fuel(w)).sum())
}

fn part2(input: &Vec<i32>) -> io::Result<i32> {
    Ok(input
        .iter()
        .map(|&w| calculate_fuel(w))
        .flat_map(|w| {
            iter::successors(Some(w), |&w| {
                if w == 0 {
                    None
                } else {
                    Some(calculate_fuel(w))
                }
            })
        })
        .sum())
}

fn calculate_fuel(mass: i32) -> i32 {
    ((mass / 3) - 2).max(0)
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn fuel_calculated_correctly() {
        assert_eq!(calculate_fuel(12), 2);
        assert_eq!(calculate_fuel(14), 2);
        assert_eq!(calculate_fuel(1969), 654);
        assert_eq!(calculate_fuel(100756), 33583);
    }
}
