fn main() {
    let input = include_str!("./input.txt");
    let output = solve(input);
    dbg!(output);
}

#[derive(Debug)]
struct Round {
    time: u64,
    distance: u64,
}

fn solve(input: &str) -> u64 {
    let mut numbers = input.lines().map(|line| {
        line.split_once(':')
            .unwrap()
            .1
            .split_whitespace()
            .collect::<String>()
            .parse::<u64>()
            .unwrap()
    });
    let round = Round {
        time: numbers.next().unwrap(),
        distance: numbers.next().unwrap(),
    };
    (0..round.time)
        .map(|t| (round.time - t) * t)
        .filter(|&d| d > round.distance)
        .count() as u64
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let result = solve(
            "\
Time:      7  15   30
Distance:  9  40  200",
        );
        assert_eq!(result, 71503);
    }
}
