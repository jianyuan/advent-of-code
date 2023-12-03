fn main() {
    let input = include_str!("./input.txt");
    let output = solve(input);
    dbg!(output);
}

const WORDS: [&str; 9] = [
    "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
];

fn solve(input: &str) -> u32 {
    input
        .lines()
        .map(|line| {
            let mut nums = line.chars().enumerate().filter_map(|(i, c)| {
                if c.is_numeric() {
                    c.to_digit(10)
                } else {
                    WORDS
                        .iter()
                        .enumerate()
                        .find_map(|(n, word)| line[i..].starts_with(word).then_some(n as u32 + 1))
                }
            });

            let first = nums.next().unwrap();
            let last = nums.last().unwrap_or(first);

            first * 10 + last
        })
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let result = solve(
            "two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen",
        );
        assert_eq!(result, 281);
    }
}
