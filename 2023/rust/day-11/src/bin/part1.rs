fn main() {
    let input = include_str!("./input.txt");
    let output = solve(input);
    dbg!(output);
}

fn solve(input: &str) -> u32 {
    let map = input
        .lines()
        .map(|line| line.chars().collect::<Vec<_>>())
        .collect::<Vec<_>>();

    let mut expand_cols = Vec::new();
    let mut expand_rows = Vec::new();
    let mut galaxies = Vec::new();

    for (col, line) in map.iter().enumerate() {
        for (row, c) in line.iter().enumerate() {
            if *c == '#' {
                galaxies.push((row as u32, col as u32));
            }
        }
    }

    for (col, line) in map.iter().enumerate() {
        if line.iter().all(|c| *c == '.') {
            expand_rows.push(col as u32);
        }
    }

    for row in 0..map[0].len() {
        if map.iter().all(|line| line[row] == '.') {
            expand_cols.push(row as u32);
        }
    }

    let galaxies = galaxies
        .iter()
        .map(|&(x, y)| {
            let row_delta = expand_cols.iter().filter(|&&a| a < x).count() as u32;
            let col_delta = expand_rows.iter().filter(|&&b| b < y).count() as u32;
            (x + row_delta, y + col_delta)
        })
        .collect::<Vec<_>>();

    let mut pairs: Vec<((u32, u32), (u32, u32))> = Vec::new();
    for i in 0..galaxies.len() {
        for j in i + 1..galaxies.len() {
            pairs.push((galaxies[i], galaxies[j]));
        }
    }

    pairs
        .iter()
        .map(|(a, b)| {
            let row_delta = a.0.abs_diff(b.0);
            let col_delta = a.1.abs_diff(b.1);
            row_delta + col_delta
        })
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let result = solve(
            "\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....",
        );
        assert_eq!(result, 374);
    }
}
