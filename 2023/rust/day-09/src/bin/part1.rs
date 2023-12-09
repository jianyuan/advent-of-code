fn main() {
    let input = include_str!("./input.txt");
    let output = solve(input);
    dbg!(output);
}

fn solve(input: &str) -> i32 {
    let history = input
        .lines()
        .map(|line| {
            line.split_whitespace()
                .map(|n| n.parse::<i32>().unwrap())
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();

    let next_values = history
        .iter()
        .map(|numbers| {
            let mut stack = vec![numbers.clone()];
            while stack
                .last()
                .map_or(false, |last| last.iter().sum::<i32>() != 0)
            {
                let current = stack
                    .last()
                    .unwrap()
                    .windows(2)
                    .map(|x| x[1] - x[0])
                    .collect::<Vec<_>>();
                stack.push(current);
            }

            stack.iter().rev().fold(0, |acc, x| acc + x.last().unwrap())
        })
        .collect::<Vec<_>>();

    next_values.iter().sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let result = solve(
            "\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45",
        );
        assert_eq!(result, 114);
    }
}
