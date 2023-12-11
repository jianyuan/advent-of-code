use std::collections::HashMap;

fn main() {
    let input = include_str!("./input.txt");
    let output = solve(input);
    dbg!(output);
}

fn solve(input: &str) -> u32 {
    let map: HashMap<(i32, i32), char> = HashMap::from_iter(
        input
            .lines()
            .enumerate()
            .map(|(j, line)| {
                line.chars()
                    .enumerate()
                    .map(|(i, c)| ((i as i32, j as i32), c))
                    .collect::<Vec<_>>()
            })
            .flatten(),
    );

    let start = map.iter().find(|(_, &c)| c == 'S').unwrap().0.clone();
    let first_neighbour = vec![(-1, 0), (1, 0), (0, -1), (0, 1)]
        .iter()
        .map(|(dx, dy)| (start.0 as i32 + dx, start.1 as i32 + dy))
        .find(|&(x, y)| {
            map.get(&(x, y))
                .and_then(|&c| Some(c != '.'))
                .unwrap_or(false)
        })
        .unwrap();

    let mut ans = 1;
    let mut pair = (start, first_neighbour);
    loop {
        ans += 1;
        let (src, dest) = pair;
        let (dx, dy) = (dest.0 - src.0, dest.1 - src.1);
        let c = map.get(&dest).unwrap();
        let new_dest = match (c, dx, dy) {
            ('|', 0, 1) => (dest.0, dest.1 + 1),
            ('|', 0, -1) => (dest.0, dest.1 - 1),
            ('-', -1, 0) => (dest.0 - 1, dest.1),
            ('-', 1, 0) => (dest.0 + 1, dest.1),
            ('L', 0, 1) => (dest.0 + 1, dest.1),
            ('L', -1, 0) => (dest.0, dest.1 - 1),
            ('J', 1, 0) => (dest.0, dest.1 - 1),
            ('J', 0, 1) => (dest.0 - 1, dest.1),
            ('F', 0, -1) => (dest.0 + 1, dest.1),
            ('F', -1, 0) => (dest.0, dest.1 + 1),
            ('7', 1, 0) => (dest.0, dest.1 + 1),
            ('7', 0, -1) => (dest.0 - 1, dest.1),
            _ => unreachable!(),
        };
        if new_dest == start {
            break;
        }
        pair = (dest, new_dest);
    }

    ans / 2
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let result = solve(
            "\
.....
.S-7.
.|.|.
.L-J.
.....",
        );
        assert_eq!(result, 4);

        let result = solve(
            "\
..F7.
.FJ|.
SJ.L7
|F--J
LJ...",
        );
        assert_eq!(result, 8);
    }
}
