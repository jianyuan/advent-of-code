fn main() {
    let input = include_str!("./input.txt");
    let output = solve(input);
    dbg!(output);
}

#[derive(Debug)]
struct Round {
    time: u32,
    distance: u32,
}

fn solve(input: &str) -> u32 {
    let mut numbers = input.lines().map(|line| {
        line.split_once(':')
            .unwrap()
            .1
            .split_whitespace()
            .map(|s| s.parse::<u32>().unwrap())
    });
    let times = numbers.next().unwrap();
    let distances = numbers.next().unwrap();
    let rounds = times
        .zip(distances)
        .map(|(time, distance)| Round { time, distance })
        .collect::<Vec<_>>();
    rounds
        .iter()
        .map(|r| {
            (0..=r.time)
                .map(|t| (r.time - t) * t)
                .filter(|&d| d > r.distance)
                .count() as u32
        })
        .product::<u32>()
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
        assert_eq!(result, 288);
    }
}
