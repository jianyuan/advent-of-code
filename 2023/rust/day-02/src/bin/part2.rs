fn main() {
    let input = include_str!("./input1.txt");
    let output = solution(input);
    dbg!(output);
}

#[derive(Debug)]
struct Game {
    id: u32,
    rounds: Vec<Round>,
}

#[derive(Debug)]
struct Round {
    red: u32,
    green: u32,
    blue: u32,
}

impl Round {
    fn empty() -> Self {
        Self {
            red: 0,
            green: 0,
            blue: 0,
        }
    }

    fn contains(&self, other: &Round) -> bool {
        self.red >= other.red && self.green >= other.green && self.blue >= other.blue
    }

    fn power(&self) -> u32 {
        self.red * self.green * self.blue
    }
}

fn parse(input: &str) -> Vec<Game> {
    input
        .lines()
        .map(|line| {
            let tokens = line.split(": ").collect::<Vec<_>>();
            let id = tokens[0]
                .split(' ')
                .skip(1)
                .next()
                .unwrap()
                .parse::<u32>()
                .unwrap();

            let rounds = tokens[1]
                .split("; ")
                .collect::<Vec<_>>()
                .iter()
                .map(|token| {
                    token.split(", ").collect::<Vec<_>>().iter().fold(
                        Round::empty(),
                        |mut round, token| {
                            let mut tokens = token.split(' ');
                            let num = tokens.next().unwrap().parse::<u32>().unwrap();
                            let color = tokens.next().unwrap();

                            match color {
                                "red" => round.red += num,
                                "green" => round.green += num,
                                "blue" => round.blue += num,
                                _ => panic!("invalid color"),
                            }

                            round
                        },
                    )
                })
                .collect::<Vec<_>>();

            Game { id, rounds }
        })
        .collect()
}

fn solution(input: &str) -> String {
    let games = parse(input);

    games
        .iter()
        .map(|game| {
            game.rounds
                .iter()
                .fold(Round::empty(), |acc, round| Round {
                    red: acc.red.max(round.red),
                    green: acc.green.max(round.green),
                    blue: acc.blue.max(round.blue),
                })
                .power()
        })
        .sum::<u32>()
        .to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_solution() {
        let result = solution(
            "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green",
        );
        assert_eq!(result, "2286");
    }
}
