use std::iter::once;

fn main() {
    let input = include_str!("./input.txt");
    let output = solve(input);
    dbg!(output);
}

fn solve(input: &str) -> u32 {
    input
        .lines()
        .map(|line| {
            let (records, damaged) = line.split_once(' ').unwrap();
            let records = records.chars().collect::<Vec<_>>();
            let damaged = damaged
                .split(',')
                .map(|s| s.parse::<u32>().unwrap())
                .collect::<Vec<_>>();

            let mut possible_records: Vec<(Vec<char>, Vec<u32>)> = Vec::new();
            possible_records.push((vec![], damaged.iter().rev().cloned().collect()));

            for i in 0..records.len() {
                let mut next_records: Vec<(Vec<char>, Vec<u32>)> = Vec::new();

                for (record, damaged) in possible_records.iter() {
                    match (&records[i], record.last(), damaged.last()) {
                        ('?', None | Some('.'), Some(d)) if *d > 0 => {
                            next_records.push((
                                record.iter().cloned().chain(once('#')).collect(),
                                damaged
                                    .iter()
                                    .take(damaged.len() - 1)
                                    .cloned()
                                    .chain(once(d - 1))
                                    .collect(),
                            ));
                            next_records.push((
                                record.iter().cloned().chain(once('.')).collect(),
                                damaged.clone(),
                            ));
                        }
                        ('?', Some('#'), Some(d)) if *d > 0 => {
                            next_records.push((
                                record.iter().cloned().chain(once('#')).collect(),
                                damaged
                                    .iter()
                                    .take(damaged.len() - 1)
                                    .cloned()
                                    .chain(once(d - 1))
                                    .collect(),
                            ));
                        }
                        ('?', Some('#'), Some(0)) => {
                            next_records.push((
                                record.iter().cloned().chain(once('.')).collect(),
                                damaged.iter().take(damaged.len() - 1).cloned().collect(),
                            ));
                        }
                        ('.', Some('#'), Some(d)) if *d > 0 => {
                            // Invalid
                        }
                        ('.', Some('#'), Some(0)) => {
                            next_records.push((
                                record.iter().cloned().chain(once('.')).collect(),
                                damaged.iter().take(damaged.len() - 1).cloned().collect(),
                            ));
                        }
                        ('.', None | Some('.'), Some(d)) if *d > 0 => {
                            next_records.push((
                                record.iter().cloned().chain(once('.')).collect(),
                                damaged.clone(),
                            ));
                        }
                        ('.' | '?', Some('.'), None) => {
                            next_records.push((
                                record.iter().cloned().chain(once('.')).collect(),
                                damaged.clone(),
                            ));
                        }
                        ('#', None | Some('#' | '.'), Some(d)) if *d > 0 => {
                            next_records.push((
                                record.iter().cloned().chain(once('#')).collect(),
                                damaged
                                    .iter()
                                    .take(damaged.len() - 1)
                                    .cloned()
                                    .chain(once(d - 1))
                                    .collect(),
                            ));
                        }
                        ('#', Some('#' | '.'), None | Some(0)) => {
                            // Invalid
                        }
                        _ => unreachable!(),
                    }
                }

                possible_records = next_records;
            }

            possible_records
                .iter()
                .filter(|(_, damaged)| damaged.is_empty() || damaged.get(0) == Some(&0))
                .count() as u32
        })
        .sum::<u32>()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let result = solve(
            "\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1",
        );
        assert_eq!(result, 525152);
    }
}
