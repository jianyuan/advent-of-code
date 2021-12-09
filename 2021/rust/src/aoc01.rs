mod utils;

fn get_input() -> Vec<u32> {
    utils::load("data/day01.txt")
        .lines()
        .map(|x| x.parse().unwrap())
        .collect()
}

fn part1(data: &Vec<u32>) -> usize {
    data.windows(2).filter(|x| x[0] < x[1]).count()
}

fn part2(data: &Vec<u32>) -> usize {
    let new_data = data
        .windows(3)
        .map(|x| x.into_iter().sum::<u32>())
        .collect::<Vec<_>>();
    part1(&new_data)
}

fn main() {
    let data = get_input();

    println!("Part 1: {}", part1(&data));
    println!("Part 2: {}", part2(&data));
}
