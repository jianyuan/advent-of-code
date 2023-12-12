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

            // Brute force all possible records
            let mut possible_records: Vec<Vec<char>> = Vec::new();
            possible_records.push(vec![]);

            for i in 0..records.len() {
                let mut next_records: Vec<Vec<char>> = Vec::new();
                match records[i] {
                    '?' => {
                        next_records.extend(
                            possible_records
                                .iter()
                                .map(|r| r.iter().cloned().chain(vec!['.']).collect())
                                .collect::<Vec<_>>(),
                        );
                        next_records.extend(
                            possible_records
                                .iter()
                                .map(|r| r.iter().cloned().chain(vec!['#']).collect())
                                .collect::<Vec<_>>(),
                        );
                    }
                    _ => {
                        next_records.extend(
                            possible_records
                                .iter()
                                .map(|r| r.iter().cloned().chain(vec![records[i]]).collect())
                                .collect::<Vec<_>>(),
                        );
                    }
                }

                possible_records = next_records;
            }

            possible_records
                .iter()
                .filter(|record| {
                    let mut damaged = damaged.clone().into_iter().rev().collect::<Vec<_>>();
                    let mut current = 0;

                    for i in 0..record.len() {
                        let last = if i > 0 { Some(record[i - 1]) } else { None };
                        match (last, record[i]) {
                            (Some('#'), '.') => {
                                if current > 0 {
                                    return false;
                                }
                            }
                            (Some('#'), '#') => {
                                if current == 0 {
                                    return false;
                                }
                                current -= 1;
                            }
                            (None | Some('.'), '#') => {
                                if current > 0 || damaged.is_empty() {
                                    return false;
                                }
                                current = damaged.pop().unwrap() - 1;
                            }
                            (None | Some('.'), '.') => {}
                            _ => unimplemented!("{:?} {} {:?}", last, record[i], damaged),
                        }
                    }

                    current == 0 && damaged.is_empty()
                })
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
        assert_eq!(result, 21);
    }
}
