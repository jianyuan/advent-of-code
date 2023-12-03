fn main() {
    let input = include_str!("./input.txt");
    let output = solution(input);
    dbg!(output);
}

#[derive(Debug)]
struct Game {
    id: u32,
    rounds: Vec<Round>,
}

#[derive(Debug, Default)]
struct Round {
    red: u32,
    green: u32,
    blue: u32,
}

impl Round {
    fn contains(&self, other: &Round) -> bool {
        self.red >= other.red && self.green >= other.green && self.blue >= other.blue
    }
}

fn parse(input: &str) -> Vec<Game> {
    input
        .lines()
        .map(|line| {
            let tokens: (&str, &str) = line.split_once(": ").unwrap();
            let id = tokens.0.split_once(' ').unwrap().1.parse::<u32>().unwrap();

            let rounds = tokens
                .1
                .split("; ")
                .into_iter()
                .map(|token| {
                    token
                        .split(", ")
                        .into_iter()
                        .fold(Round::default(), |mut round, token| {
                            let tokens = token.split_once(' ').unwrap();
                            let num = tokens.0.parse::<u32>().unwrap();
                            let color = tokens.1;

                            match color {
                                "red" => round.red += num,
                                "green" => round.green += num,
                                "blue" => round.blue += num,
                                _ => unreachable!(),
                            }

                            round
                        })
                })
                .collect();

            Game { id, rounds }
        })
        .collect()
}

fn solution(input: &str) -> u32 {
    let games = parse(input);

    let target = Round {
        red: 12,
        green: 13,
        blue: 14,
    };

    games
        .iter()
        .filter(|game| game.rounds.iter().all(|round| target.contains(round)))
        .map(|game| game.id)
        .sum()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn text_example() {
        let result = solution(
            "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
        );
        assert_eq!(result, 8);
    }
}
