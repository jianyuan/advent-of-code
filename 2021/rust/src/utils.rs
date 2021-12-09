use std::fs;

pub fn load(file: &str) -> String {
    fs::read_to_string(file).unwrap()
}
