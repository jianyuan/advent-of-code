fn main() {
    let input = include_str!("./input.txt");
    let output = solve(input);
    dbg!(output);
}

#[derive(Debug)]
struct Mapping {
    src: std::ops::RangeInclusive<i64>,
    dest: std::ops::RangeInclusive<i64>,
    len: i64,
}

fn solve(input: &str) -> i64 {
    let (seeds, input) = input.split_once("\n\n").unwrap();
    let seeds = seeds
        .split_once(": ")
        .unwrap()
        .1
        .split_whitespace()
        .map(|s| s.parse::<i64>().unwrap())
        .collect::<Vec<_>>();

    let mappings = input
        .split("\n\n")
        .map(|s| {
            s.split("\n")
                .skip(1)
                .map(|s| s.split_whitespace().map(|s| s.parse::<i64>().unwrap()))
                .map(|mut d| {
                    let dest_start = d.next().unwrap();
                    let src_start = d.next().unwrap();
                    let len: i64 = d.next().unwrap();
                    Mapping {
                        src: src_start..=src_start + len,
                        dest: dest_start..=dest_start + len,
                        len,
                    }
                })
                .collect::<Vec<_>>()
        })
        .collect::<Vec<_>>();

    let seed_ranges = seeds
        .chunks(2)
        .map(|d| vec![d[0]..=d[0] + d[1] - 1])
        .collect::<Vec<_>>();

    let ranges = seed_ranges
        .iter()
        .map(|ranges| {
            let mut final_ranges = ranges.clone();
            for mapping in &mappings {
                let mut new_ranges = Vec::new();
                let mut current_ranges = final_ranges.clone();
                for m in mapping {
                    let mut old_ranges = Vec::new();
                    for range in &current_ranges {
                        dbg!(&range, m);

                        if (range.start() > m.src.start() && range.start() > m.src.end())
                            || (range.start() < m.src.start() && range.end() < m.src.start())
                        {
                            dbg!("case 1");
                            old_ranges.push(range.clone());
                        } else if range.start() >= m.src.start() && range.end() <= m.src.end() {
                            dbg!("case 2");
                            new_ranges.push(
                                (*range.start() - m.src.start() + m.dest.start())
                                    ..=(*range.end() + m.dest.start() - m.src.start()),
                            )
                        } else if range.start() <= m.src.start() && range.end() <= m.src.end() {
                            dbg!("case 3");
                            old_ranges.push(*range.start()..=(*m.src.start() - 1));
                            new_ranges.push(
                                *m.dest.start()..=(*range.end() - *m.src.start() + *m.dest.start()),
                            );
                        } else if range.start() >= m.src.start() && range.end() >= m.src.end() {
                            dbg!("case 4");
                            old_ranges.push(*m.src.end()..=*range.end());
                            new_ranges.push(
                                *range.start() - *m.src.start() + *m.dest.start()..=*m.dest.end(),
                            );
                        } else if range.start() <= m.src.start() && range.end() >= m.src.end() {
                            dbg!("case 5");
                            old_ranges.push(*range.start()..=*m.src.start() - 1);
                            old_ranges.push(*m.src.end() + 1..=*range.end());
                            new_ranges.push(m.dest.clone());
                        } else {
                            unreachable!();
                        }
                        dbg!(&new_ranges);
                        dbg!(&old_ranges);
                    }
                    current_ranges = old_ranges;
                }

                new_ranges.extend(current_ranges);
                final_ranges = new_ranges;
            }
            final_ranges
        })
        .collect::<Vec<_>>();

    ranges.iter().flatten().map(|r| *r.start()).min().unwrap()
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
        assert_eq!(result, 46);
    }
}
