package main

import (
	"log"
	"math"
)

const Digits = 6

type Rule func(int) bool

func getDigit(n, digit int) int {
	return (n / int(math.Pow10(digit))) % 10
}

func IsASixDigitNumber(n int) bool {
	lastDigit := n / int(math.Pow10(Digits-1))
	return lastDigit > 0 && lastDigit <= 9
}

func TwoAdjacentDigitsAreTheSame(n int) bool {
	for i := 0; i < Digits-1; i++ {
		if getDigit(n, i) == getDigit(n, i+1) {
			return true
		}
	}
	return false
}

func DigitsNeverDecreaseFromLeftToRight(n int) bool {
	for i := 0; i < Digits-1; i++ {
		if getDigit(n, i) < getDigit(n, i+1) {
			return false
		}
	}
	return true
}

func CheckNumberWithRules(n int, rules []Rule) bool {
	for _, rule := range rules {
		if !rule(n) {
			return false
		}
	}
	return true
}

func TwoAdjacentMatchingDigitsAreNotPartOfALargerGroupOfMatchingDigits(n int) bool {
	matches := make(map[int]int)

	for i := 0; i < Digits-1; i++ {
		digitA := getDigit(n, i)
		digitB := getDigit(n, i+1)
		if digitA == digitB {
			matches[digitA]++
		}
	}

	if len(matches) == 0 {
		return false
	}

	for _, freq := range matches {
		if freq == 1 {
			return true
		}
	}

	return false
}

var (
	RulesPart1 = []Rule{
		IsASixDigitNumber,
		TwoAdjacentDigitsAreTheSame,
		DigitsNeverDecreaseFromLeftToRight,
	}
	RulesPart2 = []Rule{
		IsASixDigitNumber,
		TwoAdjacentMatchingDigitsAreNotPartOfALargerGroupOfMatchingDigits,
		DigitsNeverDecreaseFromLeftToRight,
	}
)

func main() {
	var rangeMin, rangeMax = 109165, 576723

	// Part 1
	{
		var answer int
		for i := rangeMin; i <= rangeMax; i++ {
			if CheckNumberWithRules(i, RulesPart1) {
				answer++
			}
		}

		log.Println("Part 1:", answer)
	}

	// Part 2
	{
		var answer int
		for i := rangeMin; i <= rangeMax; i++ {
			if CheckNumberWithRules(i, RulesPart2) {
				answer++
			}
		}

		log.Println("Part 2:", answer)
	}
}
