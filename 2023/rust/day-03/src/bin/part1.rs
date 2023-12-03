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

fn is_symbol(c: char) -> bool {
    !c.is_numeric() && c != '.'
}

fn solve(input: &str) -> u32 {
    let grid = input
        .lines()
        .map(|line| line.chars().collect::<Vec<_>>())
        .collect::<Vec<_>>();

    let mut sum = 0;

    for (y, line) in grid.iter().enumerate() {
        let mut last = vec![];
        let mut is_part = false;

        for (x, c) in line.iter().enumerate() {
            if c.is_numeric() {
                is_part |= DIRECTIONS
                    .iter()
                    .filter_map(|(dx, dy)| {
                        let nx = x as isize + dx;
                        let ny = y as isize + dy;
                        if nx < 0 || ny < 0 {
                            None
                        } else {
                            Some((nx as usize, ny as usize))
                        }
                    })
                    .filter_map(|(nx, ny)| grid.get(ny).and_then(|line| line.get(nx)))
                    .any(|c| is_symbol(*c));

                last.push(*c);
            } else {
                if is_part && last.len() > 0 {
                    sum += last.iter().collect::<String>().parse::<u32>().unwrap();
                }

                last.clear();
                is_part = false;
            }
        }

        if is_part && last.len() > 0 {
            sum += last
                .iter()
                .collect::<String>()
                .parse::<u32>()
                .unwrap_or_default();
        }
    }

    sum
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
        assert_eq!(result, 4361);
    }
}
