use std::collections::HashMap;

fn main() {
    let input = include_str!("./input.txt");
    let output = solve(input);
    dbg!(output);
}

const DIRECTIONS: [(isize, isize); 8] = [
    (-1, -1), // top left
    (0, -1),  // top
    (1, -1),  // top right
    (-1, 0),  // left
    (1, 0),   // right
    (-1, 1),  // bottom left
    (0, 1),   // bottom
    (1, 1),   // bottom right
];

fn solve(input: &str) -> u32 {
    let grid = input
        .lines()
        .map(|line| line.chars().collect::<Vec<_>>())
        .collect::<Vec<_>>();

    let mut gear_ratios = HashMap::new();

    for (y, line) in grid.iter().enumerate() {
        let mut start = None;
        for end in 0..line.len() + 1 {
            if line.get(end).map(|c| c.is_numeric()).unwrap_or_default() {
                if start.is_none() {
                    start = Some(end);
                }
            } else {
                if let Some(start) = start {
                    let value = line[start..end]
                        .iter()
                        .collect::<String>()
                        .parse::<u32>()
                        .unwrap();

                    let mut seen = Vec::new();
                    for x in start..end {
                        for (dx, dy) in DIRECTIONS.iter() {
                            let nx = x as isize + dx;
                            let ny = y as isize + dy;
                            if nx < 0 || ny < 0 {
                                continue;
                            }

                            if let Some(c) =
                                grid.get(ny as usize).and_then(|line| line.get(nx as usize))
                            {
                                if *c == '*' && !seen.contains(&(nx, ny)) {
                                    let ratio = gear_ratios.entry((nx, ny)).or_insert(Vec::new());
                                    ratio.push(value);
                                    seen.push((nx, ny));
                                }
                            }
                        }
                    }
                }
                start = None;
            }
        }
    }

    gear_ratios
        .iter()
        .filter(|(_, v)| v.len() == 2)
        .map(|(_, v)| v[0] * v[1])
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let result = solve(
            "\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..",
        );
        assert_eq!(result, 467835);
    }
}
