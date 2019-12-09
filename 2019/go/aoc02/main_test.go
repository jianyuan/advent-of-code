package main

import (
	"testing"

	"github.com/stretchr/testify/assert"
)

func TestCPU(t *testing.T) {
	for _, tc := range []struct {
		memory   []int
		expected []int
	}{
		{[]int{1, 0, 0, 0, 99}, []int{2, 0, 0, 0, 99}},
		{[]int{2, 3, 0, 3, 99}, []int{2, 3, 0, 6, 99}},
		{[]int{2, 4, 4, 5, 99, 0}, []int{2, 4, 4, 5, 99, 9801}},
		{[]int{1, 1, 1, 4, 99, 5, 6, 0, 99}, []int{30, 1, 1, 4, 2, 5, 6, 0, 99}},
	} {
		cpu := &CPU{
			Memory: tc.memory,
		}
		cpu.RunUntilFinish()
		assert.Equal(t, tc.expected, cpu.Memory)

	}
}
