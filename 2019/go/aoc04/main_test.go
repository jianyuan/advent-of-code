package main

import (
	"fmt"
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestIsASixDigitNumber(t *testing.T) {
	for _, tc := range []int{100000, 999999} {
		t.Run(fmt.Sprintf("%d", tc), func(t *testing.T) {
			assert.True(t, IsASixDigitNumber(tc))
		})
	}
	for _, tc := range []int{99999, 1000000} {
		t.Run(fmt.Sprintf("%d", tc), func(t *testing.T) {
			assert.False(t, IsASixDigitNumber(tc))
		})
	}
}

func TestTwoAdjacentDigitsAreTheSame(t *testing.T) {
	for _, tc := range []int{111111, 122345} {
		t.Run(fmt.Sprintf("%d", tc), func(t *testing.T) {
			assert.True(t, TwoAdjacentDigitsAreTheSame(tc))
		})
	}
	for _, tc := range []int{123789} {
		t.Run(fmt.Sprintf("%d", tc), func(t *testing.T) {
			assert.False(t, TwoAdjacentDigitsAreTheSame(tc))
		})
	}
}

func TestDigitsNeverDecreaseFromLeftToRight(t *testing.T) {
	for _, tc := range []int{111123, 135679} {
		t.Run(fmt.Sprintf("%d", tc), func(t *testing.T) {
			assert.True(t, DigitsNeverDecreaseFromLeftToRight(tc))
		})
	}
	for _, tc := range []int{223450} {
		t.Run(fmt.Sprintf("%d", tc), func(t *testing.T) {
			assert.False(t, DigitsNeverDecreaseFromLeftToRight(tc))
		})
	}
}

func TestTwoAdjacentMatchingDigitsAreNotPartOfALargerGroupOfMatchingDigits(t *testing.T) {
	for _, tc := range []int{112233, 111122, 111223, 557777, 446888, 113444, 112222, 122334, 123345, 123445, 123455} {
		t.Run(fmt.Sprintf("%d", tc), func(t *testing.T) {
			assert.True(t, TwoAdjacentMatchingDigitsAreNotPartOfALargerGroupOfMatchingDigits(tc))
		})
	}
	for _, tc := range []int{123444, 124444, 122235, 111123, 111111, 123789} {
		t.Run(fmt.Sprintf("%d", tc), func(t *testing.T) {
			assert.False(t, TwoAdjacentMatchingDigitsAreNotPartOfALargerGroupOfMatchingDigits(tc))
		})
	}
}

func TestCheckNumberWithPart1Rules(t *testing.T) {
	for _, tc := range []int{111111} {
		t.Run(fmt.Sprintf("%d", tc), func(t *testing.T) {
			assert.True(t, CheckNumberWithRules(tc, RulesPart1), tc)
		})
	}
	for _, tc := range []int{223450, 123789} {
		t.Run(fmt.Sprintf("%d", tc), func(t *testing.T) {
			assert.False(t, CheckNumberWithRules(tc, RulesPart1), tc)
		})
	}
}
func TestCheckNumberWithPart2Rules(t *testing.T) {
	for _, tc := range []int{112233, 111122} {
		t.Run(fmt.Sprintf("%d", tc), func(t *testing.T) {
			assert.True(t, CheckNumberWithRules(tc, RulesPart2), tc)
		})
	}
	for _, tc := range []int{123444} {
		t.Run(fmt.Sprintf("%d", tc), func(t *testing.T) {
			assert.False(t, CheckNumberWithRules(tc, RulesPart2), tc)
		})
	}
}
