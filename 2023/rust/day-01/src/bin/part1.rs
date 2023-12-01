fn main() {
    let input = include_str!("./input1.txt");
    let output = part1(input);
    dbg!(output);
}

fn part1(input: &str) -> String {
    input
        .lines()
        .map(|line| {
            let mut nums = line.chars().filter_map(|c| c.to_digit(10));
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
    fn test_part1() {
        let result = part1(
            "1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet",
        );
        assert_eq!(result, "142");
    }
}
