use std::collections::{HashMap, HashSet};

fn main() {
    let input = include_str!("./input.txt");
    let output = solve(input);
    dbg!(output);
}

#[derive(Clone, Debug, Default)]
struct Card {
    id: u32,
    winning_numbers: HashSet<u32>,
    my_numbers: HashSet<u32>,
}

fn solve(input: &str) -> u32 {
    let cards = input
        .lines()
        .map(|line| {
            let (id, numbers) = line.split_once(": ").unwrap();
            let id = id
                .split_whitespace()
                .skip(1)
                .next()
                .unwrap()
                .parse::<u32>()
                .unwrap();

            let mut numbers = numbers.split(" | ").map(|n| {
                n.split_whitespace()
                    .map(|n| n.parse::<u32>().unwrap())
                    .collect::<HashSet<_>>()
            });
            let winning_numbers = numbers.next().unwrap();
            let my_numbers = numbers.next().unwrap();

            Card {
                id,
                winning_numbers,
                my_numbers,
            }
        })
        .collect::<Vec<_>>();

    let mut counter = HashMap::new();
    for card in cards {
        let entry = counter.entry(card.id).or_default();
        *entry += 1;
        let count = *entry;

        let matches = card.winning_numbers.intersection(&card.my_numbers).count() as u32;
        let new_ids = (card.id + 1)..=(card.id + matches);

        for id in new_ids {
            let entry = counter.entry(id).or_default();
            *entry += count;
        }
    }

    counter.values().sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let result = solve(
            "\
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11",
        );
        assert_eq!(result, 30);
    }
}
