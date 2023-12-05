fn main() {
    let input = include_str!("./input.txt");
    let output = solve(input);
    dbg!(output);
}

#[derive(Debug)]
struct Mapping {
    destination: u64,
    source: u64,
    length: u64,
}

fn solve(input: &str) -> u64 {
    let (seeds, input) = input.split_once("\n\n").unwrap();
    let seeds = seeds
        .split_once(": ")
        .unwrap()
        .1
        .split_whitespace()
        .map(|s| s.parse::<u64>().unwrap())
        .collect::<Vec<_>>();

    let mappings = input
        .split("\n\n")
        .map(|s| {
            s.split("\n")
                .skip(1)
                .map(|s| s.split_whitespace().map(|s| s.parse::<u64>().unwrap()))
                .map(|mut d| Mapping {
                    destination: d.next().unwrap(),
                    source: d.next().unwrap(),
                    length: d.next().unwrap(),
                })
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();

    seeds
        .iter()
        .map(|&seed| {
            let mut new_seed = seed;
            for mapping in &mappings {
                for &Mapping {
                    source,
                    destination,
                    length,
                } in mapping
                {
                    let range = source..=source + length;
                    if range.contains(&new_seed) {
                        new_seed = destination + (new_seed - source);
                        break;
                    }
                }
            }

            new_seed
        })
        .min()
        .unwrap()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let result = solve(
            "\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4",
        );
        assert_eq!(result, 35);
    }
}
