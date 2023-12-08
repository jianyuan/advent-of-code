use std::collections::HashMap;

fn main() {
    let input = include_str!("./input.txt");
    let output = solve(input);
    dbg!(output);
}

#[derive(Debug)]
struct Hand {
    cards: Vec<char>,
    strengths: Vec<u32>,
    rank: u32,
    bid: u32,
}

impl Hand {
    fn new(cards: Vec<char>, bid: u32, strength: &str) -> Self {
        let strengths = cards
            .iter()
            .map(|card| strength.find(*card).unwrap() as u32)
            .collect();

        let mut counts = cards
            .iter()
            .fold(HashMap::new(), |mut acc, card| {
                *acc.entry(card).or_insert(0) += 1;
                acc
            })
            .into_values()
            .collect::<Vec<_>>();
        counts.sort_by(|a, b| b.cmp(a));

        let rank = match counts.as_slice() {
            [5] => 6,
            [4, ..] => 5,
            [3, 2] => 4,
            [3, ..] => 3,
            [2, 2, ..] => 2,
            [2, 1, ..] => 1,
            _ => 0,
        };

        Self {
            cards,
            strengths,
            rank,
            bid,
        }
    }
}

fn solve(input: &str) -> u32 {
    let strength = "23456789TJQKA";

    let mut hands = input
        .split('\n')
        .map(|line| {
            let (cards, bid) = line.split_once(' ').unwrap();
            Hand::new(cards.chars().collect(), bid.parse().unwrap(), strength)
        })
        .collect::<Vec<_>>();

    hands.sort_by(|a, b| a.rank.cmp(&b.rank).then(a.strengths.cmp(&b.strengths)));

    dbg!(&hands);

    hands
        .iter()
        .enumerate()
        .map(|(i, hand)| hand.bid * (i + 1) as u32)
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_example() {
        let result = solve(
            "\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483",
        );
        assert_eq!(result, 6440);
    }
}
