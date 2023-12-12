use std::collections::{HashMap, HashSet};

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

    let mut points = HashSet::new();
    points.insert(start);
    let mut pair = (start, first_neighbour);
    loop {
        let (src, dest) = pair;
        points.insert(dest);
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

    input
        .lines()
        .enumerate()
        .map(|(y, line)| {
            let mut ans = 0;
            let mut last = None;
            let mut inside = false;
            for (x, c) in line.chars().enumerate() {
                if points.contains(&(x as i32, y as i32)) {
                    if match (last, c) {
                        (_, '-') | (Some('L'), '7') | (Some('F'), 'J') => false,
                        (_, _) => true,
                    } {
                        last = Some(c);
                        inside = !inside;
                    }
                } else {
                    if inside {
                        ans += 1;
                    }
                }
            }

            ans
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
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........",
        );
        assert_eq!(result, 4);

        let result = solve(
            "\
..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........",
        );
        assert_eq!(result, 4);

        let result = solve(
            "\
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...",
        );
        assert_eq!(result, 8);
    }
}
