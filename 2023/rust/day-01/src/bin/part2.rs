fn main() {
    let input = include_str!("./input1.txt");
    let output = part2(input);
    dbg!(output);
}

fn part2(input: &str) -> String {
    let words = [
        "one", "two", "three", "four", "five", "six", "seven", "eight", "nine",
    ]
    .map(|word| word.chars().collect::<Vec<_>>());

    input
        .lines()
        .map(|line| {
            let line = line.chars().collect::<Vec<_>>();
            let mut nums = (0..line.len()).filter_map(|i| {
                if line[i].is_numeric() {
                    line[i].to_digit(10)
                } else {
                    words
                        .iter()
                        .enumerate()
                        .find_map(|(n, word)| line[i..].starts_with(word).then_some(n as u32 + 1))
                }
            });

            let first = nums.next().unwrap();
            let last = nums.last().unwrap_or(first);

            first * 10 + last
        })
        .sum::<u32>()
        .to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part2() {
        let result = part2(
            "two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen",
        );
        assert_eq!(result, "281");
    }
}
