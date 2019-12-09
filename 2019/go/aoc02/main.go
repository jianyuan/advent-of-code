package main

import (
	"bytes"
	"log"
	"os"
	"strconv"
	"strings"
)

type CPU struct {
	pc     int
	Memory []int
}

func (cpu *CPU) RunUntilFinish() {
	for cpu.pc < len(cpu.Memory) {
		opcode := cpu.Memory[cpu.pc]
		switch opcode {
		case 1: // add
			a := cpu.Memory[cpu.pc+1]
			b := cpu.Memory[cpu.pc+2]
			w := cpu.Memory[cpu.pc+3]
			cpu.Memory[w] = cpu.Memory[a] + cpu.Memory[b]
			cpu.pc += 4
		case 2: // multiply
			a := cpu.Memory[cpu.pc+1]
			b := cpu.Memory[cpu.pc+2]
			w := cpu.Memory[cpu.pc+3]
			cpu.Memory[w] = cpu.Memory[a] * cpu.Memory[b]
			cpu.pc += 4
		case 99: // stop
			return
		default:
			log.Fatalln("Opcode not implemented:", opcode)
		}
	}
}

func runCPU(input []int, noun, verb int) int {
	memory := make([]int, len(input))
	copy(memory, input)
	cpu := &CPU{
		Memory: memory,
	}
	cpu.Memory[1] = noun
	cpu.Memory[2] = verb
	cpu.RunUntilFinish()
	return cpu.Memory[0]
}

func part1(input []int) int {
	return runCPU(input, 12, 2)
}

func part2(input []int) int {
	for noun := 0; noun <= 99; noun++ {
		for verb := 0; verb <= 99; verb++ {
			output := runCPU(input, noun, verb)
			if output == 19690720 {
				return 100*noun + verb
			}
		}
	}
	return 0
}

func main() {
	var b bytes.Buffer
	_, err := b.ReadFrom(os.Stdin)
	if err != nil {
		log.Fatal(err)
	}

	rawInput := b.String()
	rawInput = strings.TrimSpace(rawInput)
	rawInputNumbers := strings.Split(rawInput, ",")

	memory := make([]int, 0, len(rawInputNumbers))
	for _, rawInputNumber := range rawInputNumbers {
		rawInt, err := strconv.ParseInt(rawInputNumber, 10, 64)
		if err != nil {
			log.Fatal(err)
		}
		memory = append(memory, int(rawInt))
	}

	log.Println("Part 1:", part1(memory))
	log.Println("Part 2:", part2(memory))
}
